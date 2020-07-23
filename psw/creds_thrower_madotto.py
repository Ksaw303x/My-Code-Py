import random
import requests

wordlist = []
with open('dictionary.txt') as f:
    wordlist = f.readlines()
    wordlist = [w.strip() for w in wordlist]

def getAddress():
    matr = 100000 + random.randint(10000,50000)
    return str(matr) + '@aulecsit.uniud.it'

def getPassword():
    nums = random.choice(['', str(random.randint(1,99))])
    return (random.choice(wordlist) + nums)

tgt = 'http://robinio.gearhostpreview.com/uniud.php'

while True:
    addr = getAddress()
    passwd = getPassword()
    r = requests.post(tgt, data = {'Email': addr, 'Passwd': passwd})
    if r.status_code == requests.codes.ok:
        print('OK, sent ' + addr + ':' + passwd)
    else:
        print('ERROR, the server responded abnormally: ' + str(r.status_code))
