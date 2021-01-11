import re
import requests
from io import BytesIO
from bs4 import BeautifulSoup


class TikTok:

    URL_REGEX = re.compile(
        r'^(?:http|ftp)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|)'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    def __init__(self):

        self.url = 'https://vm.tiktok.com/J8DvHmf/'

    @property
    def is_valid_url(self):
        """
        :param url: the url of the video
        :return:

        check if is a tiktok url and is valid
        """
        if 'tiktok' not in self.url:
            return False

        if not re.match(self.URL_REGEX, self.url):
            return False

        return True

    @staticmethod
    def __web_scrapper(url):
        """
        :param url: url of the tiktok video
        :return: download link
        """
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = 'id=' + url

        page = requests.post('https://ssstiktok.io/api/1/fetch', headers=headers, data=data)
        soup = BeautifulSoup(page.content, 'html.parser')
        download_link = 'https://ssstiktok.io/' + soup.find('a')['href']
        return download_link

    def get_video(self):
        download_link = self.__web_scrapper(self.url)
        res = requests.get(download_link)
        print(res)
        video = BytesIO()
        for chunk in res:
            video.write(chunk)

        return video.seek(0)

    def run(self):

        out = 'Devi dare come arg un url valido'

        if not self.url:
            print(out)
            return

        if not self.is_valid_url:
            print(out)
            return

        self.get_video()


if __name__ == '__main__':
    tt = TikTok()
    tt.run()

