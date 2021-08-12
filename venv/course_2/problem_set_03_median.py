import constants
from constants import compose
from constants import reduce
from heap import Heap


def median_maintenance(filename, size=10000):
    l, h, m = Heap(min=False), Heap(min=True), 0

    with open(filename, "r") as f:
        maps = [int, str.strip]
        nums = list(map(compose(*maps), f))

    for i, n in enumerate(nums[:size]):
        if l.peek() is None and h.peek() is None:
            h.push(i, n)
        elif l.peek() is None:
            l.push(i, n) if n <= h.peek() else h.push(i, n)

        elif n <= l.peek():
            l.push(i, n)
        elif n >= h.peek():
            h.push(i, n)
        else:
            l.push(i, n) if l.size() > h.size() else h.push(i, n)

        if h.size() == l.size() + 2:
            l.insert(h.extract())
        elif l.size() == h.size() + 2:
            h.insert(l.extract())

        if (i + 1) % 2 == 0:
            m += l.peek()
        else:
            m += l.peek() if l.size() > h.size() else h.peek()

    return m % 10000


if __name__ == constants.MAIN:
    from time import time

    start = time()
    meds = median_maintenance('problem_set_03_median.txt')
    end = time()
    print(f'time = {end - start}')
    print(meds)