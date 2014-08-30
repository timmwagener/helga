
"""
char_metadata_view
==========================================

Subclass of QTableView to display char metadata
"""




#Import
#------------------------------------------------------------------
#python
import logging
#PySide
from PySide import QtGui
from PySide import QtCore







#CharMetadataView class
#------------------------------------------------------------------
class CharMetadataView(QtGui.QTableView):
    """
    Subclass of QTableView.
    """

    def __new__(cls, *args, **kwargs):
        """
        CharMetadataView instance factory.
        """

        #char_metadata_view_instance
        char_metadata_view_instance = super(CharMetadataView, cls).__new__(cls, args, kwargs)

        return char_metadata_view_instance
    
    
    def __init__(self, 
                logging_level = logging.DEBUG,
                parent=None):
    	"""
    	Customize instance.
    	"""
        
        #super class constructor
        super(CharMetadataView, self).__init__(parent)


        #instance variables
        #------------------------------------------------------------------

        
        
        #logger
        #------------------------------------------------------------------
        #logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logging_level = logging_level
        self.logger.setLevel(self.logging_level)

