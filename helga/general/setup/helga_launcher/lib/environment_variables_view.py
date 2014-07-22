
"""
environment_variables_view
==========================================

Subclass of QTableView to display env. vars.
"""




#Import
#------------------------------------------------------------------
#python
import logging
#PyQt4
from PyQt4 import QtGui
from PyQt4 import QtCore







#EnvironmentVariablesView class
#------------------------------------------------------------------
class EnvironmentVariablesView(QtGui.QTableView):
    """
    Subclass of QTableView. (...you never know, what you need to override)
    """
    
    def __init__(self, 
                logging_level = logging.DEBUG,
                parent=None): 
        
        #super class constructor
        super(EnvironmentVariablesView, self).__init__(parent)

