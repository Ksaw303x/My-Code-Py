import requests
import json


class InstagramLikeScraper(object):

    def __init__(self):

        self.names_list = []

    def __extract_data(self, url):
        r = requests.get(url)
        json_data = json.loads(r.content)
        try:
            users_data = json_data['data']['shortcode_media']['edge_liked_by']['edges']
        except Exception as e:
            print(e)
            return

        for el in users_data:
            try:
                username = el['node'].get('username')
                self.names_list.append(username)
            except Exception as e:
                print(e)
                return

    def __save_to_file(self, file_name):
        out = open(file_name, 'w')
        for line in self.names_list:
            out.write(line + "\n")
        out.close()

    def like_scraper(self, file_name_in, file_name_out):
        with open(file_name_in) as f:
            for line in f:
                self.__extract_data(line)

        self.__save_to_file(file_name_out)


class MergeLists(object):
    def __init__(self):
        self.list_a = []
        self.list_b = []

        self.out = []

    def __read_file(self, file_name_a, file_name_b):
        with open(file_name_a) as f:
            for line in f:
                self.list_a.append(line)

        with open(file_name_b) as f:
            for line in f:
                self.list_b.append(line)

    def __stupid_compare(self):
        for el1 in self.list_a:
            for el2 in self.list_b:
                if el1 == el2:
                    self.out.append(el1)

    def compare(self, file_name_a, file_name_b):
        self.__read_file(file_name_a, file_name_b)
        self.__stupid_compare()
        return self.out


def main():
    ils = InstagramLikeScraper()
    ils.like_scraper('links_a.txt', 'a_out.txt')
    ils.like_scraper('links_b.txt', 'b_out.txt')

    c = MergeLists()
    final_list = c.compare('a_out.txt', 'b_out.txt')

    out = open('final.txt', 'w')
    for line in final_list:
        out.write(line + "\n")
    out.close()


if __name__ == '__main__':
    main()
