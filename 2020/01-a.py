def main():
    f = open("input/01.input")
    nums = [int(l) for l in f.readlines()]
    print(nums)
    
    for a in nums:
        for b in nums:
            if a + b == 2020:
                print(a, b, a * b)
                return

main()
