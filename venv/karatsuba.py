def trim(a):
    if a == '0':
        return '0'
    if a == '':
        return ''
    if a[0] == '0':
        return trim(a[1:])
    return a


def add_with_carry(a, b, carry):
    if len(a) == len(b) == 0:
        return carry if int(carry) > 0 else ''

    a = a if len(a) > 0 else '0'
    b = b if len(b) > 0 else '0'

    num = int(a[0]) + int(b[0]) + int(carry)
    if num < 10:
        result = str(num) + add_with_carry(a[1:], b[1:], '0')
        return result
    result = str(num % 10) + add_with_carry(a[1:], b[1:], str(num // 10))
    return result


def subtract_with_borrow(a, b, borrow):
    if len(a) == len(b) == 0:
        return ''
    if len(a) == 0:
        a = '0'
    if len(b) == 0:
        b = '0'

    if len(a) == len(b) == 1:
        if a == '0':
            return ''
        num = int(a) - int(b) - int(borrow)
        return str(int(a) - int(b) - int(borrow)) if num != 0 else ''

    l = int(a[0])
    r = int(b[0])

    if l < r + int(borrow):
        d = 10 + l - r - int(borrow)
        return str(d) + subtract_with_borrow(a[1:], b[1:], '1')
    return str(l - r - int(borrow)) + subtract_with_borrow(a[1:], b[1:], '0')


def add(a, b):
    """
    :param a: first number to be added
    :param b: second number to be added
    :return:  sum of the two numbers

    The function trims the numbers reverses them according to the
    Reverse Polish notation for easier computation and iteration
    and passes them to the recursive function add_with_carry.

    Trimming is necessary as the normalization process creates leading zeros
    """
    a = trim(a)
    b = trim(b)
    return add_with_carry(a[::-1], b[::-1], '0')[::-1]


def subtract(a, b):
    """
    :param a: first number to be added
    :param b: second number to be added
    :return:  difference of the two numbers

    The function trims the numbers reverses them according to the
    Reverse Polish notation for easier computation and iteration
    and passes them to the recursive function subtract_with_borrow.

    Trimming is necessary as the normalization process creates leading zeros
    """
    num_a = int(trim(a))
    num_b = int(trim(b))

    high, low, minus = (a, b, '') if num_a >= num_b else (b, a, '-')

    result = minus + subtract_with_borrow(high[::-1], low[::-1], '0')[::-1]
    return result


def pad_right(a, n):
    list_num = list(a) + ['0' for _ in range(n)]
    return ''.join(list_num)


def pad_left(a, n):
    list_num = ['0' for _ in range(n)] + list(a)
    return ''.join(list_num)


def normalize(p, q):
    big, small = (p, q) if (len(p) >= len(q)) else (q, p)
    n = max(len(p), len(q))
    small = pad_left(small, n - len(small))
    return big, small, n


def split(p):
    from math import ceil

    n = len(p)
    n_by_2 = n//2
    list_num = list(p)
    a = ''.join(list_num[:n-n_by_2])
    b = ''.join(list_num[n-n_by_2:])

    return a, b, n_by_2


def multiply(p, q):
    """
    :param p: first number to be multiplied provided as a string of digits
    :param q: second number to be multiplied provided as a string of digits
    :return: product using karatsuba multiplication algorithm

    len(p) - 1 = n
    len(q) - 1 = n

    p = a x 10^(n/2) + b
    q = c x 10^(n/2) + d

    p x q = ac x 10^n + (ad + bc) * 10^(n/2) + bd
    """

    p, q, n = normalize(p, q)

    if n == 1:
        prod = str(int(p)*int(q))
        return prod

    a, b, n_by_2 = split(p)
    c, d, n_by_2 = split(q)

    ac = multiply(a, c)
    bd = multiply(b, d)
    abcd = multiply(add(a, b), add(c, d))
    adbc = subtract(abcd, add(ac, bd))

    prod = add(add(pad_right(ac, 2*n_by_2), pad_right(adbc, n_by_2)), bd)

    return prod


def test_normalize():
    assert normalize('1234', '56') == ('1234', '0056', 4)
    assert normalize('12345', '56') == ('12345', '00056', 5)
    print("test_normalize passed")


def test_pad_left():
    assert pad_left('1234', 5) == '000001234'
    print("test_pad_left passed")


def test_pad_right():
    assert pad_right('1234', 5) == '123400000'
    print("test_pad_right passed")


def test_split():
    assert split('1234') == ('12', '34', 2)
    assert split('12345') == ('123', '45', 3)
    print('test_split passed')


def random_num_string_generator(size):
    from random import randrange
    return f"{randrange(1, 10)}" + ''.join([f"{randrange(10)}" for _ in range(1, size)])


def test_add_with_carry():
    assert add_with_carry('3', '5', '0') == '8'
    assert add_with_carry('32', '71', '0') == '04'
    assert add_with_carry('932', '71', '0') == '652'
    print('test_add_with_carry passed')


def test_func_size_num_cases(func, size_a, size_b, num_cases):
    """
    :param func:        function being tested
    :param size_a:      number of digits in the first number (starting digits could be zero)
    :param size_b:      number of digits in the second number (starting digits could be zero)
    :param num_cases:   number of test cases
    :return:            void
    """

    for _ in range(num_cases):
        a = random_num_string_generator(size_a)
        b = random_num_string_generator(size_b)

        prod = func(a, b)


def test_multiply_size_num_cases(size, num_cases):
    test_func_size_num_cases(multiply, size, size, num_cases)


if __name__ == '__main__':
    a = '3141592653589793238462643383279502884197169399375105820974944592'
    b = '2718281828459045235360287471352662497757247093699959574966967627'
    c = multiply(a, b)
    print(c)
    # from plot import plot
    # from performance import performance
    #
    # sizes, times = performance(test_multiply_size_num_cases, 30, 10)
    # plot(sizes, times, loglog=True)
