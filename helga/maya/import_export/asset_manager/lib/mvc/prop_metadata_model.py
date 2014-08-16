
"""
shot_metadata_model
==========================================

Subclass of QAbstractTableModel to display and edit shot_metadata.
"""




#Import
#------------------------------------------------------------------
#python
import logging
#PySide
from PySide import QtGui
from PySide import QtCore







#ShotMetadataModel class
#------------------------------------------------------------------
class ShotMetadataModel(QtCore.QAbstractTableModel):
    """
    Class customized to display shot metadata.
    """

    def __new__(cls, *args, **kwargs):
        """
        ShotMetadataModel instance factory.
        """

        #shot_metadata_model_instance
        shot_metadata_model_instance = super(ShotMetadataModel, cls).__new__(cls, args, kwargs)

        return shot_metadata_model_instance
    
    
    def __init__(self, 
                logging_level = logging.DEBUG,
                parent=None):
        """
        Customize instance.
        """
        
        #super class init
        super(ShotMetadataModel, self).__init__(parent)


        #instance variables
        #------------------------------------------------------------------

        #header_name_list
        self.header_name_list = ['Shotname', 'Alembic Path', 'Shotcam']

        #data_list
        self.data_list = [[]]
        
        
        #logger
        #------------------------------------------------------------------
        #logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logging_level = logging_level
        self.logger.setLevel(self.logging_level)
        
    
    def headerData(self, section, orientation, role = QtCore.Qt.DisplayRole):
        """
        Return header description for section.
        """
        
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
        return len(self.header_name_list) 

    
    def data(self, index, role = QtCore.Qt.DisplayRole):
        """
        Return data for current index. The returned data is
        rendered by QItemDelegate.
        """

        #index invalid
        if not(index.isValid()):
            #log
            self.logger.debug('index {0} not valid.'.format(index))
            #evaluate in superclass
            return super(ShotMetadataModel, self).data(self, index, role)
        
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
