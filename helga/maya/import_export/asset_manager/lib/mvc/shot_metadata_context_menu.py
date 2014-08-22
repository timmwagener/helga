

"""
shot_metadata_context_menu
==========================================

Menu created on right-click at ShotMetadataView instance.

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













#ShotMetadataContextMenu class
#------------------------------------------------------------------
class ShotMetadataContextMenu(QtGui.QMenu):

    
    def __new__(cls, *args, **kwargs):
        """
        ShotMetadataContextMenu instance factory.
        """

        #shot_metadata_context_menu_instance
        shot_metadata_context_menu_instance = super(ShotMetadataContextMenu, cls).__new__(cls, args, kwargs)

        return shot_metadata_context_menu_instance

    
    def __init__(self, 
                logging_level = logging.DEBUG,
                parent = None):
        """
        Customize instance.
        """

        #super
        self.parent_class = super(ShotMetadataContextMenu, self)
        self.parent_class.__init__(parent)

        #setObjectName
        self.setObjectName(self.__class__.__name__)


        #instance variables
        #------------------------------------------------------------------

        #asset_manager_functionality
        self.asset_manager_functionality = asset_manager_functionality.AssetManagerFunctionality()

        #view
        self.view = None


        
        #logger
        #------------------------------------------------------------------
        #logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logging_level = logging_level
        self.logger.setLevel(self.logging_level)
        

        #Init procedure
        #------------------------------------------------------------------

        #setup_ui
        self.setup_ui()

        #connect_ui
        self.connect_ui()

        #style_ui
        self.style_ui()

        #test_methods
        self.test_methods()

        



        

        
        
        
        
        
    
    
    
    #UI setup methods
    #------------------------------------------------------------------
    
    def setup_ui(self):
        """
        Setup menu ui.
        """

        #add_actions
        self.add_actions()

    
    def connect_ui(self):
        """
        Connect UI widgets with slots or functions.
        """

        #Actions

        #actn_select_nodes
        self.actn_select_nodes.triggered.connect(self.select_nodes)

        #actn_delete_nodes
        self.actn_delete_nodes.triggered.connect(self.delete_nodes)

        #actn_create_node
        self.actn_create_node.triggered.connect(self.create_node)
        

    def style_ui(self):
        """
        Setup tool palette, tool stylesheet and specific widget stylesheets.
        """

        #styled_background
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Popup)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)

        #correct_styled_background_attribute
        self.correct_styled_background_attribute()

        #set_margins_and_spacing
        self.set_margins_and_spacing()

        #adjust size (Shrink to minimum size)
        self.adjustSize()
    
    

    def add_actions(self):
        """
        Add actions to menu.
        """
        
        #actn_select_nodes
        self.actn_select_nodes = QtGui.QAction('Select nodes', self)
        self.addAction(self.actn_select_nodes)

        #actn_delete_nodes
        self.actn_delete_nodes = QtGui.QAction('Delete nodes', self)
        self.addAction(self.actn_delete_nodes)

        #actn_create_node
        self.actn_create_node = QtGui.QAction('Create shot metadata node', self)
        self.addAction(self.actn_create_node)



    


    #Getter & Setter
    #------------------------------------------------------------------

    def set_view(self, view):
        """
        Set self.view
        """

        self.view = view

        




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


    def get_selected_indices(self):
        """
        Return list of selected indices from view.
        """

        #if view
        if (self.view):
            #selected_indices_list
            selected_indices_list = self.view.selectedIndexes()
        #else
        else:
            #selected_indices_list
            selected_indices_list = []

        return selected_indices_list


    def indices_list_to_data_list(self, model_index_list):
        """
        Convert a list of modelindices to the list of
        data they contain. This does NOT give the pynodes from the models
        data list, but the content of the view fields.
        """

        try:
            #data_list
            data_list = [model_index.data() for model_index in model_index_list]

        except:
            #data_list
            data_list = []

        return data_list


    def indices_list_to_pynode_list(self, model_index_list):
        """
        Convert a list of modelindices to the list of
        pynodes from the model.
        """

        #pynode_list
        pynode_list = []

        try:
            #iterate
            for index in model_index_list:

                #index invalid
                if not(index.isValid()):
                    
                    #log
                    self.logger.debug('Index {0} not valid.'.format(index))
                    continue
                
                
                #row & col
                row = index.row()
                col = index.column()

                #model
                model = index.model()

                #append
                pynode_list.append(model.data_list[row][0]) #column is always zero

        except:
            pass

        return pynode_list



    
    @QtCore.Slot()
    def select_nodes(self):
        """
        Select nodes.
        """

        #selected_indices_list
        selected_indices_list = self.get_selected_indices()
        #pynode_list
        pynode_list = self.indices_list_to_pynode_list(selected_indices_list)
        #clean_pynode_list
        clean_pynode_list = self.asset_manager_functionality.remove_duplicate_pynodes(pynode_list)

        #select
        self.asset_manager_functionality.select_nodes(clean_pynode_list)


    @QtCore.Slot()
    def delete_nodes(self):
        """
        Delete nodes.
        """

        #selected_indices_list
        selected_indices_list = self.get_selected_indices()
        #pynode_list
        pynode_list = self.indices_list_to_pynode_list(selected_indices_list)
        #clean_pynode_list
        clean_pynode_list = self.asset_manager_functionality.remove_duplicate_pynodes(pynode_list)

        #select
        self.asset_manager_functionality.delete_nodes(clean_pynode_list)


    @QtCore.Slot()
    def create_node(self):
        """
        Create node.
        """
    
        #create
        self.asset_manager_functionality.create_node('HelgaShotsMetadata')

    





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


    


