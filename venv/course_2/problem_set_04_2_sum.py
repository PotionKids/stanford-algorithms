import constants
from constants import compose
from constants import reduce


def read_nums(filename, size=10):
    with open(filename, "r") as f:
        maps = [int, str.strip]
        nums = list(map(compose(*maps), f))
        return nums


# noinspection PyShadowingBuiltins
def dictionarize(nums):
    result = {}
    for ind, num in enumerate(nums):
        inds = result.get(num, list())
        inds.append(ind)
        result[num] = inds
    return result


# noinspection PyShadowingBuiltins
def two_sum(map, t):
    for num, inds in map.items():
        vals = map.get(t - num, None)
        if vals is None:
            continue
        elif num != t - num:
            return True
        elif num == t - num:
            if len(vals) > 2:
                return True
    return False


# noinspection PyShadowingBuiltins
def two_sums(map, targets=range(-10000, 10001)):
    count = 0
    for t in targets:
        if two_sum(map, t):
            count += 1
    return count



if __name__ == constants.MAIN:
    from time import time

    nums = read_nums('problem_set_04_2_sum.txt')
    dic = dictionarize(nums)
    start = time()
    print(two_sums(dic))
    end = time()
    print(f'time = {end - start}')
