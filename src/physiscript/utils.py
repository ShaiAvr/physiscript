from __future__ import annotations
from collections.abc import Sequence
from typing import final, ClassVar, TypeAlias

import pyperclip

__all__ = ["Color", "ColorLike", "get_clipboard", "set_clipboard"]


@final
class Color:
    __slots__ = ("_r", "_g", "_b", "_a")

    _r: float
    _g: float
    _b: float
    _a: float

    # Taken from
    # https://github.com/pygame-community/pygame-ce/blob/main/src_py/colordict.py
    _PRE_DEFINED_COLORS: ClassVar[dict[str, tuple[int, int, int, int]]] = {
        "alice-blue": (240, 248, 255, 255),
        "antique-white": (250, 235, 215, 255),
        "antique-white1": (255, 239, 219, 255),
        "antique-white2": (238, 223, 204, 255),
        "antique-white3": (205, 192, 176, 255),
        "antique-white4": (139, 131, 120, 255),
        "aqua": (0, 255, 255, 255),
        "aquamarine": (127, 255, 212, 255),
        "aquamarine1": (127, 255, 212, 255),
        "aquamarine2": (118, 238, 198, 255),
        "aquamarine3": (102, 205, 170, 255),
        "aquamarine4": (69, 139, 116, 255),
        "azure": (240, 255, 255, 255),
        "azure1": (240, 255, 255, 255),
        "azure3": (193, 205, 205, 255),
        "azure2": (224, 238, 238, 255),
        "azure4": (131, 139, 139, 255),
        "beige": (245, 245, 220, 255),
        "bisque": (255, 228, 196, 255),
        "bisque1": (255, 228, 196, 255),
        "bisque2": (238, 213, 183, 255),
        "bisque3": (205, 183, 158, 255),
        "bisque4": (139, 125, 107, 255),
        "black": (0, 0, 0, 255),
        "blanched-almond": (255, 235, 205, 255),
        "blue": (0, 0, 255, 255),
        "blue1": (0, 0, 255, 255),
        "blue2": (0, 0, 238, 255),
        "blue3": (0, 0, 205, 255),
        "blue4": (0, 0, 139, 255),
        "blue-violet": (138, 43, 226, 255),
        "brown": (165, 42, 42, 255),
        "brown1": (255, 64, 64, 255),
        "brown2": (238, 59, 59, 255),
        "brown3": (205, 51, 51, 255),
        "brown4": (139, 35, 35, 255),
        "burly-wood": (222, 184, 135, 255),
        "burly-wood1": (255, 211, 155, 255),
        "burly-wood2": (238, 197, 145, 255),
        "burly-wood3": (205, 170, 125, 255),
        "burly-wood4": (139, 115, 85, 255),
        "cadet-blue": (95, 158, 160, 255),
        "cadet-blue1": (152, 245, 255, 255),
        "cadet-blue2": (142, 229, 238, 255),
        "cadet-blue3": (122, 197, 205, 255),
        "cadet-blue4": (83, 134, 139, 255),
        "chartreuse": (127, 255, 0, 255),
        "chartreuse1": (127, 255, 0, 255),
        "chartreuse2": (118, 238, 0, 255),
        "chartreuse3": (102, 205, 0, 255),
        "chartreuse4": (69, 139, 0, 255),
        "chocolate": (210, 105, 30, 255),
        "chocolate1": (255, 127, 36, 255),
        "chocolate2": (238, 118, 33, 255),
        "chocolate3": (205, 102, 29, 255),
        "chocolate4": (139, 69, 19, 255),
        "coral": (255, 127, 80, 255),
        "coral1": (255, 114, 86, 255),
        "coral2": (238, 106, 80, 255),
        "coral3": (205, 91, 69, 255),
        "coral4": (139, 62, 47, 255),
        "corn-flower-blue": (100, 149, 237, 255),
        "corn-silk": (255, 248, 220, 255),
        "corn-silk1": (255, 248, 220, 255),
        "corn-silk2": (238, 232, 205, 255),
        "corn-silk3": (205, 200, 177, 255),
        "corn-silk4": (139, 136, 120, 255),
        "crimson": (220, 20, 60, 255),
        "cyan": (0, 255, 255, 255),
        "cyan1": (0, 255, 255, 255),
        "cyan2": (0, 238, 238, 255),
        "cyan3": (0, 205, 205, 255),
        "cyan4": (0, 139, 139, 255),
        "dark-blue": (0, 0, 139, 255),
        "dark-cyan": (0, 139, 139, 255),
        "dark-goldenrod": (184, 134, 11, 255),
        "dark-goldenrod1": (255, 185, 15, 255),
        "dark-goldenrod2": (238, 173, 14, 255),
        "dark-goldenrod3": (205, 149, 12, 255),
        "dark-goldenrod4": (139, 101, 8, 255),
        "dark-gray": (169, 169, 169, 255),
        "dark-green": (0, 100, 0, 255),
        "dark-grey": (169, 169, 169, 255),
        "dark-khaki": (189, 183, 107, 255),
        "dark-magenta": (139, 0, 139, 255),
        "dark-olive-green": (85, 107, 47, 255),
        "dark-olive-green1": (202, 255, 112, 255),
        "dark-olive-green2": (188, 238, 104, 255),
        "dark-olive-green3": (162, 205, 90, 255),
        "dark-olive-green4": (110, 139, 61, 255),
        "dark-orange": (255, 140, 0, 255),
        "dark-orange1": (255, 127, 0, 255),
        "dark-orange2": (238, 118, 0, 255),
        "dark-orange3": (205, 102, 0, 255),
        "dark-orange4": (139, 69, 0, 255),
        "dark-orchid": (153, 50, 204, 255),
        "dark-orchid1": (191, 62, 255, 255),
        "dark-orchid2": (178, 58, 238, 255),
        "dark-orchid3": (154, 50, 205, 255),
        "dark-orchid4": (104, 34, 139, 255),
        "dark-red": (139, 0, 0, 255),
        "dark-salmon": (233, 150, 122, 255),
        "dark-sea-green": (143, 188, 143, 255),
        "dark-sea-green1": (193, 255, 193, 255),
        "dark-sea-green2": (180, 238, 180, 255),
        "dark-sea-green3": (155, 205, 155, 255),
        "dark-sea-green4": (105, 139, 105, 255),
        "dark-slate-blue": (72, 61, 139, 255),
        "dark-slate-gray": (47, 79, 79, 255),
        "dark-slate-gray1": (151, 255, 255, 255),
        "dark-slate-gray2": (141, 238, 238, 255),
        "dark-slate-gray3": (121, 205, 205, 255),
        "dark-slate-gray4": (82, 139, 139, 255),
        "dark-slate-grey": (47, 79, 79, 255),
        "dark-turquoise": (0, 206, 209, 255),
        "dark-violet": (148, 0, 211, 255),
        "deep-pink": (255, 20, 147, 255),
        "deep-pink1": (255, 20, 147, 255),
        "deep-pink2": (238, 18, 137, 255),
        "deep-pink3": (205, 16, 118, 255),
        "deep-pink4": (139, 10, 80, 255),
        "deep-sky-blue": (0, 191, 255, 255),
        "deep-sky-blue1": (0, 191, 255, 255),
        "deep-sky-blue2": (0, 178, 238, 255),
        "deep-sky-blue3": (0, 154, 205, 255),
        "deep-sky-blue4": (0, 104, 139, 255),
        "dim-gray": (105, 105, 105, 255),
        "dim-grey": (105, 105, 105, 255),
        "dodger-blue": (30, 144, 255, 255),
        "dodger-blue1": (30, 144, 255, 255),
        "dodger-blue2": (28, 134, 238, 255),
        "dodger-blue3": (24, 116, 205, 255),
        "dodger-blue4": (16, 78, 139, 255),
        "firebrick": (178, 34, 34, 255),
        "firebrick1": (255, 48, 48, 255),
        "firebrick2": (238, 44, 44, 255),
        "firebrick3": (205, 38, 38, 255),
        "firebrick4": (139, 26, 26, 255),
        "floral-white": (255, 250, 240, 255),
        "forest-green": (34, 139, 34, 255),
        "fuchsia": (255, 0, 255, 255),
        "gainsboro": (220, 220, 220, 255),
        "ghost-white": (248, 248, 255, 255),
        "gold": (255, 215, 0, 255),
        "gold1": (255, 215, 0, 255),
        "gold2": (238, 201, 0, 255),
        "gold3": (205, 173, 0, 255),
        "gold4": (139, 117, 0, 255),
        "goldenrod": (218, 165, 32, 255),
        "goldenrod1": (255, 193, 37, 255),
        "goldenrod2": (238, 180, 34, 255),
        "goldenrod3": (205, 155, 29, 255),
        "goldenrod4": (139, 105, 20, 255),
        "gray": (190, 190, 190, 255),
        "gray0": (0, 0, 0, 255),
        "gray1": (3, 3, 3, 255),
        "gray2": (5, 5, 5, 255),
        "gray3": (8, 8, 8, 255),
        "gray4": (10, 10, 10, 255),
        "gray5": (13, 13, 13, 255),
        "gray6": (15, 15, 15, 255),
        "gray7": (18, 18, 18, 255),
        "gray8": (20, 20, 20, 255),
        "gray9": (23, 23, 23, 255),
        "gray10": (26, 26, 26, 255),
        "gray11": (28, 28, 28, 255),
        "gray12": (31, 31, 31, 255),
        "gray13": (33, 33, 33, 255),
        "gray14": (36, 36, 36, 255),
        "gray15": (38, 38, 38, 255),
        "gray16": (41, 41, 41, 255),
        "gray17": (43, 43, 43, 255),
        "gray18": (46, 46, 46, 255),
        "gray19": (48, 48, 48, 255),
        "gray20": (51, 51, 51, 255),
        "gray21": (54, 54, 54, 255),
        "gray22": (56, 56, 56, 255),
        "gray23": (59, 59, 59, 255),
        "gray24": (61, 61, 61, 255),
        "gray25": (64, 64, 64, 255),
        "gray26": (66, 66, 66, 255),
        "gray27": (69, 69, 69, 255),
        "gray28": (71, 71, 71, 255),
        "gray29": (74, 74, 74, 255),
        "gray30": (77, 77, 77, 255),
        "gray31": (79, 79, 79, 255),
        "gray32": (82, 82, 82, 255),
        "gray33": (84, 84, 84, 255),
        "gray34": (87, 87, 87, 255),
        "gray35": (89, 89, 89, 255),
        "gray36": (92, 92, 92, 255),
        "gray37": (94, 94, 94, 255),
        "gray38": (97, 97, 97, 255),
        "gray39": (99, 99, 99, 255),
        "gray40": (102, 102, 102, 255),
        "gray41": (105, 105, 105, 255),
        "gray42": (107, 107, 107, 255),
        "gray43": (110, 110, 110, 255),
        "gray44": (112, 112, 112, 255),
        "gray45": (115, 115, 115, 255),
        "gray46": (117, 117, 117, 255),
        "gray47": (120, 120, 120, 255),
        "gray48": (122, 122, 122, 255),
        "gray49": (125, 125, 125, 255),
        "gray50": (127, 127, 127, 255),
        "gray51": (130, 130, 130, 255),
        "gray52": (133, 133, 133, 255),
        "gray53": (135, 135, 135, 255),
        "gray54": (138, 138, 138, 255),
        "gray55": (140, 140, 140, 255),
        "gray56": (143, 143, 143, 255),
        "gray57": (145, 145, 145, 255),
        "gray58": (148, 148, 148, 255),
        "gray59": (150, 150, 150, 255),
        "gray60": (153, 153, 153, 255),
        "gray61": (156, 156, 156, 255),
        "gray62": (158, 158, 158, 255),
        "gray63": (161, 161, 161, 255),
        "gray64": (163, 163, 163, 255),
        "gray65": (166, 166, 166, 255),
        "gray66": (168, 168, 168, 255),
        "gray67": (171, 171, 171, 255),
        "gray68": (173, 173, 173, 255),
        "gray69": (176, 176, 176, 255),
        "gray70": (179, 179, 179, 255),
        "gray71": (181, 181, 181, 255),
        "gray72": (184, 184, 184, 255),
        "gray73": (186, 186, 186, 255),
        "gray74": (189, 189, 189, 255),
        "gray75": (191, 191, 191, 255),
        "gray76": (194, 194, 194, 255),
        "gray77": (196, 196, 196, 255),
        "gray78": (199, 199, 199, 255),
        "gray79": (201, 201, 201, 255),
        "gray80": (204, 204, 204, 255),
        "gray81": (207, 207, 207, 255),
        "gray82": (209, 209, 209, 255),
        "gray83": (212, 212, 212, 255),
        "gray84": (214, 214, 214, 255),
        "gray85": (217, 217, 217, 255),
        "gray86": (219, 219, 219, 255),
        "gray87": (222, 222, 222, 255),
        "gray88": (224, 224, 224, 255),
        "gray89": (227, 227, 227, 255),
        "gray90": (229, 229, 229, 255),
        "gray91": (232, 232, 232, 255),
        "gray92": (235, 235, 235, 255),
        "gray93": (237, 237, 237, 255),
        "gray94": (240, 240, 240, 255),
        "gray95": (242, 242, 242, 255),
        "gray96": (245, 245, 245, 255),
        "gray97": (247, 247, 247, 255),
        "gray98": (250, 250, 250, 255),
        "gray99": (252, 252, 252, 255),
        "gray100": (255, 255, 255, 255),
        "green": (0, 255, 0, 255),
        "green1": (0, 255, 0, 255),
        "green2": (0, 238, 0, 255),
        "green3": (0, 205, 0, 255),
        "green4": (0, 139, 0, 255),
        "green-yellow": (173, 255, 47, 255),
        "grey": (190, 190, 190, 255),
        "grey0": (0, 0, 0, 255),
        "grey1": (3, 3, 3, 255),
        "grey2": (5, 5, 5, 255),
        "grey3": (8, 8, 8, 255),
        "grey4": (10, 10, 10, 255),
        "grey5": (13, 13, 13, 255),
        "grey6": (15, 15, 15, 255),
        "grey7": (18, 18, 18, 255),
        "grey8": (20, 20, 20, 255),
        "grey9": (23, 23, 23, 255),
        "grey10": (26, 26, 26, 255),
        "grey11": (28, 28, 28, 255),
        "grey12": (31, 31, 31, 255),
        "grey13": (33, 33, 33, 255),
        "grey14": (36, 36, 36, 255),
        "grey15": (38, 38, 38, 255),
        "grey16": (41, 41, 41, 255),
        "grey17": (43, 43, 43, 255),
        "grey18": (46, 46, 46, 255),
        "grey19": (48, 48, 48, 255),
        "grey20": (51, 51, 51, 255),
        "grey21": (54, 54, 54, 255),
        "grey22": (56, 56, 56, 255),
        "grey23": (59, 59, 59, 255),
        "grey24": (61, 61, 61, 255),
        "grey25": (64, 64, 64, 255),
        "grey26": (66, 66, 66, 255),
        "grey27": (69, 69, 69, 255),
        "grey28": (71, 71, 71, 255),
        "grey29": (74, 74, 74, 255),
        "grey30": (77, 77, 77, 255),
        "grey31": (79, 79, 79, 255),
        "grey32": (82, 82, 82, 255),
        "grey33": (84, 84, 84, 255),
        "grey34": (87, 87, 87, 255),
        "grey35": (89, 89, 89, 255),
        "grey36": (92, 92, 92, 255),
        "grey37": (94, 94, 94, 255),
        "grey38": (97, 97, 97, 255),
        "grey39": (99, 99, 99, 255),
        "grey40": (102, 102, 102, 255),
        "grey41": (105, 105, 105, 255),
        "grey42": (107, 107, 107, 255),
        "grey43": (110, 110, 110, 255),
        "grey44": (112, 112, 112, 255),
        "grey45": (115, 115, 115, 255),
        "grey46": (117, 117, 117, 255),
        "grey47": (120, 120, 120, 255),
        "grey48": (122, 122, 122, 255),
        "grey49": (125, 125, 125, 255),
        "grey50": (127, 127, 127, 255),
        "grey51": (130, 130, 130, 255),
        "grey52": (133, 133, 133, 255),
        "grey53": (135, 135, 135, 255),
        "grey54": (138, 138, 138, 255),
        "grey55": (140, 140, 140, 255),
        "grey56": (143, 143, 143, 255),
        "grey57": (145, 145, 145, 255),
        "grey58": (148, 148, 148, 255),
        "grey59": (150, 150, 150, 255),
        "grey60": (153, 153, 153, 255),
        "grey61": (156, 156, 156, 255),
        "grey62": (158, 158, 158, 255),
        "grey63": (161, 161, 161, 255),
        "grey64": (163, 163, 163, 255),
        "grey65": (166, 166, 166, 255),
        "grey66": (168, 168, 168, 255),
        "grey67": (171, 171, 171, 255),
        "grey68": (173, 173, 173, 255),
        "grey69": (176, 176, 176, 255),
        "grey70": (179, 179, 179, 255),
        "grey71": (181, 181, 181, 255),
        "grey72": (184, 184, 184, 255),
        "grey73": (186, 186, 186, 255),
        "grey74": (189, 189, 189, 255),
        "grey75": (191, 191, 191, 255),
        "grey76": (194, 194, 194, 255),
        "grey77": (196, 196, 196, 255),
        "grey78": (199, 199, 199, 255),
        "grey79": (201, 201, 201, 255),
        "grey80": (204, 204, 204, 255),
        "grey81": (207, 207, 207, 255),
        "grey82": (209, 209, 209, 255),
        "grey83": (212, 212, 212, 255),
        "grey84": (214, 214, 214, 255),
        "grey85": (217, 217, 217, 255),
        "grey86": (219, 219, 219, 255),
        "grey87": (222, 222, 222, 255),
        "grey88": (224, 224, 224, 255),
        "grey89": (227, 227, 227, 255),
        "grey90": (229, 229, 229, 255),
        "grey91": (232, 232, 232, 255),
        "grey92": (235, 235, 235, 255),
        "grey93": (237, 237, 237, 255),
        "grey94": (240, 240, 240, 255),
        "grey95": (242, 242, 242, 255),
        "grey96": (245, 245, 245, 255),
        "grey97": (247, 247, 247, 255),
        "grey98": (250, 250, 250, 255),
        "grey99": (252, 252, 252, 255),
        "grey100": (255, 255, 255, 255),
        "honeydew": (240, 255, 240, 255),
        "honeydew1": (240, 255, 240, 255),
        "honeydew2": (224, 238, 224, 255),
        "honeydew3": (193, 205, 193, 255),
        "honeydew4": (131, 139, 131, 255),
        "hot-pink": (255, 105, 180, 255),
        "hot-pink1": (255, 110, 180, 255),
        "hot-pink2": (238, 106, 167, 255),
        "hot-pink3": (205, 96, 144, 255),
        "hot-pink4": (139, 58, 98, 255),
        "indian-red": (205, 92, 92, 255),
        "indian-red1": (255, 106, 106, 255),
        "indian-red2": (238, 99, 99, 255),
        "indian-red3": (205, 85, 85, 255),
        "indian-red4": (139, 58, 58, 255),
        "indigo": (75, 0, 130, 255),
        "ivory": (255, 255, 240, 255),
        "ivory1": (255, 255, 240, 255),
        "ivory2": (238, 238, 224, 255),
        "ivory3": (205, 205, 193, 255),
        "ivory4": (139, 139, 131, 255),
        "khaki": (240, 230, 140, 255),
        "khaki1": (255, 246, 143, 255),
        "khaki2": (238, 230, 133, 255),
        "khaki3": (205, 198, 115, 255),
        "khaki4": (139, 134, 78, 255),
        "lavender": (230, 230, 250, 255),
        "lavender-blush": (255, 240, 245, 255),
        "lavender-blush1": (255, 240, 245, 255),
        "lavender-blush2": (238, 224, 229, 255),
        "lavender-blush3": (205, 193, 197, 255),
        "lavender-blush4": (139, 131, 134, 255),
        "lawn-green": (124, 252, 0, 255),
        "lemon-chiffon": (255, 250, 205, 255),
        "lemon-chiffon1": (255, 250, 205, 255),
        "lemon-chiffon2": (238, 233, 191, 255),
        "lemon-chiffon3": (205, 201, 165, 255),
        "lemon-chiffon4": (139, 137, 112, 255),
        "light-blue": (173, 216, 230, 255),
        "light-blue1": (191, 239, 255, 255),
        "light-blue2": (178, 223, 238, 255),
        "light-blue3": (154, 192, 205, 255),
        "light-blue4": (104, 131, 139, 255),
        "light-coral": (240, 128, 128, 255),
        "light-cyan": (224, 255, 255, 255),
        "light-cyan1": (224, 255, 255, 255),
        "light-cyan2": (209, 238, 238, 255),
        "light-cyan3": (180, 205, 205, 255),
        "light-cyan4": (122, 139, 139, 255),
        "light-goldenrod": (238, 221, 130, 255),
        "light-goldenrod1": (255, 236, 139, 255),
        "light-goldenrod2": (238, 220, 130, 255),
        "light-goldenrod3": (205, 190, 112, 255),
        "light-goldenrod4": (139, 129, 76, 255),
        "light-golden-rod-yellow": (250, 250, 210, 255),
        "light-gray": (211, 211, 211, 255),
        "light-green": (144, 238, 144, 255),
        "light-grey": (211, 211, 211, 255),
        "light-pink": (255, 182, 193, 255),
        "light-pink1": (255, 174, 185, 255),
        "light-pink2": (238, 162, 173, 255),
        "light-pink3": (205, 140, 149, 255),
        "light-pink4": (139, 95, 101, 255),
        "light-salmon": (255, 160, 122, 255),
        "light-salmon1": (255, 160, 122, 255),
        "light-salmon2": (238, 149, 114, 255),
        "light-salmon3": (205, 129, 98, 255),
        "light-salmon4": (139, 87, 66, 255),
        "light-sea-green": (32, 178, 170, 255),
        "light-sky-blue": (135, 206, 250, 255),
        "light-sky-blue1": (176, 226, 255, 255),
        "light-sky-blue2": (164, 211, 238, 255),
        "light-sky-blue3": (141, 182, 205, 255),
        "light-sky-blue4": (96, 123, 139, 255),
        "light-slate-blue": (132, 112, 255, 255),
        "light-slate-gray": (119, 136, 153, 255),
        "light-slate-grey": (119, 136, 153, 255),
        "light-steel-blue": (176, 196, 222, 255),
        "light-steel-blue1": (202, 225, 255, 255),
        "light-steel-blue2": (188, 210, 238, 255),
        "light-steel-blue3": (162, 181, 205, 255),
        "light-steel-blue4": (110, 123, 139, 255),
        "light-yellow": (255, 255, 224, 255),
        "light-yellow1": (255, 255, 224, 255),
        "light-yellow2": (238, 238, 209, 255),
        "light-yellow3": (205, 205, 180, 255),
        "light-yellow4": (139, 139, 122, 255),
        "linen": (250, 240, 230, 255),
        "lime": (0, 255, 0, 255),
        "lime-green": (50, 205, 50, 255),
        "magenta": (255, 0, 255, 255),
        "magenta1": (255, 0, 255, 255),
        "magenta2": (238, 0, 238, 255),
        "magenta3": (205, 0, 205, 255),
        "magenta4": (139, 0, 139, 255),
        "maroon": (176, 48, 96, 255),
        "maroon1": (255, 52, 179, 255),
        "maroon2": (238, 48, 167, 255),
        "maroon3": (205, 41, 144, 255),
        "maroon4": (139, 28, 98, 255),
        "medium-aquamarine": (102, 205, 170, 255),
        "medium-blue": (0, 0, 205, 255),
        "medium-orchid": (186, 85, 211, 255),
        "medium-orchid1": (224, 102, 255, 255),
        "medium-orchid2": (209, 95, 238, 255),
        "medium-orchid3": (180, 82, 205, 255),
        "medium-orchid4": (122, 55, 139, 255),
        "medium-purple": (147, 112, 219, 255),
        "medium-purple1": (171, 130, 255, 255),
        "medium-purple2": (159, 121, 238, 255),
        "medium-purple3": (137, 104, 205, 255),
        "medium-purple4": (93, 71, 139, 255),
        "medium-sea-green": (60, 179, 113, 255),
        "medium-slate-blue": (123, 104, 238, 255),
        "medium-spring-green": (0, 250, 154, 255),
        "medium-turquoise": (72, 209, 204, 255),
        "medium-violet-red": (199, 21, 133, 255),
        "midnight-blue": (25, 25, 112, 255),
        "mint-cream": (245, 255, 250, 255),
        "misty-rose": (255, 228, 225, 255),
        "misty-rose1": (255, 228, 225, 255),
        "misty-rose2": (238, 213, 210, 255),
        "misty-rose3": (205, 183, 181, 255),
        "misty-rose4": (139, 125, 123, 255),
        "moccasin": (255, 228, 181, 255),
        "navajo-white": (255, 222, 173, 255),
        "navajo-white1": (255, 222, 173, 255),
        "navajo-white2": (238, 207, 161, 255),
        "navajo-white3": (205, 179, 139, 255),
        "navajo-white4": (139, 121, 94, 255),
        "navy": (0, 0, 128, 255),
        "navy-blue": (0, 0, 128, 255),
        "old-lace": (253, 245, 230, 255),
        "olive": (128, 128, 0, 255),
        "olive-drab": (107, 142, 35, 255),
        "olive-drab1": (192, 255, 62, 255),
        "olive-drab2": (179, 238, 58, 255),
        "olive-drab3": (154, 205, 50, 255),
        "olive-drab4": (105, 139, 34, 255),
        "orange": (255, 165, 0, 255),
        "orange1": (255, 165, 0, 255),
        "orange2": (238, 154, 0, 255),
        "orange3": (205, 133, 0, 255),
        "orange4": (139, 90, 0, 255),
        "orange-red": (255, 69, 0, 255),
        "orange-red1": (255, 69, 0, 255),
        "orange-red2": (238, 64, 0, 255),
        "orange-red3": (205, 55, 0, 255),
        "orange-red4": (139, 37, 0, 255),
        "orchid": (218, 112, 214, 255),
        "orchid1": (255, 131, 250, 255),
        "orchid2": (238, 122, 233, 255),
        "orchid3": (205, 105, 201, 255),
        "orchid4": (139, 71, 137, 255),
        "pale-green": (152, 251, 152, 255),
        "pale-green1": (154, 255, 154, 255),
        "pale-green2": (144, 238, 144, 255),
        "pale-green3": (124, 205, 124, 255),
        "pale-green4": (84, 139, 84, 255),
        "pale-goldenrod": (238, 232, 170, 255),
        "pale-turquoise": (175, 238, 238, 255),
        "pale-turquoise1": (187, 255, 255, 255),
        "pale-turquoise2": (174, 238, 238, 255),
        "pale-turquoise3": (150, 205, 205, 255),
        "pale-turquoise4": (102, 139, 139, 255),
        "pale-violet-red": (219, 112, 147, 255),
        "pale-violet-red1": (255, 130, 171, 255),
        "pale-violet-red2": (238, 121, 159, 255),
        "pale-violet-red3": (205, 104, 137, 255),
        "pale-violet-red4": (139, 71, 93, 255),
        "papaya-whip": (255, 239, 213, 255),
        "peach-puff": (255, 218, 185, 255),
        "peach-puff1": (255, 218, 185, 255),
        "peach-puff2": (238, 203, 173, 255),
        "peach-puff3": (205, 175, 149, 255),
        "peach-puff4": (139, 119, 101, 255),
        "peru": (205, 133, 63, 255),
        "pink": (255, 192, 203, 255),
        "pink1": (255, 181, 197, 255),
        "pink2": (238, 169, 184, 255),
        "pink3": (205, 145, 158, 255),
        "pink4": (139, 99, 108, 255),
        "plum": (221, 160, 221, 255),
        "plum1": (255, 187, 255, 255),
        "plum2": (238, 174, 238, 255),
        "plum3": (205, 150, 205, 255),
        "plum4": (139, 102, 139, 255),
        "powder-blue": (176, 224, 230, 255),
        "purple": (160, 32, 240, 255),
        "purple1": (155, 48, 255, 255),
        "purple2": (145, 44, 238, 255),
        "purple3": (125, 38, 205, 255),
        "purple4": (85, 26, 139, 255),
        "red": (255, 0, 0, 255),
        "red1": (255, 0, 0, 255),
        "red2": (238, 0, 0, 255),
        "red3": (205, 0, 0, 255),
        "red4": (139, 0, 0, 255),
        "rosy-brown": (188, 143, 143, 255),
        "rosy-brown1": (255, 193, 193, 255),
        "rosy-brown2": (238, 180, 180, 255),
        "rosy-brown3": (205, 155, 155, 255),
        "rosy-brown4": (139, 105, 105, 255),
        "royal-blue": (65, 105, 225, 255),
        "royal-blue1": (72, 118, 255, 255),
        "royal-blue2": (67, 110, 238, 255),
        "royal-blue3": (58, 95, 205, 255),
        "royal-blue4": (39, 64, 139, 255),
        "salmon": (250, 128, 114, 255),
        "salmon1": (255, 140, 105, 255),
        "salmon2": (238, 130, 98, 255),
        "salmon3": (205, 112, 84, 255),
        "salmon4": (139, 76, 57, 255),
        "saddle-brown": (139, 69, 19, 255),
        "sandy-brown": (244, 164, 96, 255),
        "sea-green": (46, 139, 87, 255),
        "sea-green1": (84, 255, 159, 255),
        "sea-green2": (78, 238, 148, 255),
        "sea-green3": (67, 205, 128, 255),
        "sea-green4": (46, 139, 87, 255),
        "seashell": (255, 245, 238, 255),
        "seashell1": (255, 245, 238, 255),
        "seashell2": (238, 229, 222, 255),
        "seashell3": (205, 197, 191, 255),
        "seashell4": (139, 134, 130, 255),
        "sienna": (160, 82, 45, 255),
        "sienna1": (255, 130, 71, 255),
        "sienna2": (238, 121, 66, 255),
        "sienna3": (205, 104, 57, 255),
        "sienna4": (139, 71, 38, 255),
        "silver": (192, 192, 192, 255),
        "sky-blue": (135, 206, 235, 255),
        "sky-blue1": (135, 206, 255, 255),
        "sky-blue2": (126, 192, 238, 255),
        "sky-blue3": (108, 166, 205, 255),
        "sky-blue4": (74, 112, 139, 255),
        "slate-blue": (106, 90, 205, 255),
        "slate-blue1": (131, 111, 255, 255),
        "slate-blue2": (122, 103, 238, 255),
        "slate-blue3": (105, 89, 205, 255),
        "slate-blue4": (71, 60, 139, 255),
        "slate-gray": (112, 128, 144, 255),
        "slate-gray1": (198, 226, 255, 255),
        "slate-gray2": (185, 211, 238, 255),
        "slate-gray3": (159, 182, 205, 255),
        "slate-gray4": (108, 123, 139, 255),
        "slate-grey": (112, 128, 144, 255),
        "snow": (255, 250, 250, 255),
        "snow1": (255, 250, 250, 255),
        "snow2": (238, 233, 233, 255),
        "snow3": (205, 201, 201, 255),
        "snow4": (139, 137, 137, 255),
        "spring-green": (0, 255, 127, 255),
        "spring-green1": (0, 255, 127, 255),
        "spring-green2": (0, 238, 118, 255),
        "spring-green3": (0, 205, 102, 255),
        "spring-green4": (0, 139, 69, 255),
        "steel-blue": (70, 130, 180, 255),
        "steel-blue1": (99, 184, 255, 255),
        "steel-blue2": (92, 172, 238, 255),
        "steel-blue3": (79, 148, 205, 255),
        "steel-blue4": (54, 100, 139, 255),
        "tan": (210, 180, 140, 255),
        "tan1": (255, 165, 79, 255),
        "tan2": (238, 154, 73, 255),
        "tan3": (205, 133, 63, 255),
        "tan4": (139, 90, 43, 255),
        "teal": (0, 128, 128, 255),
        "thistle": (216, 191, 216, 255),
        "thistle1": (255, 225, 255, 255),
        "thistle2": (238, 210, 238, 255),
        "thistle3": (205, 181, 205, 255),
        "thistle4": (139, 123, 139, 255),
        "tomato": (255, 99, 71, 255),
        "tomato1": (255, 99, 71, 255),
        "tomato2": (238, 92, 66, 255),
        "tomato3": (205, 79, 57, 255),
        "tomato4": (139, 54, 38, 255),
        "turquoise": (64, 224, 208, 255),
        "turquoise1": (0, 245, 255, 255),
        "turquoise2": (0, 229, 238, 255),
        "turquoise3": (0, 197, 205, 255),
        "turquoise4": (0, 134, 139, 255),
        "violet": (238, 130, 238, 255),
        "violet-red": (208, 32, 144, 255),
        "violet-red1": (255, 62, 150, 255),
        "violet-red2": (238, 58, 140, 255),
        "violet-red3": (205, 50, 120, 255),
        "violet-red4": (139, 34, 82, 255),
        "wheat": (245, 222, 179, 255),
        "wheat1": (255, 231, 186, 255),
        "wheat2": (238, 216, 174, 255),
        "wheat3": (205, 186, 150, 255),
        "wheat4": (139, 126, 102, 255),
        "white": (255, 255, 255, 255),
        "white-smoke": (245, 245, 245, 255),
        "yellow": (255, 255, 0, 255),
        "yellow1": (255, 255, 0, 255),
        "yellow2": (238, 238, 0, 255),
        "yellow3": (205, 205, 0, 255),
        "yellow4": (139, 139, 0, 255),
        "yellow-green": (154, 205, 50, 255),
    }

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
            color = cls._PRE_DEFINED_COLORS.get(value)
            if color is not None:
                return cls.from_rgba(*color)
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
        raise ValueError(f"Can't create color from '{value}'")

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
        return self._r

    @property
    def green(self) -> float:
        return self._g

    @property
    def blue(self) -> float:
        return self._b

    @property
    def alpha(self) -> float:
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


BytesLike: TypeAlias = bytes | bytearray | memoryview
ColorLike: TypeAlias = Color | str | BytesLike | int | Sequence[float]


def get_clipboard() -> str:
    return pyperclip.paste()


def set_clipboard(text: str) -> None:
    pyperclip.copy(text)
