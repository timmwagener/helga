
"""
asset_manager_slider_action
==========================================

Subclass of QWidgetAction to allow for slider in menu.
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









#AssetManagerSliderAction class
#------------------------------------------------------------------
class AssetManagerSliderAction(QtGui.QWidgetAction):
    """
    Subclass of QWidgetAction to allow for QSlider to be added as
    an action to a menu.
    """

    #Signals
    #------------------------------------------------------------------

    value_changed = QtCore.Signal(int)


    def __new__(cls, *args, **kwargs):
        """
        AssetManagerSliderAction instance factory.
        """

        #asset_manager_slider_action_instance
        asset_manager_slider_action_instance = super(AssetManagerSliderAction, cls).__new__(cls, args, kwargs)

        return asset_manager_slider_action_instance

    
    def __init__(self, 
                    logging_level = logging.DEBUG,
                    text = 'Slider',
                    minimum = 1,
                    maximum = 10000,
                    initial_value = 2000,
                    parent = None):
        """
        AssetManagerSliderAction instance customization.
        """

        #parent_class
        self.parent_class = super(AssetManagerSliderAction, self)
        #super class constructor
        self.parent_class.__init__(parent)

        #objectName
        self.setObjectName(self.__class__.__name__)


        #instance variables
        #------------------------------------------------------------------
        
        #initial_value
        self.initial_value = initial_value
        #minimum
        self.minimum = minimum
        #maximum
        self.maximum = maximum
        #text
        self.text = text

        #wdgt_slider_complete
        self.wdgt_slider_complete = None

        
        #logger
        #------------------------------------------------------------------
        #logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logging_level = logging_level
        self.logger.setLevel(self.logging_level)


        

        









    #UI setup methods
    #------------------------------------------------------------------
    
    def setup_additional_ui(self, parent = None):
        """
        Setup additional UI.
        """
        
        #wdgt_slider_complete
        self.wdgt_slider_complete = QtGui.QWidget(parent = parent)
        self.wdgt_slider_complete.setObjectName(self.__class__.__name__ + 
                                                type(self.wdgt_slider_complete).__name__)

        #lyt_slider_complete
        self.lyt_slider_complete = QtGui.QVBoxLayout(self.wdgt_slider_complete)

        
        #Header

        #wdgt_slider_header
        self.wdgt_slider_header = QtGui.QWidget()
        self.wdgt_slider_header.setObjectName(self.__class__.__name__ + 
                                                type(self.wdgt_slider_header).__name__)
        self.lyt_slider_complete.addWidget(self.wdgt_slider_header)

        #lyt_slider_header
        self.lyt_slider_header = QtGui.QHBoxLayout(self.wdgt_slider_header)

        #lbl_slider
        self.lbl_slider = QtGui.QLabel(text = self.text)
        self.lbl_slider.setObjectName(self.__class__.__name__ + type(self.lbl_slider).__name__)
        self.lyt_slider_header.addWidget(self.lbl_slider)


        #Slider

        #wdgt_slider
        self.wdgt_slider = QtGui.QWidget()
        self.wdgt_slider.setObjectName(self.__class__.__name__ + 
                                                type(self.wdgt_slider).__name__)
        self.lyt_slider_complete.addWidget(self.wdgt_slider)

        #lyt_slider
        self.lyt_slider = QtGui.QHBoxLayout(self.wdgt_slider)

        #slider
        self.slider = QtGui.QSlider()
        self.slider.setObjectName(self.__class__.__name__ + 
                                    type(self.slider).__name__)
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setRange(self.minimum, self.maximum)
        self.slider.setValue(self.initial_value)
        self.lyt_slider.addWidget(self.slider)

        #lcd_number
        self.lcd_number = QtGui.QLCDNumber()
        self.lcd_number.setObjectName(self.__class__.__name__ + 
                                        type(self.lcd_number).__name__)
        self.lcd_number.display(self.initial_value)
        self.lcd_number.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.lyt_slider.addWidget(self.lcd_number)


    def connect_ui(self):
        """
        Connect UI widgets with slots or functions.
        """
        
        #slider
        self.slider.valueChanged.connect(self.on_value_changed)


    def style_ui(self):
        """
        Setup tool palette, tool stylesheet and specific widget stylesheets.
        """

        #correct_styled_background_attribute
        self.correct_styled_background_attribute()

        #set_margins_and_spacing
        self.set_margins_and_spacing()

        #adjust size (Shrink to minimum size)
        self.wdgt_slider_complete.adjustSize()

        







    


    #Virtual Methods
    #------------------------------------------------------------------

    def createWidget(self, parent = None):
        """
        Virtual function that creates and returns a widget to display in menu.
        """

        #setup_additional_ui
        self.setup_additional_ui(parent = parent)

        #connect_ui
        self.connect_ui()

        #style_ui
        self.style_ui()

        #log
        self.logger.debug('QWidgetAction created')

        

        return self.wdgt_slider_complete
    
    
    
    #Methods
    #------------------------------------------------------------------

    def correct_styled_background_attribute(self):
        """
        Set QtCore.Qt.WA_StyledBackground True for all widgets.
        Without this attr. set, the background-color stylesheet
        will have no effect on QWidgets. This should replace the
        need for palette settings.
        ToDo:
        Maybe add exclude list when needed.
        """

        #wdgt_list
        wdgt_list = self.findChildren(QtGui.QWidget) #Return several types ?!?!

        #iterate and set
        for wdgt in wdgt_list:
            
            #check type
            if(type(wdgt) is QtGui.QWidget):

                #styled_background
                wdgt.setAttribute(QtCore.Qt.WA_StyledBackground, True)


    def set_margins_and_spacing(self):
        """
        Eliminate margin and spacing for all layout widgets.
        """

        #margin_list
        margin_list = [0,0,0,0]

        #lyt_classes_list
        lyt_classes_list = [QtGui.QStackedLayout, QtGui.QGridLayout, QtGui.QFormLayout, 
                            QtGui.QBoxLayout, QtGui.QVBoxLayout, QtGui.QHBoxLayout, QtGui.QBoxLayout]

        #lyt_list
        lyt_list = []
        for lyt_class in lyt_classes_list:
            lyt_list += [wdgt for wdgt in self.findChildren(lyt_class)]


        
        #set margin and spacing
        for lyt in lyt_list:

            #check type
            if(type(lyt) in lyt_classes_list):

                #set
                lyt.setContentsMargins(*margin_list)
                lyt.setSpacing(0)



    #Slots
    #------------------------------------------------------------------

    @QtCore.Slot(int)
    def on_value_changed(self, value):
        """
        Value of slider changed.
        """

        #set value in lcd display
        self.lcd_number.display(value)
        
        #emit value_changed
        self.value_changed.emit(value)

    


