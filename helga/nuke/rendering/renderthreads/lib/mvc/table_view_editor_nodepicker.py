

"""
table_view_editor_nodepicker
==========================================

Editor created in EditRole in QItemDelegate. It is initialized with a certain
node type and allows to pick from all nodes of the same type that are in the scene.

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

#asset_manager_functionality
from lib import asset_manager_functionality
if(do_reload):reload(asset_manager_functionality)









#Globals
#------------------------------------------------------------------

#Pathes
TOOL_ROOT_PATH = asset_manager_globals.TOOL_ROOT_PATH
MEDIA_PATH = asset_manager_globals.MEDIA_PATH
ICONS_PATH = asset_manager_globals.ICONS_PATH









#form_class, base_class
#------------------------------------------------------------------

#ui_file
ui_file_name = 'table_view_editor_nodepicker.ui'
ui_file = os.path.join(MEDIA_PATH, ui_file_name)

#form_class, base_class
form_class, base_class = global_functions.load_ui_type(ui_file)








#TableViewEditorNodepicker class
#------------------------------------------------------------------
class TableViewEditorNodepicker(form_class, base_class):

    
    def __new__(cls, *args, **kwargs):
        """
        TableViewEditorNodepicker instance factory.
        """

        #table_view_editor_nodepicker_instance
        table_view_editor_nodepicker_instance = super(TableViewEditorNodepicker, cls).__new__(cls, args, kwargs)

        return table_view_editor_nodepicker_instance

    
    def __init__(self, 
                logging_level = logging.DEBUG,
                node_type = 'transform',
                use_parent_in_model = False,
                parent = None):
        """
        Customize instance.
        """

        #super
        self.parent_class = super(TableViewEditorNodepicker, self)
        self.parent_class.__init__(parent)

        #setObjectName
        self.setObjectName(self.__class__.__name__)


        #instance variables
        #------------------------------------------------------------------
        self.title_name = self.__class__.__name__
        self.version = 0.1
        self.title = self.title_name +' ' + str(self.version)

        #node_type
        self.node_type = node_type
        #use_parent_in_model
        self.use_parent_in_model = use_parent_in_model

        #node_name_list
        self.node_name_list = []
        #node_name_list_filtered
        self.node_name_list_filtered = []

        #asset_manager_functionality
        self.asset_manager_functionality = asset_manager_functionality.AssetManagerFunctionality()

        
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
        self.set_label('Nodetype: {0}'.format(self.node_type))

        #setup_mvc
        self.setup_mvc()

        #setup_style
        self.setup_style()

    
    def connect_ui(self):
        """
        Connect UI widgets with slots or functions.
        """

        #node_view
        self.node_view.clicked.connect(self.on_nodepicker_clicked)
        #le_filter
        self.le_filter.textChanged.connect(self.update_model)
        

    def setup_style(self):
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
        Set self.lbl_nodetype
        """

        self.lbl_nodetype.setText(msg)


    def get_label(self):
        """
        Return text from self.lbl_nodetype
        """

        return str(self.lbl_nodetype.text())


    def get_filter_string(self):
        """
        Return text from self.le_filter
        """

        return str(self.le_filter.text())








    #MVC
    #------------------------------------------------------------------

    def setup_mvc(self):
        """
        Setup model-view controller for nodepicker.
        """
    
        #customize node_view
        self.node_view.setAlternatingRowColors(True)

        #node_model
        self.node_model = QtGui.QStandardItemModel(self.node_view)
        self.node_view.setModel(self.node_model)

        #node_selection_model
        self.node_selection_model = QtGui.QItemSelectionModel(self.node_model)
        self.node_view.setSelectionModel(self.node_selection_model)

        #update_model
        self.update_model()
        
        


    def set_node_name_list(self, node_type):
        """
        Set node data in model.
        """

        #node_list
        node_list = self.asset_manager_functionality.get_nodes_of_type(node_type)

        #node_name_list
        #parent (usefull for cameras, lights etc. to get their transform instead of shape nodes)
        if (self.use_parent_in_model):
            node_name_list = [node.getParent().name() for node in node_list]
        #use node name
        else:
            node_name_list = [node.name() for node in node_list]

        #set instance var
        self.node_name_list = node_name_list


    def filter_node_name_list(self, filter_string):
        """
        Filter node_name_list.
        """

        #node_name_list_filtered
        node_name_list_filtered = [node_name for node_name in self.node_name_list if(filter_string in node_name)]

        #set instance var
        self.node_name_list_filtered = node_name_list_filtered

    
    @QtCore.Slot()
    def update_model(self):
        """
        Set node data in model.
        """

        #clear
        self.node_model.clear()

        #set_node_name_list
        self.set_node_name_list(self.node_type)

        #filter_node_name_list
        filter_string = self.get_filter_string()
        self.filter_node_name_list(filter_string)

        #iterate and set model
        for node_name in sorted(self.node_name_list_filtered):

            #node_item
            node_item = QtGui.QStandardItem(node_name)

            #append
            self.node_model.appendRow(node_item)


    def get_selected_node_name(self):
        """
        Set node data in model.
        """

        #selected_node_name_list
        selected_node_name_list = self.node_view.selectedIndexes()

        try:
            #only one selection is valid so the list defaults to one element
            selected_node_index = selected_node_name_list[0]

        except:
            return ''

        #selected_node_name
        selected_node_name = selected_node_index.data()

        return selected_node_name


    def set_selection_from_node_name(self, node_name_to_match):
        """
        Set index selected where node_name matches.
        """

        #matching_item_list
        matching_item_list = self.node_model.findItems(node_name_to_match)

        #not found item
        if not (matching_item_list):
            return 

        #matching_index
        matching_index = matching_item_list[0].index() #Only one item can match. Nodes have unique pathes

        #select
        self.node_view.setCurrentIndex(matching_index)






    




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
    def on_nodepicker_clicked(self, index):
        print('Currently selected cam {0}'.format(index.data()))




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


    







#Run
#------------------------------------------------------------------

def run():
    """
    Standardized run() method
    """
    
    #table_view_editor_nodepicker_instance
    table_view_editor_nodepicker_instance = TableViewEditorNodepicker()
    table_view_editor_nodepicker_instance.show()












#Test
#------------------------------------------------------------------

if (__name__ == '__main__'):

    #run
    run()
