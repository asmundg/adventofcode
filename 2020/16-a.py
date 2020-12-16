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

    print(rules, invalid)
    return invalid


def main(data):
    rules, my_ticket, nearby = data

    invalid = [validate(rules, ticket) for ticket in nearby]
    print(sum([field for values in invalid for field in values]))


main(get_data())
