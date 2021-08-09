from collections import deque
from constants import *


class Stack:
    def __init__(self):
        self.items = deque()

    def size(self):
        return len(self.items)

    def is_empty(self):
        return self.size() == 0

    def is_not_empty(self):
        return not self.is_empty()

    def push(self, value):
        self.items.append(value)

    def pop(self):
        return self.items.pop() if self.is_not_empty() else None

    def top(self):
        return self.items[-1] if self.is_not_empty() else None


    def __str__(self):
        if self.is_empty():
            return 'stack is empty'
        s = 'top of the stack\n-------------\n'
        s += '\n-------------\n'.join(str(item) for item in reversed(self.items))
        s += '\n-------------\nbottom of the stack'
        return s

    def __repr__(self):
        return self.__str__()


if __name__ == MAIN:
    stack = Stack()
    stack.push(10)
    stack.push(5)
    print(stack)
    stack.pop()
    stack.top()
    stack.pop()
    print(stack.pop())
