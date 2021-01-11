from time import time
from random import randrange


def my_hash_code(string):
    h = 0
    for c in string:
        h += ord(c)
    return h


def main():

    values ='abcdefghigklmopqrstuvwxyzABC0123456789'
    len_values = len(values)
    str_out = ''
    for count in range(1000000):
        str_out += values[randrange(len_values-1)]

    t1 = time()
    hash1 = my_hash_code(str_out)
    t2 = time()
    t = (t2 - t1)
    print('executed in {}'.format(t))
    print(hash1)


if __name__ == '__main__':
    main()
