

class Cipher:

    def __init__(self):
        self.modulo = 95

    def encode(self, message):
        return message

    def decode(self, message):
        return message

    def verify(self):
        example_message = "This is a test :)"
        print(f"Verifying cipher with example text: {example_message}")
        encoded = self.encode(example_message)
        print(f"Encoded message is {encoded}")
        decoded = self.decode(encoded)
        print(f"Decoded message is {decoded}")
        print(f"Successful? {decoded == example_message}")


class Caesar(Cipher):

    def __init__(self, key):
        super().__init__()
        self.key = key

    def encode(self, message):
        new_message = ""
        for letter in message:
            value = ord(letter) - 32
            new_value = (value + self.key) % self.modulo
            new_message += chr(new_value + 32)
        return new_message

    def decode(self, message):
        new_message = ""
        for letter in message:
            value = ord(letter) - 32
            new_value = (value - self.key) % self.modulo
            new_message += chr(new_value + 32)
        return new_message


class Multiplication(Cipher):

    def __init__(self):
        super().__init__()
        print("Initialized :) ")


def main():
    my_cipher = Caesar(5)
    my_cipher.verify()


if __name__ == "__main__":
    main()
