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
        'cleopatra_sinns',
        'mollyflwers',
        'mr_alex_and_girls_'

    ]
    for model in models:
        p = multiprocessing.Process(target=record, args=(model,))
        p.start()

    r_p = Recorder('mr_alex_and_girls_', save_directory)
    r_p.record()
