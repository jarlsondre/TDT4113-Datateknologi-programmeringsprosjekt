
import math
import random
import crypto_utils


class Cipher:

    def __init__(self, key):
        self.modulo = 95
        self.key = key

    def encode(self, message):
        return message

    def set_key(self, key):
        self.key = key

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

    def __init__(self, key_tuple):
        super().__init__(key_tuple)

    def encode(self, message):
        new_message = ""
        for letter in message:
            value = ord(letter) - 32
            new_value = (value * self.key[0] + self.key[1]) % self.modulo
            new_message += chr(new_value + 32)
        return new_message

    def decode(self, message):
        new_message = ""
        modular_inverse = crypto_utils.modular_inverse(
            self.key[0], self.modulo)
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
        return new_message

    def decode(self, message):
        new_message = ""
        for i in range(len(message)):
            value1 = (ord(message[i])) - 32
            value2 = (ord(self.key[i % len(self.key)])) - 32
            new_value = (value1 - value2) % self.modulo
            new_message += chr(new_value + 32)
        return new_message


class RSA(Cipher):

    def __init__(self):
        number, encrypt, decrypt = self.generate_keys()
        self.public_key = (number, encrypt)
        self.private_key = (number, decrypt)
        print(self.private_key, self.public_key)

    def generate_keys(self):
        prime1 = crypto_utils.generate_random_prime(8)
        prime2 = crypto_utils.generate_random_prime(8)
        while prime1 == prime2:
            prime2 = crypto_utils.generate_random_prime(8)
        number = prime2 * prime1
        phi = (prime1 - 1) * (prime2 - 1)
        encrypt, decrypt = 12, 16  # Setting initial values with gcd > 1
        while math.gcd(encrypt, phi) != 1:
            encrypt = random.randint(3, phi - 1)
            decrypt = crypto_utils.modular_inverse(encrypt, phi)
        return number, encrypt, decrypt

    def encode(self, message):
        encryption_blocks = crypto_utils.blocks_from_text(message, 1)
        new_blocks = []
        for block in encryption_blocks:
            encrypted_block = pow(block, self.public_key[1], self.public_key[0])
            new_blocks.append(encrypted_block)
        return new_blocks

    def decode(self, message):
        new_blocks = []
        for block in message:
            decrypted_block = pow(block, self.private_key[1], self.private_key[0])
            new_blocks.append(decrypted_block)
        new_message = crypto_utils.text_from_blocks(new_blocks, 8)
        return new_message


def main():
    my_cipher = RSA()
    my_cipher.verify()


if __name__ == "__main__":
    main()
