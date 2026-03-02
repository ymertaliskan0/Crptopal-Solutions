mem = {0: 0, 1: 1, 2: 1}


def find(n):
    n1 = 0
    n2 = 1

    n3 = 0
    n4 = 1

    m = n
    while m > 1:
        if m % 2 == 1:
            n3t = n3 * n1 + n4 * n2
            n4t = n3 * n2 + n4 * (n1 + n2)
            n3, n4 = n3t, n4t
        n1t = n1 * n1 + n2 * n2
        n2t = n1 * n2 + n2 * (n1 + n2)
        n1, n2 = n1t, n2t

        m //= 2

    return n3 * n1 + n4 * n2


num = 13
print(find(num))
