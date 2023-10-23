"""Utility functions and classes.
"""
from __future__ import annotations
from collections.abc import Sequence
from typing import final, TypeAlias

import pyperclip

__all__ = ["Color", "ColorLike", "get_clipboard", "set_clipboard"]


@final
class Color:
    """A utility class for representing colors and converting between color formats.

    A color is stored in *normalized RGBA* format. That is, all coordinates take values
    between 0 and 1. The color's coordinates can be accessed by the :py:attr:`red`,
    :py:attr:`green`, :py:attr:`blue` and :py:attr:`alpha` properties.
    """

    __slots__ = ("_r", "_g", "_b", "_a")

    _r: float
    _g: float
    _b: float
    _a: float

    def __init__(self, red: float, green: float, blue: float, alpha: float = 1) -> None:
        if not (
            0 <= red <= 1 and 0 <= green <= 1 and 0 <= blue <= 1 and 0 <= alpha <= 1
        ):
            raise ValueError("RGBA coordinates must be normalized (between 0 and 1)")
        self._r = red
        self._g = green
        self._b = blue
        self._a = alpha

    @classmethod
    def create(cls, value: ColorLike) -> Color:
        if isinstance(value, Color):
            return value
        if isinstance(value, str):
            # Check if it's a pre-defined color
            color = _PRE_DEFINED_COLORS.get(value)
            if color is not None:
                return color
            # Check if it's an HTML color
            color = cls._parse_html_color(value)
            if color is not None:
                return color
            color = cls._parse_hex_color(value)
            if color is not None:
                return color
            raise ValueError(f"Invalid string format for color: '{value}'")
        if isinstance(value, BytesLike):
            return cls.from_bytes(value)
        if isinstance(value, int):
            return cls.from_int(value)
        if isinstance(value, Sequence):
            if len(value) not in (3, 4):
                raise ValueError("Sequence must be of length 3 (RGB) or 4 (RGBA)")
            return cls(*value)
        raise TypeError(f"Can't create color from '{value}'")

    @classmethod
    def names(cls) -> list[str]:
        return list(_PRE_DEFINED_COLORS.keys())

    @classmethod
    def _parse_html_color(cls, color: str) -> Color | None:
        # color of the format '#rrggbb' or '#rrggbbaa'
        if len(color) % 2 == 0 or color[0] != "#":
            return None
        try:
            color_coords = [int(color[i : i + 2], 16) for i in range(1, len(color), 2)]
        except ValueError:
            return None
        else:
            if len(color_coords) == 3:
                return cls.from_rgb(*color_coords)
            if len(color_coords) == 4:
                return cls.from_rgba(*color_coords)
            return None

    @classmethod
    def _parse_hex_color(cls, color: str) -> Color | None:
        # color of the format '0xrrggbb' or '0xrrggbbaa'
        if len(color) not in (8, 10) or color[0] != "0" or color[1] not in ("x", "X"):
            return None
        try:
            color_coords = [int(color[i : i + 2], 16) for i in range(2, len(color), 2)]
        except ValueError:
            return None
        else:
            if len(color_coords) == 3:
                return cls.from_rgb(*color_coords)
            if len(color_coords) == 4:
                return cls.from_rgba(*color_coords)
            return None

    @classmethod
    def from_rgb(cls, red: int, green: int, blue: int) -> Color:
        if not (0 <= red <= 255 and 0 <= green <= 255 and 0 <= blue <= 255):
            raise ValueError("RGB coordinates must be between 0 and 255")
        return cls(red / 255, green / 255, blue / 255)

    @classmethod
    def from_rgba(cls, red: int, green: int, blue: int, alpha: int) -> Color:
        if not (
            0 <= red <= 255
            and 0 <= green <= 255
            and 0 <= blue <= 255
            and 0 <= alpha <= 255
        ):
            raise ValueError("RGBA coordinates must be between 0 and 255")
        return cls(red / 255, green / 255, blue / 255, alpha / 255)

    @classmethod
    def from_html(cls, color: str) -> Color:
        color_obj = cls._parse_html_color(color)
        if color_obj is None:
            raise ValueError(f"Invalid HTML format for color {color}")
        return color_obj

    @classmethod
    def from_hex(cls, color: str) -> Color:
        color_obj = cls._parse_hex_color(color)
        if color_obj is None:
            raise ValueError(f"Invalid HEX format for color {color}")
        return color_obj

    @classmethod
    def from_int(cls, color: int) -> Color:
        if not (0 <= color <= 0xFFFFFFFF):
            raise ValueError(
                "An integer for an RGBA color must be between 0 and 0xFFFFFFFF"
            )
        r = (color >> 24) & 0xFF
        g = (color >> 16) & 0xFF
        b = (color >> 8) & 0xFF
        a = color & 0xFF
        return cls.from_rgba(r, g, b, a)

    @classmethod
    def from_bytes(cls, color: BytesLike) -> Color:
        if len(color) == 3:
            return cls.from_rgb(*color)
        if len(color) == 4:
            return cls.from_rgba(*color)
        raise ValueError(f"Invalid bytes format for color: '{bytes(color)}'")

    @property
    def red(self) -> float:
        """The `red` coordinate of the color (between 0 and 1)."""
        return self._r

    @property
    def green(self) -> float:
        """The `green` coordinate of the color (between 0 and 1)."""
        return self._g

    @property
    def blue(self) -> float:
        """The `blue` coordinate of the color (between 0 and 1)."""
        return self._b

    @property
    def alpha(self) -> float:
        """The `alpha` coordinate of the color (between 0 and 1)."""
        return self._a

    def rgb(self) -> tuple[int, int, int]:
        return (round(255 * self._r), round(255 * self._g), round(255 * self._b))

    def rgba(self) -> tuple[int, int, int, int]:
        return (
            round(255 * self._r),
            round(255 * self._g),
            round(255 * self._b),
            round(255 * self._a),
        )

    def normalized_rgb(self) -> tuple[float, float, float]:
        return (self._r, self._g, self._b)

    def normalized_rgba(self) -> tuple[float, float, float, float]:
        return (self._r, self._g, self._b, self._a)

    def __int__(self) -> int:
        r, g, b, a = self.rgba()
        return a + (b << 8) + (g << 16) + (r << 24)

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}"
            f"(red={self._r}, green={self._g}, blue={self._b}, alpha={self._a})"
        )

    def __hash__(self) -> int:
        return hash((type(self), self._r, self._g, self._b, self._a))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Color):
            return NotImplemented
        return (
            self._r == other._r
            and self._g == other._g
            and self._b == other._b
            and self._a == other._a
        )


# Taken from
# https://github.com/pygame-community/pygame-ce/blob/main/src_py/colordict.py
_PRE_DEFINED_COLORS: dict[str, Color] = {
    "alice-blue": Color.from_rgb(240, 248, 255),
    "antique-white": Color.from_rgb(250, 235, 215),
    "antique-white1": Color.from_rgb(255, 239, 219),
    "antique-white2": Color.from_rgb(238, 223, 204),
    "antique-white3": Color.from_rgb(205, 192, 176),
    "antique-white4": Color.from_rgb(139, 131, 120),
    "aqua": Color.from_rgb(0, 255, 255),
    "aquamarine": Color.from_rgb(127, 255, 212),
    "aquamarine1": Color.from_rgb(127, 255, 212),
    "aquamarine2": Color.from_rgb(118, 238, 198),
    "aquamarine3": Color.from_rgb(102, 205, 170),
    "aquamarine4": Color.from_rgb(69, 139, 116),
    "azure": Color.from_rgb(240, 255, 255),
    "azure1": Color.from_rgb(240, 255, 255),
    "azure3": Color.from_rgb(193, 205, 205),
    "azure2": Color.from_rgb(224, 238, 238),
    "azure4": Color.from_rgb(131, 139, 139),
    "beige": Color.from_rgb(245, 245, 220),
    "bisque": Color.from_rgb(255, 228, 196),
    "bisque1": Color.from_rgb(255, 228, 196),
    "bisque2": Color.from_rgb(238, 213, 183),
    "bisque3": Color.from_rgb(205, 183, 158),
    "bisque4": Color.from_rgb(139, 125, 107),
    "black": Color.from_rgb(0, 0, 0),
    "blanched-almond": Color.from_rgb(255, 235, 205),
    "blue": Color.from_rgb(0, 0, 255),
    "blue1": Color.from_rgb(0, 0, 255),
    "blue2": Color.from_rgb(0, 0, 238),
    "blue3": Color.from_rgb(0, 0, 205),
    "blue4": Color.from_rgb(0, 0, 139),
    "blue-violet": Color.from_rgb(138, 43, 226),
    "brown": Color.from_rgb(165, 42, 42),
    "brown1": Color.from_rgb(255, 64, 64),
    "brown2": Color.from_rgb(238, 59, 59),
    "brown3": Color.from_rgb(205, 51, 51),
    "brown4": Color.from_rgb(139, 35, 35),
    "burly-wood": Color.from_rgb(222, 184, 135),
    "burly-wood1": Color.from_rgb(255, 211, 155),
    "burly-wood2": Color.from_rgb(238, 197, 145),
    "burly-wood3": Color.from_rgb(205, 170, 125),
    "burly-wood4": Color.from_rgb(139, 115, 85),
    "cadet-blue": Color.from_rgb(95, 158, 160),
    "cadet-blue1": Color.from_rgb(152, 245, 255),
    "cadet-blue2": Color.from_rgb(142, 229, 238),
    "cadet-blue3": Color.from_rgb(122, 197, 205),
    "cadet-blue4": Color.from_rgb(83, 134, 139),
    "chartreuse": Color.from_rgb(127, 255, 0),
    "chartreuse1": Color.from_rgb(127, 255, 0),
    "chartreuse2": Color.from_rgb(118, 238, 0),
    "chartreuse3": Color.from_rgb(102, 205, 0),
    "chartreuse4": Color.from_rgb(69, 139, 0),
    "chocolate": Color.from_rgb(210, 105, 30),
    "chocolate1": Color.from_rgb(255, 127, 36),
    "chocolate2": Color.from_rgb(238, 118, 33),
    "chocolate3": Color.from_rgb(205, 102, 29),
    "chocolate4": Color.from_rgb(139, 69, 19),
    "coral": Color.from_rgb(255, 127, 80),
    "coral1": Color.from_rgb(255, 114, 86),
    "coral2": Color.from_rgb(238, 106, 80),
    "coral3": Color.from_rgb(205, 91, 69),
    "coral4": Color.from_rgb(139, 62, 47),
    "corn-flower-blue": Color.from_rgb(100, 149, 237),
    "corn-silk": Color.from_rgb(255, 248, 220),
    "corn-silk1": Color.from_rgb(255, 248, 220),
    "corn-silk2": Color.from_rgb(238, 232, 205),
    "corn-silk3": Color.from_rgb(205, 200, 177),
    "corn-silk4": Color.from_rgb(139, 136, 120),
    "crimson": Color.from_rgb(220, 20, 60),
    "cyan": Color.from_rgb(0, 255, 255),
    "cyan1": Color.from_rgb(0, 255, 255),
    "cyan2": Color.from_rgb(0, 238, 238),
    "cyan3": Color.from_rgb(0, 205, 205),
    "cyan4": Color.from_rgb(0, 139, 139),
    "dark-blue": Color.from_rgb(0, 0, 139),
    "dark-cyan": Color.from_rgb(0, 139, 139),
    "dark-goldenrod": Color.from_rgb(184, 134, 11),
    "dark-goldenrod1": Color.from_rgb(255, 185, 15),
    "dark-goldenrod2": Color.from_rgb(238, 173, 14),
    "dark-goldenrod3": Color.from_rgb(205, 149, 12),
    "dark-goldenrod4": Color.from_rgb(139, 101, 8),
    "dark-gray": Color.from_rgb(169, 169, 169),
    "dark-green": Color.from_rgb(0, 100, 0),
    "dark-grey": Color.from_rgb(169, 169, 169),
    "dark-khaki": Color.from_rgb(189, 183, 107),
    "dark-magenta": Color.from_rgb(139, 0, 139),
    "dark-olive-green": Color.from_rgb(85, 107, 47),
    "dark-olive-green1": Color.from_rgb(202, 255, 112),
    "dark-olive-green2": Color.from_rgb(188, 238, 104),
    "dark-olive-green3": Color.from_rgb(162, 205, 90),
    "dark-olive-green4": Color.from_rgb(110, 139, 61),
    "dark-orange": Color.from_rgb(255, 140, 0),
    "dark-orange1": Color.from_rgb(255, 127, 0),
    "dark-orange2": Color.from_rgb(238, 118, 0),
    "dark-orange3": Color.from_rgb(205, 102, 0),
    "dark-orange4": Color.from_rgb(139, 69, 0),
    "dark-orchid": Color.from_rgb(153, 50, 204),
    "dark-orchid1": Color.from_rgb(191, 62, 255),
    "dark-orchid2": Color.from_rgb(178, 58, 238),
    "dark-orchid3": Color.from_rgb(154, 50, 205),
    "dark-orchid4": Color.from_rgb(104, 34, 139),
    "dark-red": Color.from_rgb(139, 0, 0),
    "dark-salmon": Color.from_rgb(233, 150, 122),
    "dark-sea-green": Color.from_rgb(143, 188, 143),
    "dark-sea-green1": Color.from_rgb(193, 255, 193),
    "dark-sea-green2": Color.from_rgb(180, 238, 180),
    "dark-sea-green3": Color.from_rgb(155, 205, 155),
    "dark-sea-green4": Color.from_rgb(105, 139, 105),
    "dark-slate-blue": Color.from_rgb(72, 61, 139),
    "dark-slate-gray": Color.from_rgb(47, 79, 79),
    "dark-slate-gray1": Color.from_rgb(151, 255, 255),
    "dark-slate-gray2": Color.from_rgb(141, 238, 238),
    "dark-slate-gray3": Color.from_rgb(121, 205, 205),
    "dark-slate-gray4": Color.from_rgb(82, 139, 139),
    "dark-slate-grey": Color.from_rgb(47, 79, 79),
    "dark-turquoise": Color.from_rgb(0, 206, 209),
    "dark-violet": Color.from_rgb(148, 0, 211),
    "deep-pink": Color.from_rgb(255, 20, 147),
    "deep-pink1": Color.from_rgb(255, 20, 147),
    "deep-pink2": Color.from_rgb(238, 18, 137),
    "deep-pink3": Color.from_rgb(205, 16, 118),
    "deep-pink4": Color.from_rgb(139, 10, 80),
    "deep-sky-blue": Color.from_rgb(0, 191, 255),
    "deep-sky-blue1": Color.from_rgb(0, 191, 255),
    "deep-sky-blue2": Color.from_rgb(0, 178, 238),
    "deep-sky-blue3": Color.from_rgb(0, 154, 205),
    "deep-sky-blue4": Color.from_rgb(0, 104, 139),
    "dim-gray": Color.from_rgb(105, 105, 105),
    "dim-grey": Color.from_rgb(105, 105, 105),
    "dodger-blue": Color.from_rgb(30, 144, 255),
    "dodger-blue1": Color.from_rgb(30, 144, 255),
    "dodger-blue2": Color.from_rgb(28, 134, 238),
    "dodger-blue3": Color.from_rgb(24, 116, 205),
    "dodger-blue4": Color.from_rgb(16, 78, 139),
    "firebrick": Color.from_rgb(178, 34, 34),
    "firebrick1": Color.from_rgb(255, 48, 48),
    "firebrick2": Color.from_rgb(238, 44, 44),
    "firebrick3": Color.from_rgb(205, 38, 38),
    "firebrick4": Color.from_rgb(139, 26, 26),
    "floral-white": Color.from_rgb(255, 250, 240),
    "forest-green": Color.from_rgb(34, 139, 34),
    "fuchsia": Color.from_rgb(255, 0, 255),
    "gainsboro": Color.from_rgb(220, 220, 220),
    "ghost-white": Color.from_rgb(248, 248, 255),
    "gold": Color.from_rgb(255, 215, 0),
    "gold1": Color.from_rgb(255, 215, 0),
    "gold2": Color.from_rgb(238, 201, 0),
    "gold3": Color.from_rgb(205, 173, 0),
    "gold4": Color.from_rgb(139, 117, 0),
    "goldenrod": Color.from_rgb(218, 165, 32),
    "goldenrod1": Color.from_rgb(255, 193, 37),
    "goldenrod2": Color.from_rgb(238, 180, 34),
    "goldenrod3": Color.from_rgb(205, 155, 29),
    "goldenrod4": Color.from_rgb(139, 105, 20),
    "gray": Color.from_rgb(190, 190, 190),
    "gray0": Color.from_rgb(0, 0, 0),
    "gray1": Color.from_rgb(3, 3, 3),
    "gray2": Color.from_rgb(5, 5, 5),
    "gray3": Color.from_rgb(8, 8, 8),
    "gray4": Color.from_rgb(10, 10, 10),
    "gray5": Color.from_rgb(13, 13, 13),
    "gray6": Color.from_rgb(15, 15, 15),
    "gray7": Color.from_rgb(18, 18, 18),
    "gray8": Color.from_rgb(20, 20, 20),
    "gray9": Color.from_rgb(23, 23, 23),
    "gray10": Color.from_rgb(26, 26, 26),
    "gray11": Color.from_rgb(28, 28, 28),
    "gray12": Color.from_rgb(31, 31, 31),
    "gray13": Color.from_rgb(33, 33, 33),
    "gray14": Color.from_rgb(36, 36, 36),
    "gray15": Color.from_rgb(38, 38, 38),
    "gray16": Color.from_rgb(41, 41, 41),
    "gray17": Color.from_rgb(43, 43, 43),
    "gray18": Color.from_rgb(46, 46, 46),
    "gray19": Color.from_rgb(48, 48, 48),
    "gray20": Color.from_rgb(51, 51, 51),
    "gray21": Color.from_rgb(54, 54, 54),
    "gray22": Color.from_rgb(56, 56, 56),
    "gray23": Color.from_rgb(59, 59, 59),
    "gray24": Color.from_rgb(61, 61, 61),
    "gray25": Color.from_rgb(64, 64, 64),
    "gray26": Color.from_rgb(66, 66, 66),
    "gray27": Color.from_rgb(69, 69, 69),
    "gray28": Color.from_rgb(71, 71, 71),
    "gray29": Color.from_rgb(74, 74, 74),
    "gray30": Color.from_rgb(77, 77, 77),
    "gray31": Color.from_rgb(79, 79, 79),
    "gray32": Color.from_rgb(82, 82, 82),
    "gray33": Color.from_rgb(84, 84, 84),
    "gray34": Color.from_rgb(87, 87, 87),
    "gray35": Color.from_rgb(89, 89, 89),
    "gray36": Color.from_rgb(92, 92, 92),
    "gray37": Color.from_rgb(94, 94, 94),
    "gray38": Color.from_rgb(97, 97, 97),
    "gray39": Color.from_rgb(99, 99, 99),
    "gray40": Color.from_rgb(102, 102, 102),
    "gray41": Color.from_rgb(105, 105, 105),
    "gray42": Color.from_rgb(107, 107, 107),
    "gray43": Color.from_rgb(110, 110, 110),
    "gray44": Color.from_rgb(112, 112, 112),
    "gray45": Color.from_rgb(115, 115, 115),
    "gray46": Color.from_rgb(117, 117, 117),
    "gray47": Color.from_rgb(120, 120, 120),
    "gray48": Color.from_rgb(122, 122, 122),
    "gray49": Color.from_rgb(125, 125, 125),
    "gray50": Color.from_rgb(127, 127, 127),
    "gray51": Color.from_rgb(130, 130, 130),
    "gray52": Color.from_rgb(133, 133, 133),
    "gray53": Color.from_rgb(135, 135, 135),
    "gray54": Color.from_rgb(138, 138, 138),
    "gray55": Color.from_rgb(140, 140, 140),
    "gray56": Color.from_rgb(143, 143, 143),
    "gray57": Color.from_rgb(145, 145, 145),
    "gray58": Color.from_rgb(148, 148, 148),
    "gray59": Color.from_rgb(150, 150, 150),
    "gray60": Color.from_rgb(153, 153, 153),
    "gray61": Color.from_rgb(156, 156, 156),
    "gray62": Color.from_rgb(158, 158, 158),
    "gray63": Color.from_rgb(161, 161, 161),
    "gray64": Color.from_rgb(163, 163, 163),
    "gray65": Color.from_rgb(166, 166, 166),
    "gray66": Color.from_rgb(168, 168, 168),
    "gray67": Color.from_rgb(171, 171, 171),
    "gray68": Color.from_rgb(173, 173, 173),
    "gray69": Color.from_rgb(176, 176, 176),
    "gray70": Color.from_rgb(179, 179, 179),
    "gray71": Color.from_rgb(181, 181, 181),
    "gray72": Color.from_rgb(184, 184, 184),
    "gray73": Color.from_rgb(186, 186, 186),
    "gray74": Color.from_rgb(189, 189, 189),
    "gray75": Color.from_rgb(191, 191, 191),
    "gray76": Color.from_rgb(194, 194, 194),
    "gray77": Color.from_rgb(196, 196, 196),
    "gray78": Color.from_rgb(199, 199, 199),
    "gray79": Color.from_rgb(201, 201, 201),
    "gray80": Color.from_rgb(204, 204, 204),
    "gray81": Color.from_rgb(207, 207, 207),
    "gray82": Color.from_rgb(209, 209, 209),
    "gray83": Color.from_rgb(212, 212, 212),
    "gray84": Color.from_rgb(214, 214, 214),
    "gray85": Color.from_rgb(217, 217, 217),
    "gray86": Color.from_rgb(219, 219, 219),
    "gray87": Color.from_rgb(222, 222, 222),
    "gray88": Color.from_rgb(224, 224, 224),
    "gray89": Color.from_rgb(227, 227, 227),
    "gray90": Color.from_rgb(229, 229, 229),
    "gray91": Color.from_rgb(232, 232, 232),
    "gray92": Color.from_rgb(235, 235, 235),
    "gray93": Color.from_rgb(237, 237, 237),
    "gray94": Color.from_rgb(240, 240, 240),
    "gray95": Color.from_rgb(242, 242, 242),
    "gray96": Color.from_rgb(245, 245, 245),
    "gray97": Color.from_rgb(247, 247, 247),
    "gray98": Color.from_rgb(250, 250, 250),
    "gray99": Color.from_rgb(252, 252, 252),
    "gray100": Color.from_rgb(255, 255, 255),
    "green": Color.from_rgb(0, 255, 0),
    "green1": Color.from_rgb(0, 255, 0),
    "green2": Color.from_rgb(0, 238, 0),
    "green3": Color.from_rgb(0, 205, 0),
    "green4": Color.from_rgb(0, 139, 0),
    "green-yellow": Color.from_rgb(173, 255, 47),
    "grey": Color.from_rgb(190, 190, 190),
    "grey0": Color.from_rgb(0, 0, 0),
    "grey1": Color.from_rgb(3, 3, 3),
    "grey2": Color.from_rgb(5, 5, 5),
    "grey3": Color.from_rgb(8, 8, 8),
    "grey4": Color.from_rgb(10, 10, 10),
    "grey5": Color.from_rgb(13, 13, 13),
    "grey6": Color.from_rgb(15, 15, 15),
    "grey7": Color.from_rgb(18, 18, 18),
    "grey8": Color.from_rgb(20, 20, 20),
    "grey9": Color.from_rgb(23, 23, 23),
    "grey10": Color.from_rgb(26, 26, 26),
    "grey11": Color.from_rgb(28, 28, 28),
    "grey12": Color.from_rgb(31, 31, 31),
    "grey13": Color.from_rgb(33, 33, 33),
    "grey14": Color.from_rgb(36, 36, 36),
    "grey15": Color.from_rgb(38, 38, 38),
    "grey16": Color.from_rgb(41, 41, 41),
    "grey17": Color.from_rgb(43, 43, 43),
    "grey18": Color.from_rgb(46, 46, 46),
    "grey19": Color.from_rgb(48, 48, 48),
    "grey20": Color.from_rgb(51, 51, 51),
    "grey21": Color.from_rgb(54, 54, 54),
    "grey22": Color.from_rgb(56, 56, 56),
    "grey23": Color.from_rgb(59, 59, 59),
    "grey24": Color.from_rgb(61, 61, 61),
    "grey25": Color.from_rgb(64, 64, 64),
    "grey26": Color.from_rgb(66, 66, 66),
    "grey27": Color.from_rgb(69, 69, 69),
    "grey28": Color.from_rgb(71, 71, 71),
    "grey29": Color.from_rgb(74, 74, 74),
    "grey30": Color.from_rgb(77, 77, 77),
    "grey31": Color.from_rgb(79, 79, 79),
    "grey32": Color.from_rgb(82, 82, 82),
    "grey33": Color.from_rgb(84, 84, 84),
    "grey34": Color.from_rgb(87, 87, 87),
    "grey35": Color.from_rgb(89, 89, 89),
    "grey36": Color.from_rgb(92, 92, 92),
    "grey37": Color.from_rgb(94, 94, 94),
    "grey38": Color.from_rgb(97, 97, 97),
    "grey39": Color.from_rgb(99, 99, 99),
    "grey40": Color.from_rgb(102, 102, 102),
    "grey41": Color.from_rgb(105, 105, 105),
    "grey42": Color.from_rgb(107, 107, 107),
    "grey43": Color.from_rgb(110, 110, 110),
    "grey44": Color.from_rgb(112, 112, 112),
    "grey45": Color.from_rgb(115, 115, 115),
    "grey46": Color.from_rgb(117, 117, 117),
    "grey47": Color.from_rgb(120, 120, 120),
    "grey48": Color.from_rgb(122, 122, 122),
    "grey49": Color.from_rgb(125, 125, 125),
    "grey50": Color.from_rgb(127, 127, 127),
    "grey51": Color.from_rgb(130, 130, 130),
    "grey52": Color.from_rgb(133, 133, 133),
    "grey53": Color.from_rgb(135, 135, 135),
    "grey54": Color.from_rgb(138, 138, 138),
    "grey55": Color.from_rgb(140, 140, 140),
    "grey56": Color.from_rgb(143, 143, 143),
    "grey57": Color.from_rgb(145, 145, 145),
    "grey58": Color.from_rgb(148, 148, 148),
    "grey59": Color.from_rgb(150, 150, 150),
    "grey60": Color.from_rgb(153, 153, 153),
    "grey61": Color.from_rgb(156, 156, 156),
    "grey62": Color.from_rgb(158, 158, 158),
    "grey63": Color.from_rgb(161, 161, 161),
    "grey64": Color.from_rgb(163, 163, 163),
    "grey65": Color.from_rgb(166, 166, 166),
    "grey66": Color.from_rgb(168, 168, 168),
    "grey67": Color.from_rgb(171, 171, 171),
    "grey68": Color.from_rgb(173, 173, 173),
    "grey69": Color.from_rgb(176, 176, 176),
    "grey70": Color.from_rgb(179, 179, 179),
    "grey71": Color.from_rgb(181, 181, 181),
    "grey72": Color.from_rgb(184, 184, 184),
    "grey73": Color.from_rgb(186, 186, 186),
    "grey74": Color.from_rgb(189, 189, 189),
    "grey75": Color.from_rgb(191, 191, 191),
    "grey76": Color.from_rgb(194, 194, 194),
    "grey77": Color.from_rgb(196, 196, 196),
    "grey78": Color.from_rgb(199, 199, 199),
    "grey79": Color.from_rgb(201, 201, 201),
    "grey80": Color.from_rgb(204, 204, 204),
    "grey81": Color.from_rgb(207, 207, 207),
    "grey82": Color.from_rgb(209, 209, 209),
    "grey83": Color.from_rgb(212, 212, 212),
    "grey84": Color.from_rgb(214, 214, 214),
    "grey85": Color.from_rgb(217, 217, 217),
    "grey86": Color.from_rgb(219, 219, 219),
    "grey87": Color.from_rgb(222, 222, 222),
    "grey88": Color.from_rgb(224, 224, 224),
    "grey89": Color.from_rgb(227, 227, 227),
    "grey90": Color.from_rgb(229, 229, 229),
    "grey91": Color.from_rgb(232, 232, 232),
    "grey92": Color.from_rgb(235, 235, 235),
    "grey93": Color.from_rgb(237, 237, 237),
    "grey94": Color.from_rgb(240, 240, 240),
    "grey95": Color.from_rgb(242, 242, 242),
    "grey96": Color.from_rgb(245, 245, 245),
    "grey97": Color.from_rgb(247, 247, 247),
    "grey98": Color.from_rgb(250, 250, 250),
    "grey99": Color.from_rgb(252, 252, 252),
    "grey100": Color.from_rgb(255, 255, 255),
    "honeydew": Color.from_rgb(240, 255, 240),
    "honeydew1": Color.from_rgb(240, 255, 240),
    "honeydew2": Color.from_rgb(224, 238, 224),
    "honeydew3": Color.from_rgb(193, 205, 193),
    "honeydew4": Color.from_rgb(131, 139, 131),
    "hot-pink": Color.from_rgb(255, 105, 180),
    "hot-pink1": Color.from_rgb(255, 110, 180),
    "hot-pink2": Color.from_rgb(238, 106, 167),
    "hot-pink3": Color.from_rgb(205, 96, 144),
    "hot-pink4": Color.from_rgb(139, 58, 98),
    "indian-red": Color.from_rgb(205, 92, 92),
    "indian-red1": Color.from_rgb(255, 106, 106),
    "indian-red2": Color.from_rgb(238, 99, 99),
    "indian-red3": Color.from_rgb(205, 85, 85),
    "indian-red4": Color.from_rgb(139, 58, 58),
    "indigo": Color.from_rgb(75, 0, 130),
    "ivory": Color.from_rgb(255, 255, 240),
    "ivory1": Color.from_rgb(255, 255, 240),
    "ivory2": Color.from_rgb(238, 238, 224),
    "ivory3": Color.from_rgb(205, 205, 193),
    "ivory4": Color.from_rgb(139, 139, 131),
    "khaki": Color.from_rgb(240, 230, 140),
    "khaki1": Color.from_rgb(255, 246, 143),
    "khaki2": Color.from_rgb(238, 230, 133),
    "khaki3": Color.from_rgb(205, 198, 115),
    "khaki4": Color.from_rgb(139, 134, 78),
    "lavender": Color.from_rgb(230, 230, 250),
    "lavender-blush": Color.from_rgb(255, 240, 245),
    "lavender-blush1": Color.from_rgb(255, 240, 245),
    "lavender-blush2": Color.from_rgb(238, 224, 229),
    "lavender-blush3": Color.from_rgb(205, 193, 197),
    "lavender-blush4": Color.from_rgb(139, 131, 134),
    "lawn-green": Color.from_rgb(124, 252, 0),
    "lemon-chiffon": Color.from_rgb(255, 250, 205),
    "lemon-chiffon1": Color.from_rgb(255, 250, 205),
    "lemon-chiffon2": Color.from_rgb(238, 233, 191),
    "lemon-chiffon3": Color.from_rgb(205, 201, 165),
    "lemon-chiffon4": Color.from_rgb(139, 137, 112),
    "light-blue": Color.from_rgb(173, 216, 230),
    "light-blue1": Color.from_rgb(191, 239, 255),
    "light-blue2": Color.from_rgb(178, 223, 238),
    "light-blue3": Color.from_rgb(154, 192, 205),
    "light-blue4": Color.from_rgb(104, 131, 139),
    "light-coral": Color.from_rgb(240, 128, 128),
    "light-cyan": Color.from_rgb(224, 255, 255),
    "light-cyan1": Color.from_rgb(224, 255, 255),
    "light-cyan2": Color.from_rgb(209, 238, 238),
    "light-cyan3": Color.from_rgb(180, 205, 205),
    "light-cyan4": Color.from_rgb(122, 139, 139),
    "light-goldenrod": Color.from_rgb(238, 221, 130),
    "light-goldenrod1": Color.from_rgb(255, 236, 139),
    "light-goldenrod2": Color.from_rgb(238, 220, 130),
    "light-goldenrod3": Color.from_rgb(205, 190, 112),
    "light-goldenrod4": Color.from_rgb(139, 129, 76),
    "light-golden-rod-yellow": Color.from_rgb(250, 250, 210),
    "light-gray": Color.from_rgb(211, 211, 211),
    "light-green": Color.from_rgb(144, 238, 144),
    "light-grey": Color.from_rgb(211, 211, 211),
    "light-pink": Color.from_rgb(255, 182, 193),
    "light-pink1": Color.from_rgb(255, 174, 185),
    "light-pink2": Color.from_rgb(238, 162, 173),
    "light-pink3": Color.from_rgb(205, 140, 149),
    "light-pink4": Color.from_rgb(139, 95, 101),
    "light-salmon": Color.from_rgb(255, 160, 122),
    "light-salmon1": Color.from_rgb(255, 160, 122),
    "light-salmon2": Color.from_rgb(238, 149, 114),
    "light-salmon3": Color.from_rgb(205, 129, 98),
    "light-salmon4": Color.from_rgb(139, 87, 66),
    "light-sea-green": Color.from_rgb(32, 178, 170),
    "light-sky-blue": Color.from_rgb(135, 206, 250),
    "light-sky-blue1": Color.from_rgb(176, 226, 255),
    "light-sky-blue2": Color.from_rgb(164, 211, 238),
    "light-sky-blue3": Color.from_rgb(141, 182, 205),
    "light-sky-blue4": Color.from_rgb(96, 123, 139),
    "light-slate-blue": Color.from_rgb(132, 112, 255),
    "light-slate-gray": Color.from_rgb(119, 136, 153),
    "light-slate-grey": Color.from_rgb(119, 136, 153),
    "light-steel-blue": Color.from_rgb(176, 196, 222),
    "light-steel-blue1": Color.from_rgb(202, 225, 255),
    "light-steel-blue2": Color.from_rgb(188, 210, 238),
    "light-steel-blue3": Color.from_rgb(162, 181, 205),
    "light-steel-blue4": Color.from_rgb(110, 123, 139),
    "light-yellow": Color.from_rgb(255, 255, 224),
    "light-yellow1": Color.from_rgb(255, 255, 224),
    "light-yellow2": Color.from_rgb(238, 238, 209),
    "light-yellow3": Color.from_rgb(205, 205, 180),
    "light-yellow4": Color.from_rgb(139, 139, 122),
    "linen": Color.from_rgb(250, 240, 230),
    "lime": Color.from_rgb(0, 255, 0),
    "lime-green": Color.from_rgb(50, 205, 50),
    "magenta": Color.from_rgb(255, 0, 255),
    "magenta1": Color.from_rgb(255, 0, 255),
    "magenta2": Color.from_rgb(238, 0, 238),
    "magenta3": Color.from_rgb(205, 0, 205),
    "magenta4": Color.from_rgb(139, 0, 139),
    "maroon": Color.from_rgb(176, 48, 96),
    "maroon1": Color.from_rgb(255, 52, 179),
    "maroon2": Color.from_rgb(238, 48, 167),
    "maroon3": Color.from_rgb(205, 41, 144),
    "maroon4": Color.from_rgb(139, 28, 98),
    "medium-aquamarine": Color.from_rgb(102, 205, 170),
    "medium-blue": Color.from_rgb(0, 0, 205),
    "medium-orchid": Color.from_rgb(186, 85, 211),
    "medium-orchid1": Color.from_rgb(224, 102, 255),
    "medium-orchid2": Color.from_rgb(209, 95, 238),
    "medium-orchid3": Color.from_rgb(180, 82, 205),
    "medium-orchid4": Color.from_rgb(122, 55, 139),
    "medium-purple": Color.from_rgb(147, 112, 219),
    "medium-purple1": Color.from_rgb(171, 130, 255),
    "medium-purple2": Color.from_rgb(159, 121, 238),
    "medium-purple3": Color.from_rgb(137, 104, 205),
    "medium-purple4": Color.from_rgb(93, 71, 139),
    "medium-sea-green": Color.from_rgb(60, 179, 113),
    "medium-slate-blue": Color.from_rgb(123, 104, 238),
    "medium-spring-green": Color.from_rgb(0, 250, 154),
    "medium-turquoise": Color.from_rgb(72, 209, 204),
    "medium-violet-red": Color.from_rgb(199, 21, 133),
    "midnight-blue": Color.from_rgb(25, 25, 112),
    "mint-cream": Color.from_rgb(245, 255, 250),
    "misty-rose": Color.from_rgb(255, 228, 225),
    "misty-rose1": Color.from_rgb(255, 228, 225),
    "misty-rose2": Color.from_rgb(238, 213, 210),
    "misty-rose3": Color.from_rgb(205, 183, 181),
    "misty-rose4": Color.from_rgb(139, 125, 123),
    "moccasin": Color.from_rgb(255, 228, 181),
    "navajo-white": Color.from_rgb(255, 222, 173),
    "navajo-white1": Color.from_rgb(255, 222, 173),
    "navajo-white2": Color.from_rgb(238, 207, 161),
    "navajo-white3": Color.from_rgb(205, 179, 139),
    "navajo-white4": Color.from_rgb(139, 121, 94),
    "navy": Color.from_rgb(0, 0, 128),
    "navy-blue": Color.from_rgb(0, 0, 128),
    "old-lace": Color.from_rgb(253, 245, 230),
    "olive": Color.from_rgb(128, 128, 0),
    "olive-drab": Color.from_rgb(107, 142, 35),
    "olive-drab1": Color.from_rgb(192, 255, 62),
    "olive-drab2": Color.from_rgb(179, 238, 58),
    "olive-drab3": Color.from_rgb(154, 205, 50),
    "olive-drab4": Color.from_rgb(105, 139, 34),
    "orange": Color.from_rgb(255, 165, 0),
    "orange1": Color.from_rgb(255, 165, 0),
    "orange2": Color.from_rgb(238, 154, 0),
    "orange3": Color.from_rgb(205, 133, 0),
    "orange4": Color.from_rgb(139, 90, 0),
    "orange-red": Color.from_rgb(255, 69, 0),
    "orange-red1": Color.from_rgb(255, 69, 0),
    "orange-red2": Color.from_rgb(238, 64, 0),
    "orange-red3": Color.from_rgb(205, 55, 0),
    "orange-red4": Color.from_rgb(139, 37, 0),
    "orchid": Color.from_rgb(218, 112, 214),
    "orchid1": Color.from_rgb(255, 131, 250),
    "orchid2": Color.from_rgb(238, 122, 233),
    "orchid3": Color.from_rgb(205, 105, 201),
    "orchid4": Color.from_rgb(139, 71, 137),
    "pale-green": Color.from_rgb(152, 251, 152),
    "pale-green1": Color.from_rgb(154, 255, 154),
    "pale-green2": Color.from_rgb(144, 238, 144),
    "pale-green3": Color.from_rgb(124, 205, 124),
    "pale-green4": Color.from_rgb(84, 139, 84),
    "pale-goldenrod": Color.from_rgb(238, 232, 170),
    "pale-turquoise": Color.from_rgb(175, 238, 238),
    "pale-turquoise1": Color.from_rgb(187, 255, 255),
    "pale-turquoise2": Color.from_rgb(174, 238, 238),
    "pale-turquoise3": Color.from_rgb(150, 205, 205),
    "pale-turquoise4": Color.from_rgb(102, 139, 139),
    "pale-violet-red": Color.from_rgb(219, 112, 147),
    "pale-violet-red1": Color.from_rgb(255, 130, 171),
    "pale-violet-red2": Color.from_rgb(238, 121, 159),
    "pale-violet-red3": Color.from_rgb(205, 104, 137),
    "pale-violet-red4": Color.from_rgb(139, 71, 93),
    "papaya-whip": Color.from_rgb(255, 239, 213),
    "peach-puff": Color.from_rgb(255, 218, 185),
    "peach-puff1": Color.from_rgb(255, 218, 185),
    "peach-puff2": Color.from_rgb(238, 203, 173),
    "peach-puff3": Color.from_rgb(205, 175, 149),
    "peach-puff4": Color.from_rgb(139, 119, 101),
    "peru": Color.from_rgb(205, 133, 63),
    "pink": Color.from_rgb(255, 192, 203),
    "pink1": Color.from_rgb(255, 181, 197),
    "pink2": Color.from_rgb(238, 169, 184),
    "pink3": Color.from_rgb(205, 145, 158),
    "pink4": Color.from_rgb(139, 99, 108),
    "plum": Color.from_rgb(221, 160, 221),
    "plum1": Color.from_rgb(255, 187, 255),
    "plum2": Color.from_rgb(238, 174, 238),
    "plum3": Color.from_rgb(205, 150, 205),
    "plum4": Color.from_rgb(139, 102, 139),
    "powder-blue": Color.from_rgb(176, 224, 230),
    "purple": Color.from_rgb(160, 32, 240),
    "purple1": Color.from_rgb(155, 48, 255),
    "purple2": Color.from_rgb(145, 44, 238),
    "purple3": Color.from_rgb(125, 38, 205),
    "purple4": Color.from_rgb(85, 26, 139),
    "red": Color.from_rgb(255, 0, 0),
    "red1": Color.from_rgb(255, 0, 0),
    "red2": Color.from_rgb(238, 0, 0),
    "red3": Color.from_rgb(205, 0, 0),
    "red4": Color.from_rgb(139, 0, 0),
    "rosy-brown": Color.from_rgb(188, 143, 143),
    "rosy-brown1": Color.from_rgb(255, 193, 193),
    "rosy-brown2": Color.from_rgb(238, 180, 180),
    "rosy-brown3": Color.from_rgb(205, 155, 155),
    "rosy-brown4": Color.from_rgb(139, 105, 105),
    "royal-blue": Color.from_rgb(65, 105, 225),
    "royal-blue1": Color.from_rgb(72, 118, 255),
    "royal-blue2": Color.from_rgb(67, 110, 238),
    "royal-blue3": Color.from_rgb(58, 95, 205),
    "royal-blue4": Color.from_rgb(39, 64, 139),
    "salmon": Color.from_rgb(250, 128, 114),
    "salmon1": Color.from_rgb(255, 140, 105),
    "salmon2": Color.from_rgb(238, 130, 98),
    "salmon3": Color.from_rgb(205, 112, 84),
    "salmon4": Color.from_rgb(139, 76, 57),
    "saddle-brown": Color.from_rgb(139, 69, 19),
    "sandy-brown": Color.from_rgb(244, 164, 96),
    "sea-green": Color.from_rgb(46, 139, 87),
    "sea-green1": Color.from_rgb(84, 255, 159),
    "sea-green2": Color.from_rgb(78, 238, 148),
    "sea-green3": Color.from_rgb(67, 205, 128),
    "sea-green4": Color.from_rgb(46, 139, 87),
    "seashell": Color.from_rgb(255, 245, 238),
    "seashell1": Color.from_rgb(255, 245, 238),
    "seashell2": Color.from_rgb(238, 229, 222),
    "seashell3": Color.from_rgb(205, 197, 191),
    "seashell4": Color.from_rgb(139, 134, 130),
    "sienna": Color.from_rgb(160, 82, 45),
    "sienna1": Color.from_rgb(255, 130, 71),
    "sienna2": Color.from_rgb(238, 121, 66),
    "sienna3": Color.from_rgb(205, 104, 57),
    "sienna4": Color.from_rgb(139, 71, 38),
    "silver": Color.from_rgb(192, 192, 192),
    "sky-blue": Color.from_rgb(135, 206, 235),
    "sky-blue1": Color.from_rgb(135, 206, 255),
    "sky-blue2": Color.from_rgb(126, 192, 238),
    "sky-blue3": Color.from_rgb(108, 166, 205),
    "sky-blue4": Color.from_rgb(74, 112, 139),
    "slate-blue": Color.from_rgb(106, 90, 205),
    "slate-blue1": Color.from_rgb(131, 111, 255),
    "slate-blue2": Color.from_rgb(122, 103, 238),
    "slate-blue3": Color.from_rgb(105, 89, 205),
    "slate-blue4": Color.from_rgb(71, 60, 139),
    "slate-gray": Color.from_rgb(112, 128, 144),
    "slate-gray1": Color.from_rgb(198, 226, 255),
    "slate-gray2": Color.from_rgb(185, 211, 238),
    "slate-gray3": Color.from_rgb(159, 182, 205),
    "slate-gray4": Color.from_rgb(108, 123, 139),
    "slate-grey": Color.from_rgb(112, 128, 144),
    "snow": Color.from_rgb(255, 250, 250),
    "snow1": Color.from_rgb(255, 250, 250),
    "snow2": Color.from_rgb(238, 233, 233),
    "snow3": Color.from_rgb(205, 201, 201),
    "snow4": Color.from_rgb(139, 137, 137),
    "spring-green": Color.from_rgb(0, 255, 127),
    "spring-green1": Color.from_rgb(0, 255, 127),
    "spring-green2": Color.from_rgb(0, 238, 118),
    "spring-green3": Color.from_rgb(0, 205, 102),
    "spring-green4": Color.from_rgb(0, 139, 69),
    "steel-blue": Color.from_rgb(70, 130, 180),
    "steel-blue1": Color.from_rgb(99, 184, 255),
    "steel-blue2": Color.from_rgb(92, 172, 238),
    "steel-blue3": Color.from_rgb(79, 148, 205),
    "steel-blue4": Color.from_rgb(54, 100, 139),
    "tan": Color.from_rgb(210, 180, 140),
    "tan1": Color.from_rgb(255, 165, 79),
    "tan2": Color.from_rgb(238, 154, 73),
    "tan3": Color.from_rgb(205, 133, 63),
    "tan4": Color.from_rgb(139, 90, 43),
    "teal": Color.from_rgb(0, 128, 128),
    "thistle": Color.from_rgb(216, 191, 216),
    "thistle1": Color.from_rgb(255, 225, 255),
    "thistle2": Color.from_rgb(238, 210, 238),
    "thistle3": Color.from_rgb(205, 181, 205),
    "thistle4": Color.from_rgb(139, 123, 139),
    "tomato": Color.from_rgb(255, 99, 71),
    "tomato1": Color.from_rgb(255, 99, 71),
    "tomato2": Color.from_rgb(238, 92, 66),
    "tomato3": Color.from_rgb(205, 79, 57),
    "tomato4": Color.from_rgb(139, 54, 38),
    "turquoise": Color.from_rgb(64, 224, 208),
    "turquoise1": Color.from_rgb(0, 245, 255),
    "turquoise2": Color.from_rgb(0, 229, 238),
    "turquoise3": Color.from_rgb(0, 197, 205),
    "turquoise4": Color.from_rgb(0, 134, 139),
    "violet": Color.from_rgb(238, 130, 238),
    "violet-red": Color.from_rgb(208, 32, 144),
    "violet-red1": Color.from_rgb(255, 62, 150),
    "violet-red2": Color.from_rgb(238, 58, 140),
    "violet-red3": Color.from_rgb(205, 50, 120),
    "violet-red4": Color.from_rgb(139, 34, 82),
    "wheat": Color.from_rgb(245, 222, 179),
    "wheat1": Color.from_rgb(255, 231, 186),
    "wheat2": Color.from_rgb(238, 216, 174),
    "wheat3": Color.from_rgb(205, 186, 150),
    "wheat4": Color.from_rgb(139, 126, 102),
    "white": Color.from_rgb(255, 255, 255),
    "white-smoke": Color.from_rgb(245, 245, 245),
    "yellow": Color.from_rgb(255, 255, 0),
    "yellow1": Color.from_rgb(255, 255, 0),
    "yellow2": Color.from_rgb(238, 238, 0),
    "yellow3": Color.from_rgb(205, 205, 0),
    "yellow4": Color.from_rgb(139, 139, 0),
    "yellow-green": Color.from_rgb(154, 205, 50),
}
_PRE_DEFINED_COLORS = dict(sorted(_PRE_DEFINED_COLORS.items()))

BytesLike: TypeAlias = bytes | bytearray | memoryview
ColorLike: TypeAlias = Color | str | BytesLike | int | Sequence[float]


def get_clipboard() -> str:
    return pyperclip.paste()


def set_clipboard(text: str) -> None:
    pyperclip.copy(text)
