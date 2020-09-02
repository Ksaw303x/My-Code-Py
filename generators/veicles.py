from random import randrange, choice
import string


def generate_license_number():
    out = ''
    letters = string.ascii_letters
    numbers = '1234567890'
    out += ''.join(choice(letters).upper() for i in range(2))
    out += ''.join(choice(numbers).upper() for i in range(3))
    out += ''.join(choice(letters).upper() for i in range(2))
    return out


if __name__ == '__main__':
    licenses = []
    for i in range(10000):
        license_number = generate_license_number()
        if license_number not in licenses:
            licenses.append(license_number)

    with open('targhe.txt', 'w') as f:
        for el in licenses:
            f.writelines('{}\n'.format(el))
