

class Person:

    def __init__(self):
        pass

    def set_key(self):
        pass

    def get_key(self):
        pass

    def operate_cipher(self):
        pass


class Sender(Person):

    def set_key(self):
        print("Setting key...")


class Receiver(Person):

    def set_key(self):
        print("Setting key... hehe")