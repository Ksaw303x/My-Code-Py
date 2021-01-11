from random import randrange, choice
import string


def generate_cf(length=None):
    length = length if length else randrange(16, 17)
    letters = string.ascii_uppercase + '1234567890'
    return ''.join(choice(letters) for i in range(length))


def generate_mail_with_id(provider='gmail.com'):
    _id = randrange(123209, 140000)
    return '{}@{}'.format(_id, provider)


def data_extractor(directory):
    data = []
    with open(directory, 'r') as f:
        for line in f.readline():
            data.append(line)
    return data


def generate_name():
    data = []
    with open('data/names.txt', 'r') as f:
        for line in f.readline():
            data.append(line)
    return choice(data)


def generate_surname():
    data = []
    with open('data/surnames.txt', 'r') as f:
        for line in f.readline():
            data.append(line)
    return choice(data)


def generate_place():
    data = []
    with open('data/surnames.txt', 'r') as f:
        for line in f.readline():
            data.append(line)
    return choice(data)
