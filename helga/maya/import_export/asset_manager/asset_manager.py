

"""
asset_manager
==========================================

GUI to export Alembics from Maya. Building atop of our asset based pipeline.

It takes care of:

#. Cameras
#. Characters
#. Props


-----------------------

Idea list:

#. Queue/Threadpool for alembic export
#. Feed closures to Queue
#. Export chars, props and cameras
#. Use descriptor protocol
#. Take care of preroll for chars in code.

-----------------------

**Author:** `Timm Wagener <mailto:wagenertimm@gmail.com>`_
"""











#Add tool relative pathes
#------------------------------------------------------------------

#import
import sys
import os

#tool_root_path
tool_root_path = os.path.dirname(__file__)
sys.path.append(tool_root_path)

#media_path
media_path = os.path.join(tool_root_path, 'media')
sys.path.append(media_path)

#icons_path
icons_path = os.path.join(media_path, 'icons')
sys.path.append(icons_path)


















#Import
#------------------------------------------------------------------
#python
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

#asset_manager_logging_handler
from lib import asset_manager_logging_handler
if(do_reload):reload(asset_manager_logging_handler)

#asset_manager_functionality
from lib import asset_manager_functionality
if(do_reload):reload(asset_manager_functionality)

#asset_manager_button
from lib import asset_manager_button
if(do_reload):reload(asset_manager_button)

#asset_manager_stylesheets
from media import asset_manager_stylesheets
if(do_reload):reload(asset_manager_stylesheets)

#shot_metadata_model
from lib.mvc import shot_metadata_model
if(do_reload):reload(shot_metadata_model)

#shot_metadata_view
from lib.mvc import shot_metadata_view
if(do_reload):reload(shot_metadata_view)

#shot_metadata_item_delegate
from lib.mvc import shot_metadata_item_delegate
if(do_reload):reload(shot_metadata_item_delegate)









#Cleanup old instances
#------------------------------------------------------------------

def get_widget_by_name_closure(wdgt_name):
    """
    Practicing closures. Doesnt really make sense here, or could at least
    be done much simpler/better.
    Want to try it with filter in order to get more into the builtins.
    """

    def get_widget_by_name(wdgt):
        """
        Function that is closed in. Accepts and checks all
        widgets against wdgt_name from enclosing function.
        ALl this mess to be able to use it with filter.
        """
        try:
            if (wdgt.__class__.__name__ == wdgt_name):
                return True
        except:
            pass
        return False

    return get_widget_by_name


def check_and_delete_wdgt_instances_with_name(wdgt_name):
    """
    Search for all occurences with wdgt_name and delete them.
    """

    #get_wdgt_closure
    get_wdgt_closure = get_widget_by_name_closure(wdgt_name)

    #wdgt_asset_manager_list
    wdgt_asset_manager_list = filter(get_wdgt_closure, QtGui.QApplication.allWidgets())

    #iterate and delete
    for index, wdgt_asset_manager in enumerate(wdgt_asset_manager_list):

        try:
            #mute logger
            wdgt_asset_manager.status_handler.wdgt_status = None
            #delete
            wdgt_asset_manager.deleteLater()
       
        except:
            pass

    return wdgt_asset_manager_list













#form_class, base_class
#------------------------------------------------------------------

#ui_file
ui_file_name = 'asset_manager.ui'
ui_file = os.path.join(media_path, ui_file_name)

#form_class, base_class
form_class, base_class = global_functions.load_ui_type(ui_file)








#AssetManager class
#------------------------------------------------------------------
class AssetManager(form_class, base_class):

    def __new__(cls, *args, **kwargs):
        """
        AssetManager instance factory.
        """

        #delete old instances
        check_and_delete_wdgt_instances_with_name(cls.__name__)

        #asset_manager_instance
        asset_manager_instance = super(AssetManager, cls).__new__(cls, args, kwargs)

        return asset_manager_instance

    
    def __init__(self, 
                logging_level = logging.DEBUG,
                auto_update_models = True,
                parent = global_functions.get_main_window()):
        """
        Customize instance.
        """

        #super
        self.parent_class = super(AssetManager, self)
        self.parent_class.__init__(parent)

        #setObjectName
        self.setObjectName(self.__class__.__name__)


        #instance variables
        #------------------------------------------------------------------
        self.title_name = self.__class__.__name__
        self.version = 0.1
        self.title = self.title_name +' ' + str(self.version)
        self.icon_path = os.path.join(icons_path, 'icon_asset_manager.png')

        #asset_manager_functionality
        self.asset_manager_functionality = asset_manager_functionality.AssetManagerFunctionality()

        #auto_update_models
        self.auto_update_models = auto_update_models
        #auto_update_timer
        self.auto_update_timer = None

        #shot_metadata_list
        self.shot_metadata_list = []
        #prop_metadata_list
        self.prop_metadata_list = []
        #char_metadata_list
        self.char_metadata_list = []

        

        
        #logger
        #------------------------------------------------------------------
        #logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logging_level = logging_level
        self.logger.setLevel(self.logging_level)

        #status_handler
        self.status_handler = asset_manager_logging_handler.StatusStreamHandler(self)
        self.logger.addHandler(self.status_handler)
        

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
        
        #make sure its floating intead of embedded
        self.setWindowFlags(QtCore.Qt.Window)

        #set title
        self.setWindowTitle(self.title)

        #helga_tool_header
        self.wdgt_helga_header = global_functions.get_helga_header_widget(self.title, self.icon_path)
        self.lyt_header.addWidget(self.wdgt_helga_header)

        #setup_stacked_widget
        self.setup_stacked_widget() #buttons and widgets

        #setup_progressbar
        self.setup_progressbar()

        #setup_mvc
        self.setup_mvc()

        #auto_update_models
        if(self.auto_update_models):
            self.setup_auto_update_models()

        #set_margins_and_spacing
        self.set_margins_and_spacing()

        #set_stylesheet
        QtGui.qApp.setStyleSheet(asset_manager_stylesheets.get_stylesheet())


    def connect_ui(self):
        """
        Connect UI widgets with slots or functions.
        """
        
        #btn_show_shot_metadata
        self.btn_show_shot_metadata.clicked.connect(functools.partial(self.stkwdgt_metadata.setCurrentIndex, 0))
        #btn_show_prop_metadata
        self.btn_show_prop_metadata.clicked.connect(functools.partial(self.stkwdgt_metadata.setCurrentIndex, 1))
        #btn_show_char_metadata
        self.btn_show_char_metadata.clicked.connect(functools.partial(self.stkwdgt_metadata.setCurrentIndex, 2))

        #btn_export
        self.btn_export.clicked.connect(functools.partial(self.dummy_method, 'Export'))

        #btn_update_models
        if not(self.auto_update_models):
            self.btn_update_models.clicked.connect(self.update_models)


    def setup_stacked_widget(self):
        """
        Setup stacked widget ui to test sweet ui design.
        """

        #setup_stacked_widget_pages
        self.setup_stacked_widget_pages()

        #setup_stacked_widget_buttons
        self.setup_stacked_widget_buttons()

    
    def setup_stacked_widget_pages(self):
        """
        Setup stacked widget pages
        """

        #wdgt_shot_metadata
        self.wdgt_shot_metadata = QtGui.QWidget()
        self.lyt_shot_metadata = QtGui.QVBoxLayout()
        self.wdgt_shot_metadata.setLayout(self.lyt_shot_metadata)
        self.customize_palette(self.wdgt_shot_metadata, 
                                self.wdgt_shot_metadata.backgroundRole(), 
                                QtCore.Qt.green)

        #wdgt_prop_metadata
        self.wdgt_prop_metadata = QtGui.QWidget()
        self.lyt_prop_metadata = QtGui.QVBoxLayout()
        self.wdgt_prop_metadata.setLayout(self.lyt_prop_metadata)
        self.customize_palette(self.wdgt_prop_metadata, 
                                self.wdgt_prop_metadata.backgroundRole(), 
                                QtCore.Qt.blue)

        #wdgt_char_metadata
        self.wdgt_char_metadata = QtGui.QWidget()
        self.lyt_char_metadata = QtGui.QVBoxLayout()
        self.wdgt_char_metadata.setLayout(self.lyt_char_metadata)
        self.customize_palette(self.wdgt_char_metadata, 
                                self.wdgt_char_metadata.backgroundRole(), 
                                QtCore.Qt.red)
        

        
        

        #stkwdgt_metadata
        self.stkwdgt_metadata =  QtGui.QStackedWidget()
        self.stkwdgt_metadata.addWidget(self.wdgt_shot_metadata)
        self.stkwdgt_metadata.addWidget(self.wdgt_prop_metadata)
        self.stkwdgt_metadata.addWidget(self.wdgt_char_metadata)
        
        #add stkwdgt_metadata to layout
        self.lyt_stacked_widget_container.addWidget(self.stkwdgt_metadata, 1, 1)


    def setup_stacked_widget_buttons(self):
        """
        Setup stacked widget buttons
        """

        #btn_show_shot_metadata
        self.btn_show_shot_metadata = asset_manager_button.AssetManagerButton( icon_name = 'icn_docs.png',
                                                                                icon_hover_name = 'icn_export.png', 
                                                                                parent = self)
        self.btn_show_shot_metadata.setObjectName('btn_show_shot_metadata')
        self.lyt_metadata_buttons.addWidget(self.btn_show_shot_metadata)
        

        #btn_show_prop_metadata
        self.btn_show_prop_metadata = asset_manager_button.AssetManagerButton(icon_name = 'icn_docs.png',
                                                                                icon_hover_name = 'icn_export.png', 
                                                                                parent = self)
        self.btn_show_prop_metadata.setObjectName('btn_show_prop_metadata')
        self.lyt_metadata_buttons.addWidget(self.btn_show_prop_metadata)
        

        #btn_show_char_metadata
        self.btn_show_char_metadata = asset_manager_button.AssetManagerButton(icon_name = 'icn_docs.png',
                                                                                icon_hover_name = 'icn_export.png', 
                                                                                parent = self)
        self.btn_show_char_metadata.setObjectName('btn_show_char_metadata')
        self.lyt_metadata_buttons.addWidget(self.btn_show_char_metadata)
        

        #setup_model_update_button
        if not(self.auto_update_models):
            self.setup_model_update_button()

        #setup_export_button
        self.setup_export_button()


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
            lyt.setContentsMargins(*margin_list)
            lyt.setSpacing(0)


    def setup_export_button(self):
        """
        Create self.btn_export
        """

        #btn_export
        self.btn_export = QtGui.QPushButton(text = 'Export', parent = self)

        #add to lyt_buttons
        self.lyt_metadata_buttons.addWidget(self.btn_export)


    def setup_model_update_button(self):
        """
        Create self.btn_update_models
        """

        #btn_update_models
        self.btn_update_models = QtGui.QPushButton(text = 'Update Models', parent = self)

        #add to lyt_buttons
        self.lyt_metadata_buttons.addWidget(self.btn_update_models)


    def setup_progressbar(self):
        """
        Setup self.progressbar.
        """

        #progressbar
        self.progressbar = QtGui.QProgressBar()
        #customize
        self.progressbar.setTextVisible(False)
        self.progressbar.setValue(30)
        self.progressbar.setOrientation(QtCore.Qt.Vertical)
        self.progressbar.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)

        #add to lyt
        self.lyt_metadata_progress.addWidget(self.progressbar)
        
    
    def setup_mvc(self):
        """
        Setup all model-view controller.
        """

        #setup_mvc_shot_metadata
        self.setup_mvc_shot_metadata()


    def setup_mvc_shot_metadata(self):
        """
        Setup model-view controller for shot metadata.
        """
    
        #shot_metadata_view
        self.shot_metadata_view = shot_metadata_view.ShotMetadataView(self.logging_level)
        self.shot_metadata_view.setWordWrap(True)
        #set resize mode for horizontal header
        self.shot_metadata_view.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.shot_metadata_view.horizontalHeader().setStretchLastSection(True)
        self.shot_metadata_view.verticalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.shot_metadata_view.setAlternatingRowColors(True)
        #add to ui
        self.lyt_shot_metadata.addWidget(self.shot_metadata_view)

        #shot_metadata_item_delegate
        self.shot_metadata_item_delegate = shot_metadata_item_delegate.ShotMetadataItemDelegate(self.logging_level)
        #set in view
        self.shot_metadata_view.setItemDelegate(self.shot_metadata_item_delegate)

        
        #shot_metadata_model
        self.shot_metadata_model = shot_metadata_model.ShotMetadataModel(self.logging_level)
        #set model in view
        self.shot_metadata_view.setModel(self.shot_metadata_model)

        #shot_metadata_selection_model
        self.shot_metadata_selection_model = QtGui.QItemSelectionModel(self.shot_metadata_model)
        self.shot_metadata_view.setSelectionModel(self.shot_metadata_selection_model)
    



    #MVC methods
    #------------------------------------------------------------------

    def convert_list_for_tablemodel(self, list_to_convert):
        """
        [obj, obj, obj] >> [[obj], [obj], [obj]]
        """

        #list false
        if not (list_to_convert):
            return [[]]

        #table_model_list
        table_model_list = [[pynode] for pynode in list_to_convert]

        return table_model_list


    def setup_auto_update_models(self, interval = 2000):
        """
        Create QTimer to automatically trigger update_models in intervals.
        """

        #auto_update_timer
        self.auto_update_timer = QtCore.QTimer(self)
        self.auto_update_timer.timeout.connect(self.update_models)
        self.auto_update_timer.start(interval)

    
    def update_models(self):
        """
        Update all models.
        """

        #update if neccessary
        if (self.update_models_necessary()):

            #log
            print('Update models: {0}'.format(time.time()))
            
            #update_shotmetadata_model
            self.update_shotmetadata_model()

            #update_propmetadata_model
            self.update_propmetadata_model()

            #update_charmetadata_model
            self.update_charmetadata_model()


    def get_hashstring_from_list(self, list_to_convert):
        """
        Convert a list to a hashable string.
        """

        #if list_to_convert empty
        if not (list_to_convert):
            return ''
        

        #sorted_list
        sorted_list = sorted([pynode.name() for pynode in list_to_convert])

        #hashable_string
        hashable_string = ''

        #iterate and concatenate
        for name in sorted_list:
            hashable_string += name

        return hashable_string


    def update_models_necessary(self):
        """
        Hash and check model metadata lists and 
        decide if update_models() is necessary.
        """

        #model data

        #shot_metadata_list_string
        shot_metadata_list_string = self.get_hashstring_from_list(self.shot_metadata_list)
        #prop_metadata_list_string
        prop_metadata_list_string = self.get_hashstring_from_list(self.prop_metadata_list)
        #char_metadata_list_string
        char_metadata_list_string = self.get_hashstring_from_list(self.char_metadata_list)

        #current_metadata_lists_string
        current_metadata_lists_string = shot_metadata_list_string + prop_metadata_list_string + char_metadata_list_string
        current_metadata_lists_string = str(current_metadata_lists_string)
        

        #current_metadata_lists_hash_object
        current_metadata_lists_hash_object = hashlib.sha1(bytearray(current_metadata_lists_string))
        current_model_lists_hex_digest = current_metadata_lists_hash_object.hexdigest()
        


        #scene data
        
        #new_shot_metadata_list
        new_shot_metadata_list = self.asset_manager_functionality.get_nodes_of_type('HelgaShotsMetadata')
        #new_prop_metadata_list
        new_prop_metadata_list = self.asset_manager_functionality.get_nodes_of_type('HelgaPropMetadata')
        #new_char_metadata_list
        new_char_metadata_list = self.asset_manager_functionality.get_nodes_of_type('HelgaCharacterMetadata')

        #new_shot_metadata_list_string
        new_shot_metadata_list_string = self.get_hashstring_from_list(new_shot_metadata_list)
        #new_prop_metadata_list_string
        new_prop_metadata_list_string = self.get_hashstring_from_list(new_prop_metadata_list)
        #new_char_metadata_list_string
        new_char_metadata_list_string = self.get_hashstring_from_list(new_char_metadata_list)

        #new_metadata_lists_string
        new_metadata_lists_string = new_shot_metadata_list_string + new_prop_metadata_list_string + new_char_metadata_list_string
        new_metadata_lists_string = str(new_metadata_lists_string)
        

        #new_metadata_lists_hash_object
        new_metadata_lists_hash_object = hashlib.sha1(bytearray(new_metadata_lists_string))
        new_model_lists_hex_digest = new_metadata_lists_hash_object.hexdigest()
        


        #compare and return
        if(new_model_lists_hex_digest == current_model_lists_hex_digest):
            return False

        return True


    def update_shotmetadata_model(self):
        """
        Update self.shot_metadata_model
        """

        #set_shot_metadata_list from scene
        self.set_shot_metadata_list()

        #list_for_tablemodel
        table_model_list = self.convert_list_for_tablemodel(self.shot_metadata_list)

        #set in model
        self.shot_metadata_model.update(table_model_list)


    def update_propmetadata_model(self):
        """
        Update self.prop_metadata_model
        """

        #set_prop_metadata_list from scene
        self.set_prop_metadata_list()

        '''
        #list_for_tablemodel
        table_model_list = self.convert_list_for_tablemodel(self.shot_metadata_list)

        #set in model
        self.shot_metadata_model.update(table_model_list)
        '''


    def update_charmetadata_model(self):
        """
        Update self.char_metadata_model
        """

        #set_char_metadata_list from scene
        self.set_char_metadata_list()

        '''
        #list_for_tablemodel
        table_model_list = self.convert_list_for_tablemodel(self.shot_metadata_list)

        #set in model
        self.shot_metadata_model.update(table_model_list)
        '''


    #Getter & Setter
    #------------------------------------------------------------------

    def set_status(self, new_value):
        """
        Set le_status text
        """
        
        #clear
        self.le_status.clear()
        #set text
        self.le_status.setText(new_value)
        

    def get_status(self):
        """
        Return content of le_status
        """

        return str(self.le_status.text())


    def customize_palette(self, wdgt, role, color):
        """
        Set background color for widget.
        """

        #setAutoFillBackground
        try:
            if(role == wdgt.backgroundRole()):
                wdgt.setAutoFillBackground(True)
        except:
            pass
        
        try:
            
            #palette_to_customize
            palette_to_customize = wdgt.palette()
            #set color
            palette_to_customize.setColor(role, color)
            wdgt.setPalette(palette_to_customize)
        
        except:

            #log
            self.logger.debug('Error setting palette for {0} - {1}'.format(wdgt.objectName(), wdgt))



    def set_shot_metadata_list(self):
        """
        Set self.shot_metadata_list
        """
        
        self.shot_metadata_list = self.asset_manager_functionality.get_nodes_of_type('HelgaShotsMetadata')


    def set_prop_metadata_list(self):
        """
        Set self.prop_metadata_list
        """
        
        self.prop_metadata_list = self.asset_manager_functionality.get_nodes_of_type('HelgaPropMetadata')


    def set_char_metadata_list(self):
        """
        Set self.char_metadata_list
        """
        
        self.char_metadata_list = self.asset_manager_functionality.get_nodes_of_type('HelgaCharacterMetadata')






    #Events
    #------------------------------------------------------------------

    def closeEvent(self, event):
        """
        Customized closeEvent
        """

        #stop timer
        if(self.auto_update_timer):
            self.auto_update_timer.stop()

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

        #asset_manager_functionality test
        print(self.asset_manager_functionality.get_nodes_of_type('HelgaShotsMetadata'))

        #------------------------------------------------------------------



        #log
        self.logger.debug('\n\n-----------------------------\nFinished test methods.')


    








#Run
#------------------------------------------------------------------

def run():
    """
    Standardized run() method
    """
    
    #asset_manager_instance
    asset_manager_instance = AssetManager()
    asset_manager_instance.show()












#Test
#------------------------------------------------------------------

if (__name__ == '__main__'):

    #run
    run()