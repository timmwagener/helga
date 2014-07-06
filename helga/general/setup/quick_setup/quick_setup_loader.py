

"""
quick_setup_loader
==========================================

Helper module to enable import of quick_setup.

-----------------------

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

    #quick_setup_instance
    quick_setup_instance = quick_setup.QuickSetup()

    #exit
    sys.exit(app_quick_setup.exec_())







#Run if not imported
#------------------------------------------------------------------
if (__name__ == '__main__'):

    #load_quick_setup
    load_quick_setup()
    
    
    
    
        

        