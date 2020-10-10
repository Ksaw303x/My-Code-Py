import os
import textwrap
from io import BytesIO
from random import randrange
from PIL import Image, ImageDraw, ImageFont

BLACK = '#616161'  # gray 700 series
WHITE = '#FFFFFF'  # gray 200 series
GREY = '#9E9E9E'
LIGHT_GREY = '#BDBDBD'


"""
# all 500 class colors from material.io
RED = '#F44336'
PINK = '#E91E63'
PURPLE = '#9C27B0'
DEEP_PURPLE = '#673AB7'
INDIGO = '#3F51B5'
BLUE = '#2196F3'
LIGHT_BLUE = '#03A9F4'
CYAN = '#00BCD4'
TEAL = '#009688'
GREEN = '#4CAF50'
LIGHT_GREEN = '#8BC34A'
LIME = '#CDDC39'
YELLOW = '#FFEB3B'
AMBER = '#FFC107'
ORANGE = '#FF9800'
DEEP_ORANGE = '#FF5722'

# all 400 class colors from material.io
RED = '#EF5350'
PINK = '#EC407A'
PURPLE = '#AB47BC'
DEEP_PURPLE = '#7E57C2'
INDIGO = '#5C6BC0'
BLUE = '#42A5F5'
LIGHT_BLUE = '#29B6F6'
CYAN = '#26C6DA'
TEAL = '#26A69A'
GREEN = '#66BB6A'
LIGHT_GREEN = '#9CCC65'
LIME = '#D4E157'
YELLOW = '#FFEE58'
AMBER = '#FFCA28'
ORANGE = '#FFA726'
DEEP_ORANGE = '#FF7043'
"""

# all 300 class colors from material.io
RED = '#E57373'
PINK = '#F06292'
PURPLE = '#BA68C8'
DEEP_PURPLE = '#9575CD'
INDIGO = '#7986CB'
BLUE = '#64B5F6'
LIGHT_BLUE = '#4FC3F7'
CYAN = '#4DD0E1'
TEAL = '#4DB6AC'
GREEN = '#81C784'
LIGHT_GREEN = '#AED581'
LIME = '#DCE775'
YELLOW = '#FFF176'
AMBER = '#FFD54F'
ORANGE = '#FFB74D'
DEEP_ORANGE = '#FF8A65'


# color combinations for the canvas (background, text)
# a function will select randomly a color set
COLORS_COMBINATIONS = [
    (RED, WHITE),
    (PINK, WHITE),
    (PURPLE, WHITE),
    (DEEP_PURPLE, WHITE),
    (INDIGO, WHITE),
    (BLUE, WHITE),
    (LIGHT_BLUE, WHITE),
    (CYAN, WHITE),
    (TEAL, WHITE),
    (GREEN, WHITE),
    (LIGHT_GREEN, WHITE),  # BLACK
    # (LIME, BLACK),
    # (YELLOW, BLACK),
    # (AMBER, BLACK),
    (ORANGE, WHITE),
    (DEEP_ORANGE, WHITE),
]


class Paginator:

    def __init__(self, logo_path, name_tag):

        self.logo_path = logo_path
        self.name_tag = name_tag

        self.width = 1080
        self.height = 1080

        # select a random color combination
        idx = randrange(0, len(COLORS_COMBINATIONS))
        self.background_color = COLORS_COMBINATIONS[idx][0]
        self.text_color = COLORS_COMBINATIONS[idx][1]

        # font directory
        self.font_dir = '{}/fonts/KeplerStd-Bold-Italic.otf'.format(os.path.dirname(os.path.realpath(__file__)))
        self.font_dir_name_tah = '{}/fonts/KeplerStd-Italic.otf'.format(os.path.dirname(os.path.realpath(__file__)))

        # generate the empty canvas with a color
        self.image = Image.new('RGBA', (self.width, self.height), self.background_color)

        # create the draw obj
        self.draw = ImageDraw.Draw(self.image)

        # draw a rectangle as outside border of the text
        self.rectangle_offset = 15

    def _draw_logo(self):
        logo_dir = f'{os.path.dirname(os.path.realpath(__file__))}/{self.logo_path}'
        logo = Image.open(logo_dir).convert('RGBA')

        logo_width, logo_height = logo.size
        offset = ((self.width - logo_width) // 2, (self.height - logo_height) // 2)

        # merge Logo with background keeping the transparency layer
        self.image.paste(logo, offset, mask=logo)

    def _draw_rectangle(self):
        self.draw.rectangle(
            [
                (self.rectangle_offset, self.rectangle_offset),
                (self.width - self.rectangle_offset, self.height - self.rectangle_offset)
            ],
            outline=self.text_color,
            width=6
        )

    def _draw_name_tag(self):
        """draw name tag"""
        font_name_tag = ImageFont.truetype(self.font_dir, int(45))

        name_tag_width, name_tag_height = font_name_tag.getsize(self.name_tag)
        # x = self.width - line_width - self.rectangle_offset - 25
        x = (self.width - name_tag_width) // 2
        y = self.height - 108/2 - name_tag_height/2
        self.draw.text(
            (x, y),
            self.name_tag,
            font=font_name_tag,
            fill=self.text_color
        )

    def paginate_text(self, text):
        """
        Paginator is designed with a 1080 pixel resolution
        it will not scale up and down based on that if the height and height will be changed.
        Not tested with non square resolutions.

        :param text: the text that have to be put in the image
        """
        self._draw_logo()

        # if there is no text return just the template
        if text:
            font_max_dim = 180

            # calculate the font dimension based on the length of the text
            # y = (x * text_len + 1) reduce the text linearly based on the text len (front_dim / y)
            # g(x)=(80)/(x*0.02+1.4)+12
            # 50 is the base text dimension
            font_dim = (font_max_dim / (0.025 * len(text) + 1.4) + 25)
            font = ImageFont.truetype(self.font_dir, int(font_dim))

            # wrap text
            # inversely proportional to the font_dim
            # width_dim = (100 / (font_dim + 1) * 12) - 6 (old)
            # h(x)=(100)/(x+12)*14-8
            width_dim = ((100 / (font_dim + 12) * 17) + 1)
            lines = textwrap.wrap(text, width=int(width_dim))

            # debug
            # print('text len: {} - font dim: {} - width_dim: {}'.format(len(text), font_dim, width_dim))

            # calculate the center of the text
            line_width, line_height = font.getsize(lines[0])
            y_text = self.height / 2 - line_height / 2 * len(lines)

            # draw the text
            for line in lines:
                line_width, line_height = font.getsize(line)
                self.draw.text(
                    (30, y_text),
                    line,
                    font=font,
                    fill=self.text_color
                )
                y_text += line_height

        self._draw_name_tag()

    def paginate_image(self, image: bytearray):
        """
        :param image: the image to paginate
        """

        # convert the byte-array image into pil image
        im = Image.open(image)

        # resize the image
        size = (int(self.width * 0.9), int(self.height * 0.8))
        im.thumbnail(
            size,
            Image.ANTIALIAS
        )

        # center the image
        im_width, im_height = im.size
        offset = ((self.width - im_width) // 2, (self.height - im_height) // 2)

        self.image.paste(im, offset)

        self._draw_name_tag()

    def get_image(self):
        """
        :return: image converted as byte array
        """
        # convert the image in bytes to send it
        img_bytes = BytesIO()
        img_bytes.name = 'post.jpeg'
        converted = self.image.convert('RGB')  # prepare to JPEG save
        converted.save(img_bytes, format='JPEG', subsampling=0, quality=100)  # save ad jpeg - quality 95% ~85kb file
        img_bytes.seek(0)

        return img_bytes

    def save_image(self, file_dir):
        self.image.save(file_dir, format='PNG')

    def show_image(self):
        self.image.show()
