

"""
table_view_editor_pathpicker
==========================================

Editor created in EditRole in QItemDelegate. It is initialized with a certain
base path and allows to pick from all subdirectories.

-----------------------

**Author:** `Timm Wagener <mailto:wagenertimm@gmail.com>`_
"""












#Import
#------------------------------------------------------------------
#python
import sys
import os
import functools
import logging
import subprocess
import time
import shutil
import webbrowser
import yaml
import hashlib
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

#asset_manager_globals
from lib import asset_manager_globals
if(do_reload):reload(asset_manager_globals)









#Globals
#------------------------------------------------------------------

#Pathes
TOOL_ROOT_PATH = asset_manager_globals.TOOL_ROOT_PATH
MEDIA_PATH = asset_manager_globals.MEDIA_PATH
ICONS_PATH = asset_manager_globals.ICONS_PATH









#form_class, base_class
#------------------------------------------------------------------

#ui_file
ui_file_name = 'table_view_editor_pathpicker.ui'
ui_file = os.path.join(MEDIA_PATH, ui_file_name)

#form_class, base_class
form_class, base_class = global_functions.load_ui_type(ui_file)








#TableViewEditorPathpicker class
#------------------------------------------------------------------
class TableViewEditorPathpicker(form_class, base_class):

    
    def __new__(cls, *args, **kwargs):
        """
        TableViewEditorPathpicker instance factory.
        """

        #table_view_editor_pathpicker_instance
        table_view_editor_pathpicker_instance = super(TableViewEditorPathpicker, cls).__new__(cls, args, kwargs)

        return table_view_editor_pathpicker_instance

    
    def __init__(self, 
                logging_level = logging.DEBUG,
                base_path = '',
                parent = None):
        """
        Customize instance.
        """

        #super
        self.parent_class = super(TableViewEditorPathpicker, self)
        self.parent_class.__init__(parent)

        #setObjectName
        self.setObjectName(self.__class__.__name__)


        #instance variables
        #------------------------------------------------------------------
        self.title_name = self.__class__.__name__
        self.version = 0.1
        self.title = self.title_name +' ' + str(self.version)

        #base_path
        self.base_path = base_path

        #path_list
        self.path_list = []
        #path_list_filtered
        self.path_list_filtered = []

        

        
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

        #make frameless and invisible
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Window | QtCore.Qt.WindowSystemMenuHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)

        #set title
        self.setWindowTitle(self.title)

        #set_label
        self.set_label('Base path: {0}'.format(self.base_path))

        #setup_mvc
        self.setup_mvc()

    
    def connect_ui(self):
        """
        Connect UI widgets with slots or functions.
        """

        #path_view
        self.path_view.clicked.connect(self.on_pathpicker_clicked)
        #le_path_filter
        self.le_path_filter.textChanged.connect(self.update_model)
        

    def style_ui(self):
        """
        Setup tool palette, tool stylesheet and specific widget stylesheets.
        """

        #correct_styled_background_attribute
        self.correct_styled_background_attribute()

        #set_margins_and_spacing
        self.set_margins_and_spacing()

        #adjust size (Shrink to minimum size)
        self.adjustSize()
    
    


    



    #Getter & Setter
    #------------------------------------------------------------------

    def set_label(self, msg):
        """
        Set self.lbl_base_path
        """

        self.lbl_base_path.setText(msg)


    def get_label(self):
        """
        Return text from self.lbl_base_path
        """

        return str(self.lbl_base_path.text())


    def get_filter_string(self):
        """
        Return text from self.le_path_filter
        """

        return str(self.le_path_filter.text())








    #MVC
    #------------------------------------------------------------------

    def setup_mvc(self):
        """
        Setup model-view controller for nodepicker.
        """
    
        #customize path_view
        self.path_view.setAlternatingRowColors(True)

        #path_model
        self.path_model = QtGui.QStandardItemModel(self.path_view)
        self.path_view.setModel(self.path_model)

        #path_selection_model
        self.path_selection_model = QtGui.QItemSelectionModel(self.path_model)
        self.path_view.setSelectionModel(self.path_selection_model)

        #update_model
        self.update_model()
        
        


    def set_path_list(self, base_path):
        """
        Set path data in model.
        """

        #path exists
        if not (os.path.isdir(base_path)):
            #log
            self.logger.debug('Base path {0} does not exist. Set empty list'.format(base_path))
            self.path_list = []
            return

        #nested_path_list
        while (True):
            nested_path_list = [x[1] for x in os.walk(base_path, followlinks = True)]
            break
        
        #path_list
        try:
            path_list = nested_path_list[0]
        except:
            #log
            self.logger.debug('Base path {0} does not exist or does not have sub directories. Set empty list'.format(base_path))
            self.path_list = []
            return

        #set instance var
        self.path_list = path_list


    def filter_path_list(self, filter_string):
        """
        Filter path_list.
        """

        #path_list_filtered
        path_list_filtered = [path for path in self.path_list if(filter_string in path)]

        #set instance var
        self.path_list_filtered = path_list_filtered

    
    @QtCore.Slot()
    def update_model(self):
        """
        Set path data in model.
        """

        #clear
        self.path_model.clear()

        #set_path_list
        self.set_path_list(self.base_path)

        #filter_path_list
        filter_string = self.get_filter_string()
        self.filter_path_list(filter_string)

        #iterate and set model
        for path in sorted(self.path_list_filtered):

            #path_item
            path_item = QtGui.QStandardItem(path)

            #append
            self.path_model.appendRow(path_item)


    def get_selected_path(self):
        """
        Get selected path from model.
        """

        #selected_path_list
        selected_path_list = self.path_view.selectedIndexes()

        try:
            #only one selection is valid so the list defaults to one element
            selected_path_index = selected_path_list[0]

        except:
            return ''

        #selected_path
        selected_path = selected_path_index.data()

        return selected_path


    def set_selection_from_path(self, path_to_match):
        """
        Set index selected where path matches.
        """

        #matching_item_list
        matching_item_list = self.path_model.findItems(path_to_match)

        #not found item
        if not (matching_item_list):
            return 

        #matching_index
        matching_index = matching_item_list[0].index() #Only one item can match.

        #select
        self.path_view.setCurrentIndex(matching_index)






    




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




    #Slots
    #------------------------------------------------------------------

    @QtCore.Slot(QtCore.QModelIndex)
    def on_pathpicker_clicked(self, index):
        print('Currently selected path: {0}'.format(index.data()))




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

        pass


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

        #------------------------------------------------------------------



        #log
        self.logger.debug('\n\n-----------------------------\nFinished test methods.')


    




