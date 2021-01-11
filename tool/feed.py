import requests
from time import sleep
from my_feed import Updater

from my_feed.modules.post import PostModel, MediaModel
from my_feed.modules.types import PostType

HEADER = {'User-agent': 'bot'}


if __name__ == '__main__':

    u = Updater()

    u.add_reddit_channel('BelleDelphinePatreon')
    u.add_reddit_channel('hentai')
    # u.add_reddit_channel('relationship_advice')
    # u.add_reddit_channel('videos')
    # u.add_reddit_channel('PublicFreakout')

    while True:

        data = u.update()

        for post in data:
            post: PostModel

            if post.type == PostType.TEXT:
                print(post.type, post.title)
                continue

            if post.type == PostType.EMBED:
                media = post.media[0]
                print(post.type, post.title, media.url)
                continue

            if post.type == PostType.NONE:
                print(post.type, post.title)
                continue

            if post.media and post.type == PostType.IMAGE:
                for media in post.media:
                    media: MediaModel

                    res = requests.get(media.url, headers=HEADER)
                    print(post.type, post.id, media.url)

                    if res.status_code == 200:
                        with open('img/%s.jpg' % media.id, 'wb') as f:
                            f.write(res.content)
                            f.close()

        sleep(300)
