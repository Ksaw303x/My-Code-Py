import xmltodict
from pprint import pprint
import json
import requests


class Feed:

    def __init__(self):

        self.urls = []

    def update(self):
        out = xmltodict.parse(my_xml)
        print(type(out))
        pprint(out)


if __name__ == '__main__':
    f = Feed()
    f.update()
