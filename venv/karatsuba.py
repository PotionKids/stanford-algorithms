def trim(a):
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
    # print(f"subtract_with_borrow({a}, {b}, {borrow})")
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

    if l < r:
        d = 10 + l - r
        # print(f"swb result = {str(d) + subtract_with_borrow(a[1:], b[1:], '1')}")
        return str(d) + subtract_with_borrow(a[1:], b[1:], '1')
    # print(f"swb result = {str(l - r) + subtract_with_borrow(a[1:], b[1:], '0')}")
    return str(l - r) + subtract_with_borrow(a[1:], b[1:], '0')


def add(a, b):
    return trim(add_with_carry(a[::-1], b[::-1], '0')[::-1])


def subtract(a, b):
    num_a = int(a)
    num_b = int(b)

    high, low, minus = (a, b, '') if num_a >= num_b else (b, a, '-')

    result = minus + subtract_with_borrow(high[::-1], low[::-1], '0')[::-1]
    print(f"result = {result}")
    return trim(result)


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
    n_by_2 = ceil(n/2)
    list_num = list(p)
    a = ''.join(list_num[:n_by_2])
    b = ''.join(list_num[n_by_2:])

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

    print(f"multiply({p}, {q})")

    p, q, n = normalize(p, q)

    print(f"after normalizing multiply({p}, {q}) and n = {n}")

    if n == 1:
        prod = str(int(p)*int(q))
        print(f"prod = {prod}")
        return prod

    a, b, n_by_2 = split(p)
    c, d, n_by_2 = split(q)

    ac = multiply(a, c)
    bd = multiply(b, d)
    abcd = multiply(add(a, b), add(c, d))
    adbc = subtract(abcd, add(ac, bd))

    # ac 21, bd 32, a+b c+d 7*15 = 105, ad + bc = 52

    print(f"add({pad_right(ac, 2*n_by_2)}, {pad_right(adbc, n_by_2)}, {bd})")
    prod = add(add(pad_right(ac, 2*n_by_2), pad_right(adbc, n_by_2)), bd)

    print(f"prod = {prod}")
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


def test_add_with_carry():
    assert add_with_carry('3', '5', '0') == '8'
    assert add_with_carry('32', '71', '0') == '04'
    assert add_with_carry('932', '71', '0') == '652'
    print('test_add_with_carry passed')


def test_add():
    # assert add('3', '5') == '8'
    # assert add('23', '17') == '40'
    # assert add('239', '17') == '256'
    assert add('21', '32') == '53'
    print('test_add passed')


def test_subtract():
    # assert subtract('8', '3') == '5'
    # assert subtract('3', '8') == '-5'
    # assert subtract('18', '23') == '-5'
    # assert subtract('105', add('21', '32')) == '52'
    assert subtract('105', '53') == '52'


def test_multiply():
    # assert multiply('3', '5') == '15'
    # assert multiply('12', '5') == '60'
    # assert multiply('12', '56') == '672'
    # assert multiply('34', '78') == '2652'
    # ac 21, bd 32, a+b c+d 7*15 = 105, ad + bc = 52
    assert multiply('1234', '5678') == '7006652'
    # ac 672, bd 2652, a+b c+d 68*112 = 7616, ad + bc = 4292


if __name__ == '__main__':
    # test_pad_left()
    # test_pad_right()
    # test_normalize()
    # test_split()
    # test_add_with_carry()
    # test_add()
    # test_subtract()
    test_multiply()
    # a = subtract_with_borrow('', '', '0')
    # b = subtract_with_borrow('1', '', '1')
    # print(f"a = {a}, b = {b}")
