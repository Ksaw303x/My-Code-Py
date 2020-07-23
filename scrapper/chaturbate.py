from scrapper.modules.chaturbate_search import ChaturbateSearch, ChatrubateCam, Gender, Tag
from random import randrange


class Bot:
    @staticmethod
    def send_text(text):
        print(text)


class Chaturbate:

    def __init__(self):

        self.bot = Bot()
        self._first = None

    def run(self):

        girls_list = []  # self.__web_scrapper(URL)
        len_vl = len(girls_list) - 1

        # Send the first o the query
        if self._first is not None:
            self.bot.send_text(girls_list[0].url)
            return


if __name__ == '__main__':
    """
    you can search with and without a tag
    
    inside the search method you can specify
    - In search() you can specify a gender
        - gender=Gender.MALE (MALE, FEMALE, TRANS, COUPLE) DEFAULT: Gender.NONE (query all)
    - In search() you can specify a gender
        - tag=Tag.ASIAN (a lot of tags) to build custom tag use my_tag=Tag(TAG) and then pass my_tag to the method
        - gender=Gender.MALE (MALE, FEMALE, TRANS, COUPLE) DEFAULT: Gender.NONE (query all)
    
    in both the search you can add this aditional parameters
        query="yumi" a keyword to find in username on the site DEFAULT: ""
        nr_pages: the number of pages where search in (more pages == more time) DEFAULT: 1
        
    in filters you have to use a lambda in numeric fields
    lambda x: if x == 18
    """
    # cams = ChaturbateSearch().search().filter_by(age=18, filter_gender=Gender.COUPLE)

    cams = ChaturbateSearch().search_tag(
        tag=Tag.ASIAN,
        gender=Gender.FEMALE
    )

    cams = cams.filter_by(
        age=lambda age: True if 18 <= age <= 19 else False,
    )

    if cams.results:
        for cam in cams.results:
            cam: ChatrubateCam
            print(
                cam.gender.name.title(),
                cam.age,
                cam.url,
                'location:"{}" uptime: {} spectators: {}'.format(cam.location, cam.uptime_min, cam.spectators)
            )
    else:
        print('Nothing Found')




