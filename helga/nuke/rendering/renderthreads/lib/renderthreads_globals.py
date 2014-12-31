
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


# Version
# ------------------------------------------------------------------
VERSION = 0.1


# Pathes
# ------------------------------------------------------------------
TOOL_ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
MEDIA_PATH = os.path.join(TOOL_ROOT_PATH, 'media')
ICONS_PATH = os.path.join(MEDIA_PATH, 'icons')
FONTS_PATH = os.path.join(MEDIA_PATH, 'fonts')
UI_PATH = os.path.join(MEDIA_PATH, 'ui')


# Fonts
# ------------------------------------------------------------------
# FONTS_LIST [(Font Name, Font File Name), (Font Name, Font File Name)...]
FONTS_LIST = [('Futura LT Light', 'futura-lt-light.ttf')]

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
BRIGHT_ORANGE = QtGui.QColor('# f9661e')
DARK_ORANGE = BRIGHT_ORANGE.darker(DARKENING_FACTOR)


# Icons
# ------------------------------------------------------------------
ICON_RENDERTHREADS = os.path.join(ICONS_PATH, 'icn_renderthreads.png').replace('\\', '/')


# Text
# ------------------------------------------------------------------
SHOT_METADATA_EXPLANATION_HEADER = 'Shot Metadata'
