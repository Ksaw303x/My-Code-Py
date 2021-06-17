import json
from credit_shield.pack.credit_shield import CreditShield


with open('secrets.json', 'rb') as f:
    c = json.load(f)
    USERNAME = c.get('username')
    PASSWORD = c.get('password')


if __name__ == '__main__':

    api = CreditShield()
    api.login(USERNAME, PASSWORD)
    out = api.get()
    print(out)
