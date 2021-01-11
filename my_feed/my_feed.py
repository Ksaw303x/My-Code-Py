from datetime import datetime, timedelta
from my_feed.platforms.reddit import Reddit


class Channel:

    def __init__(self, target):
        # initialize last update with an old time
        self.last_update: datetime = datetime.now() - timedelta(hours=5)

        # update the data every minutes interval
        self.update_interval: int = 30

        # how to identify the last update, to not send again the same data
        # this value can be a string, slug, or int based on the platform that you are using
        self.last_update_id = None

        # the channel specification, this must match che update requirements in the platform api
        self.target: str = target

        # where to send back the updated data
        # TODO: implement as multi-endpoint system (discord, telegram)
        self.endpoints: list = []


class Updater:

    def __init__(self):

        # for efficiency use one array per platform, so you can update all un once
        # recycling the api object
        self.__reddit_feed = []

    def add_reddit_channel(self, target):
        """
        Add a reddit channel where update from.
        :param target: the name of the channel (eg: 'Anime' for reddit)
        """
        self.__reddit_feed.append(Channel(target))

    def update(self):
        """
        perform the update for each platform
        :return: a List of Updates
        """
        out = []

        reddit = Reddit()

        for channel in self.__reddit_feed:
            channel: Channel

            now = datetime.now()
            if now - channel.last_update > timedelta(minutes=channel.update_interval):
                # get the data for the current channel
                out += reddit.update(channel.target, channel.last_update_id)
                # update the last id
                channel.last_update_id = reddit.last_post_id
                # channel.last_update = now

        return out
