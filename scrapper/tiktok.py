import os
import sys
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException

win = 'https://chromedriver.storage.googleapis.com/85.0.4183.87/chromedriver_win32.zip'


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
    wd = webdriver.Chrome('./{}/{}'.format(folder, webdriver_name), options=chrome_options)

    return wd


if __name__ == '__main__':
    webdriver = load_webdriver()
    webdriver.get('https://www.google.com')
