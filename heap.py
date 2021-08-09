"""
Heap Data Structure

Writing my own implementation of heap with the following requirements:

1. It should be able to function as both a min and a max heap.
2. The min or max heap property can't be changed once initialized.
3. Items are stored as key: value pairs.
4. The heap is sorted based on the values.
5. Allows for deletion of a key: value pair given the key.
6. Performance guarantees:
    a. Heapify              ~ O(n)
    b. Extract min / max    ~ O(log(n))
    c. Insert               ~ O(log(n))
    d. Delete               ~ O(log(n))

Heapify:

We start with the leaves. If the heap property is violated we swap the leaf with it's parent. Now we have the property for the last two levels. Let's start counting from the bottom. Level 1 and Level 2 have the heap property now. We move upwards. After k steps Level 1 to k will have the heap property restored. For each node in Level k+1 if the heap property is violated trickle the node down  till it finds the right position in the heap.

Note that the time complexity of this operation is:

t ~ O(n / 2) + ... + O(n / 2^k) * k + .... O(n / 2^ log(n) * log(n))

t ~ O(n [1/(2^1) + 2/(2^2) + ... k/(2^k) + ... log(n)/(2^(log(n))]

Consider Tk     = 1/2 + 2/2^2 + ... + k/2^k
now      Tk/2   =       1/2^2 + ... + (k-1)/2^k + k/2^(k+1)

Subtracting
        Tk/2    = 1/2 [1 + 1/2 + 1/2^2 + ... + 1/2^(k-1)] - k/2^(k+1)
        Tk/2    = 1/2 [[1 - (1/2)^k]/(1/2)] - k/2^(k+1)
        Tk/2    = 1 - (1/2)^k - k/2^(k+1)
Substituting k  = log(n)
        T/2     = 1 - (1/n) - log(n)/2n
        T       ~ O(1)

Therefore t ~ O(n)
"""

import constants
from constants import pp


class Pair:
    def __init__(self, key, val):
        self.key = key
        self.val = val

    @staticmethod
    def key_val(pair):
        return pair.key, pair.val

    @staticmethod
    def pairs(tuples):
        return [Pair(t[0], t[1]) for t in tuples]

    def __eq__(self, other):
        return self.val == other.val

    def __lt__(self, other):
        return self.val < other.val

    def __le__(self, other):
        return self == other or self < other

    def __gt__(self, other):
        return not self <= other

    def __ge__(self, other):
        return not self < other

    def __str__(self):
        return str(self.key) + ' : ' + str(self.val)

    def __repr__(self):
        return str(self)


class Heap:
    def __init__(self, pairs=None, min=True):
        self.min = min
        if not pairs:
            self.pairs = []
            self.map = {}
        else:
            self.pairs = pairs
            print(f'self.pairs = {self.pairs}')
            self.map = {pair.key: index for index, pair in enumerate(self.pairs)}
            pp(self.map)

        self.heapify()

    def __len__(self):
        return len(self.pairs)

    def is_empty(self):
        return len(self) == 0

    def size(self):
        return len(self)

    def valid_index(self, index):
        return index < self.size()

    def heapify(self):
        for key, _ in map(Pair.key_val, reversed(self.pairs)):
            print(f'key in heapify = {key}')
            self.trickle_down(self.parent(key))

    def parent(self, key):
        index = self.index(key)
        print(f'index in parent = {index}')
        print(self.key((index + 1)//2 - 1))
        return self.key((index + 1)//2 - 1) if index else None

    def trickle_down(self, key):
        print(f'trickle down key = {key}')
        print(f'self.pairs = {self.pairs}')
        pp(self.map)
        if key is None:
            return
        while not self.valid_down(key):
            self.drop(key)

    def last(self):
        return self.size() - 1

    def insert(self, pair):
        self.pairs.append(pair)
        self.map[pair.key] = self.last()

    def index(self, key):
        return self.map[key]

    def extend(self, pairs):
        for pair in pairs:
            self.insert(pair)

    def key(self, ind):
        return self.pairs[ind].key if self.valid_index(ind) else None

    def swap_index(self, i, j):
        self.pairs[i], self.pairs[j] = self.pairs[j], self.pairs[i]

    def swap_map(self, i, j):
        k_i, k_j = self.key(i), self.key(j)
        self.map[k_i], self.map[k_j] = j, i

    def swap(self, i, j):
        self.swap_map(i, j)
        self.swap_index(i, j)


    def swap_keys(self, k, l):
        self.swap(self.index(k), self.index(l))

    def pair(self, key):
        return self.pairs[self.index(key)]

    def value(self, key):
        return self.pair(key).val

    def comp(self, key_l, key_r):
        if not key_l or not key_r:
            return True
        val_l, val_r = self.value(key_l), self.value(key_r)
        return val_l < val_r if min else val_l > val_r


    def left_child(self, key):
        left = (self.index(key) + 1) * 2 - 1
        return self.key(left) if self.valid_index(left) else None

    def right_child(self, key):
        right = (self.index(key) + 1) * 2
        return self.key(right) if self.valid_index(right) else None

    def valid_up(self, key):
        return self.comp(self.parent(key), key)

    def valid_down(self, key):
        left, right = self.left_child(key), self.right_child(key)
        return self.comp(key, left) and self.comp(key, right)

    def invalid_children(self, key):
        left, right = self.left_child(key), self.right_child(key)
        left = None if self.comp(key, left) else left
        right = None if self.comp(key, right) else right
        return left, right

    def preferred(self, l, r):
        select, _ = (l, r) if self.comp(l, r) else (r, l)
        return select

    def swap_child(self, key):
        left, right = self.invalid_children(key)
        if not left and not right:
            return
        elif not left:
            self.swap_keys(key, right)
        elif not right:
            self.swap_keys(key, left)
        else:
            self.swap_keys(key, self.preferred(left, right))

    def lift(self, key):
        parent = self.parent(key)
        if not parent:
            return
        ind, par = self.index(key), self.index(parent)
        self.swap(ind, par)

    def drop(self, key):
        self.swap_child(key)


    def bubble_up(self, key):
        while not self.valid_up(key):
            self.lift(key)

    def __str__(self):
        return str(self.pairs)

    def __repr__(self):
        return str(self)


if __name__ == constants.MAIN:
    l = Pair.pairs([(1, 2), (5, 7)])
    heap = Heap(l, min=False)
    heap.extend(l)
    heap.insert(Pair(13, 11))
    print(heap)
    print(heap.map)
    print(f'left child of (1, 2) = {heap.left_child(1)}')
    print(f'right child of (1, 2) = {heap.right_child(1)}')

