
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
FONTS_PATH = os.path.join(MEDIA_PATH, 'fonts')

#Fonts (append if non existent)

#futura-lt-light
FUTURA_LT_LIGHT = 'Futura LT Light'
if not (FUTURA_LT_LIGHT in QtGui.QFontDatabase().families()):
	current_font_path = os.path.join(FONTS_PATH, 'futura-lt-light.ttf').replace('\\', '/')
	QtGui.QFontDatabase.addApplicationFont(current_font_path)
	#log
	print('Installed tool relative font: {0} from {1}'.format(FUTURA_LT_LIGHT, current_font_path))



#AssetManager Sizes
STACKEDWIDGET_DIVIDER_HEIGHT = 3

#transparency
TABLEVIEW_EDITOR_TRANSPARENCY = 125

#darkening_factor
DARKENING_FACTOR = 120

#brightening_factor
BRIGHTENING_FACTOR = 150

#AssetManager colors
BRIGHT_ORANGE = QtGui.QColor('#f9661e')
DARK_ORANGE = BRIGHT_ORANGE.darker(DARKENING_FACTOR)
BRIGHT_BLUE = QtGui.QColor('#119bd2')
DARK_BLUE = BRIGHT_BLUE.darker(DARKENING_FACTOR)
BRIGHT_GREEN = QtGui.QColor('#58bf02')
DARK_GREEN = BRIGHT_GREEN.darker(DARKENING_FACTOR)
BRIGHT_GREY = QtGui.QColor('#dbdce0')
GREY = QtGui.QColor('#1f1f1f')
DARK_GREY = QtGui.QColor('#131313')
DARK_BLUE = QtGui.QColor('#006cbf')
BRIGHT_BLUE = QtGui.QColor('#008df9')
WHITE = QtGui.QColor('#ffffff')
RED = QtGui.QColor('#ff0000')

#Header
HEADER_IMAGE = os.path.join(ICONS_PATH, 'icn_asset_manager_header_one.png').replace('\\', '/')

#AssetManager Icons
ICON_EXPORT = os.path.join(ICONS_PATH, 'icn_export.png').replace('\\', '/')
ICON_CHAR = os.path.join(ICONS_PATH, 'icn_char.png').replace('\\', '/')
ICON_PROP = os.path.join(ICONS_PATH, 'icn_prop.png').replace('\\', '/')
ICON_SHOT = os.path.join(ICONS_PATH, 'icn_shot.png').replace('\\', '/')
ICON_UPDATE = os.path.join(ICONS_PATH, 'icn_update.png').replace('\\', '/')
ICON_DOCS = os.path.join(ICONS_PATH, 'icn_docs.png').replace('\\', '/')
ICON_TRUE = os.path.join(ICONS_PATH, 'icn_true.png').replace('\\', '/')
ICON_FALSE = os.path.join(ICONS_PATH, 'icn_false.png').replace('\\', '/')


#Text
SHOT_METADATA_EXPLANATION_HEADER = 'Shot Metadata'
SHOT_METADATA_EXPLANATION_TEXT = 'Displays the metadata needed for a shot. When you hit export, you will export the camera specified in shotcam. Only one shot metadata node per shot, otherwise exporting is disabled.'
PROP_METADATA_EXPLANATION_HEADER = 'Prop Metadata'
PROP_METADATA_EXPLANATION_TEXT = 'Displays all the props in the scene and their metadata. When you hit export, you will export the ones that are active as Alembic files.'
CHAR_METADATA_EXPLANATION_HEADER = 'Character Metadata'
CHAR_METADATA_EXPLANATION_TEXT = 'Displays all the characters in the scene and their metadata. When you hit export, you will export the ones that are active as Alembic files.'



