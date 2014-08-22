
"""
asset_manager_globals
==========================================

Module that has asset manager tool globals
"""






#Import
#------------------------------------------------------------------
#import
import os
#PySide
from PySide import QtGui
from PySide import QtCore







#Globals
#------------------------------------------------------------------

#Pathes
TOOL_ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
MEDIA_PATH = os.path.join(TOOL_ROOT_PATH, 'media')
ICONS_PATH = os.path.join(MEDIA_PATH, 'icons')

#AssetManager Sizes
STACKEDWIDGET_DIVIDER_HEIGHT = 3

#transparency
TABLEVIEW_EDITOR_TRANSPARENCY = 125

#AssetManager colors
BRIGHT_ORANGE = QtGui.QColor('#f9661e')
DARK_ORANGE = QtGui.QColor('#b13b00')
BRIGHT_GREY = QtGui.QColor('#dbdce0')
GREY = QtGui.QColor('#1f1f1f')
DARK_GREY = QtGui.QColor('#131313')
DARK_BLUE = QtGui.QColor('#006cbf')
BRIGHT_BLUE = QtGui.QColor('#008df9')
WHITE = QtGui.QColor('#ffffff')

#Header
HEADER_IMAGE = os.path.join(icons_path, 'icn_asset_manager_header_one.png').replace('\\', '/')

#AssetManager Icons
ICON_EXPORT = os.path.join(icons_path, 'icn_export.png').replace('\\', '/')
ICON_CHAR = os.path.join(icons_path, 'icn_char.png').replace('\\', '/')
ICON_PROP = os.path.join(icons_path, 'icn_prop.png').replace('\\', '/')
ICON_SHOT = os.path.join(icons_path, 'icn_shot.png').replace('\\', '/')
ICON_UPDATE = os.path.join(icons_path, 'icn_update.png').replace('\\', '/')
ICON_DOCS = os.path.join(icons_path, 'icn_docs.png').replace('\\', '/')

#Text
SHOT_METADATA_EXPLANATION_HEADER = 'Shot Metadata'
SHOT_METADATA_EXPLANATION_TEXT = 'Displays the metadata needed for a shot.\
When you hit export, you will export the camera specified in shotcam.'
PROP_METADATA_EXPLANATION_HEADER = 'Prop Metadata'
PROP_METADATA_EXPLANATION_TEXT = 'Displays all the props in the scene and their metadata. \
When you hit export, you will export the ones that are active as Alembic files. You can export either \
the proxy, a locator or the render geo. Anything thats active in the spreadsheet will be processed.'
CHAR_METADATA_EXPLANATION_HEADER = 'Character Metadata'
CHAR_METADATA_EXPLANATION_TEXT = 'Displays all the characters in the scene and their metadata. \
When you hit export, you will export the ones that are active as Alembic files.'



