import pytest

from physiscript.utils import Color


@pytest.mark.parametrize(
    ("created_color", "expected_color"),
    [
        (Color.create(Color(0.4, 0.5, 1)), Color(0.4, 0.5, 1)),
        (Color.create("red"), Color(1, 0, 0)),
        (Color.create("#3C54FF"), Color.from_rgb(0x3C, 0x54, 0xFF)),
        (Color.create("#EE98FE80"), Color.from_rgba(0xEE, 0x98, 0xFE, 0x80)),
        (Color.create("0x404040"), Color.from_rgb(0x40, 0x40, 0x40)),
        (Color.create("0x33225599"), Color.from_rgba(0x33, 0x22, 0x55, 0x99)),
        (Color.create(bytes([255, 255, 255])), Color(1, 1, 1)),
        (Color.create(bytearray([0, 128, 0, 200])), Color.from_rgba(0, 128, 0, 200)),
        (Color.create(0x4566FFFF), Color.from_rgba(0x45, 0x66, 0xFF, 0xFF)),
        (Color.create([0, 1, 0.5]), Color(0, 1, 0.5)),
    ],
)
def test_create(created_color: Color, expected_color: Color) -> None:
    assert created_color == expected_color
