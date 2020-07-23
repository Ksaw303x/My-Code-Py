import requests
from bs4 import BeautifulSoup
from .chaturbate_types import Gender, Tag, ChatrubateCam
from .chaturbate_exceptions import NoResults


class ChaturbateSearch:

    URL = 'https://it.chaturbate.com/'

    def __init__(self):
        self.__cams_list = []
        self.__result_list = []

    def __web_scrapper(self, url):
        """
        Load the page and build the User object for every cam in the page
        :param url:
        :return:
        """
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        
        cams = soup.findAll(attrs={'class': 'room_list_room'})
        if not cams:
            return False

        for cam in cams:
            g = ChatrubateCam(cam.find('a')['href'])
            span = cam.find('span')
            g.age = span.text
            g.gender = Gender.gender_by_id(span.attrs['class'][1])
            g.build_url(self.URL)
            g.location = cam.find('li', attrs={'class': 'location'}).text
            g.build_info(cam.find('li', attrs={'class': 'cams'}).text)

            # if this cam is already in results skip it
            if g not in self.__cams_list:
                self.__cams_list.append(g)
        return True

    def __search(self, url_specification, query='', nr_pages=1):
        """
        :param url_specification:
        :param query: filter cams by query
        :param nr_pages: the max number of pages where search in
        """
        self.__cams_list = []  # reset cam list

        for page in range(nr_pages):
            status = self.__web_scrapper(self.URL + '{}?keywords="{}"&page={}'.format(
                url_specification,
                query,
                page
            )
                                         )
            if not status and page is 0:
                raise NoResults(url=url_specification, query=query)

    def search_tag(self, tag: Tag, gender=Gender.NONE, *argv):
        """
        Search cams filtering by tag, its required
        :param tag: one of the tag set by the admin of the cam
        :param gender: query directly the page where the gender is filtered by the site
        :return: self
        """
        self.__search(Tag.tag_url(tag.value) + gender.value[2], *argv)
        return self

    def search(self, gender=Gender.NONE, *argv):
        """
        Search cams mainly by gender if is provided
        :param gender: query directly the page where the gender is filtered by the site
        :return: self
        """
        self.__search(gender.value[1], *argv)
        return self

    def filter_by(self, age=None, gender=Gender.NONE, uptime=None, spectators=None):
        """
        Filter cams by parameters
        :param age: filter by the age of the ppl to search
        :param gender: filter by gender
        :param uptime: filter by uptime
        :param spectators: filter by number of spectators
        """
        for user_cam in self.__cams_list:
            # gender must match if is specified else take all
            if gender != Gender.NONE and gender != user_cam.gender:
                continue
            # fields must match the regex if is specified else take all
            if age and not age(user_cam.age):
                continue
            if uptime and not age(user_cam.age):
                continue
            if spectators and not age(user_cam.age):
                continue
            self.__result_list.append(user_cam)

        return self

    @property
    def results(self):
        return self.__result_list
