
"""
asset_manager_stylesheets
==========================================

Module that has only one method.

#. get_stylesheet
"""








#Add tool relative pathes
#------------------------------------------------------------------

#import
import sys
import os

#icons_path
icons_path = os.path.join(os.path.dirname(__file__), 'icons')
sys.path.append(icons_path)







#Import
#------------------------------------------------------------------

#PySide
from PySide import QtGui
from PySide import QtCore







#get_stylesheet
#------------------------------------------------------------------

def get_stylesheet():
    """
    Return stylesheet string, defining all stylesheets for AssetManager.
    """

    #str_stylesheet
    str_stylesheet = " \
\
\
/* AssetManagerButton */\
AssetManagerButton { background-color: red; } \
AssetManagerButton:hover { background-color: green; } \
AssetManagerButton:pressed { background-color: blue; } \
\
\
/* AssetManagerButton - btn_show_shot_metadata */\
AssetManagerButton#btn_show_shot_metadata { border-image: url(%(icon_path)s/icn_docs.png); background-color: red; } \
AssetManagerButton#btn_show_shot_metadata:hover { border-image: url(%(icon_path)s/icn_export.png); background-color: green; } \
AssetManagerButton#btn_show_shot_metadata:pressed { border-image: url(%(icon_path)s/icon_asset_manager.png); background-color: blue; } \
\
\
/* AssetManagerButton - btn_show_prop_metadata */\
AssetManagerButton#btn_show_prop_metadata { border-image: url(%(icon_path)s/icn_docs.png); background-color: red; } \
AssetManagerButton#btn_show_prop_metadata:hover { border-image: url(%(icon_path)s/icn_export.png); background-color: green; } \
AssetManagerButton#btn_show_prop_metadata:pressed { border-image: url(%(icon_path)s/icon_asset_manager.png); background-color: blue; } \
\
\
/* AssetManagerButton - btn_show_char_metadata */\
AssetManagerButton#btn_show_char_metadata { border-image: url(%(icon_path)s/icn_docs.png); background-color: red; } \
AssetManagerButton#btn_show_char_metadata:hover { border-image: url(%(icon_path)s/icn_export.png); background-color: green; } \
AssetManagerButton#btn_show_char_metadata:pressed { border-image: url(%(icon_path)s/icon_asset_manager.png); background-color: blue; } \
\
\
"%{'icon_path' : icons_path.replace('\\', '/')}

    return str_stylesheet
