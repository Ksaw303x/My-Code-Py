class Media:

    def __init__(self, media_id, media_type, url):
        self.media_id = media_id
        self.media_type = media_type
        self.url = url


class FeedData:

    def __init__(self, data_id, title, created_at, media, url):
        self.data_id = data_id
        self.title = title
        self.created_at = created_at
        self.media = media
        self.url = url
