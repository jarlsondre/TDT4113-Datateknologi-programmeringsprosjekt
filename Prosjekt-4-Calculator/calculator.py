from function import Function, Operator
import numpy
from container import Queue, Stack

class Calculator:

    def __init__(self):
        # Define the functions suppor ted by linking them to Python
        # functions. These can be made elsewherein the program 
        # or imported (e.g., from numpy)
        self.functions = {'EXP': Function (numpy.exp),
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
            if isinstance(current_item,(int, float)): # Checking if current item is a number 
                calculation_stack.push(current_item)
            elif current_item in self.functions: # Checking if current item is a function
                calculation_stack.push(self.functions[current_item].execute(calculation_stack.pop()))
            else: # If it's not a function or a number, then it must be an operator
                first_item = calculation_stack.pop()
                second_item = calculation_stack.pop()
                calculation_stack.push(self.operators[current_item].execute(second_item, first_item))
        return calculation_stack.pop()
    
    def build_rpn_queue(self, input_queue):
        temp_stack = Stack()
        self.output_queue = Queue() # Clearing the stored output_queue
        while not input_queue.is_empty():
            current_item = input_queue.pop()
            if isinstance(current_item, (int, float)): # If the element is a number
                self.output_queue.push(current_item)
            elif current_item in self.functions or current_item == '(':
                temp_stack.push(current_item)
            elif current_item == ')':
                while (top_elem := temp_stack.pop()) != '(':
                    self.output_queue.push(top_elem)
            elif current_item in self.operators:  # If the element is an operator
                while not temp_stack.is_empty() and self.operators.get(temp_stack.peek(), self.operators[current_item]).strength >= self.operators[current_item].strength and temp_stack.peek() != '(':
                    self.output_queue.push(temp_stack.pop())
                temp_stack.push(current_item)
        while not temp_stack.is_empty():  # Pushing the remaining elements from stack to queue
            self.output_queue.push(temp_stack.pop())
     




def provided_test1():
    calc = Calculator()
    print(calc.functions['EXP'].execute(
        calc.operators['ADD'].execute(1,
        calc.operators['MULTIPLY'].execute(2, 3))))

def provided_test2():
    test_queue = [1, 2, 3, 'MULTIPLY', 'ADD', 'EXP']
    calc = Calculator()
    for i in range(len(test_queue)):
        calc.output_queue.push(test_queue[i])
    print(calc.evaluate_rpn_queue())

def self_made_test1():
    test_queue = Queue()
    test_list = ['EXP', '(', 1, 'ADD', 2, 'MULTIPLY', 3, ')']
    for elem in test_list:
        test_queue.push(elem)
    print(test_queue)
    calc = Calculator()
    calc.build_rpn_queue(test_queue)
    print(calc.output_queue)
    print(calc.evaluate_rpn_queue())

self_made_test1()