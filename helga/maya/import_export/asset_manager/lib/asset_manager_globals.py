
"""
asset_manager_globals
==========================================

Module that has asset manager tool globals
"""








#Add tool relative pathes
#------------------------------------------------------------------

#import
import sys
import os

#tool_root_path
tool_root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(tool_root_path)

#media_path
media_path = os.path.join(tool_root_path, 'media')
sys.path.append(media_path)

#icons_path
icons_path = os.path.join(media_path, 'icons')
sys.path.append(icons_path)







#Import
#------------------------------------------------------------------

#PySide
from PySide import QtGui
from PySide import QtCore







#Globals
#------------------------------------------------------------------

#AssetManager Sizes
STACKEDWIDGET_DIVIDER_HEIGHT = 3

#AssetManager colors
BRIGHT_ORANGE = QtGui.QColor('#f9661e')
DARK_ORANGE = QtGui.QColor('#b13b00')
BRIGHT_GREY = QtGui.QColor('#dbdce0')
GREY = QtGui.QColor('#1f1f1f')
DARK_GREY = QtGui.QColor('#131313')

#AssetManager Icons
ICON_EXPORT = os.path.join(icons_path, 'icn_export.png').replace('\\', '/')
ICON_CHAR = os.path.join(icons_path, 'icn_char.png').replace('\\', '/')
ICON_PROP = os.path.join(icons_path, 'icn_prop.png').replace('\\', '/')
ICON_SHOT = os.path.join(icons_path, 'icn_shot.png').replace('\\', '/')
ICON_UPDATE = os.path.join(icons_path, 'icn_update.png').replace('\\', '/')
ICON_DOCS = os.path.join(icons_path, 'icn_docs.png').replace('\\', '/')

ICON_EXPORT_HOVER = os.path.join(icons_path, 'icn_export_hover.png').replace('\\', '/')
ICON_CHAR_HOVER = os.path.join(icons_path, 'icn_char_hover.png').replace('\\', '/')
ICON_PROP_HOVER = os.path.join(icons_path, 'icn_prop_hover.png').replace('\\', '/')
ICON_SHOT_HOVER = os.path.join(icons_path, 'icn_shot_hover.png').replace('\\', '/')
ICON_UPDATE_HOVER = os.path.join(icons_path, 'icn_update_hover.png').replace('\\', '/')
ICON_DOCS_HOVER = os.path.join(icons_path, 'icn_docs_hover.png').replace('\\', '/')


