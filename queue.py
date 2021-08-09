from collections import deque
from constants import *


class Queue:
    def __init__(self):
        self.items = deque()

    def size(self):
        return len(self.items)

    def is_empty(self):
        return self.size() == 0

    def is_not_empty(self):
        return not self.is_empty()

    def enq(self, value):
        self.items.appendleft(value)

    def deq(self):
        return self.items.pop() if self.is_not_empty() else None

    def peek(self):
        return self.items[-1] if self.is_not_empty() else None


    def __str__(self):
        if self.is_empty():
            return 'queue is empty'
        s = 'front of the queue\n-------------\n'
        s += '\n-------------\n'.join(str(item) for item in reversed(self.items))
        s += '\n-------------\nback of the queue'
        return s

    def __repr__(self):
        return self.__str__()


if __name__ == MAIN:
    queue = Queue()
    queue.enq(10)
    queue.enq(5)
    print(queue)
    queue.deq()
    queue.peek()
    queue.deq()
    print(queue.deq())
