import os
import sys
from selenium import webdriver
from bs4 import BeautifulSoup

USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; nl-NL; rv:1.7.5) Gecko/20041202 Firefox/1.0'


class TiktokDownloader:

    def __init__(self):

        self.url = ''
        self.__retry_iterations = 0

    @staticmethod
    def get_webdriver_path():
        folder = 'commands/social/tiktok/webdriver/'
        if not os.path.exists(folder):
            os.makedirs(folder)

        if sys.platform.startswith('linux') and sys.maxsize > 2 ** 32:
            webdriver_name = 'driver'
        elif sys.platform.startswith('win'):
            webdriver_name = 'chromedriver.exe'
        else:
            raise RuntimeError('Could not determine chrome driver download URL for this platform.')

        return './{}/{}'.format(folder, webdriver_name)

    def __get_video_download_link(self, url):  # with selenium
        param_declaration = url.find('?')
        url = url[:param_declaration]

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-automation")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # chrome_options.add_argument("--proxy-server={0}".format(proxy.proxy))
        chrome_options.add_experimental_option("mobileEmulation", {"deviceName": "Galaxy S5"})
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        # chrome_options.add_argument('--headless')  # do not show the browser

        webdriver_path = self.get_webdriver_path()
        wd = webdriver.Chrome(webdriver_path, options=chrome_options)

        wd.get(url)  # open the given link

        # new_url = wd.current_url  # get the link when the page is full loaded

        soup = BeautifulSoup(wd.page_source, 'html.parser')
        body = soup.body
        video_box = body.find('video', id='tiktokVideo')
        video_url = video_box.get('src')

        print(video_url)
        # wd.close()
        return video_url

    def get_file(self):
        self.__retry_iterations = 0
        download_link = self.__get_video_download_link(self.url)
        print(download_link)


if __name__ == '__main__':
    # video_url = 'https://vm.tiktok.com/ZSPqLXRS/'
    _url = 'https://www.tiktok.com/@shanghaiobserved/video/6868974713188715782'

    tl = TiktokDownloader()
    tl.url = _url
    tl.get_file()
