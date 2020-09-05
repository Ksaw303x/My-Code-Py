import os
import sys
from selenium import webdriver
from bs4 import BeautifulSoup

USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; nl-NL; rv:1.7.5) Gecko/20041202 Firefox/1.0'


def load_webdriver():
    folder = 'webdriver/'
    if not os.path.exists(folder):
        os.makedirs(folder)

    if sys.platform.startswith('linux') and sys.maxsize > 2 ** 32:
        webdriver_name = 'chromedriver'
    elif sys.platform.startswith('win'):
        webdriver_name = 'chromedriver.exe'
    else:
        raise RuntimeError('Could not determine chrome driver download URL for this platform.')

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('user-agent={}'.format(USER_AGENT))
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1420,1080')
    chrome_options.add_argument('--headless')  # do not show the browser

    wd = webdriver.Chrome('./{}/{}'.format(folder, webdriver_name), options=chrome_options)

    return wd


if __name__ == '__main__':
    # url = 'https://vm.tiktok.com/ZSPqLXRS/'
    url = 'https://www.tiktok.com/@shanghaiobserved/video/6868974713188715782'

    param_declaration = url.find('?')
    url = url[:param_declaration]

    webdriver = load_webdriver()
    webdriver.get(url)

    new_url = webdriver.current_url

    soup = BeautifulSoup(webdriver.page_source, 'html.parser')
    body = soup.body
    video_box = body.find('video', id='tiktokVideo')
    video_url = video_box.get('src')
    print(video_url)

    # webdriver.close()
