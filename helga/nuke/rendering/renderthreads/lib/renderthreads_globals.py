
"""
renderthreads_globals
==========================================

Module that has renderthreads tool globals
"""


# Import
# ------------------------------------------------------------------
# import
import os
# PySide
from PySide import QtGui
from PySide import QtCore


# Version and Title
# ------------------------------------------------------------------
TITLE = 'renderthreads'
VERSION = 0.1


# Pathes
# ------------------------------------------------------------------
TOOL_ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
LIB_PATH = os.path.join(TOOL_ROOT_PATH, 'lib')
GUI_PATH = os.path.join(LIB_PATH, 'gui')
MVC_PATH = os.path.join(LIB_PATH, 'mvc')
THIRD_PARTY_PATH = os.path.join(LIB_PATH, 'third_party')

MEDIA_PATH = os.path.join(TOOL_ROOT_PATH, 'media')
ICONS_PATH = os.path.join(MEDIA_PATH, 'icons')
FONTS_PATH = os.path.join(MEDIA_PATH, 'fonts')
UI_PATH = os.path.join(MEDIA_PATH, 'ui')


# Fonts
# ------------------------------------------------------------------
# Sizes
FONT_SIZE_DEFAULT = 10
FONT_SIZE_LARGE = 14
FONT_SIZE_SMALL = 8
# Fonts
FUTURA_LT_LIGHT = ('Futura LT Light', 'futura-lt-light.ttf')

# FONTS_LIST [(Font Name, Font File Name), (Font Name, Font File Name)...]
FONTS_LIST = [FUTURA_LT_LIGHT]

# iterate and install if not installed
for font_name, font_file_name in FONTS_LIST:
    # font not installed
    if not (font_name in QtGui.QFontDatabase().families()):
        # current_font_path
        current_font_path = os.path.join(FONTS_PATH, font_file_name).replace('\\', '/')
        # add font
        QtGui.QFontDatabase.addApplicationFont(current_font_path)


# Colors
# ------------------------------------------------------------------
#darkening_factor
DARKENING_FACTOR = 120
#brightening_factor
BRIGHTENING_FACTOR = 150

BLACK = QtGui.QColor('#000000')
WHITE = QtGui.QColor('#f5f5f5')
GREY = QtGui.QColor('#484f57')
GREY_DARK = GREY.darker(DARKENING_FACTOR)
GREY_BRIGHT = GREY.lighter(DARKENING_FACTOR)
RED = QtGui.QColor('#fb3e2a')
RED_DARK = RED.darker(DARKENING_FACTOR)
RED_BRIGHT = RED.lighter(DARKENING_FACTOR)
BLUE = QtGui.QColor('#07faff')
BLUE_DARK = BLUE.darker(DARKENING_FACTOR)
BLUE_BRIGHT = BLUE.lighter(DARKENING_FACTOR)


# Images
# ------------------------------------------------------------------
HEADER_IMAGE = os.path.join(ICONS_PATH, 'icn_renderthreads.png').replace('\\', '/')  # Temp

ICON_RENDERTHREADS = os.path.join(ICONS_PATH, 'icn_renderthreads.png').replace('\\', '/')


# Text
# ------------------------------------------------------------------
SHOT_METADATA_EXPLANATION_HEADER = 'Shot Metadata'
