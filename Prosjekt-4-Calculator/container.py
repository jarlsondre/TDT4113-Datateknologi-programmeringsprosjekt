""" Module for creating different kinds of containers, namely Stacks and Queues """

class Container():
    """ Super class for container data structures """

    def __init__(self):
        self._items = []

    def size(self):
        """ Returns the size of the container structure """
        return len(self._items)

    def is_empty(self):
        """ Returns a boolean indicating whether or not the container is empty or not """
        return len(self._items) == 0

    def push(self, item):
        """ Pushes an element into the container """
        self._items.append(item)

    def pop(self):
        """ Removes an element from the container. Which element depends on the inheriting class """
        pass

    def peek(self):
        """ Returns the top element """
        pass

    def __str__(self):
        return self._items.__str__()


class Queue(Container):
    """ Implementation of the Queue data structure. Extends Container """

    def pop(self):
        """ Removes the element that is at the first position in the queue and returns it """
        return self._items.pop(0)

    def peek(self):
        """ Returns the element that is at the first position in the queue without removing it """
        return self._items[0]


class Stack(Container):
    """ Implementation of the Stack data structure. Extends Container """


    def pop(self):
        """ Removes the element that is at the top of the stack and returns it """
        return self._items.pop()

    def peek(self):
        """ Returns the element that is at the top of the stack without removing it """
        return self._items[-1]
