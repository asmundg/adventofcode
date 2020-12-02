def main():
    f = open("input/01.input")
    nums = [int(l) for l in f.readlines()]
    print(nums)
    
    for a in nums:
        for b in nums:
            for c in nums:
                if a + b + c == 2020:
                    print(a, b, c, a * b * c)
                    return

main()
