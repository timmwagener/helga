
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


#Import variable
do_reload = True


#asset_manager

#asset_manager_globals
import asset_manager_globals
if(do_reload):reload(asset_manager_globals)







#Globals
#------------------------------------------------------------------

#AssetManager colors
BRIGHT_ORANGE = asset_manager_globals.BRIGHT_ORANGE
DARK_ORANGE = asset_manager_globals.DARK_ORANGE
BRIGHT_GREY = asset_manager_globals.BRIGHT_GREY
GREY = asset_manager_globals.GREY
DARK_GREY = asset_manager_globals.DARK_GREY






#get_stylesheet
#------------------------------------------------------------------

def get_stylesheet():
    """
    Return stylesheet string, defining all stylesheets for AssetManager.
    """

    #ss_dict
    ss_dict = {'bright_orange' : BRIGHT_ORANGE.name(),
			    'dark_orange' : DARK_ORANGE.name(),
			    'bright_grey' : BRIGHT_GREY.name(),
			    'grey' : GREY.name(),
			    'dark_grey' : DARK_GREY.name()}


    #str_stylesheet
    str_stylesheet = " \
\
\
/* AssetManagerButton */\
AssetManagerButton { background-color: %(dark_grey)s; } \
AssetManagerButton:hover { background-color: %(dark_grey)s; } \
AssetManagerButton:pressed { background-color: %(grey)s; } \
\
\
/* QWidget - wdgt_explanation */\
QWidget#wdgt_explanation { background: %(bright_orange)s; } \
\
\
/* QLabel - lbl_explanation_header */\
QLabel#lbl_explanation_header { background-color: %(bright_orange)s; font: 75 20pt \"MS Shell Dlg 2\"; color: %(bright_grey)s; margin-top: 10; margin-left: 10; margin-bottom: 4; margin-right: 10; } \
\
\
/* QLabel - lbl_explanation_text */\
QLabel#lbl_explanation_text { background-color: %(bright_orange)s; font: 75 10pt \"MS Shell Dlg 2\"; color: %(bright_grey)s; margin-top: 4; margin-left: 10; margin-bottom: 4; margin-right: 10; } \
\
\
"%ss_dict

    return str_stylesheet
