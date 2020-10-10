from tool.post_render.modules.paginator import Paginator


def run(arg):

    name_tag = '@name_tag'
    paginator = Paginator('Spotted-Logo-15-z.png', name_tag)

    paginator.paginate_text(arg)
    paginator.show_image()
    # img = paginator.get_image()


if __name__ == '__main__':
    run('hello')
