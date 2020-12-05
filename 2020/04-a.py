passportKeys = sorted(["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid"])
idKeys = sorted(["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"])


def valid(fields):
    keys = sorted([f.split(":")[0] for f in fields.replace("\n", " ").split()])
    print(keys)
    return keys == passportKeys or keys == idKeys


with open("input/04.input") as f:
    data = f.read()
    print(sum([valid(fields) for fields in data.split("\n\n")]))
