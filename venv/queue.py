from collections import deque


class Queue:
    def __init__(self, values=None):
        self.items = deque()
        if values is None:
            return
        for value in values:
            self.enqueue(value)

    def size(self):
        return len(self.items)

    def empty(self):
        return self.size() == 0

    def not_empty(self):
        return not self.is_empty()

    def enq(self, value):
        self.items.append(value)

    def enq_list(self, values):
        for value in values:
            self.enq(value)

    def deq(self):
        if self.is_empty():
            return None
        return self.items.popleft()