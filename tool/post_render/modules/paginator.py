import os
import textwrap
from typing import List
from enum import Enum
from io import BytesIO
from random import randrange
from PIL import Image, ImageDraw, ImageFont
from numpy import array
from .colors import *

QUOTATION_MARKS_DIR = 'img/assets/quotation-marks.png'

# color combinations for the canvas (background, text)
# a function will select randomly a color set
COLORS_COMBINATIONS = (
    (RED_900, RED_200, WHITE),
    (PINK_900, PINK_200, WHITE),
    (PURPLE_900, PINK_300, WHITE),
    (DEEP_PURPLE_900, DEEP_PURPLE_500, WHITE),
    (INDIGO_900, INDIGO_500, WHITE),
    (BLUE_900, BLUE_500, WHITE),
    (LIGHT_BLUE_900, LIGHT_BLUE_600, WHITE),
    (CYAN_900, CYAN_600, WHITE),
    (TEAL_900, TEAL_600, WHITE),
    (GREEN_900, GREEN_800, WHITE),
    (LIGHT_GREEN_900, LIGHT_GREEN_800, WHITE),
    (LIME_900, LIME_600, WHITE),
    (YELLOW_900, YELLOW_200, WHITE),
    (AMBER_900, AMBER_200, WHITE),
    (ORANGE_900, ORANGE_200, WHITE),
    (DEEP_ORANGE_900, DEEP_ORANGE_200, WHITE),
    (RED_100, RED_500, BLACK),
    (PINK_100, PINK_500, BLACK),
    (PURPLE_100, PINK_500, BLACK),
    (DEEP_PURPLE_100, DEEP_PURPLE_500, BLACK),
    (INDIGO_100, INDIGO_500, BLACK),
    (BLUE_100, BLUE_500, BLACK),
    (LIGHT_BLUE_100, LIGHT_BLUE_600, BLACK),
    (CYAN_100, CYAN_600, BLACK),
    (TEAL_100, TEAL_600, BLACK),
    (GREEN_200, GREEN_800, BLACK),
    (LIGHT_GREEN_200, LIGHT_GREEN_800, BLACK),
    (LIME_100, LIME_600, BLACK),
    (YELLOW_100, YELLOW_600, BLACK),
    (AMBER_100, AMBER_600, BLACK),
    (ORANGE_100, ORANGE_600, BLACK),
    (DEEP_ORANGE_100, DEEP_ORANGE_500, BLACK),
)

BN_COLORS_COMBINATIONS = [
    # (GRAY_200, GRAY_500, BLACK),
    # (GRAY_300, GRAY_600, BLACK),
    (GRAY_900, GRAY_700, WHITE),
]

# define default font types
# FONT_TEXT = 'fonts/KeplerStd-Bold-Italic.otf',
FONT_TEXT = 'fonts/Roboto-Black.ttf'
FONT_NAME_TAG = 'fonts/KeplerStd-Bold-Italic.otf'


class Resolutions(Enum):
    """Resolution data for the platform"""
    INSTAGRAM = (1080, 1080)
    TWITTER = (1200, 675)
    LOW = (750, 750)


class Paginator:

    def __init__(self, logo_path, resolution: tuple, name_tag=None, colors: List[tuple] = COLORS_COMBINATIONS):
        """
        :param logo_path: the logo relative directory
        :param resolution: the resolution at tuple (width, height)
        :param name_tag: the name tag, to show in the post, if None no name_tag will be shown
        """

        self.logo_path = logo_path
        self.name_tag = name_tag

        self.width = resolution[0]
        self.height = resolution[1]

        self.x_origin = self.width // 7  # align text on left virtual border
        self.y_origin = self.height // 7  # align text on left virtual border

        # select a random color combination
        idx = randrange(0, len(colors))
        color = colors[idx]

        # load colors from the tuple
        self.background_color = color[0]
        self.primary_color = color[1]
        self.text_color = color[2]

        # check if the background is dark
        self.is_dark = False
        if self.text_color == WHITE:
            self.is_dark = True

        # generate the empty canvas with a color
        self.image = Image.new('RGBA', (self.width, self.height), self.background_color)

        # create the draw obj
        self.draw = ImageDraw.Draw(self.image)

    @staticmethod
    def _load_font(font_dir, dim):
        font_full_dir = f'{os.path.dirname(os.path.realpath(__file__))}/{font_dir}'
        font = ImageFont.truetype(font_full_dir, int(dim))
        return font

    @staticmethod
    def _open_image(img_dir, color=None, opacity=None):
        """
        Open an image and convert it to RGBA
        :param img_dir: relative directory
        :param color: the value of color
        :param opacity: the opacity in percentage
        :return: the img obj
        """
        full_img_dir = f'{os.path.dirname(os.path.realpath(__file__))}/{img_dir}'
        img = Image.open(full_img_dir).convert('RGBA')

        if opacity or color:
            data = array(img)  # "data" is a height x width x 4 numpy array
            red, green, blue, alpha = data.T  # Temporarily unpack the bands for readability

            if opacity:
                future_alpha = 255 // 100 * opacity

                # Replace white with the color (leaves alpha values alone)
                not_transparent_areas = (alpha != 0)
                data[..., 3:][not_transparent_areas.T] = future_alpha  # set the new color

            if color:
                h = color.lstrip('#')
                future_color = tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

                # Replace white with the color (leaves alpha values alone)
                white_areas = (red == 255) & (blue == 255) & (green == 255)
                data[..., :-1][white_areas.T] = future_color  # set the new color

            img = Image.fromarray(data)

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

    def _draw_logo(self, color=None, logo_position='right-down'):

        # check if is center
        # center position need different resize
        if logo_position == 'center':
            logo = self._open_image(self.logo_path, color=color, opacity=15)
            self._resize_image(logo, (0.9, 0.9))
            logo_width, logo_height = logo.size
            offset = [
                ((self.width - logo_width)//2),
                ((self.height - logo_height)//2)
            ]

        else:
            logo = self._open_image(self.logo_path, color=color)
            self._resize_image(logo, (0.12, 0.12), )
            logo_width, logo_height = logo.size

            # compute position for the small logo
            choices = {
                'right-up': [self.width - logo_width - self.width//20, self.height//20],
                'left-up': [self.width//20, self.height//20],
                'center-up': [(self.width - logo_width)//2, self.height//20],
                'right-down': [self.width//20, self.height - logo_height - self.height//20],
                'left-down': [self.width - logo_width - self.width//20, self.height - logo_height - self.height//20],
                'center-down': [(self.width - logo_width)//2, self.height - logo_height - self.height//20],
            }
            try:
                offset = choices[logo_position]
            except KeyError:
                offset = choices['right-down']

        # merge Logo with background keeping the transparency layer
        self.image.paste(logo, offset, mask=logo)

    def _draw_rectangle(self):
        offset = 15
        self.draw.rectangle(
            [
                (offset, offset),
                (self.width - offset, self.height - offset)
            ],
            outline=self.text_color,
            width=6
        )

    def _draw_name_tag(self, align='right', y_position=None):
        """
        :param align:
        :param y_position:
        :return:
        """

        # no name tag is defined, abort
        if not self.name_tag:
            return

        # generate the name tag dimension based on the resolution
        font_name_tag_dim = self.width * self.height // 35000

        font_name_tag = self._load_font(
            FONT_NAME_TAG,
            font_name_tag_dim
        )

        name_tag_width, name_tag_height = font_name_tag.getsize(self.name_tag)

        # compute y position
        # if not cursor is provided put the text at the bottom
        if y_position:
            y = y_position
        else:
            y = (self.height - self.height // 10 - name_tag_height) // 2

        # compute x position
        # default right
        choices = {
            'center': (self.width - name_tag_width)//2,
            'left': self.x_origin,
            'right': self.width - self.x_origin - name_tag_width,
        }
        try:
            x = choices[align]
        except ValueError:
            x = choices['right']

        self.draw.text(
            (x, y),
            self.name_tag,
            font=font_name_tag,
            fill=self.text_color
        )

    def paginate_text(
            self,
            text,
            top_image='quotation-marks',
            text_align='left',
            line_position='center',
            colorize_logo=False,
            logo_position='center-up'
    ):
        """
        Paginator is designed with a 1080 pixel resolution
        it will not scale up and down based on that if the height and height will be changed.
        Not tested with non square resolutions.

        :param text: the text that have to be put in the image
        :param top_image: the image that define what type of post is this
        :param text_align: align center, left, right
        :param line_position: draw the line bottom, left, right, if None no line
        :param colorize_logo: true  or false if the logo have to be colored with primary_color
        :param logo_position: center, center-up, center-down, right-down, left-down, right-up, left-up
            the position where display the logo image
        """
        # Draw the logo
        if colorize_logo:
            logo_color = self.primary_color
        else:
            logo_color = self.text_color
        self._draw_logo(color=logo_color, logo_position=logo_position)

        # if there is no text return just the template
        if text:

            # Calculate the font base dimension based on the resolution
            font_text_max_dim = self.width * self.height // 6000
            font_text_mim_dim = self.width * self.height // 45000

            # FONT DIM CALCULATIONS --------------------------------------------------------------
            # resize the font dimension based on the length of the text
            # y = (x * text_len + 1) reduce the text based on the text len (front_dim / y)
            # g(x)=(190)/(0.025*x+1.4)+25
            font_dim = (font_text_max_dim / (0.025 * len(text) + 1.4) + font_text_mim_dim)
            font_text = self._load_font(
                FONT_TEXT,
                font_dim
            )

            # wrap text
            # inversely proportional to the font_dim, based on the image width
            # h(x)=(100)/(x+12)*14-8
            width_dim = ((100 / (font_dim + 8) * (12*(self.width/600))) - 2)
            lines = textwrap.wrap(text, width=int(width_dim))

            # debug
            print('text len: {} - font dim: {} - width_dim: {}'.format(len(text), font_dim, width_dim))

            # QUOTATION MARKS --------------------------------------------------------------
            # calculate the center of the text
            line_width, line_height = font_text.getsize(lines[0])
            y_text = self.height / 2 - line_height / 2 * len(lines)

            if top_image:
                # merge Quotation Marks with background keeping the transparency layer
                # Position: just over the text
                quotation_marks = self._open_image(QUOTATION_MARKS_DIR, color=self.primary_color)
                self._resize_image(quotation_marks, (0.08, 0.08))
                qm_width, qm_height = quotation_marks.size
                offset = (self.x_origin, int(y_text - qm_height*1.5))

                # draw circle before paste quotation marks
                """
                bd = qm_width/4
                self.draw.ellipse(
                    [(offset[0] - bd, offset[1] - bd), (offset[0] + qm_width + bd, offset[1] + qm_width + bd)],
                    fill=self.primary_color,
                )
                """
                self.image.paste(quotation_marks, offset, mask=quotation_marks)

            # TEXT --------------------------------------------------------------
            # | |*|*|*|*|*| |
            # draw the text, center the text in 5/7 of the space, 1/7 border on each side
            longest_line = line_width  # save the longest line, for underline
            y_text_start = y_text  # save first line position, for side line

            for line in lines:

                line_width, line_height = font_text.getsize(line)
                if line_width > longest_line:
                    longest_line = (longest_line + line_width)/2  # get the average

                # calculate text position
                if text_align == 'center':
                    xy = ((self.width - line_width) / 2, y_text)
                elif text_align == 'right':
                    xy = (self.width - self.x_origin - line_width, y_text)
                else:
                    xy = (self.x_origin, y_text)

                self.draw.text(
                    xy,
                    line,
                    font=font_text,
                    fill=self.text_color
                )
                y_text += line_height

            # LINE --------------------------------------------------------------
            # draw line under or aside of the text
            longest_line = longest_line/(5/4)  # get a shorter line to not go over the logo

            if line_position == 'right':
                xy = [
                    (self.width - self.x_origin / (3 / 2), y_text_start),
                    (self.width - self.x_origin / (3 / 2), y_text)
                ]
            elif line_position == 'left':
                xy = [(self.x_origin / (3 / 2), y_text_start), (self.x_origin / (3 / 2), y_text)]
            elif line_position == 'center':
                y_text += line_height
                # if the line_position is bottom and the text_align is center
                # then center also the line
                if text_align == 'center':
                    origin = (self.width//2 - longest_line//2)
                    xy = [(origin, y_text), (origin + longest_line, y_text)]
                else:
                    xy = [(self.x_origin, y_text), (self.x_origin + longest_line, y_text)]
            else:
                xy = None

            # draw a line under the text, before tag name
            if xy:
                self.draw.line(
                    xy,
                    width=int(self.height/100),
                    fill=self.primary_color
                )

            self._draw_name_tag(align=text_align, y_position=y_text+line_height)

        else:
            self._draw_name_tag(align=text_align)

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

        converted.save('test.jpeg')
        converted.show()

        return img_bytes

    def save_image(self, file_dir):
        self.image.save(file_dir, format='PNG')

    def show_image(self):
        self.image.show()
