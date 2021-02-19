""" Module for functions and operators """

import numbers
import numpy


class Function:
    """ Class for wrapping functions """
    def __init__(self, func):
        self.func = func

    def execute(self, element, debug=True):
        """ Executing the function """
        # Check type
        if not isinstance(element, numbers.Number):
            raise TypeError("The element must be a number")
        result = self.func(element)

        # Report
        if debug is True:
            print(
                "Function: " +
                self.func.__name__ +
                "({:f}) = {:f}".format(
                    element,
                    result))
        return result


class Operator:
    """ Class for wrapping operators """
    def __init__(self, operation, strength):
        self.operation = operation
        self.strength = strength

    def execute(self, operand1, operand2):
        """ Returns the result of the operation used on the two operands """
        return self.operation(operand1, operand2)


def provided_test():
    """ Test that were given in the assignment-document """
    add_op = Operator(operation=numpy.add, strength=0)
    multiply_op = Operator(operation=numpy.multiply, strength=1)
    print(add_op.execute(1, multiply_op.execute(2, 3)))
