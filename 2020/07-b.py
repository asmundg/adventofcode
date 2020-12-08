import re
import pprint

bag_re = re.compile(r"^(\d+) ((?:\w+) (?:\w+)) bags?")
sentence_re = re.compile(
    "^((?:\w+) (?:\w+)) bags contain (((\d+) (\w+) (\w+) bags?(?:, )?)+|(?:no other bags)).$"
)

graph = {}

with open("input/07.input") as f:
    for l in f.readlines():
        container, contained_sentence = sentence_re.match(l).groups()[0:2]
        if "no other bags" in contained_sentence:
            graph[container] = set()
        else:
            graph.setdefault(container, set()).update(
                [bag_re.match(c).groups()[0:2] for c in contained_sentence.split(", ")]
            )


pprint.pprint(graph)


def contents(bag):
    return sum(
        [
            int(sub_bag[0]) + int(sub_bag[0]) * contents(sub_bag[1])
            for sub_bag in graph[bag]
        ]
    )


print(contents("shiny gold"))
