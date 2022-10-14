import requests
import string
from random import randrange, choice

url = 'http://sandbox1.reply.it/ba3eab423b1f3ff4df2b8da016084b61/'

# header with token
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/80.0.3987.132 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
    'Authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJyb2xlIjoidXNlciJ9.'
                     'jcBjGaU-N9koHQvZ8mYKmNi5B-QNmCTejbSUUsodkDw',
    'xAuthorization': 'superbo0ss',
    'x-user': 'superbo0ss',
    'user': 'superbo0ss',
    'x-superbo0ss': 'true',
    'superbo0ss': '1'
}


def generate_string(length):
    letters = string.ascii_letters
    return ''.join(choice(letters) for i in range(length))


def send_request(text):
    # send a request to the server

    payload = {
        'text': text,
        'user': 'superbo0ss',
    }
    res = requests.post(url+'chat', data=payload, headers=HEADERS)
    print(text, res.status_code, res.content)


def get_token():
    # get token from the server
    res = requests.get(url+'token', headers=HEADERS)
    print(res.status_code, res.content, res.headers)


if __name__ == '__main__':

    # get_token()

    # send_request(' a ')
    # send_request('i feel ')
    # send_request('whats')
    # send_request(' please')
    send_request('please')
    send_request('r u')
    send_request('allroles')
    send_request('àèù#àùà#')

    # send_request('please whats a superbo0ss')

    # send_request('help please')
    # send_request('user')
