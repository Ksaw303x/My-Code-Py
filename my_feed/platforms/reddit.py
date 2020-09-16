import json
import requests
from enum import Enum
from pprint import pprint

from my_feed.modules.models import PostModel
from my_feed.modules.types import PostType

HEADER = {'User-agent': 'bot'}


class Reddit:

    class __RedditPostTypes(Enum):
        REDDIT_VIDEO = 'reddit:video'
        VIDEO = 'rich:video'
        IMAGE = 'image'
        LINK = 'link'
        NONE = None

    def __init__(self):
        self.r_list = []  # list of all the sub-reddit where to get the data

    @staticmethod
    def __request_data(r, after=None):
        """
        Call the reddit api for the data
        :param r: the sub-reddit
        :param after: the last post id received (eg: t1-sxsdfew")
        :return: the data as dictionary
        :raise ConnectionError: if the api don't respond with a 200
        """
        url = 'https://www.reddit.com/r/%s/new.json?limit=20' % r
        res = requests.get(url, headers=HEADER)
        if res.status_code == 200:
            json_data = res.content
            return json.loads(json_data).get('data')
        else:
            raise ConnectionError

    def __build_feed(self, feed_data):

        out = []
        posts = feed_data.get('children')

        for el in posts:

            data = el.get('data')
            # pprint(data)

            # create the std post object
            # with the base data
            post = PostModel(
                post_id=data.get('id'),
                title=data.get('title'),
                created_at=data.get('created_utc'),
                url='https://www.reddit.com%s' % data.get('permalink')
            )

            # reddit way to define what type of post is it
            post_hint = data.get('post_hint')
            try:
                post_type_hint = self.__RedditPostTypes(post_hint)
            except Exception as exc:
                print(post_hint, exc)
                post_type_hint = self.__RedditPostTypes.NONE

            # the post has video extract the video
            # the video on reddit can be only one per post
            if data.get('media'):
                post.type = PostType.EMBED
                post.add_media(
                    media_id=data.get('id'),
                    media_url=data.get('url')
                )

            # if the post don't have a video in it, check for images
            # the images on reddit can be more than one per post (loop?)
            elif data.get('preview'):
                # the post contains just a link, and reddit is not able to load it as embed
                if post_type_hint == self.__RedditPostTypes.LINK:
                    post.type = PostType.EMBED
                else:
                    post.type = PostType.IMAGE
                post.add_media(
                    media_id=data.get('id'),
                    media_url=data.get('url')
                )

            # if the post don't contains neither video or image it should tbe a text post
            else:
                post.type = PostType.TEXT

            # check if there are a description in the post
            # the caption text aside the title
            description = data.get('selftext')
            if description:
                post.description = description

            out.append(post)  # add the post to the out

        return out

    def update(self):
        if not self.r_list:
            return

        all_feed_data = []
        for el in self.r_list:
            data = self.__request_data(el)
            feed = self.__build_feed(data)
            all_feed_data += feed

        return all_feed_data
