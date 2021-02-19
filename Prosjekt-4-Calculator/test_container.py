""" Module for testing container.py file """

import unittest
import container


class TestStack(unittest.TestCase):
    """ Class for testing the Stack datastructure """

    def setUp(self):
        self.stack_instance = container.Stack()
        self.stack_instance.push(3)
        self.stack_instance.push(2)
        self.stack_instance.push(5)

    def test_pop(self):
        self.assertEqual(self.stack_instance.pop(), 5)
        self.assertEqual(self.stack_instance.pop(), 2)
        self.assertEqual(self.stack_instance.pop(), 3)

    def test_peek(self):
        self.assertEqual(self.stack_instance.peek(), 5)
        self.stack_instance.pop()
        self.assertEqual(self.stack_instance.peek(), 2)

    def test_size(self):
        self.assertEqual(self.stack_instance.size(), 3)
        self.stack_instance.pop()
        self.assertEqual(self.stack_instance.size(), 2)

    def test_is_empty(self):
        for _ in range(self.stack_instance.size()):
            self.stack_instance.pop()
        self.assertTrue(self.stack_instance.is_empty)


class TestQueue(unittest.TestCase):
    """ Class for testing the Queue datastructure """

    def setUp(self):
        self.queue_instance = container.Queue()
        self.queue_instance.push(3)
        self.queue_instance.push(2)
        self.queue_instance.push(5)

    def test_pop(self):
        self.assertEqual(self.queue_instance.pop(), 3)
        self.assertEqual(self.queue_instance.pop(), 2)
        self.assertEqual(self.queue_instance.pop(), 5)

    def test_peek(self):
        self.assertEqual(self.queue_instance.peek(), 3)
        self.queue_instance.pop()
        self.assertEqual(self.queue_instance.peek(), 2)

    def test_size(self):
        self.assertEqual(self.queue_instance.size(), 3)
        self.queue_instance.pop()
        self.assertEqual(self.queue_instance.size(), 2)

    def test_is_empty(self):
        for _ in range(self.queue_instance.size()):
            self.queue_instance.pop()
        self.assertTrue(self.queue_instance.is_empty)


if __name__ == "__main__":
    unittest.main()
