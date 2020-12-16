import functools
import re

rule_re = re.compile(r"(.+): (\d+)-(\d+) or (\d+)-(\d+)")


def get_data():
    rules = {}
    with open("input/16.input") as f:
        while True:
            line = f.readline().strip()
            if line == "":
                f.readline()
                break

            print(line)
            field, a, b, c, d = rule_re.match(line).groups()
            rules[field] = ((int(a), int(b)), (int(c), int(d)))

        my_ticket = [int(word) for word in f.readline().split(",")]

        f.readline()
        f.readline()

        nearby = [[int(word) for word in line.split(",")] for line in f.readlines()]

        return (rules, my_ticket, nearby)


def validate(rules, ticket):
    invalid = []
    for field in ticket:
        for rule_a, rule_b in rules.values():
            if (rule_a[0] <= field <= rule_a[1]) or (rule_b[0] <= field <= rule_b[1]):
                break
        else:
            invalid.append(field)

    return not invalid


# All tickets must match positional rule
def validate_strict(rules, try_rules, tickets):
    for i, rule_name in enumerate(try_rules):
        rule_a, rule_b = rules[rule_name]
        for ticket in tickets:
            if (ticket[i] < rule_a[0] or ticket[i] > rule_a[1]) and (
                ticket[i] < rule_b[0] or ticket[i] > rule_b[1]
            ):
                return False
    return True


# known: ["field1", "field2"]
# rest: ["field3"]
# Try rules from rest until it and known rules validate all tickets
# Then add to known, remove from rest and continue
def map_rules(rules, known, rest, tickets, invalid_branches):
    if not rest:
        return known

    print(known)

    for try_rule in rest:
        try_rules = known + [try_rule]

        # For all permutations of the given prefix, we know that
        # the subtree doesn't have a solution
        cache_key = ",".join(sorted(try_rules))
        if cache_key in invalid_branches:
            continue

        if validate_strict(rules, try_rules, tickets):
            new_rest = [rule for rule in rest if rule != try_rule]
            all_known = map_rules(rules, try_rules, new_rest, tickets, invalid_branches)
            if all_known:
                return all_known

            # Exhausted subtree, there's no solution for this set of
            # try_rules (their order doesn't matter, since there is no
            # solution using the remaining rules)
            invalid_branches.add(cache_key)

    return None


def main(data):
    rules, my_ticket, nearby = data

    valid = [ticket for ticket in nearby if validate(rules, ticket)]
    rules = map_rules(
        rules,
        [],
        rules.keys(),
        valid + [my_ticket],
        set(),
    )
    print(rules)

    print(
        functools.reduce(
            lambda a, b: a * b,
            [
                my_ticket[i]
                for i in range(len(my_ticket))
                if rules[i].startswith("departure")
            ],
            1,
        )
    )


main(get_data())
