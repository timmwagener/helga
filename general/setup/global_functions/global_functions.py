
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




#Functions
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




#Test
#----------------------------------------------------

if(__name__ == '__main__'):

    #test interpreter maya
    interpreter_keyword = 'maya'
    print('Interpreter matches keyword {0}: {1}'.format(interpreter_keyword, 
                                                        check_interpreter(interpreter_keyword)))

    #test interpreter nuke
    interpreter_keyword = 'Nuke'
    print('Interpreter matches keyword {0}: {1}'.format(interpreter_keyword, 
                                                        check_interpreter(interpreter_keyword)))

    
    divider()


    #test get_maya_main_window
    maya_main_window = get_maya_main_window()

    if(maya_main_window):
        print('Maya main window: {0} \nof type: {1}'.format(maya_main_window.windowTitle(),
                                                                type(maya_main_window)))
    else:
        print('Maya main window pointer could not be aquired')

    
    divider()

    #test get_nuke_main_window
    nuke_main_window = get_nuke_main_window()

    if(nuke_main_window):
        print('Nuke main window: {0} \nof type: {1}'.format(nuke_main_window.windowTitle(),
                                                                type(nuke_main_window)))
    else:
        print('Nuke main window pointer could not be aquired')


    divider()

    #test get_main_window
    main_window = get_main_window()

    if(main_window):
        print('Main window: {0} \nof type: {1}'.format(main_window.windowTitle(),
                                                                type(main_window)))
    else:
        print('Main window pointer could not be aquired')


