import requests
from bs4 import BeautifulSoup
from random import randrange


URL = 'https://it.chaturbate.com/'


class ChatrubateUser:
    def __init__(self, username: str):
        self.username: str = username.replace('/', '')
        self.url: str = URL + self.username
        self.__age: int = 20
        self.gender = None

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, value):
        try:
            self.__age = int(value)
        except ValueError:
            self.__age = None


class Bot:

    def send_text(self, text):
        print(text)


class Chatrubate(object):

    def __init__(self, *args, **kwargs):

        self.bot = Bot()

        self._first = None
        self._idx = None
        self._n = None
        self._girls = None

    def __web_scrapper(self, url):

        ppl_list = []
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        for vid in soup.findAll(attrs={'class': 'room_list_room'}):
            g = ChatrubateUser(vid.find('a')['href'])
            g.age = vid.find('span').text
            ppl_list.append(g)
        return ppl_list

    def find_by_age(self, age):
        result = []
        for page in range(3):
            data = self.__web_scrapper(URL+'?page={}'.format(page))
            for user in data:
                if user.age == age:
                    result.append(user)
                    print(user.url)

    def run(self):

        girls_list = self.__web_scrapper(URL)
        len_vl = len(girls_list) - 1

        # Send the first o the query
        if self._first is not None:
            self.bot.send_text(girls_list[0].url)
            return

        if self._girls is not None:
            out = ''
            girls = girls_list[:20]
            for girl in girls:
                out += '{}\n'.format(girl.username)
            self.bot.send_text(out)
            return

        # send in chat a stack of videos
        if self._n:
            n = int(self._n)
            for girl in girls_list:
                self.bot.send_text(girl.url)
                n -= 1
                if n is 0:
                    break
            return

        # Send a specific video in the query array
        if self._idx:
            idx = int(self._idx) - 1

            if idx > len_vl:
                idx = len_vl
            if idx < 0:
                idx = 0

        else:
            idx = randrange(0, len_vl)

        self.bot.send_text(girls_list[idx].url)


if __name__ == '__main__':
    c = Chatrubate()
    c.find_by_age(45)
