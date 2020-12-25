def find_loop(pubkey):
    iterations = 0
    key = 1
    while True:
        key = (key * 7) % 20201227
        iterations += 1

        if key == pubkey:
            return iterations

def transform(subject, iterations):
    key = 1
    for _ in range(iterations):
        key = (key * subject) % 20201227
    return key

def main():
        print(find_loop(5764801))
        print(find_loop(17807724))
        print(transform(17807724, 8))
        print(transform(5764801, 11))

        a = 12090988
        b = 240583
        a_loop = find_loop(a)
        b_loop = find_loop(b)
        print(transform(b, a_loop))
        print(transform(a, b_loop))


main()
