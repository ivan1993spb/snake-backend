"""The module contains a set of classes which provide generation of screenshots
"""

__license__ = "MIT"
__docformat__ = 'reStructuredText'

import math

import numpy as np
from PIL import Image


class Canvas:
    """A bare canvas
    """

    BLACK_COLOR = (0x0, 0x0, 0x0)

    @staticmethod
    def _init_img(width, height, background_color=None):
        """Returns an image with given size and initial background color

        :param width: image width
        :param height: image height
        :param background_color: initial background color
        :return: image
        """
        if background_color and background_color != Canvas.BLACK_COLOR:
            return np.full((height, width, 3), background_color, dtype=np.uint8)
        return np.zeros((height, width, 3), dtype=np.uint8)


class GridCanvas(Canvas):
    """A grid canvas
    """

    LINE_SIZE_FACTOR = 0.10
    LINE_SIZE_MIN = 1
    DOT_SIZE_MIN = 5

    def __init__(self, map_dot_width, map_dot_height, max_img_px_width, max_img_px_height,
                 border_size, border_color, grid_color, background_color=None):
        """Initializes a GridCanvas instance.

        :param map_dot_width: map width in dots
        :param map_dot_height: map height in dots
        :param max_img_px_width: limit result image width in px
        :param max_img_px_height: limit result image height in px
        :param border_size: border size in px
        :param border_color: border color
        :param grid_color: grid color
        :param background_color: background color
        """
        self._map_dot_width = map_dot_width
        self._map_dot_height = map_dot_height
        self._max_img_px_width = max_img_px_width
        self._max_img_px_height = max_img_px_height

        self._border_size = border_size

        self._dot, self._line = self._calculate_grid_properties()
        self._img_px_width, self._img_px_height = self._calculate_img_size()

        self.img = self._init_img(self._img_px_width,
                                  self._img_px_height,
                                  background_color)

        self._draw_border(border_color)
        self._draw_grid(grid_color)

    def _calculate_grid_properties(self):
        """Calculates grid properties: sizes of cell and line.
        """
        cell = min(
            math.ceil((self._max_img_px_width - self._border_size * 2) / self._map_dot_width),
            math.ceil((self._max_img_px_height - self._border_size * 2) / self._map_dot_height)
        )

        line = math.floor(cell * self.LINE_SIZE_FACTOR)

        if line < self.LINE_SIZE_MIN and cell - line > self.DOT_SIZE_MIN:
            line = self.LINE_SIZE_MIN

        dot = cell - line

        return dot, line

    def _calculate_img_size(self):
        img_px_width = \
            self._dot * self._map_dot_width + \
            self._line * (self._map_dot_width + 1) + \
            self._border_size * 2
        img_px_height = \
            self._dot * self._map_dot_height + \
            self._line * (self._map_dot_height + 1) + \
            self._border_size * 2
        return img_px_width, img_px_height

    def _calculate_rect_px_x_y(self, dot_x, dot_y):
        """Calculates a rectangle position on a canvas by given dot position.
        Returns coordinates of top left corner and right bottom corner of the
        rectangle.

        :param dot_x: dot X
        :param dot_y: dot Y
        :rtype: ((int, int), (int, int))
        """
        px_x_1 = self._border_size + self._dot * dot_x + self._line * (dot_x + 1)
        px_y_1 = self._border_size + self._dot * dot_y + self._line * (dot_y + 1)
        px_x_2 = px_x_1 + self._dot
        px_y_2 = px_y_1 + self._dot
        return (px_x_1, px_y_1), (px_x_2, px_y_2)

    def _draw_grid(self, grid_color):
        """Draws a grid of given color.

        :param grid_color: color tuple in RGB format
        :type grid_color: (int, int, int)
        """
        if self._line > 0:
            # Horizontal
            for line_px_x in range(self._border_size,
                                   self._img_px_width - self._border_size,
                                   self._line + self._dot):
                self._draw_px_rect(line_px_x,
                                   self._border_size,
                                   line_px_x + self._line,
                                   self._img_px_height - self._border_size,
                                   grid_color)
            # Vertical
            for line_px_y in range(self._border_size,
                                   self._img_px_height - self._border_size,
                                   self._line + self._dot):
                self._draw_px_rect(self._border_size,
                                   line_px_y,
                                   self._img_px_width - self._border_size,
                                   line_px_y + self._line,
                                   grid_color)

    def _draw_border(self, border_color):
        """Draws borders of given color.

        :param border_color: color tuple in RGB format
        :type border_color: (int, int, int)
        """
        if self._border_size > 0:
            # Western border
            self._draw_px_rect(0,
                               0,
                               self._border_size,
                               self._img_px_height,
                               border_color)

            # Northern border
            self._draw_px_rect(0,
                               0,
                               self._img_px_width,
                               self._border_size,
                               border_color)

            # Eastern border
            self._draw_px_rect(self._img_px_width - self._border_size,
                               0,
                               self._img_px_width,
                               self._img_px_height,
                               border_color)

            # Southern border
            self._draw_px_rect(0,
                               self._img_px_height - self._border_size,
                               self._img_px_width,
                               self._img_px_height,
                               border_color)

    def draw_dot(self, dot_x, dot_y, color):
        """Draws a single dot.
        """
        (px_x_1, px_y_1), (px_x_2, px_y_2) = self._calculate_rect_px_x_y(dot_x, dot_y)
        self._draw_px_rect(px_x_1, px_y_1, px_x_2, px_y_2, color)

    def _draw_px_rect(self, x1, y1, x2, y2, color):
        self.img[y1:y2, x1:x2] = color

    def size(self):
        """Returns the size of an image

        :return: width and height in px
        :rtype: (int, int)
        """
        return self._img_px_width, self._img_px_height

    def __repr__(self):
        return '{}.{}(width={}, height={}, dot={}, line={})'.format(__name__,
                                                                    self.__class__.__name__,
                                                                    self._img_px_width,
                                                                    self._img_px_height,
                                                                    self._dot,
                                                                    self._line)


class Screenshot:
    """A game screenshot
    """

    COLOR_BACKGROUND = (0x0, 0x0, 0x0)
    BORDER_SIZE = 2
    COLOR_BORDER = (0x0, 0x11, 0x0)
    COLOR_GRID = (0x0, 0x22, 0x0)

    def __init__(self, map_size, max_size, game_objects: list, strict_sized=False):
        """Initializes a screenshot.

        :param map_size: size of map in dots
        :type map_size: (int, int)
        :param max_size: limits for result image in px
        :type max_size: (int, int)
        :param game_objects: list of game objects
        :param strict_sized: a flag whether to generate an image with strict limited size or not
        """
        self._map_dot_width, self._map_dot_height = map_size
        self._max_img_px_width, self._max_img_px_height = max_size

        self._canvas = GridCanvas(self._map_dot_width,
                                  self._map_dot_height,
                                  self._max_img_px_width,
                                  self._max_img_px_height,
                                  self.BORDER_SIZE,
                                  self.COLOR_BORDER,
                                  self.COLOR_GRID,
                                  self.COLOR_BACKGROUND)

        self._draw_objects(game_objects)

        self._image = self._rgb_image(strict_sized)

    def _draw_objects(self, game_objects: list):
        for game_object in game_objects:
            for (x, y), color in game_object.dots():
                self._canvas.draw_dot(x, y, color)

    def _rgb_image(self, strict_sized: bool):
        if not strict_sized:
            return Image.fromarray(self._canvas.img, 'RGB')

        strict_width, strict_height = self._calculate_strict_size()
        return Image.fromarray(self._canvas.img, 'RGB').resize((strict_width, strict_height))

    @property
    def img(self):
        """A result image
        """
        return self._image

    def _calculate_strict_size(self):
        height, width, _ = self._canvas.img.shape

        max_length = min(self._max_img_px_width, self._max_img_px_height)

        if width == height:
            return max_length, max_length

        if width > height:
            return max_length, height * max_length // width

        return width * max_length // height, max_length

    def __repr__(self):
        return '{}.{}(dot_w={}, dot_h={}, max_px_w={}, max_px_h={})'.format(__name__,
                                                                            self.__class__.__name__,
                                                                            self._map_dot_width,
                                                                            self._map_dot_height,
                                                                            self._max_img_px_width,
                                                                            self._max_img_px_height)
