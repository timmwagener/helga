

"""
table_view_editor_framerange
==========================================

Editor created in EditRole in QItemDelegate. It allows for comfortable
control for setting an integer value from a framerange.

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

#asset_manager_stylesheets
from lib import asset_manager_stylesheets
if(do_reload):reload(asset_manager_stylesheets)

#asset_manager_hover_button
from lib import asset_manager_hover_button
if(do_reload):reload(asset_manager_hover_button)

#asset_manager_functionality
from lib import asset_manager_functionality
if(do_reload):reload(asset_manager_functionality)



















#form_class, base_class
#------------------------------------------------------------------

#ui_file
ui_file_name = 'table_view_editor_framerange.ui'
ui_file = os.path.join(media_path, ui_file_name)

#form_class, base_class
form_class, base_class = global_functions.load_ui_type(ui_file)








#TableViewEditorFramerange class
#------------------------------------------------------------------
class TableViewEditorFramerange(form_class, base_class):

    
    def __new__(cls, *args, **kwargs):
        """
        TableViewEditorFramerange instance factory.
        """

        #table_view_editor_framerate_instance
        table_view_editor_framerate_instance = super(TableViewEditorFramerange, cls).__new__(cls, args, kwargs)

        return table_view_editor_framerate_instance

    
    def __init__(self, 
                logging_level = logging.DEBUG,
                parent = None):
        """
        Customize instance.
        """

        #super
        self.parent_class = super(TableViewEditorFramerange, self)
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

        #setMouseTracking
        self.setMouseTracking(True)

        #make frameless and invisible
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Window | QtCore.Qt.WindowSystemMenuHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        
        #replace_temp_buttons
        self.replace_temp_buttons()

        #set title
        self.setWindowTitle(self.title)

        #setup_style
        self.setup_style()

    
    def connect_ui(self):
        """
        Connect UI widgets with slots or functions.
        """

        #btn_get_current_frame
        self.btn_get_current_frame.hover_enter.connect(functools.partial(self.set_label, 'Set frame from current'))
        self.btn_get_current_frame.hover_leave.connect(functools.partial(self.set_label, 'Set frame'))
        self.btn_get_current_frame.clicked.connect(functools.partial(self.set_frame_from_ui, self.btn_get_current_frame))

        
        #btn_complete_range_start
        self.btn_complete_range_start.hover_enter.connect(functools.partial(self.set_label, 'Set frame from complete range start'))
        self.btn_complete_range_start.hover_leave.connect(functools.partial(self.set_label, 'Set frame'))
        self.btn_complete_range_start.clicked.connect(functools.partial(self.set_frame_from_ui, self.btn_complete_range_start))

        #btn_current_range_start
        self.btn_current_range_start.hover_enter.connect(functools.partial(self.set_label, 'Set frame from current range start'))
        self.btn_current_range_start.hover_leave.connect(functools.partial(self.set_label, 'Set frame'))
        self.btn_current_range_start.clicked.connect(functools.partial(self.set_frame_from_ui, self.btn_current_range_start))

        #btn_complete_range_end
        self.btn_complete_range_end.hover_enter.connect(functools.partial(self.set_label, 'Set frame from complete range end'))
        self.btn_complete_range_end.hover_leave.connect(functools.partial(self.set_label, 'Set frame'))
        self.btn_complete_range_end.clicked.connect(functools.partial(self.set_frame_from_ui, self.btn_complete_range_end))

        #btn_current_range_end
        self.btn_current_range_end.hover_enter.connect(functools.partial(self.set_label, 'Set frame from current range end'))
        self.btn_current_range_end.hover_leave.connect(functools.partial(self.set_label, 'Set frame'))
        self.btn_current_range_end.clicked.connect(functools.partial(self.set_frame_from_ui, self.btn_current_range_end))
        

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

        #set_stylesheet
        #self.setStyleSheet(asset_manager_stylesheets.get_stylesheet())
    
    


    #Getter & Setter
    #------------------------------------------------------------------

    def set_frame(self, value):
        """
        Set self.spnbx_frame
        """

        self.spnbx_frame.setValue(int(value))


    def set_frame_from_ui(self, wdgt):
        """
        Set self.spnbx_frame from a btn in the ui.
        """

        value = None

        #btn_get_current_frame
        if(wdgt.objectName() == 'btn_get_current_frame'):
            value = self.asset_manager_functionality.get_current_frame()
        
        #btn_complete_range_start
        elif(wdgt.objectName() == 'btn_complete_range_start'):
            value = self.asset_manager_functionality.get_complete_framerange_start()
        
        #btn_complete_range_end
        elif(wdgt.objectName() == 'btn_complete_range_end'):
            value = self.asset_manager_functionality.get_complete_framerange_end()
        
        #btn_current_range_start
        elif(wdgt.objectName() == 'btn_current_range_start'):
            value = self.asset_manager_functionality.get_current_framerange_start()

        #btn_current_range_end
        elif(wdgt.objectName() == 'btn_current_range_end'):
            value = self.asset_manager_functionality.get_current_framerange_end()
        

        #set frame
        self.set_frame(value)




    def get_frame(self):
        """
        Set self.spnbx_frame
        """

        return self.spnbx_frame.value()


    def set_label(self, msg):
        """
        Set self.lbl_framesource
        """

        self.lbl_framesource.setText(msg)


    def get_label(self):
        """
        Return text from self.lbl_framesource
        """

        return str(self.lbl_framesource.text())


    #Methods
    #------------------------------------------------------------------

    def replace_temp_buttons(self):
        """
        Replace temp buttons.
        """

        #tmp_button_list
        tmp_button_list = [self.tmp_btn_get_current_frame,
                            self.tmp_btn_complete_range_end,
                            self.tmp_btn_complete_range_start,
                            self.tmp_btn_current_range_end,
                            self.tmp_btn_current_range_start]


        #btn_get_current_frame
        index = self.lyt_frame_slider.indexOf(self.tmp_btn_get_current_frame)
        self.btn_get_current_frame = asset_manager_hover_button.AssetManagerHoverButton(fixed_width = 30)
        self.btn_get_current_frame.setObjectName('btn_get_current_frame')
        #current_frame
        current_frame = self.asset_manager_functionality.get_current_frame()
        self.btn_get_current_frame.setText('{0}'.format(current_frame))
        self.lyt_frame_slider.insertWidget(index, self.btn_get_current_frame)

        
        

        #btn_complete_range_start
        index = self.lyt_range_slider.indexOf(self.tmp_btn_complete_range_start)
        self.btn_complete_range_start = asset_manager_hover_button.AssetManagerHoverButton(fixed_width = 30)
        self.btn_complete_range_start.setObjectName('btn_complete_range_start')
        #complete_range_start
        complete_range_start = self.asset_manager_functionality.get_complete_framerange_start()
        self.btn_complete_range_start.setText('{0}'.format(complete_range_start))
        self.lyt_range_slider.insertWidget(index, self.btn_complete_range_start)

        
        #btn_current_range_start
        index = self.lyt_range_slider.indexOf(self.tmp_btn_current_range_start)
        self.btn_current_range_start = asset_manager_hover_button.AssetManagerHoverButton(fixed_width = 30)
        self.btn_current_range_start.setObjectName('btn_current_range_start')
        #current_range_start
        current_range_start = self.asset_manager_functionality.get_current_framerange_start()
        self.btn_current_range_start.setText('{0}'.format(current_range_start))
        self.lyt_range_slider.insertWidget(index, self.btn_current_range_start)


        #btn_current_range_end
        index = self.lyt_range_slider.indexOf(self.tmp_btn_current_range_end)
        self.btn_current_range_end = asset_manager_hover_button.AssetManagerHoverButton(fixed_width = 30)
        self.btn_current_range_end.setObjectName('btn_current_range_end')
        #current_range_end
        current_range_end = self.asset_manager_functionality.get_current_framerange_end()
        self.btn_current_range_end.setText('{0}'.format(current_range_end))
        self.lyt_range_slider.insertWidget(index, self.btn_current_range_end)


        #btn_complete_range_end
        index = self.lyt_range_slider.indexOf(self.tmp_btn_complete_range_end)
        self.btn_complete_range_end = asset_manager_hover_button.AssetManagerHoverButton(fixed_width = 30)
        self.btn_complete_range_end.setObjectName('btn_complete_range_end')
        #complete_range_end
        complete_range_end = self.asset_manager_functionality.get_complete_framerange_end()
        self.btn_complete_range_end.setText('{0}'.format(complete_range_end))
        self.lyt_range_slider.insertWidget(index, self.btn_complete_range_end)


        #hide tmp buttons
        for btn in tmp_button_list:
            btn.setParent(None)


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
    
    #table_view_editor_framerange_instance
    table_view_editor_framerange_instance = TableViewEditorFramerange()
    table_view_editor_framerange_instance.show()












#Test
#------------------------------------------------------------------

if (__name__ == '__main__'):

    #run
    run()
