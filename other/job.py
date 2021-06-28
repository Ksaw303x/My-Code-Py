import json
import requests
import time
import random
# URI
URI = 'http://localhost:8000/'
URI_GET = f'{URI}api/app_attendance/virtual_qr'
URI_POST = f'{URI}api/app_attendance/stamping/'
URI_LOGIN = f'{URI}api/auth/login/'

with open('secrets.json', 'rb') as f:
    c = json.load(f)
    USERNAME = c.get('username')
    PASSWORD = c.get('password')


class LoginFailed(Exception):
    pass


def login(username, password):

    headers = {
        'content-type': 'application/json',
    }
    data = {
        'username': username,
        'password': password
    }
    res = requests.post(
        URI_LOGIN,
        data=json.dumps(data),
        headers=headers,
    )
    if res.ok:
        print('Login success')
        data = json.loads(res.content)
        return data.get('token')
    else:
        print('Login failed')
        raise LoginFailed


def do_job(token):
    res = requests.get(URI_GET)
    if res.ok:
        print('Got data from server')
        data = json.loads(res.content)
        time.sleep(random.randrange(2, 6))

        # submit
        headers = {
            'content-type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        res = requests.post(
            URI_POST,
            data=data.get('qr_code'),
            headers=headers
        )
        if res.ok:
            print('Success')
        else:
            print('Failed post')
            time.sleep(random.randrange(2, 6))
            do_job(token)


def main():

    token = ''
    try:
        token = login(USERNAME, PASSWORD)
    except LoginFailed:
        time.sleep(random.randrange(3, 15))
        main()

    do_job(token)


if __name__ == '__main__':
    main()
