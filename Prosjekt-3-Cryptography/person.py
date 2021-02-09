import string
import math
import crypto_utils
import cipher


def read_from_file(filename):
    with open(filename) as file:
        contents = file.read()
    return contents


class Person:

    def __init__(self, key):
        self.key = key
        self.cipher = None

    def set_key(self, key):
        self.key = key
        self.cipher.set_key(key)

    def get_key(self):
        return self.key

    def set_cipher(self, cipher):
        self.cipher = cipher
        self.cipher.set_key(self.key)

    def operate_cipher(self, message):
        pass


class Sender(Person):

    def operate_cipher(self, message):
        return self.cipher.encode(message)


class Receiver(Person):

    def set_cipher(self, cipher):
        self.cipher = cipher

    def operate_cipher(self, message):
        self.cipher.set_key(self.key)
        return self.cipher.decode(message)


class Hacker(Person):

    def __init__(self):
        super().__init__(None)
        self.type = None
        self.possible_factors = [
            i for i in range(
                2, 95) if math.gcd(
                i, 95) == 1]

    def set_cipher(self, cipher):
        self.cipher = cipher

    def set_cipher_type(self, type):
        """ This could be C, M, A, or U """
        self.type = type

    def count_words(self, message, word_list):
        words_in_message = message.split(" ")  # Creating a list of words
        for j in range(len(words_in_message)):
            words_in_message[j] = words_in_message[j].strip(
                string.punctuation).lower()
        counter = 0
        for word in words_in_message:  # Counting the occurence of words
            if word in word_list:
                counter += 1
        return counter

    def find_most_common(self, counting_dict):
        highest_value = 0
        most_common = ""
        for key in counting_dict:  # Finding the message with the most words
            if counting_dict[key] > highest_value:
                highest_value = counting_dict[key]
                most_common = key
        return most_common

    def operate_cipher(self, message):
        if self.type in ['C', 'M', 'A', 'U']:
            counting_dict = {}
            word_list = read_from_file("english_words.txt").split(
                "\n")  # Taking in the list of english words
        if self.type == "C":
            for i in range(95):  # Creating all different kinds of messages
                new_message = ""
                for letter in message:  # Shifting the value
                    value = ord(letter) - 32
                    new_value = (value - i) % self.cipher.modulo
                    new_message += chr(new_value + 32)
                counting_dict[new_message] = self.count_words(
                    new_message, word_list)
            return self.find_most_common(counting_dict)
        elif self.type == "M":
            for factor in self.possible_factors:
                new_message = ""
                modular_inverse = crypto_utils.modular_inverse(
                    factor, self.cipher.modulo)
                for letter in message:
                    value = ord(letter) - 32
                    new_value = (value * modular_inverse) % self.cipher.modulo
                    new_message += chr(new_value + 32)
                counting_dict[new_message] = self.count_words(
                    new_message, word_list)
            return self.find_most_common(counting_dict)
        elif self.type == "A":
            for factor in self.possible_factors:
                for i in range(95):
                    new_message = ""
                    modular_inverse = crypto_utils.modular_inverse(
                        factor, self.cipher.modulo)
                    for letter in message:
                        value = ord(letter) - 32
                        new_value = (
                            (value - i) * modular_inverse) % self.cipher.modulo
                        new_message += chr(new_value + 32)
                    counting_dict[new_message] = self.count_words(
                        new_message, word_list)
            return self.find_most_common(counting_dict)
        elif self.type == "U":
            counter = 0
            for english_word in word_list[0:1000]:
                new_message = ""
                counter += 1
                print(counter)
                for i in range(len(message)):
                    value1 = ord(message[i]) - 32
                    value2 = ord(english_word[i % len(english_word)]) - 32
                    new_value = (value1 - value2) % self.cipher.modulo
                    new_message += chr(new_value + 32)
                counting_dict[new_message] = self.count_words(
                    new_message, word_list)
            return self.find_most_common(counting_dict)
        else:
            return None


def main():

    # Creating the cipher
    cipher1 = cipher.Unbreakable("above")

    # Creating the people
    person1 = Sender("above")
    person2 = Receiver("above")
    person1.set_cipher(cipher1)
    person2.set_cipher(cipher1)

    # Sending a message
    sending_message = "hello you"
    print("Sending the message: %s" % sending_message)
    encoded_message = person1.operate_cipher(sending_message)
    print("The encoded message is: %s" % encoded_message)

    # Hacker trying to decode message
    person3 = Hacker()
    person3.set_cipher(cipher1)
    person3.set_cipher_type("U")
    hacked_message = person3.operate_cipher(encoded_message)
    print("The hacked message is: %s" % hacked_message)

    # Receiver decoding the message
    decoded_message = person2.operate_cipher(encoded_message)
    print("The decoded message is: %s" % decoded_message)


if __name__ == "__main__":
    main()
