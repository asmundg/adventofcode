import re
import pprint

passportKeys = sorted(["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid"])
idKeys = sorted(["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"])


def between(val, lower, upper):
    return int(val) >= lower and int(val) <= upper and True


def valid_year(val, lower, upper):
    year = re.match("^([0-9]{4})$", val)
    return year and betwen(year.group(1), lower, upper) or False


def valid_height(val):
    match = re.match("^(\d+)(cm|in)$", val)
    if match == None:
        return False

    height, unit = re.match("^(\d+)(cm|in)$", val).groups()
    if unit == "cm":
        return between(height, 150, 193)
    elif unit == "in":
        return between(height, 59, 76)
    else:
        return False


validators = {
    "byr": lambda s: between(s, 1920, 2002),
    "iyr": lambda s: between(s, 2010, 2020),
    "eyr": lambda s: between(s, 2020, 2030),
    "hgt": valid_height,
    "hcl": lambda s: re.match("^#[0-9a-f]{6}$", s) != None,
    "ecl": lambda s: s in set(["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]),
    "pid": lambda s: re.match("^[0-9]{9}$", s) != None,
    "cid": lambda s: True,
}


def valid(fields):
    pairs = [f.split(":") for f in fields.replace("\n", " ").split()]
    validated = [
        {
            "key": key,
            "val": val,
            "valid": validators[key] and validators[key](val) or False,
        }
        for key, val in pairs
    ]
    pprint.pprint(validated)

    keys = sorted([obj["key"] for obj in validated])
    valid = [obj["valid"] for obj in validated]
    return (keys == passportKeys or keys == idKeys) and False not in valid


with open("input/04.input") as f:
    data = f.read()
    print(sum([valid(fields) for fields in data.split("\n\n")]))
