def gen_random_array(size, unique=False, abs_max=100):
    from random import randrange

    max_int = abs_max
    min_int = -abs_max

    if not unique:
        return [randrange(min_int, max_int) for _ in range(size)]

    seen = set()
    arr = list()
    num = min_int - 1
    seen.add(num)
    for _ in range(size):
        while num in seen:
            num = randrange(min_int, max_int)
        seen.add(num)
        arr.append(num)

    return arr
