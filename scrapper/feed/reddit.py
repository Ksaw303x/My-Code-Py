import os
import json
import requests
from pprint import pprint

HEADER = {'User-agent': 'bot'}


class Reddit:

    def __init__(self):
        self.r_list = []

        # time of the last post known
        # on start this will be 0 or must be set from a db
        self.last_post_time = None

    @staticmethod
    def __build_url(r):
        return 'https://www.reddit.com/r/%s.json' % r

    @staticmethod
    def __get_data(url):
        res = requests.get(url, headers=HEADER)
        json_data = res.content
        feed = json.loads(json_data).get('data')

        posts = feed.get('children')

        data_out = []
        for el in posts:
            data = el.get('data')
            pprint(data)

            # estract all the media
            media = []

            media_metadata = data.get('media_metadata')
            if media_metadata:

                for media_id in media_metadata.keys():
                    media_obj = media_metadata.get(media_id)
                    media.append({
                        'id': media_id,

                        # the image type (element)
                        'type': media_obj.get('e'),

                        # s = Source Immage, u = Url,
                        # 'amp;' it's an error in the reddit json response
                        'url': media_obj.get('s').get('u').replace('amp;', '')
                    })
                continue

            preview = data.get('preview')
            if not preview:
                continue

            images = preview.get('images')
            if images:

                for media_obj in images:
                    media.append({
                        'id': media_obj.get('id'),

                        # the image type (element)
                        'type': 'Image',

                        # s = Source Immage, u = Url,
                        # 'amp;' it's an error in the reddit json response
                        'url': media_obj.get('source').get('url').replace('amp;', '')
                    })

            # format the data in a nicer way
            data_out.append({
                'id': data.get('id'),
                'title': data.get('title'),
                'updated_at': data.get('created_utc'),
                'media': media,
                'url': 'https://www.reddit.com%s' % data.get('permalink'),
            })

        return data_out

    def update(self):
        if not self.r_list:
            return

        out = []
        for el in self.r_list:
            url = self.__build_url(el)
            r_data = self.__get_data(url)
            out = out + r_data

        return out


if __name__ == '__main__':

    dir_path = os.path.dirname(os.path.realpath(__file__))

    f = Reddit()

    # 'BelleDelphinePatreon'
    f.r_list.append('hentai')
    d = f.update()

    for post in d:
        post_id = post.get('id')

        for media in post.get('media'):

            if not media.get('type') == 'Image':
                continue

            media_id = media.get('id')
            url = media.get('url')
            res = requests.get(url, headers=HEADER)
            print(res.status_code, url)

            if res.status_code == 200:
                with open('img/%s.jpg' % media_id, 'wb') as f:
                    f.write(res.content)
                    f.close()
