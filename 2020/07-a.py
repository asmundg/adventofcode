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
        if not "no other bags" in contained_sentence:
            for contained in [
                bag_re.match(c).group(2) for c in contained_sentence.split(", ")
            ]:
                graph.setdefault(contained, set()).add(container)

pprint.pprint(graph)
search = set(["shiny gold"])
found = set()
while len(search):
    container = search.pop()
    if container in graph:
        found.update(graph[container])
        search.update(graph[container])
    print(found, search)

print(len(found))
