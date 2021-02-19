import re
import numpy
from function import Function, Operator
from container import Queue, Stack


class Calculator:

    def __init__(self):
        # Define the functions suppor ted by linking them to Python
        # functions. These can be made elsewherein the program
        # or imported (e.g., from numpy)
        self.functions = {'EXP': Function(numpy.exp),
                          'LOG': Function(numpy.log),
                          'SIN': Function(numpy.sin),
                          'COS': Function(numpy.cos),
                          'SQRT': Function(numpy.sqrt)}
        # Define the operators supported .
        # Link them to Python functions (here: from numpy)
        self.operators = {'ADD': Operator(numpy.add, 0),
                          'MULTIPLY': Operator(numpy.multiply, 1),
                          'DIVIDE': Operator(numpy.divide, 1),
                          'SUBTRACT': Operator(numpy.subtract, 0)}
        # Define the output−queue .
        # The parse_text method fills this with RPN.
        # The evaluate output queue method evaluates it
        self.output_queue = Queue()

    def evaluate_rpn_queue(self):
        calculation_stack = Stack()
        while not self.output_queue.is_empty():
            current_item = self.output_queue.pop()
            if isinstance(current_item, (int, float)
                          ):  # Checking if current item is a number
                calculation_stack.push(current_item)
            elif current_item in self.functions:  # Checking if current item is a function
                calculation_stack.push(
                    self.functions[current_item].execute(
                        calculation_stack.pop()))
            else:  # If it's not a function or a number, then it must be an operator
                first_item = calculation_stack.pop()
                second_item = calculation_stack.pop()
                calculation_stack.push(
                    self.operators[current_item].execute(
                        second_item, first_item))
        return calculation_stack.pop()

    def build_rpn_queue(self, input_queue):
        temp_stack = Stack()
        self.output_queue = Queue()  # Clearing the stored output_queue
        while not input_queue.is_empty():
            current_item = input_queue.pop()
            if isinstance(current_item, (int, float)
                          ):  # If the element is a number
                self.output_queue.push(current_item)
            elif current_item in self.functions or current_item == '(':
                temp_stack.push(current_item)
            elif current_item == ')':
                while (top_elem := temp_stack.pop()) != '(':
                    self.output_queue.push(top_elem)
            elif current_item in self.operators:  # If the element is an operator
                while not temp_stack.is_empty() and self.operators.get(temp_stack.peek(),
                        self.operators[current_item]).strength >= self.operators[current_item].strength and temp_stack.peek() != '(':
                    self.output_queue.push(temp_stack.pop())
                temp_stack.push(current_item)
        while not temp_stack.is_empty():  # Pushing the remaining elements from stack to queue
            self.output_queue.push(temp_stack.pop())

    def text_parser(self, input_text):
        # Matching functions
        targets = "|".join(["^" + func for func in self.functions.keys()])
        targets += "|[-0-9.]+"  # Matching numbers
        # Matching operators
        targets += "|" + "|".join(["^" + op for op in self.operators.keys()])
        targets += r"|\(|\)"  # Matching parentheses

        text_copy = input_text.replace(" ", "").upper()
        output_list = []
        while len(text_copy) > 0:
            match = re.search(targets, text_copy)
            output_list.append(text_copy[0:match.end(0)])
            text_copy = text_copy[match.end(0):]
        return_queue = Queue()
        for elem in output_list:
            if re.match("[-0-9.]+", elem) is None:
                return_queue.push(elem)
            else:
                return_queue.push(float(elem))
        return return_queue

    def calculate_expression(self, txt):
        parsed_text = self.text_parser(txt)
        self.build_rpn_queue(parsed_text)
        return self.evaluate_rpn_queue()



def provided_test1():
    print("---TEST1---")
    calc = Calculator()
    print(
        calc.functions['EXP'].execute(
            calc.operators['ADD'].execute(
                1, calc.operators['MULTIPLY'].execute(
                    2, 3))))
    print()


def provided_test2():
    print("---TEST2---")
    test_queue = [1, 2, 3, 'MULTIPLY', 'ADD', 'EXP']
    calc = Calculator()
    for elem in test_queue:
        calc.output_queue.push(elem)
    print(calc.evaluate_rpn_queue())
    print()


def self_made_test1():
    print("---TEST3---")
    test_queue = [1, 2, 3, 'MULTIPLY', 'ADD', 'EXP']
    test_queue = Queue()
    test_list = ['EXP', '(', 1, 'ADD', 2, 'MULTIPLY', 3, ')']
    for elem in test_list:
        test_queue.push(elem)
    print(test_queue)
    calc = Calculator()
    calc.build_rpn_queue(test_queue)
    print(calc.output_queue)
    print(calc.evaluate_rpn_queue())
    print()


def self_made_test2():
    print("---TEST4---")
    calc = Calculator()
    print(calc.text_parser("exp (1 add 7 multiply 2)"))
    print()


def self_made_test3():
    print("---TEST5---")
    text1 = "EXP (1 add 2 multiply 3)"
    text2 = "((15 DIVIDE (7 SUBTRACT (1 ADD 1))) MULTIPLY 3) SUBTRACT (2 ADD (1 ADD 1))"
    calc = Calculator()
    calc.build_rpn_queue(calc.text_parser(text1))
    print(calc.calculate_expression(text1))
    print(calc.calculate_expression(text2))
    print()

def run_all_tests():
    provided_test1()
    provided_test2()
    self_made_test1()
    self_made_test2()
    self_made_test3()

run_all_tests()
