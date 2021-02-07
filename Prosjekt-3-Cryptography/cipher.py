
import crypto_utils
import random

class Cipher:

    def __init__(self, key):
        self.modulo = 95
        self.key = key

    def encode(self, message):
        return message

    def decode(self, message):
        return message

    def verify(self):
        example_message = "Test: abcxyz019-!$@"
        print(f"Verifying cipher with example text: {example_message}")
        encoded = self.encode(example_message)
        print(f"Encoded message is {encoded}")
        decoded = self.decode(encoded)
        print(f"Decoded message is {decoded}")
        print(f"Successful? {decoded == example_message}")


class Caesar(Cipher):


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

    def encode(self, message):
        new_message = ""
        for letter in message:
            value = ord(letter) - 32
            new_value = (value * self.key) % self.modulo
            new_message += chr(new_value + 32)
        return new_message

    def decode(self, message):
        new_message = ""
        modular_inverse = crypto_utils.modular_inverse(self.key, self.modulo)
        for letter in message:
            value = ord(letter) - 32
            new_value = (value * modular_inverse) % self.modulo
            new_message += chr(new_value + 32)
        return new_message

class Affine(Cipher):

    def __init__(self, key1, key2):
        super().__init__(key1)
        self.key = [key1, key2]

    def encode(self, message):
        new_message = ""
        for letter in message:
            value = ord(letter) - 32
            new_value = (value * self.key[0] + self.key[1]) % self.modulo
            new_message += chr(new_value + 32)
        return new_message




    def decode(self, message):
        new_message = ""
        modular_inverse = crypto_utils.modular_inverse(self.key[0], self.modulo)
        for letter in message:
            value = ord(letter) - 32
            new_value = ((value - self.key[1]) * modular_inverse) % self.modulo
            new_message += chr(new_value + 32)
        return new_message

class Unbreakable(Cipher):

    def encode(self, message):
        new_message = ""
        for i in range(len(message)):
            value1 = (ord(message[i])) - 32
            value2 = (ord(self.key[i % len(self.key)])) - 32
            new_value = (value1 + value2) % self.modulo
            new_message += chr(new_value + 32)
        return  new_message



    def decode(self, message):
        new_message = ""
        for i in range(len(message)):
            value1 = (ord(message[i])) - 32
            value2 = (ord(self.key[i % len(self.key)])) - 32
            new_value = (value1 - value2) % self.modulo
            new_message += chr(new_value + 32)
        return  new_message


class RSA(Cipher):

    def __init__(self):
        n, e, d = self.generate_keys()
        self.public_key = (n, e)
        self.private_key = (n, d)
        print("n is %d" % n)

    def generate_keys(self):
        p = crypto_utils.generate_random_prime(8)
        q = crypto_utils.generate_random_prime(8)
        while p == q:
            q = crypto_utils.generate_random_prime(8)
        n = p*q
        phi = (p-1)*(q-1)
        e, d = 3, 3  # Setting initial values with gcd > 1
        while crypto_utils.extended_gcd(e, phi)[0] != 1:
            e = random.randint(3, phi - 1)
            d = crypto_utils.modular_inverse(e, phi)
        return n, e, d


    def encode(self, message):
        encryption_blocks = crypto_utils.blocks_from_text(message, 2)
        print(f"encryption blocks: {encryption_blocks}")
        new_blocks = []
        for block in encryption_blocks:
            c = pow(block, self.public_key[1], self.public_key[0])
            new_blocks.append(c)
        print(f"new blocks: {new_blocks}")
        return new_blocks


    def decode(self, message):
        new_blocks = []
        for block in message:
            t = pow(block, self.private_key[1], self.private_key[0])
            new_blocks.append(t)
        new_message = crypto_utils.text_from_blocks(new_blocks, 8)
        return new_message

def main():
    my_cipher = RSA()
    my_cipher.verify()


if __name__ == "__main__":
    main()
