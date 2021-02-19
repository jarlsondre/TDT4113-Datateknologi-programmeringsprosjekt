import numbers
import numpy

class Function:
    def __init__(self, func):
        self.func = func
    
    def execute(self, element , debug=True):
        # Check type
        if not isinstance(element , numbers.Number ):
            raise TypeError ("The element must be a number")
        result = self.func(element)

        # Report
        if debug is True:
            print("Function: " + self.func.__name__ + "({:f}) = {:f}".format(element , result ))
        return result 

class Operator:
    def __init__(self, operation, strength):
        self.operation = operation
        self.strength = strength

    def execute(self, operand1, operand2):
        return self.operation(operand1, operand2)


def provided_test():
    add_op = Operator(operation=numpy.add, strength=0)
    multiply_op = Operator(operation=numpy.multiply, strength=1)
    print(add_op.execute (1, multiply_op.execute(2, 3)))

