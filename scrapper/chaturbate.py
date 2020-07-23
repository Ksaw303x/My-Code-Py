from pprint import pprint
import requests
from bs4 import BeautifulSoup


class Scrapper(object):

    @staticmethod
    def web_scrapper(url):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        chat_list = []
        for vid in soup.findAll(attrs={'class': 'room_list_room'}):
            chat_user = vid.find('a')['href']
            chat_list.append(url + chat_user)

        pprint(chat_list)

    def main(self):
        url = 'https://m.chaturbate.com'
        self.web_scrapper(url)


if __name__ == '__main__':
    i = Scrapper()
    i.main()
