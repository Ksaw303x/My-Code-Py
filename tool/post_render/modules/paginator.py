import os
import textwrap
from io import BytesIO
from random import randrange
from PIL import Image, ImageDraw, ImageFont
from .colors import *

# color combinations for the canvas (background, text)
# a function will select randomly a color set
COLORS_COMBINATIONS = [
    (RED_100, BLACK),
    (PINK_100, BLACK),
    (PURPLE_100, BLACK),
    (DEEP_PURPLE_100, BLACK),
    (INDIGO_100, BLACK),
    (BLUE_100, BLACK),
    # (LIGHT_BLUE_100, BLACK),
    # (CYAN_100, BLACK),
    # (TEAL, BLACK),
    # (GREEN, BLACK),
    # (LIGHT_GREEN, BLACK),
    # (LIME, BLACK),
    # (YELLOW, BLACK),
    # (AMBER, BLACK),
    # (ORANGE, BLACK),
    # (DEEP_ORANGE, BLACK),
]


class Paginator:

    def __init__(self, logo_path, name_tag):

        self.logo_path = logo_path
        self.name_tag = name_tag

        self.width = 1080
        self.height = 1080

        self.x_origin = self.width // 7  # align text on left virtual border
        self.y_origin = self.height // 7  # align text on left virtual border

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

    @staticmethod
    def _open_image(img_dir):
        """
        Open an image and convert it to RGBA
        :param img_dir: relative directory
        :return: the img obj
        """
        full_img_dir = f'{os.path.dirname(os.path.realpath(__file__))}/{img_dir}'
        img = Image.open(full_img_dir).convert('RGBA')
        return img

    def _resize_image(self, image, size=(0.9, 0.8)):
        """
        Resize a given image, by size factor respect the canvas dimension
        keeping intact the form factor.
        The transformation is done in place so keep a copy of the img object if needed the original one
        :param image: the img obj
        :param size: a tuple or array with the scale factor default (0.9, 0.8)
        :return: resized object
        """
        size = (int(self.width * size[0]), int(self.height * size[1]))
        image.thumbnail(
            size,
            Image.ANTIALIAS
        )
        return image

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

    def _draw_name_tag(self, position=None):
        """draw name tag"""
        font_name_tag = ImageFont.truetype(self.font_dir, int(45))

        name_tag_width, name_tag_height = font_name_tag.getsize(self.name_tag)
        # x = self.width - line_width - self.rectangle_offset - 25
        # x = (self.width - name_tag_width) // 2

        y = self.height - 108/2 - name_tag_height/2
        if position:
            y = position

        self.draw.text(
            (self.x_origin, y),
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

        quotation_marks = self._open_image('img/quotation-marks.png')
        self._resize_image(quotation_marks, (0.2, 0.2))

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

            # merge Quotation Marks with background keeping the transparency layer
            # in position just over the text
            qm_width, qm_height = quotation_marks.size
            offset = (self.x_origin, int(y_text - qm_height))
            self.image.paste(quotation_marks, offset, mask=quotation_marks)

            # | |*|*|*|*|*| |
            # draw the text
            # save the longest line
            longest_line = line_width

            for line in lines:

                line_width, line_height = font.getsize(line)
                if line_width > longest_line:
                    longest_line = line_width

                self.draw.text(
                    (self.x_origin, y_text),
                    line,
                    font=font,
                    fill=self.text_color
                )
                y_text += line_height

            y_text += line_height
            # draw a line under the text, before tag name
            self.draw.line(
                [(self.x_origin, y_text), (longest_line, y_text)],
                width=int(self.height/100),
                fill=self.text_color
            )

            self._draw_name_tag(y_text+line_height)

        else:
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

        # sub-sampling at 0 keep the image sharp
        # quality 100 avoid jpeg compression
        converted.save(img_bytes, format='JPEG', subsampling=0, quality=100)
        img_bytes.seek(0)

        converted.save('test.jpeg', format='PNG')
        converted.show()

        return img_bytes

    def save_image(self, file_dir):
        self.image.save(file_dir, format='PNG')

    def show_image(self):
        self.image.show()
