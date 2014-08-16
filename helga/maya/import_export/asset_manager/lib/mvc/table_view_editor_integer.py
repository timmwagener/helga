

"""
table_view_editor_integer
==========================================

Editor created in EditRole in QItemDelegate.

-----------------------

**Author:** `Timm Wagener <mailto:wagenertimm@gmail.com>`_
"""











#Add tool relative pathes
#------------------------------------------------------------------

#import
import sys
import os

#tool_root_path
tool_root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir))
print(tool_root_path)
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

























#form_class, base_class
#------------------------------------------------------------------

#ui_file
ui_file_name = 'table_view_editor_integer.ui'
ui_file = os.path.join(media_path, ui_file_name)

#form_class, base_class
form_class, base_class = global_functions.load_ui_type(ui_file)








#TableViewEditorInteger class
#------------------------------------------------------------------
class TableViewEditorInteger(form_class, base_class):

    
    def __new__(cls, *args, **kwargs):
        """
        TableViewEditorInteger instance factory.
        """

        #table_view_editor_integer_instance
        table_view_editor_integer_instance = super(TableViewEditorInteger, cls).__new__(cls, args, kwargs)

        return table_view_editor_integer_instance

    
    def __init__(self, 
                logging_level = logging.DEBUG,
                parent = None):
        """
        Customize instance.
        """

        #super
        self.parent_class = super(TableViewEditorInteger, self)
        self.parent_class.__init__(parent)

        #setObjectName
        self.setObjectName(self.__class__.__name__)


        #instance variables
        #------------------------------------------------------------------
        self.title_name = self.__class__.__name__
        self.version = 0.1
        self.title = self.title_name +' ' + str(self.version)
        self.icon_path = os.path.join(icons_path, 'icon_asset_manager.png')

        
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

        #make frameless
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Window | QtCore.Qt.WindowSystemMenuHint)
        #self.setColor(QtGui.QColor(QtCore.Qt.transparent))

        
        #make sure its floating intead of embedded
        self.setWindowFlags(QtCore.Qt.Window)

        #set title
        self.setWindowTitle(self.title)

        #helga_tool_header
        self.wdgt_helga_header = global_functions.get_helga_header_widget(self.title, self.icon_path)
        self.lyt_header.addWidget(self.wdgt_helga_header)

        
        
    
    def connect_ui(self):
        """
        Connect UI widgets with slots or functions.
        """
        
        pass
        
    
    


    #Getter & Setter
    #------------------------------------------------------------------

    def set_integer(self, value):
        """
        Set self.spnbx_integer
        """

        self.spnbx_integer.setValue(int(value))


    def get_integer(self):
        """
        Set self.spnbx_integer
        """

        return self.spnbx_integer.value()






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
    
    #table_view_editor_integer_instance
    table_view_editor_integer_instance = TableViewEditorInteger()
    table_view_editor_integer_instance.show()












#Test
#------------------------------------------------------------------

if (__name__ == '__main__'):

    #run
    run()
