import multiprocessing
from video_player.modules.recorder import Recorder

save_directory = '/Videos'
recording = []


def record(person):
    r = Recorder(person, save_directory)
    r.record()


if __name__ == '__main__':
    models = [
        # 'mini_princess',
        # 'jillikins',
        # 'sweetiewow',
        'kimi_so',

    ]
    for model in models:
        p = multiprocessing.Process(target=record, args=(model,))
        p.start()

    r_p = Recorder('sweetiewow', save_directory)
    r_p.record()
