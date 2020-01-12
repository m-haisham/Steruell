from core import Color, colors


def DIM_LIGHT(button):
    button.mutate_color(button.color * 0.9)


def ORIGINAL_COLOR(button):
    button.mutate_color(button.original_color)


def DIM_TRANSPARENCY(button):
    button._mutable_color *= 0.9


def BLACK_TEXT_WHITE_BACKGROUND(button):
    button.mutate_color(Color(255, 255, 255, 255))
    button.text.color = colors.BLACK

def WHITE_TEXT_TRANSPARENT_BACKGROUND(button):
    button.mutate_color(colors.TRANSPARENT)
    button.text.color = colors.WHITE