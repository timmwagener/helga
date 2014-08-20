
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



#Import variable
do_reload = True


#asset_manager

#asset_manager_globals
import asset_manager_globals
if(do_reload):reload(asset_manager_globals)






#Globals
#------------------------------------------------------------------

#AssetManager colors
BRIGHT_ORANGE = asset_manager_globals.BRIGHT_ORANGE
DARK_ORANGE = asset_manager_globals.DARK_ORANGE
BRIGHT_GREY = asset_manager_globals.BRIGHT_GREY
GREY = asset_manager_globals.GREY
DARK_GREY = asset_manager_globals.DARK_GREY









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
                fixed_width = None,
                fixed_height = None,
                background_color_normal = DARK_GREY,
                hover_radial_color_normal = DARK_ORANGE,
                background_color_active = GREY,
                hover_radial_color_active = DARK_ORANGE,
                hover_radial_radius = 0.45,
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
        self.fixed_width = fixed_width
        self.fixed_height = fixed_height
        
        #colors
        self.background_color_normal = background_color_normal
        self.hover_radial_color_normal = hover_radial_color_normal
        self.background_color_active = background_color_active
        self.hover_radial_color_active = hover_radial_color_active

        #hover_radial_radius
        self.hover_radial_radius = hover_radial_radius

        #icon_path
        self.icon_path = os.path.join(icons_path, self.icon_name)
        self.icon_path = self.icon_path.replace('\\', '/')
        

        

        
        #stylesheets
        #------------------------------------------------------------------

        #ss_dict
        self.ss_dict = {'icon_path' : self.icon_path,
                        'hover_radial_radius' : self.hover_radial_radius,
                        'background_color_normal' : self.background_color_normal.name(),
                        'hover_radial_color_normal' : self.hover_radial_color_normal.name(),
                        'background_color_active' : self.background_color_active.name(),
                        'hover_radial_color_active' : self.hover_radial_color_active.name(),}
        
        #ss_normal
        self.ss_normal = " \
\
\
/* AssetManagerButton - normal */\
AssetManagerButton { border-image: url(%(icon_path)s); \
                        background-color: %(background_color_normal)s; \
} \
\
\
/* AssetManagerButton - normal - hover */\
AssetManagerButton:hover { border-image: url(%(icon_path)s); \
                            background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, \
                                                                radius:%(hover_radial_radius)s, fx:0.5, fy:0.5, \
                                                                stop:0 %(hover_radial_color_normal)s, \
                                                                stop:1 %(background_color_normal)s); \
} \
\
\
/* AssetManagerButton - normal - pressed */\
AssetManagerButton:pressed { border-image: url(%(icon_path)s); \
                                background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, \
                                                                    radius:%(hover_radial_radius)s, fx:0.5, fy:0.5, \
                                                                    stop:0 %(hover_radial_color_normal)s, \
                                                                    stop:1 %(background_color_normal)s); \
} \
\
\
"%self.ss_dict
        
        #ss_active
        self.ss_active = " \
\
\
/* AssetManagerButton - active */\
AssetManagerButton { border-image: url(%(icon_path)s); \
                        background-color: %(background_color_active)s; \
} \
\
\
/* AssetManagerButton - active - hover */\
AssetManagerButton:hover { border-image: url(%(icon_path)s); \
                            background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, \
                                                                radius:%(hover_radial_radius)s, fx:0.5, fy:0.5, \
                                                                stop:0 %(hover_radial_color_active)s, \
                                                                stop:1 %(background_color_active)s); \
} \
\
\
/* AssetManagerButton - active - pressed */\
AssetManagerButton:pressed { border-image: url(%(icon_path)s); \
                                background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, \
                                                                    radius:%(hover_radial_radius)s, fx:0.5, fy:0.5, \
                                                                    stop:0 %(hover_radial_color_active)s, \
                                                                    stop:1 %(background_color_active)s); \
} \
\
\
"%self.ss_dict

        
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

        #initialize_icons
        #self.initialize_icons()

        #set_stylesheet
        self.set_stylesheet()


    def connect_ui(self):
        """
        Connect UI widgets with slots or functions.
        """
        
        pass




    


    #Slots
    #------------------------------------------------------------------

    def set_stylesheet(self, role = 'normal'):
        """
        Set stylesheet for this widget based on role.
        """

        #active
        if(role == 'active'):
            self.setStyleSheet(self.ss_active)

        #anyting and normal
        else:
            self.setStyleSheet(self.ss_normal)








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

        #setIcon
        self.setIcon(self.icon)


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
