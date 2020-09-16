import requests
from my_feed.platforms.reddit import Reddit
from my_feed.modules.models import PostModel, MediaModel
from my_feed.modules.types import PostType

HEADER = {'User-agent': 'bot'}


if __name__ == '__main__':

    f = Reddit()

    # 'BelleDelphinePatreon', 'hentai', 'relationship_advice', 'videos', 'PublicFreakout'
    f.r_list.append('videos')
    data = f.update()

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
                print(post.type, res.status_code, media.url)

                if res.status_code == 200:
                    with open('img/%s.jpg' % media.id, 'wb') as f:
                        f.write(res.content)
                        f.close()
