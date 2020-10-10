from tool.post_render.modules.paginator import Paginator
from time import time


def run(arg):
    t1 = time()
    name_tag = '@name_tag'
    paginator = Paginator('img/Spotted-Logo-15-z.png', name_tag)

    paginator.paginate_text(arg)
    print(time() - t1)

    img = paginator.get_image()


if __name__ == '__main__':
    lorem = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
    run(lorem)
