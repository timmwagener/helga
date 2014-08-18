
"""
asset_manager_button
==========================================

Subclass of QPushButton to allow for customized drag&drop behaviour
"""




#Add tool relative pathes
#------------------------------------------------------------------

#import
import sys
import os

#tool_root_path
tool_root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(tool_root_path)

#media_path
media_path = os.path.join(tool_root_path, 'media')
sys.path.append(media_path)

#icons_path
icons_path = os.path.join(media_path, 'icons')
sys.path.append(icons_path)








#Import
#------------------------------------------------------------------
#python
import logging
#PySide
from PySide import QtGui
from PySide import QtCore







#AssetManagerButton class
#------------------------------------------------------------------
class AssetManagerButton(QtGui.QPushButton):
    """
    Subclass of QPushButton to allow for custom styling
    """

    def __new__(cls, *args, **kwargs):
        """
        AssetManagerButton instance factory.
        """

        #asset_manager_button_instance
        asset_manager_button_instance = super(AssetManagerButton, cls).__new__(cls, args, kwargs)

        return asset_manager_button_instance

    
    def __init__(self, 
                logging_level = logging.DEBUG,
                button_text = None,
                icon_name = None,
                icon_hover_name = None,
                button_width = 64,
                button_height = 64,
                parent=None):
        """
        AssetManagerButton instance customization.
        """

        #parent_class
        self.parent_class = super(AssetManagerButton, self)
        
        #super class constructor
        if(button_text):
            self.parent_class.__init__(button_text, parent)
        else:
            self.parent_class.__init__(parent)


        #instance variables
        #------------------------------------------------------------------
        self.button_text = button_text
        self.icon_name = icon_name
        self.icon_hover_name = icon_hover_name
        self.button_width = button_width
        self.button_height = button_height

        
        #logger
        #------------------------------------------------------------------
        #logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logging_level = logging_level
        self.logger.setLevel(self.logging_level)


        #Init procedure
        #------------------------------------------------------------------

        #setup_additional_ui
        self.setup_additional_ui()

        #connect_ui
        self.connect_ui()









    #UI setup methods
    #------------------------------------------------------------------
    
    def setup_additional_ui(self):
        """
        Setup additional UI.
        """
        
        #setMouseTracking
        self.setMouseTracking(True)

        #set size
        self.setFixedSize(self.button_width, self.button_height)

        #initialize_icons
        #self.initialize_icons()


    def connect_ui(self):
        """
        Connect UI widgets with slots or functions.
        """
        
        pass








    #Methods
    #------------------------------------------------------------------

    def initialize_icons(self, resize_factor = 0.5):
        """
        Create and scale self.icon and self.icon_hover
        """

        #icon_width
        icon_width = int(self.width() * resize_factor)
        #icon_height
        icon_height = int(self.height() * resize_factor)

        #icon
        self.pixmap_icon = QtGui.QPixmap(os.path.join(icons_path, self.icon_name))
        self.pixmap_icon = self.pixmap_icon.scaled(icon_width, icon_height, mode = QtCore.Qt.FastTransformation)
        self.icon = QtGui.QIcon(self.pixmap_icon)

        #log
        self.logger.debug('Initialized icon {0} for button {1}'.format(self.icon_name, self))
        
        #icon_hover
        self.pixmap_icon_hover = QtGui.QPixmap(os.path.join(icons_path, self.icon_hover_name))
        self.pixmap_icon_hover = self.pixmap_icon_hover.scaled(icon_width, icon_height, mode = QtCore.Qt.FastTransformation)
        self.icon_hover = QtGui.QIcon(self.pixmap_icon_hover)

        #log
        self.logger.debug('Initialized icon_hover {0} for button {1}'.format(self.icon_hover_name, self))

        #setIcon
        self.setIcon(self.icon)
