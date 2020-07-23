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
