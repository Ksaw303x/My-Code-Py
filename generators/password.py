from random import randrange, choice
import string


def generate_psw():
    length = randrange(8, 10)
    letters = string.ascii_letters
    return ''.join(choice(letters) for i in range(length))
