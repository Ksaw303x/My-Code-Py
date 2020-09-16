import json
import requests
from pprint import pprint

from my_feed.modules.models import PostModel
from my_feed.modules.types import PostType

HEADER = {'User-agent': 'bot'}


class Reddit:

    def __init__(self):
        self.r_list = []  # list of all the sub-reddit where to get the data

    @staticmethod
    def __request_data(r, after=None):
        url = 'https://www.reddit.com/r/%s/new.json?limit=1' % r
        res = requests.get(url, headers=HEADER)
        if res.status_code == 200:
            json_data = res.content
            return json.loads(json_data).get('data')
        else:
            raise ConnectionError

    @staticmethod
    def __get_video(data, post: PostModel):

        # the video is a youtube video or form others platforms
        if data.get('media'):
            post.add_media(
                media_id=None,
                media_type='embed',
                media_url=data.get('url')
            )

    @staticmethod
    def __get_images(data, post: PostModel):
        """
        extract all the media
        cause of the old api of reddit, check first in the media_metadata and then in the preview
        """

        media_metadata = data.get('media_metadata')
        if media_metadata:

            for media_id in media_metadata.keys():
                media_obj = media_metadata.get(media_id)
                post.add_media(
                    media_id=media_id,
                    media_type=media_obj.get('e'),
                    media_url=media_obj.get('s').get('u').replace('amp;', '')
                )

        else:
            preview = data.get('preview')
            if preview:

                images = preview.get('images')
                if images:

                    for media_obj in images:
                        post.add_media(
                            media_id=media_obj.get('id'),
                            media_type='Image',
                            media_url=media_obj.get('source').get('url').replace('amp;', '')
                        )

    def __build_feed(self, feed_data):

        posts = feed_data.get('children')

        feed_data = []
        for el in posts:

            data = el.get('data')
            pprint(data)

            # create the std post object
            post = PostModel(
                post_id=data.get('id'),
                title=data.get('title'),
                created_at=data.get('created_utc'),
                url='https://www.reddit.com%s' % data.get('permalink')
            )

            # check if is_video, is_meta
            self.__get_images(data, post)

            # check if there are a description in the post
            description = data.get('selftext')
            if description:
                post.description = description

            # decide what type of post is it
            post.type = PostType.IMAGE if post.media else (PostType.TEXT if post.description else PostType.NONE)

            feed_data.append(post)  # add the post to the feed_data

        return feed_data

    def update(self):
        if not self.r_list:
            return

        all_feed_data = []
        for el in self.r_list:
            data = self.__request_data(el)
            feed = self.__build_feed(data)
            all_feed_data += feed

        return all_feed_data
