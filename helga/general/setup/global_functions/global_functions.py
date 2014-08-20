
"""
global_functions
==========================================

Simple but hopefully helpful module to that bundles all
functions in a central place.

-----------------------

Usage
-----

::
    
    from helga.general.setup.global_functions import global_functions
    reload(global_functions)

    #some example here
    global_functions.example_function()

-----------------------
"""



#Import
#----------------------------------------------------
#python
import os
import sys
import logging
import re
import shutil
from cStringIO import StringIO
import xml.etree.ElementTree as xml
import types



#Import variable
do_reload = True

#global_variables
from helga.general.setup.global_variables import global_variables
if(do_reload):reload(global_variables)













#Functions
#----------------------------------------------------


#OS
#----------------------------------------------------

#check_interpreter
def check_interpreter(keyword):
    """
        Check if the current interpreter matches keyword
    """

    #current_interpreter_path
    current_interpreter_path = sys.executable

    #session is mayapy
    if(keyword in current_interpreter_path): 
        return True

    return False


#get_user
def get_user():
    
    return os.environ.get('USERNAME')


#copy_file
def copy_file(source_file, source_dir, destination_dir):
    
    source = source_dir + '/' +source_file
    
    shutil.copy(source, destination_dir)





















#DCC
#----------------------------------------------------

#get_user_setup_destination_dir
def get_user_setup_destination_dir(dcc):
    
    if (dcc == 'maya'):
        return get_user_setup_destination_dir_maya()
    elif (dcc == 'nuke'):
        return get_user_setup_destination_dir_nuke()
    elif (dcc == 'houdini'):
        return get_user_setup_destination_dir_houdini()


#get_user_setup_destination_dir_maya
def get_user_setup_destination_dir_maya():

    path_start = 'C:/Users/'
    username = get_user()
    path_end = '/Documents/maya/{0}/scripts'.format(global_variables.MAYA_VERSION)
    
    return path_start + username + path_end


#get_user_setup_destination_dir_nuke
def get_user_setup_destination_dir_nuke():

    path_start = 'C:/Users/'
    username = get_user()
    path_end = '/.nuke'
    
    return path_start + username + path_end


#get_user_setup_destination_dir_houdini
def get_user_setup_destination_dir_houdini():

    path_start = 'C:/Users/'
    username = get_user()
    path_end = '/Documents/houdini{0}'.format(global_variables.HOUDINI_VERSION)
    
    return path_start + username + path_end


#get_main_window
def get_main_window():
    """
        Determine current application and return main window for parenting of own windows.
    """

    #maya
    if(check_interpreter('maya')):
        return get_maya_main_window()
    #Nuke
    elif(check_interpreter('Nuke')):
        return get_nuke_main_window()

    #Application unknown
    return None



#get_maya_main_window
def get_maya_main_window():
    """
        Return the Maya main window.
    """

    try:
        #PySide
        from PySide import QtGui
        from PySide import QtCore
        import shiboken
        #maya
        import maya.OpenMayaUI as open_maya_ui

    except Exception as exception_instance:

        #log
        print('Import failed: {0}'.format(exception_instance))
        #return None
        return None

    

    #ptr_main_window
    ptr_main_window = open_maya_ui.MQtUtil.mainWindow()
    
    #if True
    if (ptr_main_window):
        return shiboken.wrapInstance(long(ptr_main_window), QtGui.QWidget)

    return None


#get_nuke_main_window
def get_nuke_main_window():
    """
        Return the Maya main window.
    """

    try:
        #PySide
        from PySide import QtGui
        from PySide import QtCore
        

    except Exception as exception_instance:

        #log
        print('Import failed: {0}'.format(exception_instance))
        #return None
        return None

    

    #ptr_main_window
    ptr_main_window = QtGui.QApplication.activeWindow()
    
    #if True
    if (ptr_main_window):
        return ptr_main_window

    return None


#divider
def divider():
    """
        Print divider line to __stdout__
    """

    print('----------------------------------------------------')
















#GUI
#----------------------------------------------------

def create_widget_from_ui_file(ui_file_path, parent =None):
    """
    Create widget that remains stylesheets from .ui file.
    This method is crashy at least in Maya. Probably because of stylesheet
    issues with Maya QApp custom style.
    Use with caution.
    """

    #lazy import

    try:
        
        #PySide
        from PySide import QtGui
        from PySide import QtCore
        from PySide import QtUiTools
        import shiboken
        import pysideuic

    except Exception as exception_instance:
        #log
        print('Import failed: {0}'.format(exception_instance))
        #return None
        return None


    #create widget

    #Create widget from ui file
    loader_instance = QtUiTools.QUiLoader()
    #file to load in as unicode obj
    ui_file = QtCore.QFile(ui_file_path)
    ui_file.open(QtCore.QFile.ReadOnly)
    #Create Widget
    ui_file_widget = loader_instance.load(ui_file, parent)
    #close ui_File
    ui_file.close()

    return ui_file_widget
     

def load_ui_type(ui_file):
    """
    Pyside lacks the "loadUiType" command, so we have to convert the ui file to py code in-memory first
    and then execute it in a special frame to retrieve the form_class.
    This function return the form and base classes for the given qtdesigner ui file.
    """

    #lazy import

    try:
        
        #PySide
        from PySide import QtGui
        from PySide import QtCore
        from PySide import QtUiTools
        import shiboken
        import pysideuic

    except Exception as exception_instance:
        #log
        print('Import failed: {0}'.format(exception_instance))
        #return None
        return None
    
    
    #compile ui

    parsed = xml.parse(ui_file)
    widget_class = parsed.find('widget').get('class')
    form_class = parsed.find('class').text

    with open(ui_file, 'r') as f:
        o = StringIO()
        frame = {}

        pysideuic.compileUi(f, o, indent=0)
        pyc = compile(o.getvalue(), '<string>', 'exec')
        exec pyc in frame

        #Fetch the base_class and form class based on their type in the xml from designer
        form_class = frame['Ui_%s'%form_class]
        base_class = eval('QtGui.%s'%widget_class)
    
    return form_class, base_class


def get_helga_header_widget(title, icon_path):
    """
    Return QWidget that represents a helga header.
    The returned widget needs to be added to a layout.
    """

    #lazy import

    try:
        #PySide
        from PySide import QtGui
        from PySide import QtCore
        from PySide import QtUiTools
        import shiboken
        import pysideuic

    except Exception as exception_instance:
        #log
        print('Import failed: {0}'.format(exception_instance))
        #return None
        return None
    

    
    class GradientWidget(QtGui.QWidget):
        """
        Widget that draws a gradient in the background.
        """

        def __init__(self, parent = None):
            """
            init
            """

            #superclass init
            super(GradientWidget, self).__init__(parent)

        
        def paintEvent(self, event):
            """
            Subclassed paintEvent
            """

            #painter
            painter = QtGui.QPainter(self)

            #gradient
            gradient = QtGui.QLinearGradient(QtCore.QPointF(self.rect().x(), self.rect().y()), 
                                                QtCore.QPointF(self.rect().width(), self.rect().height()))
            gradient.setColorAt(0, QtCore.Qt.white)
            gradient.setColorAt(1, QtCore.Qt.transparent)

            #brush
            brush = QtGui.QBrush(gradient)

            #paint
            painter.fillRect(self.rect(), brush)
    

    

    #wdgt_helga_header
    wdgt_helga_header = QtGui.QWidget()
    wdgt_helga_header.setObjectName("wdgt_helga_header")
    wdgt_helga_header.resize(439, 52)

    #lyt_helga_header
    lyt_helga_header = QtGui.QHBoxLayout(wdgt_helga_header)
    lyt_helga_header.setSpacing(0)
    lyt_helga_header.setContentsMargins(0, 0, 0, 0)
    lyt_helga_header.setObjectName("lyt_helga_header")

    #icn_helga_header_image
    icn_helga_header_image = QtGui.QPixmap(icon_path)
    icn_helga_header_image = icn_helga_header_image.scaled(32, 32)
    
    #lbl_helga_header_image
    lbl_helga_header_image = QtGui.QLabel(wdgt_helga_header)
    lbl_helga_header_image.setPixmap(icn_helga_header_image)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(lbl_helga_header_image.sizePolicy().hasHeightForWidth())
    lbl_helga_header_image.setSizePolicy(sizePolicy)
    lbl_helga_header_image.setBaseSize(QtCore.QSize(32, 0))
    lbl_helga_header_image.setObjectName("lbl_helga_header_image")
    lyt_helga_header.addWidget(lbl_helga_header_image)
    
    
    #wdgt_header_text
    wdgt_header_text = GradientWidget(wdgt_helga_header)
    wdgt_header_text.setObjectName("wdgt_header_text")
    lyt_helga_header.addWidget(wdgt_header_text)

    #lyt_header_text
    lyt_header_text = QtGui.QHBoxLayout(wdgt_header_text)
    lyt_header_text.setContentsMargins(0, 0, 0, 0)
    lyt_header_text.setObjectName("lyt_header_text")
    
    #wdgt_header_spacer_left
    wdgt_header_spacer_left = QtGui.QWidget(wdgt_header_text)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(wdgt_header_spacer_left.sizePolicy().hasHeightForWidth())
    wdgt_header_spacer_left.setSizePolicy(sizePolicy)
    wdgt_header_spacer_left.setObjectName("wdgt_header_spacer_left")
    lyt_header_text.addWidget(wdgt_header_spacer_left)
    
    #lbl_header_text
    lbl_header_text = QtGui.QLabel(wdgt_header_text)
    lbl_header_text.setText(title)
    lbl_header_text.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"+"color: rgb(241, 113, 37);\n"+"font: 75 12pt \"MS Shell Dlg 2\";")
    lbl_header_text.setObjectName("lbl_header_text")
    lyt_header_text.addWidget(lbl_header_text)
    
    #wdgt_header_spacer_right
    wdgt_header_spacer_right = QtGui.QWidget(wdgt_header_text)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(wdgt_header_spacer_right.sizePolicy().hasHeightForWidth())
    wdgt_header_spacer_right.setSizePolicy(sizePolicy)
    wdgt_header_spacer_right.setMinimumSize(QtCore.QSize(0, 0))
    wdgt_header_spacer_right.setMaximumSize(QtCore.QSize(32, 16777215))
    wdgt_header_spacer_right.setObjectName("wdgt_header_spacer_right")
    lyt_header_text.addWidget(wdgt_header_spacer_right)
    
    

    #return
    return wdgt_helga_header


def get_maya_toplevel_shelf_widget(shelf_object):
    """
    Convert ptr to shelf object to Qt instance.
    """

    #Lazy Import
    #----------------------------------------------------
    #PySide
    from PySide import QtGui
    from PySide import QtCore
    from PySide import QtUiTools
    import shiboken
    import pysideuic
    #maya
    import maya.OpenMayaUI as open_maya_ui
    import pymel.core as pm
    #----------------------------------------------------

    
    #ptr_shelf_object
    ptr_shelf_object = open_maya_ui.MQtUtil.findLayout(shelf_object)
    #ptr exists
    if (ptr_shelf_object is not None):
        return shiboken.wrapInstance(long(ptr_shelf_object), QtGui.QWidget)
    #else
    return None


def style_maya_shelves():
    """
    Style Maya shelves.
    """

    #Lazy Import
    #----------------------------------------------------
    #PySide
    from PySide import QtGui
    from PySide import QtCore
    from PySide import QtUiTools
    import shiboken
    import pysideuic
    #maya
    import pymel.core as pm
    #----------------------------------------------------


        
    #Tabwidgets (Shelves)
    #----------------------------------------------------

    #wdgt_toplevel_shelf_name
    wdgt_toplevel_shelf_name = pm.MelGlobals()['gShelfTopLevel']

    #wdgt_toplevel_shelf
    wdgt_toplevel_shelf = get_maya_toplevel_shelf_widget(wdgt_toplevel_shelf_name)

    #shelf not found
    if not(wdgt_toplevel_shelf):
        print('Shelf {0} not found. Not customizing, returning.'.format(wdgt_toplevel_shelf_name))
        return None


    #tab_wdgt_list
    tab_wdgt_list = [tab_wdgt for tab_wdgt in wdgt_toplevel_shelf.findChildren(QtGui.QTabWidget)]
    
    
    


    #Stylesheets
    #----------------------------------------------------

    #ss_shelf
    ss_shelf = " \
\
\
QWidget#%s { background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0.5 rgba(0, 0, 0, 0), stop:1 rgba(255, 255, 255, 255)); }\
\
\
"
    
    #----------------------------------------------------




    #Style
    #----------------------------------------------------
    
    #iterate and style
    for tab_wdgt in tab_wdgt_list:

        #index
        index = tab_wdgt.count()

        #setDocumentMode
        tab_wdgt.setDocumentMode(True)

        #iterate and style page
        for index in range(index):
            
            #wdgt_page
            wdgt_page = tab_wdgt.widget(index)

            #iterate scrollareas
            for wdgt_scrollarea in wdgt_page.findChildren(QtGui.QScrollArea):

                #wdgt_scrollarea_child
                wdgt_scrollarea_child = wdgt_scrollarea.widget()
                
                try:

                    #set_stylesheet
                    wdgt_scrollarea_child.setStyleSheet(ss_shelf%(wdgt_scrollarea_child.objectName()))

                except:
                    pass













#Test
#----------------------------------------------------

if(__name__ == '__main__'):

    #style_maya_shelves
    #style_maya_shelves()
    pass


