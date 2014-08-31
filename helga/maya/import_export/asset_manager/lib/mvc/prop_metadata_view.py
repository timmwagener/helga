
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






#Import variable
do_reload = True


#asset_manager

#lib.mvc

#asset_manager_view_functionality
from lib.mvc import asset_manager_view_functionality
if(do_reload):reload(asset_manager_view_functionality)






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

        #view_functionality
        self.view_functionality = asset_manager_view_functionality.AssetManagerViewFunctionality(view = self)
        
        
        #logger
        #------------------------------------------------------------------
        #logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logging_level = logging_level
        self.logger.setLevel(self.logging_level)

