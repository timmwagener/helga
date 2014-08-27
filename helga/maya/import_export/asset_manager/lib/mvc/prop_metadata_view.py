
"""
prop_metadata_view
==========================================

Subclass of QTableView to display prop metadata
"""




#Import
#------------------------------------------------------------------
#python
import logging
#PySide
from PySide import QtGui
from PySide import QtCore







#PropMetadataView class
#------------------------------------------------------------------
class PropMetadataView(QtGui.QTableView):
    """
    Subclass of QTableView.
    """

    def __new__(cls, *args, **kwargs):
        """
        PropMetadataView instance factory.
        """

        #prop_metadata_view_instance
        prop_metadata_view_instance = super(PropMetadataView, cls).__new__(cls, args, kwargs)

        return prop_metadata_view_instance
    
    
    def __init__(self, 
                logging_level = logging.DEBUG,
                parent=None):
    	"""
    	Customize instance.
    	"""
        
        #super class constructor
        super(PropMetadataView, self).__init__(parent)


        #instance variables
        #------------------------------------------------------------------

        
        
        #logger
        #------------------------------------------------------------------
        #logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logging_level = logging_level
        self.logger.setLevel(self.logging_level)

