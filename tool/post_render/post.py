from tool.post_render.modules.paginator import Paginator, Resolutions
from time import time


def run(arg):
    name_tag = '@name_tag'

    resolutions = [Resolutions.TWITTER.value, Resolutions.INSTAGRAM.value]

    for res in resolutions:
        t1 = time()
        paginator = Paginator('img/uniud/icon.png', res, name_tag)
        paginator.paginate_text(
            arg,
            top_image='quotation-marks',
            text_align='center',
            line_position=None,
            colorize_logo=True,
            logo_position='center',
            rectangle=True
        )
        print(time() - t1)

        img = paginator.get_image()


if __name__ == '__main__':
    lorem = [
        # 'Bella Raga',
        #'ciao Bella ciao Bella',
        #'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        # 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
        #'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
    ]
    for lor in lorem:
        run(lor)
