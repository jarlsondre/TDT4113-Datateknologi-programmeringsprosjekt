import numbers

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

