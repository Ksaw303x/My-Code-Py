from pprint import pprint
import requests
from bs4 import BeautifulSoup


class Scrapper(object):

    @staticmethod
    def scrapper_news_events(url):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        post_list = []
        for post in soup.findAll(attrs={'class': 'su-post'}):
            a = post.find('a')
            title = a.text
            link = a['href']
            data = post.find(attrs={'class': 'su-post-meta'}).text.replace('\t', '').replace('\n', '')
            text = post.find(attrs={'class': 'su-post-excerpt'}).text.replace('\n', '')
            post_list.append((title, link, data, text))

        pprint(post_list)

    def main(self):
        url = 'https://users.dimi.uniud.it/~marino.miculan/wordpress/news-events/'
        self.scrapper_news_events(url)


if __name__ == '__main__':
    i = Scrapper()
    i.main()
