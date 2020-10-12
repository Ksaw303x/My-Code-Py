from tool.post_render.modules.paginator import Paginator, Resolutions
from time import time
from io import BytesIO
import json


with open('configs.json', 'r') as f:
    config_data = json.loads(f.read())


def get_configs(configs: dict, operator: str, configs_type: str):
    """
    :param configs: the main config file
    :param operator: the id of the operator
    :param configs_type: the type of configs you want: 'image' or 'text' etc
    :return:
    """

    for key in configs.keys():
        config_item = configs[key]
        operators = config_item.get('operators')
        if operator in operators:
            return config_item.get(configs_type, {})

    return {}


def build_kwargs(configs: dict):
    kwargs = {}
    for key in configs.keys():
        kwargs[key] = configs.get(key)
    return kwargs


def run(arg):
    name_tag = '@name_tag'

    with open('img.jpeg', 'rb') as f:
        image = BytesIO(f.read())

    resolutions = [Resolutions.TWITTER.value, Resolutions.INSTAGRAM.value]

    # get the config data
    configs = get_configs(config_data, '123', 'image')
    kwargs = build_kwargs(configs)

    for res in resolutions:
        t1 = time()
        paginator = Paginator('img/icons/uniud.png', res, name_tag)

        paginator.paginate_image(image, **kwargs)
        """
        paginator.paginate_text(
            arg,
            top_image='quotation-marks',
            text_align='center',
            line_position=None,
            colorize_logo=True,
            logo_position='center',
            rectangle=True
        )
        """
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
