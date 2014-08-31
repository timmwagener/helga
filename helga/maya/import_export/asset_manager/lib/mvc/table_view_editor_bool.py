

"""
table_view_editor_bool
==========================================

Editor created in EditRole in QItemDelegate. It is initialized with a QRect
to set the size from.

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



#asset_manager

#asset_manager_globals
from lib import asset_manager_globals
if(do_reload):reload(asset_manager_globals)









#Globals
#------------------------------------------------------------------

#AssetManager Icons
ICON_TRUE = asset_manager_globals.ICON_TRUE
ICON_FALSE = asset_manager_globals.ICON_FALSE












#TableViewEditorBool class
#------------------------------------------------------------------
class TableViewEditorBool(QtGui.QWidget):

    
    def __new__(cls, *args, **kwargs):
        """
        TableViewEditorBool instance factory.
        """

        #table_view_editor_bool_instance
        table_view_editor_bool_instance = super(TableViewEditorBool, cls).__new__(cls, args, kwargs)

        return table_view_editor_bool_instance

    
    def __init__(self, 
                logging_level = logging.DEBUG,
                value = True,
                parent = None):
        """
        Customize instance.
        """

        #super
        self.parent_class = super(TableViewEditorBool, self)
        self.parent_class.__init__(parent)

        #setObjectName
        self.setObjectName(self.__class__.__name__)


        #instance variables
        #------------------------------------------------------------------

        #value
        self.value = value

        #pxm_bool_true
        self.pxm_bool_true = QtGui.QPixmap(ICON_TRUE)
        #pxm_bool_false
        self.pxm_bool_false = QtGui.QPixmap(ICON_FALSE)

        
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
        Setup additional UI like mvc or helga tool header.
        """

        #make frameless and invisible
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Window | QtCore.Qt.WindowSystemMenuHint)
        

        #lyt_buttons
        self.lyt_buttons = QtGui.QVBoxLayout()
        self.setLayout(self.lyt_buttons)

        #btn_true
        self.btn_true = QtGui.QPushButton('')
        self.btn_true.setObjectName(self.objectName() +'_' + 'btn_true')
        self.btn_true.setFlat(True)
        self.btn_true.setMouseTracking(True)
        self.btn_true.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.lyt_buttons.addWidget(self.btn_true)

        #btn_false
        self.btn_false = QtGui.QPushButton('')
        self.btn_false.setObjectName(self.objectName() +'_' + 'btn_false')
        self.btn_false.setFlat(True)
        self.btn_false.setMouseTracking(True)
        self.btn_false.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.lyt_buttons.addWidget(self.btn_false)



    
    def connect_ui(self):
        """
        Connect UI widgets with slots or functions.
        """

        #btn_true
        self.btn_true.clicked.connect(functools.partial(self.set_value, True))
        #btn_false
        self.btn_false.clicked.connect(functools.partial(self.set_value, False))
        

    def style_ui(self):
        """
        Setup tool palette, tool stylesheet and specific widget stylesheets.
        """

        #correct_styled_background_attribute
        self.correct_styled_background_attribute()

        #set_margins_and_spacing
        self.set_margins_and_spacing()

        #set_icons
        self.set_icon(self.btn_true, True)
        self.set_icon(self.btn_false, False)
    


    



    #Getter & Setter
    #------------------------------------------------------------------

    def set_value(self, value):
        """
        Set self.value
        """

        self.value = value


    def get_value(self):
        """
        Get self.value
        """

        return self.value








    
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


    def set_icon(self, btn, true_or_false):
        """
        Set icon on buttons
        """

        #width, height
        rect_btn = btn.geometry()
        width = rect_btn.width()
        height = rect_btn.height()
        

        #margin
        margin = 5

        #pxm_bool
        if (true_or_false):
            pxm_bool = self.pxm_bool_true.scaledToHeight(height - (margin * 2))
        else:
            pxm_bool = self.pxm_bool_false.scaledToHeight(height - (margin * 2))

        #icn_bool
        icn_bool = QtGui.QIcon(pxm_bool)

        #set icon
        btn.setIcon(icn_bool)




    

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


    




