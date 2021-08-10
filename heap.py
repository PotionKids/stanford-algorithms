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
    def __init__(self, key='z', val=100):
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


class Node:
    def __init__(self, val=Pair()):
        self.val = val
        self.left = None
        self.right = None


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
        return len(self.pairs)

    def valid_index(self, index):
        return 0 <= index < self.size()

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
            print(f'self.valid_down is {self.valid_down(key)}')
            self.drop(key)

    def drop(self, key):
        self.swap_child(key)

    def swap_child(self, key):
        left, right = self.invalid_children(key)
        print(f'invalid children: left = {left}, right = {right}')
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

    def last(self):
        print(f'self.size = {self.size}')
        return self.size() - 1

    def append(self, pair):
        self.pairs.append(pair)
        self.map[pair.key] = self.last()
        return pair.key

    def insert(self, pair):
        key = self.append(pair)
        self.bubble_up(key)

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

    def pair_index(self, index):
        return self.pairs[index] if 0 <= index < self.size() else None

    def value(self, key):
        return self.pair(key).val

    def comp(self, key_l, key_r):
        if not key_l or not key_r:
            return True
        val_l, val_r = self.value(key_l), self.value(key_r)
        return val_l <= val_r if self.min else val_l >= val_r

    def left_index(self, index):
        left = (index + 1) * 2 - 1
        return left if left < self.size() else -1

    def right_index(self, index):
        right = (index + 1) * 2
        return right if right < self.size() else -1

    def left_child(self, key):
        return self.key(self.left_index(self.index(key)))

    def right_child(self, key):
        return self.key(self.right_index(self.index(key)))

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

    def bubble_up(self, key):
        while not self.valid_up(key):
            self.lift(key)

    @staticmethod
    def level(j):
        i = 0
        while 2 ** i <= j + 1:
            i += 1
        return i

    def print(self):
        print(f'printing heap as a tree')
        n = self.size()
        height = self.level(n)
        full = 2 ** height
        space = ' '*len(str(Pair()))
        gap = ' '
        mid = full // 4
        h = 1
        index = 1
        while h <= height:
            power = 2 ** h
            start = (space + gap) * (mid - power // 4)
            s = start
            for i in range(index, power):
                if i > n:
                    break
                s += str(self.pairs[i - 1]) + space + gap
                if i == power//2 + power//4 - 1:
                    s += space + gap
            index = power
            print(s)
            print('')
            h += 1

    def subtree(self, index):
        if index < 0 or index >= self.size():
            return None
        node = Node(self.pairs[index])
        node.left = self.subtree(self.left_index(index))
        node.right = self.subtree(self.right_index(index))
        return node

    def tree(self):
        return self.subtree(0)

    def tree_string_size(self, node):
        if not node:
            return 0
        left = self.tree_string_size(node.left)
        right = self.tree_string_size(node.right)
        return left + len(' ' + str(node.val) + ' ') + right

    def string(self):
        """
        In trying to print a heap as a tree the trick is to invert the tree
        and then work one's way down. The advantge of inverting is
        we know the position of all the leaf nodes in the print canvas
        and the node of subsequent higher levels can be placed between
        two of the children. Actually it's still not perfectly symmetrical :(

        0   4   8   12  16  20  24  28  32  36  40  44  48  52  56  60
          2       10      18      26      34      42      50      58
              6               22              38              54
                      14                              46
                                      30
        starting space sequence 0 2 6 14 30 -> 0 += 2**1 += 2**2 ...

        :return:
        """
        
        n = self.level(self.size() - 1)
        arr = [(None, -1)] * ((2**n) - 1)
        for h in range(1, n + 1):
            for i in range(2**(h - 1), 2**h):
                if i <= self.size():
                    arr[i - 1] = (self.pairs[i - 1], -1)
        s = []
        p = 0
        e = 2
        c = 0
        for h in range(n, 0, -1):
            l = []
            a = p
            for i in range(2 ** (h - 1), 2 ** h):
                arr[i - 1] = (arr[i - 1][0], a)
                a += 2 ** e
                l.append(arr[i - 1])
            s.append(l)
            e += 1
            c += 1
            p += 2**c
        return reversed(s)

    @staticmethod
    def padded(pair, ref=Pair()):
        s = str(pair) + (' ' * (len(str(ref)) - len(str(pair))))
        return s

    def print_tree(self):
        s = ''
        space = ' ' * (len(str(Pair())))
        sss = self.string()
        for ss in sss:
            for ind in range(len(ss)):
                if ind == 0:
                    s += (space * ss[ind][1]) + str(ss[ind][0])
                else:
                    s += (space * (ss[ind][1] - ss[ind - 1][1])) + str(ss[ind][0])
            s += '\n\n'
        print(s)

    def __str__(self):
        return str(self.pairs)


    def __repr__(self):
        return str(self)


if __name__ == constants.MAIN:
    l = Pair.pairs([('a', 2), ('b', 7), ('c', 21), ('d', 131), ('e', 157), ('f', 137), ('g', 19), ('h', 28)])
    heap = Heap(l, min=False)
    heap.extend(Pair.pairs([('j', 29), ('k', 43), ('l', 72), ('m', 53)]))
    heap.insert(Pair('n', 124))
    heap.insert(Pair('o', 142))
    heap.print()
    s = heap.string()
    heap.print_tree()

