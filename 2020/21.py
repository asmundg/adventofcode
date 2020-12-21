import dataclasses


@dataclasses.dataclass
class Count:
    contents: dict = dataclasses.field(default_factory=dict)
    allergens: dict = dataclasses.field(default_factory=dict)
    ingredients: dict = dataclasses.field(default_factory=dict)


def data():
    counts = Count()
    with open("input/21.input") as f:
        for line in [line.strip() for line in f.readlines()]:
            ingredients, allergens = (
                line.replace(")", "").replace(",", "").split("(contains ")
            )
            for allergen in allergens.split():
                counts.allergens[allergen] = counts.allergens.get(allergen, 0) + 1
                counts.contents.setdefault(allergen, dict())

                for ingredient in ingredients.split():
                    counts.contents[allergen][ingredient] = (
                        counts.contents[allergen].get(ingredient, 0) + 1
                    )
            for ingredient in ingredients.split():
                counts.ingredients[ingredient] = (
                    counts.ingredients.get(ingredient, 0) + 1
                )

    return counts


def safe_ingredients(counts: Count):
    unsafe = set()
    for allergen in counts.allergens:
        unsafe.update(
            [
                ingredient
                for ingredient in counts.contents[allergen]
                if counts.contents[allergen][ingredient] >= counts.allergens[allergen]
            ]
        )

    ingredients = set(
        [
            ingredient
            for ingredients in counts.contents.values()
            for ingredient in ingredients
        ]
    )
    safe = set(ingredients).difference(unsafe)

    return sum(
        [
            counts.ingredients[ingredient]
            for ingredient in counts.ingredients
            if ingredient in safe
        ]
    )


def match_ingredients(counts: Count):
    allergens = sorted(
        counts.allergens, key=lambda name: counts.allergens[name], reverse=True
    )
    match = {}
    # Assume we can identify at least one certain mapping per
    # round. E.g. no permutation attempts.
    while len(match) < len(allergens):
        for allergen in allergens:
            target = counts.allergens[allergen]
            candidates = [
                ingredient
                for ingredient in counts.contents[allergen]
                if counts.contents[allergen][ingredient] == target
                and ingredient not in match
            ]
            if len(candidates) == 1:
                match[candidates[0]] = allergen
        print(match)
    return ",".join(sorted(match, key=lambda ingredient: match[ingredient]))


def main():
    d = data()
    part1 = safe_ingredients(d)
    part2 = match_ingredients(d)
    print(part1)
    print(part2)


main()
