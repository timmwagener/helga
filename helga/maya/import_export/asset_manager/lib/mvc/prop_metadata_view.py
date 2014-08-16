
"""
shot_metadata_view
==========================================

Subclass of QTableView to display shot metadata
"""




#Import
#------------------------------------------------------------------
#python
import logging
#PySide
from PySide import QtGui
from PySide import QtCore







#ShotMetadataView class
#------------------------------------------------------------------
class ShotMetadataView(QtGui.QTableView):
    """
    Subclass of QTableView.
    """

    def __new__(cls, *args, **kwargs):
        """
        ShotMetadataView instance factory.
        """

        #shot_metadata_view_instance
        shot_metadata_view_instance = super(ShotMetadataView, cls).__new__(cls, args, kwargs)

        return shot_metadata_view_instance
    
    
    def __init__(self, 
                logging_level = logging.DEBUG,
                parent=None):
    	"""
    	Customize instance.
    	"""
        
        #super class constructor
        super(ShotMetadataView, self).__init__(parent)

