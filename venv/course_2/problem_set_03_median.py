import constants
from constants import compose
from constants import reduce
from heap import Heap
from math import fabs


def median_maintenance(filename, size=10000):
    low = Heap(min=False)
    high = Heap(min=True)
    meds = 0

    with open(filename, "r") as f:
        maps = [int, str.strip]
        nums = list(map(compose(*maps), f))

    for ind, num in enumerate(nums[:size]):
        if low.peek() is None and high.peek() is None:
            high.insert_key_val(ind, num)
        elif low.peek() is None:
            if num <= high.peek().val:
                low.insert_key_val(ind, num)
            else:
                high.insert_key_val(ind, num)

        elif num <= low.peek().val:
            low.insert_key_val(ind, num)
        elif num >= high.peek().val:
            high.insert_key_val(ind, num)
        else:
            if low.size() > high.size():
                low.insert_key_val(ind, num)
            else:
                high.insert_key_val(ind, num)

        if high.size() == low.size() + 2:
            low.insert(high.extract())
        elif low.size() == high.size() + 2:
            high.insert(low.extract())

        if (ind + 1) % 2 == 0:
            meds += low.peek().val
        else:
            l, h = low.peek(), high.peek()
            ls, hs = low.size(), high.size()
            meds += l.val if ls > hs else h.val

    return meds % 10000


if __name__ == constants.MAIN:
    from time import time

    start = time()
    meds = median_maintenance('problem_set_03_median.txt')
    end = time()
    print(f'time = {end - start}')