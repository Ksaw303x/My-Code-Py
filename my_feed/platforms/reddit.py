import json
import requests
from enum import Enum

from my_feed.modules.post import PostModel
from my_feed.modules.types import PostType

# header for the requests to the reddit api
HEADER = {'User-agent': 'bot'}


class Reddit:

    class __RedditPostTypes(Enum):
        REDDIT_VIDEO = 'reddit:video'
        VIDEO = 'rich:video'
        IMAGE = 'image'
        LINK = 'link'
        NONE = None

    def __init__(self):
        self.__last_post_id = None  # reddit 'Fullname' ID of the last post get

    @property
    def last_post_id(self):
        """
        The the last post Id
        This property must be get after the update
        :return: a slug ID
        """
        return self.__last_post_id

    @staticmethod
    def __request_data(r, before=None):
        """
        Call the reddit api for the data
        :param r: the sub-reddit
        :param before: the last post id received (eg: t1-sxsdfew")
        :return: the data as dictionary
        :raise ConnectionError: if the api don't respond with a 200
        """

        url = 'https://www.reddit.com/r/%s/new.json?limit=20' % r
        if before:
            url = 'https://www.reddit.com/r/%s/new.json?before=%s' % (r, before)

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

            # create the std post object
            # with the base data
            post = PostModel(
                post_id=data.get('name'),
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

    def update(self, r, last_update_id):
        """
        :param r: the sub-reddit channel
        :param last_update_id: the id of the last known post
        :return: a list of feed data
        """
        data = self.__request_data(r, last_update_id)
        feed = self.__build_feed(data)
        # update the last_post_id with the first post in the chunk
        if feed:
            # the feed is al list of post
            # Get the first (the newest) and make it the last post id
            self.__last_post_id = feed[0].id
        else:
            # if there are no new posts keep the current one
            self.__last_post_id = last_update_id

        return feed
