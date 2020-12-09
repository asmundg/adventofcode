preamble = 25

def recalculate(numbers):
    deps = set()
    for a in numbers:
        for b in numbers:
            if a != b:
                deps.add(a + b)
    return deps


with open("input/09.input") as f:
    numbers = [int(num) for num in f.readlines()]
    window = numbers[0:preamble]
    deps = recalculate(window)

    invalid = -1
    for num in numbers[preamble:]:
        print(num, deps)
        if num in deps:
            window.append(num)
            window.pop(0)
            deps = recalculate(window)
        else:
            invalid = num
            break

    print(invalid)

    for i, a in enumerate(numbers):
        nums = [a]
        for b in numbers[i + 1:]:
            if sum(nums) + b > invalid:
                break
            else:
                nums.append(b)

        print(nums)
        if sum(nums) == invalid and len(nums) >= 2:
            print(nums, sum(nums), min(nums) + max(nums))
            break
