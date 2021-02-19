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
    
    def build_rpn_queue(self):
        pass




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

provided_test2()