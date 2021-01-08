"""Bot
"""

from typing import Any, Tuple

import numpy as np
rng = np.random.default_rng()

Dot = Tuple[int, int]


class Map:
    def __init__(self, width: int, height: int):
        self._width = width
        self._height = height

        # self._map = np.zeros((height, width), dtype=np.uint32)
        self._map = rng.integers(10, size=(height, width), dtype=np.uint32)
        self._objects = {}

    def add(self, obj: Any):
        self._objects[obj.id] = obj
        for dot in obj.dots:
            self._set_dot(dot, obj.id)

    def update(self, obj: Any):
        pass

    def delete(self, obj: Any):
        pass

    def _set_dot(self, dot: Dot, id_: int):
        x, y = dot
        self._map[y, x] = id_

    def sight(self, dot: Dot, radius: int):
        x, y = dot

        top = y - radius
        bottom = y + radius + 1
        left = x - radius
        right = x + radius + 1

        print("main", (
            (top, bottom),
            (left, right),
        ))

        cuts = []

        result_width = (radius * 2) + 1
        result_height = (radius * 2) + 1

        sight_map = np.zeros((result_height, result_width), dtype=np.uint32)

        # (top < 0, left < 0, bottom > self._height, right > self._width)

        cuts = {
            # When the sight is fully inside the map
            (0, 0, 0, 0): lambda: (
                (
                    (top, bottom), (left, right),
                    (0, result_height), (0, result_width),
                ),
            ),

            #
            (1, 0, 0, 0): lambda: (
                (
                    (0, bottom), (left, right),
                    (bottom, result_height), (0, right - left),
                ),
                (
                    (self._height + top, self._height), (left, right),
                    (0, bottom), (0, right - left),
                ),
            ),
            (0, 1, 0, 0): lambda: 1,
            (0, 0, 1, 0): lambda: 1,
            (0, 0, 0, 1): lambda: 1,

            (1, 1, 0, 0): lambda: 1,
            (0, 1, 1, 0): lambda: 1,
            (0, 0, 1, 1): lambda: 1,
            (1, 0, 0, 1): lambda: 1,

            (1, 1, 1, 1): lambda: (
                (
                    (0, result_height), (0, result_width),
                    (top, bottom), (left, right),
                ),
            ),
        }[(
            top < 0,
            left < 0,
            bottom > self._height,
            right > self._width,
        )]()

        print("result", cuts)
        print(self._map)

        for cut in cuts:
            print("cut", cut)
            (src_y_from, src_y_to), (src_x_from, src_x_to), \
                (dst_y_from, dst_y_to), (dst_x_from, dst_x_to) = cut

            sight_map[dst_y_from:dst_y_to, dst_x_from:dst_x_to] =\
                self._map[src_y_from:src_y_to, src_x_from:src_x_to]

        print(sight_map)


        if top < 0:
            pass
        if left < 0:
            pass
        if bottom > self._height:
            pass
        if right > self._width:
            pass

        # if top < 0:
        #     print((
        #         (
        #             0,
        #             self._height - self._height - top - 1,
        #         ),
        #         (
        #             0,
        #             self._width - self._width - left - 1,
        #         ),
        #         (
        #             self._height + top + 1,
        #             self._height,
        #         ),
        #         (
        #             max(left, 0),
        #             min(right, self._width),
        #         ),
        #     ))

        # if not bottom <= self._height:
        #     bottom_piece_top = 0
        #     bottom_piece_bottom = bottom - self._height
        #
        #     # bottom = self._height
        #
        #     cuts.append((
        #         (bottom_piece_top, bottom_piece_bottom),
        #         (max(left, 0), min(right, self._width)),
        #     ))
        #
        #     print("bottom", (
        #         (bottom_piece_top, bottom_piece_bottom),
        #         (left, right),
        #     ))
        #
        # if left < 0:
        #     left_piece_left = self._width + left
        #     left_piece_right = self._width
        #
        #     # left = 0
        #
        #     print("left", (
        #         (top, bottom),
        #         (left_piece_left, left_piece_right),
        #     ))
        #     cuts.append((
        #         (max(top, 0), min(bottom, self._width)),
        #         (left_piece_left, left_piece_right),
        #     ))
        #
        # if not right < self._width:
        #     right_piece_left = 0
        #     right_piece_right = right - self._width
        #
        #     # right = self._width
        #
        #     print("right", (
        #         (top, bottom),
        #         (right_piece_left, right_piece_right),
        #     ))
        #
        #     cuts.append((
        #         (max(top, 0), min(bottom, self._width)),
        #         (right_piece_left, right_piece_right),
        #     ))

        # cuts.append((
        #     (max(top, 0), min(bottom, self._width)),
        #     (max(left, 0), min(right, self._width)),
        # ))

        # print("main after", (
        #     (top, bottom),
        #     (left, right),
        # ))

        # print(self._map)
        # print(sight_map)

        # print(cuts)
        # print(self._map[top:bottom, left:right])

        # return self._map[
        #     min(top, bottom):max(top, bottom),
        #     min(left, right):max(left, right),
        # ]


class Sight:
    def __init__(self, map_: Map, dot: Dot, radius: int):
        pass
