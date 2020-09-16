from .types import PostType


class MediaModel:

    def __init__(self, media_id, media_type, url):
        self.id = media_id
        self.type = media_type
        self.url = url


class PostModel:

    def __init__(self, post_id, title, created_at, url):
        self.post_id: str = post_id
        self.title: str = title
        self.type: PostType = PostType.NONE
        self.created_at: str = created_at
        self.url: str = url
        self.media: list = []
        self.description: str = ''

    def add_media(self, media_id, media_type, media_url):
        """
        Append a new media to the Post
        """
        self.media.append(MediaModel(media_id, media_type, media_url))
