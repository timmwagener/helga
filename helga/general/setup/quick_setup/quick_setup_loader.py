

"""
quick_setup_loader
==========================================

Helper module to enable import of quick_setup.
This module makes sure the __file__ attribute of the quick_setup module delivers
a path.

-----------------------
"""





#Import
#------------------------------------------------------------------
#python
import sys
import os
import functools
import logging
import subprocess
#PyQt4
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import uic
#qdarkstyle
import qdarkstyle


#Import variable
do_reload = True

#quick_setup
import quick_setup
if(do_reload):reload(quick_setup)











#load_quick_setup
#------------------------------------------------------------------

#load_quick_setup
def load_quick_setup():
    """
    Start an QApp loop and load an instance of QuickSetup in it.
    """

    #app_quick_setup
    app_quick_setup = QtGui.QApplication(sys.argv)

    #load darkstyle
    app_quick_setup.setStyleSheet(qdarkstyle.load_stylesheet(pyside=False))

    #quick_setup_instance
    quick_setup_instance = quick_setup.QuickSetup()

    #exit
    sys.exit(app_quick_setup.exec_())







#Run if not imported
#------------------------------------------------------------------
if (__name__ == '__main__'):

    #load_quick_setup
    load_quick_setup()
    
    
    
    
        

        