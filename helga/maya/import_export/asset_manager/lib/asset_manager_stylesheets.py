
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
/* QWidget */\
QWidget { background-color: %(dark_grey)s; } \
\
\
/* QWidget - wdgt_explanation */\
QWidget#wdgt_explanation { background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 %(dark_orange)s, stop:1 %(bright_orange)s); } \
\
\
/* QWidget - wdgt_export */\
QWidget#wdgt_export { background-color: %(bright_orange)s; } \
\
\
/* QWidget - wdgt_docs */\
QWidget#wdgt_docs { background-color: %(dark_orange)s; } \
\
\
\
\
\
\
/* QLabel - lbl_explanation_header */\
QLabel#lbl_explanation_header { background-color: transparent; \
                                font: 75 20pt \"MS Shell Dlg 2\"; \
                                color: %(bright_grey)s; \
                                margin-top: 10; \
                                margin-left: 10; \
                                margin-bottom: 4; \
                                margin-right: 10; } \
\
\
/* QLabel - lbl_explanation_text */\
QLabel#lbl_explanation_text { background-color: transparent; \
                                font: 75 10pt \"MS Shell Dlg 2\"; \
                                color: %(bright_grey)s; \
                                margin-top: 4; \
                                margin-left: 10; \
                                margin-bottom: 4; \
                                margin-right: 10; } \
\
\
\
\
\
\
/* QProgressBar */\
QProgressBar { border: none;\
                 background-color: %(dark_grey)s;\
                 text-align: center;\
} \
\
\
/* QProgressBar - chunk */\
QProgressBar::chunk { border: none;\
                        background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0 %(dark_orange)s, stop:1 %(bright_orange)s); \
} \
\
\
\
\
\
\
/* QLineEdit */\
QLineEdit { border: none;\
            background-color: %(grey)s;\
} \
\
\
/* QLineEdit - le_status*/\
QLineEdit#le_status { border: none;\
                        background-color: %(dark_orange)s;\
                        color: %(bright_grey)s; \
} \
\
\
\
\
\
\
/* QScrollBar */\
QScrollBar { background: %(dark_grey)s; \
                    border: none; \
} \
\
\
\
\
\
\
/* QTableCornerButton */\
QTableCornerButton { background-color: %(grey)s; \
                        border: none; \
}\
\
\
/* QTableCornerButton - section */\
QTableCornerButton::section { background-color: %(grey)s; \
                                border: none; \
}\
\
\
\
\
\
\
/* ShotMetadataView */\
ShotMetadataView { background-color: %(grey)s; \
                    border-left: none; \
                    border-top: none; \
                    border-bottom: none; \
                    border-right: none; \
} \
\
\
\
\
\
\
/* QHeaderView - shot_metadata_view_hor_header*/\
QHeaderView#shot_metadata_view_hor_header{ background-color: %(grey)s; \
                                                    border-left: none; \
                                                    border-top: none; \
                                                    border-bottom: none; \
                                                    border-right: none; \
} \
\
\
/* QHeaderView - shot_metadata_view_hor_header - section */\
QHeaderView#shot_metadata_view_hor_header::section { background-color: qlineargradient(spread:reflect, x1:0.02, y1:0.02, x2:0, y2:0, stop:0.8 %(grey)s, stop:1 %(dark_orange)s); \
                                                    border-left: none; \
                                                    border-top: none; \
                                                    border-bottom: none; \
                                                    border-right: 1px solid %(bright_grey)s; \
} \
\
\
/* QHeaderView - shot_metadata_view_ver_header */\
QHeaderView#shot_metadata_view_ver_header { background-color: %(grey)s; \
                                                    border-left: none; \
                                                    border-top: none; \
                                                    border-bottom: none; \
                                                    border-right: none; \
} \
\
\
/* QHeaderView - shot_metadata_view_ver_header - section */\
QHeaderView#shot_metadata_view_ver_header::section { background-color: %(grey)s; \
                                                    border-left: none; \
                                                    border-top: none; \
                                                    border-bottom: none; \
                                                    border-right: none; \
} \
\
\
"%ss_dict

    return str_stylesheet
