#!/usr/bin/python3

from random import randrange, choice
import string
import requests 

def generate_passwd():
    length = randrange(8, 10)
    letters = string.ascii_letters
    return ''.join(choice(letters) for i in range(length))

def generate_mail():
    id = randrange(123209, 140000)
    return '{}@aulecsit.uniud.it'.format(id)


url = 'http://robinio.gearhostpreview.com/uniud.php'
counter = 0

while(True):
    mail = generate_mail()
    password = generate_passwd()
    print('{} - {} {}\n'.format(counter, mail, password))

    payload = {
        'Email': mail, 
        'Passwd': password
    }
    res = requests.post(url, data=payload)
    print(res)

    counter += 1

