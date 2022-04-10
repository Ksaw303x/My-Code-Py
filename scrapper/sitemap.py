import logging
import requests
from bs4 import BeautifulSoup
from pysitemap import crawler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class SiteMapManager:

    def __init__(self, url):
        self.url: str = url
        self._raw_sitemap = None

    def generate_sitemap(self):
        logger.info(f'Generating site map for {self.url}')
        crawler(self.url, out_file='sitemap.xml', exclude_urls=[".pdf", ".jpg", ".zip"])

    def load_sitemap(self):
        try:
            res = requests.get(f"{self.url}/sitemap.xml")
        except Exception as exc:
            print(exc)
            return

        if res.ok:
            self._raw_sitemap = res.text
            return True
        print(f'Site map {self.url} not found')
        self.generate_sitemap()
        return False

    def read_sitemap(self):

        if not self._raw_sitemap:
            return

        soup = BeautifulSoup(self._raw_sitemap, "html.parser")
        sitemap_count = len(soup.find_all('sitemap'))
        print(f"sitemap count: {sitemap_count}")
        print(soup.get_text())


if __name__ == '__main__':

    sites = [
        'https://Beforward.jp',
        'https://Sbtjapan.com',
        'https://Tc-v.com',
        'https://Autowini.com',
        'https://Vigo4u.com',
        'https://One2car.com',
        'https://Autotrader.co.uk',
        'https://Mobile.de',
        'https://Dubicars.com',
        'https://Cargurus.com',
    ]

    for site in sites:
        parser = SiteMapManager(site)
        parser.load_sitemap()
