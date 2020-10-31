"""The module contains a set of classes which provide generation of
screenshots.
"""

import math
from typing import Tuple

import numpy as np
from PIL import Image

from lib.schemas import ColorRGB, AnyObjectList


BLACK_COLOR: ColorRGB = (0x0, 0x0, 0x0)


class Canvas:
    """A bare canvas
    """

    @staticmethod
    def _init_img(width: int, height: int) -> np.ndarray:
        """Returns an image with given size and initial background color.

        Parameters:
          width: image's width.
          height: image's height.

        Returns:
          An empty black image.
        """
        return np.zeros((height, width, 3), dtype=np.uint8)


class GridCanvas(Canvas):
    """A grid canvas
    """

    LINE_SIZE_FACTOR = 0.10
    LINE_SIZE_MIN = 1
    DOT_SIZE_MIN = 5

    def __init__(self,
                 map_dot_width: int,
                 map_dot_height: int,
                 max_img_px_width: int,
                 max_img_px_height: int,
                 border_size: int,
                 border_color: ColorRGB,
                 grid_color: ColorRGB):
        """Initializes a GridCanvas instance.

        Parameters:
          map_dot_width: map width in dots.
          map_dot_height: map height in dots.
          max_img_px_width: limit result image width in px.
          max_img_px_height: limit result image height in px.
          border_size: border size in px.
          border_color: border color.
          grid_color: grid color.
        """
        self._map_dot_width = map_dot_width
        self._map_dot_height = map_dot_height
        self._max_img_px_width = max_img_px_width
        self._max_img_px_height = max_img_px_height

        self._border_size = border_size

        self._dot, self._line = self._calculate_grid_properties()
        self._img_px_width, self._img_px_height = self._calculate_img_size()

        self.img = self._init_img(self._img_px_width,
                                  self._img_px_height)

        self._draw_borders(border_color)
        self._draw_grid(grid_color)

    def _calculate_grid_properties(self) -> Tuple[int, int]:
        """Calculates grid properties: sizes of cell and line.

        Returns:
          Returns a tuple with dot length and grid line width both in px.
        """
        cell = min(
            math.ceil(
                (self._max_img_px_width - self._border_size * 2) /
                self._map_dot_width
            ),
            math.ceil(
                (self._max_img_px_height - self._border_size * 2) /
                self._map_dot_height
            )
        )

        line = math.floor(cell * self.LINE_SIZE_FACTOR)

        if line < self.LINE_SIZE_MIN and cell - line > self.DOT_SIZE_MIN:
            line = self.LINE_SIZE_MIN

        dot = cell - line

        return dot, line

    def _calculate_img_size(self) -> Tuple[int, int]:
        img_px_width = \
            self._dot * self._map_dot_width + \
            self._line * (self._map_dot_width + 1) + \
            self._border_size * 2
        img_px_height = \
            self._dot * self._map_dot_height + \
            self._line * (self._map_dot_height + 1) + \
            self._border_size * 2
        return img_px_width, img_px_height

    def _calculate_rect_px_x_y(self, dot_x: int, dot_y: int) \
            -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """Calculates a rectangle position on a canvas by given dot
        position. Returns coordinates of top left corner and right bottom
        corner of the rectangle.

        Parameters:
          dot_x: dot's X
          dot_y: dot's Y
        """
        px_x_1 = self._border_size + self._dot * \
            dot_x + self._line * (dot_x + 1)
        px_y_1 = self._border_size + self._dot * \
            dot_y + self._line * (dot_y + 1)
        px_x_2 = px_x_1 + self._dot
        px_y_2 = px_y_1 + self._dot
        return (px_x_1, px_y_1), (px_x_2, px_y_2)

    def _draw_grid(self, grid_color: ColorRGB):
        """Draws a grid of given color.

        Parameters:
          grid_color: color in RGB format.
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

    def _draw_borders(self, border_color: ColorRGB):
        """Draws borders of given color.

        Parameters:
          border_color: color in RGB format.
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

    def draw_dot(self, dot_x: int, dot_y: int, color: ColorRGB):
        """Draws a single dot.
        """
        (px_x_1, px_y_1), (px_x_2, px_y_2) = self._calculate_rect_px_x_y(
            dot_x,
            dot_y,
        )
        self._draw_px_rect(px_x_1, px_y_1, px_x_2, px_y_2, color)

    def _draw_px_rect(self,
                      x1: int, y1: int,
                      x2: int, y2: int,
                      color: ColorRGB):
        self.img[y1:y2, x1:x2] = color

    def size(self) -> Tuple[int, int]:
        """Returns the size of an image.

        Returns:
          A tuple with width and height in px
        """
        return self._img_px_width, self._img_px_height

    def __repr__(self):
        return '{}.{}(width={}, height={}, dot={}, line={})'.format(
            __name__,
            self.__class__.__name__,
            self._img_px_width,
            self._img_px_height,
            self._dot,
            self._line)


class Screenshot:
    """A game screenshot.
    """

    COLOR_BACKGROUND: ColorRGB = BLACK_COLOR
    BORDER_SIZE = 2
    COLOR_BORDER: ColorRGB = (0x0, 0x11, 0x0)
    COLOR_GRID: ColorRGB = (0x0, 0x22, 0x0)

    def __init__(self,
                 map_size: Tuple[int, int],
                 max_size: Tuple[int, int],
                 game_objects: AnyObjectList,
                 strict_sized: bool = False):
        """Initializes a screenshot.

        Parameters:
          map_size: size of map in dots
          max_size: limits for result image in px
          game_objects: list of game objects
          strict_sized: a flag whether to generate an image with strict
            limited size or not
        """
        self._map_dot_width, self._map_dot_height = map_size
        self._max_img_px_width, self._max_img_px_height = max_size

        self._canvas = GridCanvas(self._map_dot_width,
                                  self._map_dot_height,
                                  self._max_img_px_width,
                                  self._max_img_px_height,
                                  self.BORDER_SIZE,
                                  self.COLOR_BORDER,
                                  self.COLOR_GRID)

        self._draw_objects(game_objects)

        self._image = self._rgb_image(strict_sized)

    def _draw_objects(self, game_objects: AnyObjectList):
        for game_object in game_objects:
            color = game_object.color()
            for (x, y) in game_object.dots:
                self._canvas.draw_dot(x, y, color)

    def _rgb_image(self, strict_sized: bool) -> Image:
        if not strict_sized:
            return Image.fromarray(self._canvas.img, 'RGB')

        strict_width, strict_height = self._calculate_strict_size()
        return Image.fromarray(self._canvas.img, 'RGB').resize(
            (strict_width, strict_height))

    @property
    def img(self) -> Image:
        """A result image
        """
        return self._image

    def _calculate_strict_size(self) -> Tuple[int, int]:
        height, width, _ = self._canvas.img.shape

        max_length = min(self._max_img_px_width, self._max_img_px_height)

        if width == height:
            return max_length, max_length

        if width > height:
            return max_length, height * max_length // width

        return width * max_length // height, max_length

    def __repr__(self):
        return '{}.{}(dot_w={}, dot_h={}, max_px_w={}, max_px_h={})'.format(
            __name__,
            self.__class__.__name__,
            self._map_dot_width,
            self._map_dot_height,
            self._max_img_px_width,
            self._max_img_px_height)
