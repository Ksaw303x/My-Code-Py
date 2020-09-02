import os
import requests
import json
from time import time
from datetime import datetime
from livestreamer import Livestreamer


class Recorder:

    def __init__(self, model, save_directory):
        self.__model = model
        self.save_directory = save_directory

        options_url = 'https://it.chaturbate.com/api/chatvideocontext/{}'.format(model)
        self.options = json.loads(requests.get(options_url).content)

        self.session = Livestreamer()
        self.session.set_option('http-headers', 'referer={}'.format(options_url))

        self.streams = None
        self.__get_live_streams()

        self.__record_status = True

    def __get_live_streams(self):

        hls = self.options.get('hls_source')
        if hls:
            self.streams = self.session.streams('hlsvariant://{}'.format(hls))

    def __get_stream(self):
        stream = self.streams['best']
        stream_720 = self.streams.get('720p')
        stream_480 = self.streams.get('480p')
        if stream_720:
            return stream_720
        elif stream_480:
            return stream_720
        else:
            return stream

    def record(self):
        try:
            if not self.streams:
                print('{} No live'.format(self.__model))
                return
            stream = self.__get_stream()

            fd = stream.open()
            ts = time()
            st = datetime.fromtimestamp(ts).strftime("%Y.%m.%d_%H.%M.%S")  # start time
            if not os.path.exists(self.save_directory):
                os.makedirs(self.save_directory)
            with open("{path}/{st}_{model}.mp4".format(path=self.save_directory, model=self.__model, st=st), 'wb') as f:
                while self.__record_status:
                    try:
                        data = fd.read(1024)
                        f.write(data)
                    except Exception as exc:
                        print(exc)
                        f.close()
                        return

        except Exception as exc:
            print(exc)

    def stop(self):
        self.__record_status = False
