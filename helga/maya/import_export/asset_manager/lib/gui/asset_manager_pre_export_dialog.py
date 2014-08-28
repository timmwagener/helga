

"""
asset_manager_pre_export_dialog
==========================================

Dialog that asks wether or not the current scene should be saved
before export begins. Offers the possibility to remember your choice.

-----------------------

**Author:** `Timm Wagener <mailto:wagenertimm@gmail.com>`_
"""







#Import
#------------------------------------------------------------------
#python
import os
import sys
import functools
import logging
import subprocess
import time
import shutil
import webbrowser
import yaml
import hashlib
import string
import random
#PySide
from PySide import QtGui
from PySide import QtCore
from PySide import QtUiTools
import shiboken
import pysideuic




#Import variable
do_reload = True

#helga

#global_variables
from helga.general.setup.global_variables import global_variables
if(do_reload):reload(global_variables)

#global_functions
from helga.general.setup.global_functions import global_functions
if(do_reload):reload(global_functions)


#asset_manager

#lib

#asset_manager_globals
from lib import asset_manager_globals
if(do_reload):reload(asset_manager_globals)

#lib.gui

#asset_manager_stylesheets
from lib.gui import asset_manager_stylesheets
if(do_reload):reload(asset_manager_stylesheets)










#Globals
#------------------------------------------------------------------

#Pathes
TOOL_ROOT_PATH = asset_manager_globals.TOOL_ROOT_PATH
MEDIA_PATH = asset_manager_globals.MEDIA_PATH
ICONS_PATH = asset_manager_globals.ICONS_PATH




#darkening_factor
DARKENING_FACTOR = asset_manager_globals.DARKENING_FACTOR
#brightening_factor
BRIGHTENING_FACTOR = asset_manager_globals.BRIGHTENING_FACTOR

#AssetManager colors
BRIGHT_ORANGE = asset_manager_globals.BRIGHT_ORANGE
DARK_ORANGE = asset_manager_globals.DARK_ORANGE
BRIGHT_BLUE = asset_manager_globals.BRIGHT_BLUE
DARK_BLUE = asset_manager_globals.DARK_BLUE
BRIGHT_GREEN = asset_manager_globals.BRIGHT_GREEN
DARK_GREEN = asset_manager_globals.DARK_GREEN
BRIGHT_GREY = asset_manager_globals.BRIGHT_GREY
GREY = asset_manager_globals.GREY
DARK_GREY = asset_manager_globals.DARK_GREY
DARK_BLUE = asset_manager_globals.DARK_BLUE
BRIGHT_BLUE = asset_manager_globals.BRIGHT_BLUE
WHITE = asset_manager_globals.WHITE


#AssetManager Icons
ICON_EXPORT = asset_manager_globals.ICON_EXPORT
ICON_CHAR = asset_manager_globals.ICON_CHAR
ICON_PROP = asset_manager_globals.ICON_PROP
ICON_SHOT = asset_manager_globals.ICON_SHOT
ICON_UPDATE = asset_manager_globals.ICON_UPDATE
ICON_DOCS = asset_manager_globals.ICON_DOCS






















#form_class, base_class
#------------------------------------------------------------------

#ui_file
ui_file_name = 'asset_manager_pre_export_dialog.ui'
ui_file = os.path.join(MEDIA_PATH, ui_file_name)

#form_class, base_class
form_class, base_class = global_functions.load_ui_type(ui_file)








#AssetManagerPreExportDialog class
#------------------------------------------------------------------
class AssetManagerPreExportDialog(form_class, base_class):
    """
    AssetManagerPreExportDialog
    """


    def __new__(cls, *args, **kwargs):
        """
        AssetManagerPreExportDialog instance factory.
        """

        #asset_manager_pre_export_dialog_instance
        asset_manager_pre_export_dialog_instance = super(AssetManagerPreExportDialog, cls).__new__(cls, args, kwargs)

        return asset_manager_pre_export_dialog_instance

    
    def __init__(self,
                question = 'Question',
                logging_level = logging.DEBUG,
                parent = None):
        """
        Customize instance.
        """

        #super
        self.parent_class = super(AssetManagerPreExportDialog, self)
        self.parent_class.__init__(parent)

        #setObjectName
        self.setObjectName(self.__class__.__name__)


        #instance variables
        #------------------------------------------------------------------
        
        self.title_name = self.__class__.__name__
        self.version = 0.1
        self.title = self.title_name +' ' + str(self.version)
        self.icon_path = os.path.join(ICONS_PATH, 'icon_asset_manager.png')

        #question
        self.question = question

        #remember_choice
        self.remember_choice = False #is set in setup_additional_ui


        

        #logger
        #------------------------------------------------------------------
        #logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logging_level = logging_level
        self.logger.setLevel(self.logging_level)

        
        

        #Init procedure
        #------------------------------------------------------------------
        
        #setupUi
        self.setupUi(self)

        #setup_additional_ui
        self.setup_additional_ui()

        #connect_ui
        self.connect_ui()

        #style_ui
        self.style_ui()

        #test_methods
        self.test_methods()

        

        



        

    

    
    
    
        
        
        
    
    
    
    #UI setup methods
    #------------------------------------------------------------------
    
    def setup_additional_ui(self):
        """
        Setup additional UI like mvc or helga tool header.
        """

        #set title
        self.setWindowTitle(self.title)

        #set question
        self.lbl_question.setText(self.question)

        #set_remember_choice
        self.set_remember_choice(self.chkbx_remember_choice.isChecked())




    def connect_ui(self):
        """
        Connect UI widgets with slots or functions.
        """

        #btn_accept
        self.btn_accept.clicked.connect(self.accept)

        #btn_reject
        self.btn_reject.clicked.connect(self.reject)

        #chkbx_remember_choice
        self.chkbx_remember_choice.stateChanged.connect(self.set_remember_choice)


    def style_ui(self):
        """
        Setup tool palette, tool stylesheet and specific widget stylesheets.
        """

        #styled_background
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Dialog)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)

        #correct_styled_background_attribute
        self.correct_styled_background_attribute()

        #set_margins_and_spacing
        self.set_margins_and_spacing()

        #set_stylesheet
        self.setStyleSheet(asset_manager_stylesheets.get_stylesheet())

        #adjust size (Shrink to minimum size)
        self.adjustSize()









    #Methods
    #------------------------------------------------------------------

    def correct_styled_background_attribute(self):
        """
        Set QtCore.Qt.WA_StyledBackground True for all widgets.
        Without this attr. set, the background-color stylesheet
        will have no effect on QWidgets. This should replace the
        need for palette settings.
        ToDo:
        Maybe add exclude list when needed.
        """

        #wdgt_list
        wdgt_list = self.findChildren(QtGui.QWidget) #Return several types ?!?!

        #iterate and set
        for wdgt in wdgt_list:
            
            #check type
            if(type(wdgt) is QtGui.QWidget):

                #styled_background
                wdgt.setAttribute(QtCore.Qt.WA_StyledBackground, True)



    def set_margins_and_spacing(self):
        """
        Eliminate margin and spacing for all layout widgets.
        """

        #margin_list
        margin_list = [0,0,0,0]

        #lyt_classes_list
        lyt_classes_list = [QtGui.QStackedLayout, QtGui.QGridLayout, QtGui.QFormLayout, 
                            QtGui.QBoxLayout, QtGui.QVBoxLayout, QtGui.QHBoxLayout, QtGui.QBoxLayout]

        #lyt_list
        lyt_list = []
        for lyt_class in lyt_classes_list:
            lyt_list += [wdgt for wdgt in self.findChildren(lyt_class)]


        
        #set margin and spacing
        for lyt in lyt_list:

            #check type
            if(type(lyt) in lyt_classes_list):

                #set
                lyt.setContentsMargins(*margin_list)
                lyt.setSpacing(0)


    


    

    #Getter & Setter
    #------------------------------------------------------------------

    @QtCore.Slot(int)
    def set_remember_choice(self, value):
        """
        Set self.remember_choice
        """

        #set
        self.remember_choice = value

        #log
        self.logger.debug('Set remember choice to {0}'.format(self.remember_choice))


    def get_remember_choice(self):
        """
        Get self.remember_choice
        """

        return self.remember_choice





    #Slots
    #------------------------------------------------------------------

    


    




    #Events
    #------------------------------------------------------------------

    def closeEvent(self, event):
        """
        Customized closeEvent
        """

        #parent close event
        self.parent_class.closeEvent(event)


    




    #Test
    #------------------------------------------------------------------

    def dummy_method(self, msg = 'dummy'):
        """
        Dummy method
        """

        #log
        self.logger.debug('{0}'.format(msg))
        #print
        print('{0}'.format(msg))


    def stylesheet_test(self, wdgt):
        """
        Test if setting a stylesheet overrides all attributes or just
        the one it is setting.
        """

        #stylesheet_str
        stylesheet_str = 'background-color: red;'
        
        #set stylesheet
        wdgt.setStyleSheet(stylesheet_str)


    def test_methods(self):
        """
        Suite of test methods to execute on startup.
        """

        #log
        self.logger.debug('\n\nExecute test methods:\n-----------------------------')


        
        #test methods here
        #------------------------------------------------------------------

        #dummy_method
        self.dummy_method()

        #stylesheet_test
        #self.stylesheet_test(self.wdgt_explanation)

        #------------------------------------------------------------------



        #log
        self.logger.debug('\n\n-----------------------------\nFinished test methods.')


    


