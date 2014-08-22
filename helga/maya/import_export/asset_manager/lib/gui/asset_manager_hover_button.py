
"""
asset_manager_hover_button
==========================================

Subclass of QPushButton to allow for hover signal when hovered with mouse.
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

#asset_manager_globals
from lib import asset_manager_globals
if(do_reload):reload(asset_manager_globals)






#Globals
#------------------------------------------------------------------

#Pathes
TOOL_ROOT_PATH = asset_manager_globals.TOOL_ROOT_PATH
MEDIA_PATH = asset_manager_globals.MEDIA_PATH
ICONS_PATH = asset_manager_globals.ICONS_PATH

#AssetManager colors
BRIGHT_ORANGE = asset_manager_globals.BRIGHT_ORANGE
DARK_ORANGE = asset_manager_globals.DARK_ORANGE
BRIGHT_GREY = asset_manager_globals.BRIGHT_GREY
GREY = asset_manager_globals.GREY
DARK_GREY = asset_manager_globals.DARK_GREY









#AssetManagerHoverButton class
#------------------------------------------------------------------
class AssetManagerHoverButton(QtGui.QPushButton):
    """
    Subclass of QPushButton to allow for hover signal.
    """

    #Signals
    #------------------------------------------------------------------

    hover_enter = QtCore.Signal()
    hover_leave = QtCore.Signal()


    def __new__(cls, *args, **kwargs):
        """
        AssetManagerHoverButton instance factory.
        """

        #asset_manager_hover_button_instance
        asset_manager_hover_button_instance = super(AssetManagerHoverButton, cls).__new__(cls, args, kwargs)

        return asset_manager_hover_button_instance

    
    def __init__(self, 
                    logging_level = logging.DEBUG,
                    fixed_width = None,
                    fixed_height = None,
                    parent=None):
        """
        AssetManagerHoverButton instance customization.
        """

        #parent_class
        self.parent_class = super(AssetManagerHoverButton, self)
        
        #super class constructor
        self.parent_class.__init__(parent)


        #instance variables
        #------------------------------------------------------------------
        self.fixed_width = fixed_width
        self.fixed_height = fixed_height

        
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

        #set_size_policy
        self.set_size_policy(self.fixed_width, self.fixed_height)


    def connect_ui(self):
        """
        Connect UI widgets with slots or functions.
        """
        
        pass







    


    #Methods
    #------------------------------------------------------------------

    def set_size_policy(self, width, height):
        """
        Set size policy for self.
        """

        #fixed width and height
        if (width and height):
            self.setFixedSize(width, height)

        #else
        else:

            #set expanding
            expanding_size_policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
            self.setSizePolicy(expanding_size_policy)

            #fixed width
            if(width):
                self.setFixedWidth(width)

            #fixed height
            elif(height):
                self.setFixedHeight(height)
    
    

    #Events
    #------------------------------------------------------------------

    def enterEvent(self, event):
        """
        Enter event sends hover_enter signal.
        """

        #emit signal
        self.hover_enter.emit()
        #accept
        event.accept()

    def leaveEvent(self, event):
        """
        Leave event sends hover_leave signal.
        """

        #emit signal
        self.hover_leave.emit()
        #accept
        event.accept()


