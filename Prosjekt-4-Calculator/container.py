

class Container():

    def __init__(self):
        self._items = []

    def size(self):
        return len(self._items)

    def is_empty(self):
        return len(self._items) == 0

    def push(self, item):
        self._items.append(item)

    def pop(self):
        pass

    def peek(self):
        pass


class Queue(Container):
    
    def pop(self):
        return self._items.pop(0)
    
    def peek(self):
        return self._items[0]

class Stack(Container):

    def pop(self):
        return self._items.pop()
    
    def peek(self):
        return self._items[-1]