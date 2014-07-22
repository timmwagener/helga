
"""
environment_variables_model
==========================================

Subclass of QAbstractTableModel to display env. vars.
"""




#Import
#------------------------------------------------------------------
#python
import logging
#PyQt4
from PyQt4 import QtGui
from PyQt4 import QtCore







#EnvironmentVariablesModel class
#------------------------------------------------------------------
class EnvironmentVariablesModel(QtCore.QAbstractTableModel):
    """
    Class customized to display env. vars.
    """
    
    def __init__(self, 
                logging_level = logging.DEBUG,
                parent=None): 
        
        #super class constructor
        super(EnvironmentVariablesModel, self).__init__(parent)
        
        #header_name_list
        self.header_name_list = ['Env.Variable', 'Value']

        #data_list
        self.data_list = [[]]

    
    def headerData(self, section, orientation, role = QtCore.Qt.DisplayRole):
        
        #horizontal
        if(orientation == QtCore.Qt.Horizontal):
            
            #DisplayRole
            if (role == QtCore.Qt.DisplayRole):
                return self.header_name_list[section]

        #vertical
        elif(orientation == QtCore.Qt.Vertical):
            
            #DisplayRole
            if (role == QtCore.Qt.DisplayRole):
                return section
        
        return QtCore.QAbstractTableModel.headerData(self, section, orientation, role)

    
    def rowCount(self, parent):
        return len(self.data_list) 

    
    def columnCount(self, parent):
        return len(self.data_list[0]) 

    
    def data(self, index, role = QtCore.Qt.DisplayRole):
        
        #row & col
        row = index.row()
        col = index.column()
        
        #DisplayRole
        if (role == QtCore.Qt.DisplayRole):
            
            return self.data_list[row][col]
        
        else:
            return QtCore.QVariant()

    
    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled

    def update(self, data_list):
        
        #set data_list
        self.data_list = data_list
        #reset
        self.reset()
