

"""
prop_metadata_context_menu
==========================================

Menu created on right-click at PropMetadataView instance.

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













#PropMetadataContextMenu class
#------------------------------------------------------------------
class PropMetadataContextMenu(QtGui.QMenu):

    
    def __new__(cls, *args, **kwargs):
        """
        PropMetadataContextMenu instance factory.
        """

        #prop_metadata_context_menu_instance
        prop_metadata_context_menu_instance = super(PropMetadataContextMenu, cls).__new__(cls, args, kwargs)

        return prop_metadata_context_menu_instance

    
    def __init__(self, 
                logging_level = logging.DEBUG,
                parent = None):
        """
        Customize instance.
        """

        #super
        self.parent_class = super(PropMetadataContextMenu, self)
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

        
        #actn_select_proxy
        self.actn_select_proxy.triggered.connect(functools.partial(self.select_nodes_with_namespace_and_attr, 'helga_proxy'))

        #actn_select_rendergeo
        self.actn_select_rendergeo.triggered.connect(functools.partial(self.select_nodes_with_namespace_and_attr, 'helga_rendergeo'))

        #actn_select_locator
        self.actn_select_locator.triggered.connect(functools.partial(self.select_nodes_with_namespace_and_attr, 'helga_locator'))


        #actn_show_all
        self.actn_show_all.triggered.connect(functools.partial(self.set_visibility_on_nodes_with_namespace_and_attr, 
                                                                ['helga_proxy', 'helga_rendergeo', 'helga_locator'], True))

        #actn_hide_all
        self.actn_hide_all.triggered.connect(functools.partial(self.set_visibility_on_nodes_with_namespace_and_attr, 
                                                                ['helga_proxy', 'helga_rendergeo', 'helga_locator'], False))

        #actn_show_proxy
        self.actn_show_proxy.triggered.connect(functools.partial(self.set_visibility_on_nodes_with_namespace_and_attr, ['helga_proxy'], True))

        #actn_hide_proxy
        self.actn_hide_proxy.triggered.connect(functools.partial(self.set_visibility_on_nodes_with_namespace_and_attr, ['helga_proxy'], False))

        #actn_show_rendergeo
        self.actn_show_rendergeo.triggered.connect(functools.partial(self.set_visibility_on_nodes_with_namespace_and_attr, ['helga_rendergeo'], True))

        #actn_hide_rendergeo
        self.actn_hide_rendergeo.triggered.connect(functools.partial(self.set_visibility_on_nodes_with_namespace_and_attr, ['helga_rendergeo'], False))

        #actn_show_locator
        self.actn_show_locator.triggered.connect(functools.partial(self.set_visibility_on_nodes_with_namespace_and_attr, ['helga_locator'], True))

        #actn_hide_locator
        self.actn_hide_locator.triggered.connect(functools.partial(self.set_visibility_on_nodes_with_namespace_and_attr, ['helga_locator'], False))
        

        #actn_set_selection_true
        self.actn_set_selection_true.triggered.connect(functools.partial(self.set_selected_indices, True))

        #actn_set_selection_false
        self.actn_set_selection_false.triggered.connect(functools.partial(self.set_selected_indices, False))

    
    def style_ui(self):
        """
        Setup tool palette, tool stylesheet and specific widget stylesheets.
        """
        #set_styled_background_for_menus
        self.set_styled_background_for_menus()
        
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

        #Metadata
        #------------------------------------------------------------------

        #mnu_metadata
        self.mnu_metadata = QtGui.QMenu('Metadata', parent = self)
        self.mnu_metadata.setObjectName('mnu_metadata')
        self.addMenu(self.mnu_metadata)
        
        #actn_select_nodes
        self.actn_select_nodes = QtGui.QAction('Select nodes', self)
        self.mnu_metadata.addAction(self.actn_select_nodes)

        #actn_delete_nodes
        self.actn_delete_nodes = QtGui.QAction('Delete nodes', self)
        self.mnu_metadata.addAction(self.actn_delete_nodes)

        #actn_create_node
        self.actn_create_node = QtGui.QAction('Create prop metadata node', self)
        self.mnu_metadata.addAction(self.actn_create_node)

        

        #Geometry
        #------------------------------------------------------------------

        #mnu_geometry
        self.mnu_geometry = QtGui.QMenu('Geometry', parent = self)
        self.mnu_geometry.setObjectName('mnu_geometry')
        self.addMenu(self.mnu_geometry)

        #actn_select_proxy
        self.actn_select_proxy = QtGui.QAction('Select proxy', self)
        self.mnu_geometry.addAction(self.actn_select_proxy)

        #actn_select_rendergeo
        self.actn_select_rendergeo = QtGui.QAction('Select rendergeo', self)
        self.mnu_geometry.addAction(self.actn_select_rendergeo)

        #actn_select_locator
        self.actn_select_locator = QtGui.QAction('Select locator', self)
        self.mnu_geometry.addAction(self.actn_select_locator)



        #Visibility
        #------------------------------------------------------------------

        #mnu_visibility
        self.mnu_visibility = QtGui.QMenu('Visibility', parent = self)
        self.mnu_visibility.setObjectName('mnu_visibility')
        self.addMenu(self.mnu_visibility)


        #actn_show_all
        self.actn_show_all = QtGui.QAction('Show all', self)
        self.mnu_visibility.addAction(self.actn_show_all)

        #actn_hide_all
        self.actn_hide_all = QtGui.QAction('Hide all', self)
        self.mnu_visibility.addAction(self.actn_hide_all)

        
        #separator
        self.mnu_visibility.addSeparator()

        
        #actn_show_proxy
        self.actn_show_proxy = QtGui.QAction('Show proxy', self)
        self.mnu_visibility.addAction(self.actn_show_proxy)

        #actn_hide_proxy
        self.actn_hide_proxy = QtGui.QAction('Hide proxy', self)
        self.mnu_visibility.addAction(self.actn_hide_proxy)

        
        #separator
        self.mnu_visibility.addSeparator()

        
        #actn_show_rendergeo
        self.actn_show_rendergeo = QtGui.QAction('Show rendergeo', self)
        self.mnu_visibility.addAction(self.actn_show_rendergeo)

        #actn_hide_rendergeo
        self.actn_hide_rendergeo = QtGui.QAction('Hide rendergeo', self)
        self.mnu_visibility.addAction(self.actn_hide_rendergeo)

        
        #separator
        self.mnu_visibility.addSeparator()

        
        #actn_show_locator
        self.actn_show_locator = QtGui.QAction('Show locator', self)
        self.mnu_visibility.addAction(self.actn_show_locator)

        #actn_hide_locator
        self.actn_hide_locator = QtGui.QAction('Hide locator', self)
        self.mnu_visibility.addAction(self.actn_hide_locator)



        #Selection
        #------------------------------------------------------------------

        #mnu_selection
        self.mnu_selection = QtGui.QMenu('Selection', parent = self)
        self.mnu_selection.setObjectName('mnu_selection')
        self.addMenu(self.mnu_selection)
        
        #actn_set_selection_true
        self.actn_set_selection_true = QtGui.QAction('Set selection true', self)
        self.mnu_selection.addAction(self.actn_set_selection_true)

        #actn_set_selection_false
        self.actn_set_selection_false = QtGui.QAction('Set selection false', self)
        self.mnu_selection.addAction(self.actn_set_selection_false)

        

    


    #Getter & Setter
    #------------------------------------------------------------------

    def set_view(self, view):
        """
        Set self.view
        """

        self.view = view

        




    #Methods
    #------------------------------------------------------------------

    def set_styled_background_for_menus(self):
        """
        Set window flags and transparent background for all menus.
        """

        #wdgt_list
        wdgt_list = self.findChildren(QtGui.QWidget)

        #mnu_list
        mnu_list = [wdgt for wdgt in wdgt_list if (isinstance(wdgt, QtGui.QMenu))]

        #append self
        mnu_list.append(self)

        #iterate and set
        for menu in mnu_list:

            try:
                
                #styled_background
                menu.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Popup)
                menu.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)

            except:

                #log
                self.logger.debug('Error setting styled background and transparent flag for menu: {0}'.format(menu.objectName()))


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


    def set_selected_indices(self, value):
        """
        Sets selected indices in list to value.
        This only applies to the export columns,
        since those are all boolean.
        It will have no effect on other columns.
        """

        #selected_indices_list
        selected_indices_list = self.get_selected_indices()
        #check
        if not(selected_indices_list):
            #log
            self.logger.debug('No indices selected or no view set in context menu. Not setting values')
            return

        #model
        model = self.view.model()
        #check
        if not (model):
            #log
            self.logger.debug('Context menu view has no model. Not setting values')
            return

        #valid_column_list
        valid_column_list = [2,3,4]
        #valid_row_list
        valid_row_list = range(9999)

        #iterate
        for index in selected_indices_list:

            #index invalid
            if not(index.isValid()):
                #log
                self.logger.debug('Index {0} not valid. Continue'.format(index))
                continue
            
            
            #row & col
            row = index.row()
            col = index.column()

            #check if column valid
            if col in valid_column_list:

                #check if row valid
                if row in valid_row_list:

                    #set value
                    model.setData(index, value)

                else:

                    #log
                    self.logger.debug('Index at ({0}, {1}) not in valid row list'.format(row, col))

            else:

                #log
                self.logger.debug('Index at ({0}, {1}) not in valid column list'.format(row, col))



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


    def get_pynode_list_from_selected_indices(self):
        """
        Return duplicate free pynode list from selected indices.
        """

        #selected_indices_list
        selected_indices_list = self.get_selected_indices()
        #pynode_list
        pynode_list = self.indices_list_to_pynode_list(selected_indices_list)
        #clean_pynode_list
        clean_pynode_list = self.asset_manager_functionality.remove_duplicate_pynodes(pynode_list)

        #return
        return clean_pynode_list

    
    @QtCore.Slot()
    def select_nodes(self):
        """
        Select nodes.
        """

        #pynode_list
        pynode_list = self.get_pynode_list_from_selected_indices()

        #select
        self.asset_manager_functionality.select_nodes(pynode_list)


    @QtCore.Slot()
    def select_nodes_with_namespace_and_attr(self, attr_name):
        """
        Select nodes that have the same namespace and have an
        attribute that matches attr_name.
        """

        #pynode_list
        pynode_list = self.get_pynode_list_from_selected_indices()

        #select
        self.asset_manager_functionality.select_nodes_with_namespace_and_attr(pynode_list, attr_name)


    @QtCore.Slot()
    def set_visibility_on_nodes_with_namespace_and_attr(self, attr_name_list, visibility):
        """
        Set visibility attr. on nodes with namespace and given
        attr. name to passed visibility parm.
        """

        #pynode_list
        pynode_list = self.get_pynode_list_from_selected_indices()


        #iterate
        for attr_name in attr_name_list:
            
            #set visibility
            self.asset_manager_functionality.set_visibility_on_nodes_with_namespace_and_attr(pynode_list, attr_name, visibility = visibility)


    @QtCore.Slot()
    def delete_nodes(self):
        """
        Delete nodes.
        """

        #pynode_list
        pynode_list = self.get_pynode_list_from_selected_indices()

        #delete
        self.asset_manager_functionality.delete_nodes(pynode_list)


    @QtCore.Slot()
    def create_node(self):
        """
        Create node.
        """
    
        #create
        self.asset_manager_functionality.create_node('HelgaPropMetadata')

    





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


    


