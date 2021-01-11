import configparser as cfg
from twitter import Api
from io import BytesIO
from pprint import pprint


parser = cfg.ConfigParser()
try:
    parser.read('config.cfg')
except Exception as exception:
    print(exception)

CONSUMER_KEY = parser.get('twitter', 'CONSUMER_KEY')
CONSUMER_SECRET = parser.get('twitter', 'CONSUMER_SECRET')
ACCESS_TOKEN = parser.get('twitter', 'ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = parser.get('twitter', 'ACCESS_TOKEN_SECRET')


class Twitter:

    def __init__(self):

        # Create API object
        self.api = Api(
            consumer_key=CONSUMER_KEY,
            consumer_secret=CONSUMER_SECRET,
            access_token_key=ACCESS_TOKEN,
            access_token_secret=ACCESS_TOKEN_SECRET
        )

    def get_direct_messages(self):
        data = self.api.GetDirectMessages()
        for message in data:
            pprint(message)

    def get_post(self):
        for tweet in self.api.GetUserTimeline(user_id="spacex"):  # since_id=1111
            print(f"{tweet.user.name}:{tweet.text}:{tweet.entities}")

    def create_post(self, text, file):
        if file:
            res = self.api.UploadMediaSimple(file)
            print(res)
            self.api.PostUpdate(text, media=file)


if __name__ == '__main__':
    f = open("test_img.jpg", "rb")
    img = f.read()

    t = Twitter()
    # t.get_direct_messages()
    t.create_post('test', 'test_img.jpg')
