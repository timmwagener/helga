
"""
asset_manager_doublespinbox_checkable_action
============================================

Subclass of QWidgetAction to allow for QDoubleSpinbox in menu which has
a checkable state.
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









#AssetManagerDoubleSpinBoxCheckableAction class
#------------------------------------------------------------------
class AssetManagerDoubleSpinBoxCheckableAction(QtGui.QWidgetAction):
    """
    Subclass of QWidgetAction to allow for QDoubleSpinBox to be added as
    an action to a menu. The state of the QDoubleSpinBox is checkable.
    """

    #Signals
    #------------------------------------------------------------------

    state_changed = QtCore.Signal(bool)
    value_changed = QtCore.Signal(float)


    def __new__(cls, *args, **kwargs):
        """
        AssetManagerDoubleSpinBoxCheckableAction instance factory.
        """

        #asset_manager_doublespinbox_checkable_action_instance
        asset_manager_doublespinbox_checkable_action_instance = super(AssetManagerDoubleSpinBoxCheckableAction, cls).__new__(cls, args, kwargs)

        return asset_manager_doublespinbox_checkable_action_instance

    
    def __init__(self, 
                    logging_level = logging.DEBUG,
                    text = 'Spinbox',
                    minimum = 0.0,
                    maximum = 10000.0,
                    initial_value = 0.0,
                    initial_state = True,
                    parent = None):
        """
        AssetManagerDoubleSpinBoxCheckableAction instance customization.
        """

        #parent_class
        self.parent_class = super(AssetManagerDoubleSpinBoxCheckableAction, self)
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
        #initial_state
        self.initial_state = initial_state

        #wdgt_spinbox_complete
        self.wdgt_spinbox_complete = None

        
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
        
        #wdgt_spinbox_complete
        self.wdgt_spinbox_complete = QtGui.QWidget(parent = parent)
        self.wdgt_spinbox_complete.setObjectName(self.__class__.__name__ + 
                                                type(self.wdgt_spinbox_complete).__name__)

        #lyt_spinbox_complete
        self.lyt_spinbox_complete = QtGui.QHBoxLayout(self.wdgt_spinbox_complete)

        #chkbx_spinbox
        self.chkbx_spinbox = QtGui.QCheckBox()
        self.chkbx_spinbox.setObjectName(self.__class__.__name__ + 
                                            type(self.chkbx_spinbox).__name__)
        self.chkbx_spinbox.setText(self.text)
        self.chkbx_spinbox.setCheckable(True)
        self.chkbx_spinbox.setChecked(self.initial_state)
        self.lyt_spinbox_complete.addWidget(self.chkbx_spinbox)


        #spinbox
        self.spinbox = QtGui.QDoubleSpinBox()
        self.spinbox.setObjectName(self.__class__.__name__ + 
                                    type(self.spinbox).__name__)
        self.spinbox.setRange(self.minimum, self.maximum)
        self.spinbox.setValue(self.initial_value)
        self.spinbox.setEnabled(self.initial_state)
        self.lyt_spinbox_complete.addWidget(self.spinbox)


    def connect_ui(self):
        """
        Connect UI widgets with slots or functions.
        """

        #chkbx_spinbox
        self.chkbx_spinbox.stateChanged.connect(self.on_state_changed)
        
        #spinbox
        self.spinbox.valueChanged.connect(self.on_value_changed)


    def style_ui(self):
        """
        Setup tool palette, tool stylesheet and specific widget stylesheets.
        """

        #correct_styled_background_attribute
        self.correct_styled_background_attribute()

        #set_margins_and_spacing
        self.set_margins_and_spacing()

        #adjust size (Shrink to minimum size)
        self.wdgt_spinbox_complete.adjustSize()

        







    


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
        self.logger.debug('QWidgetAction of type {0} created'.format(self.__class__.__name__))

        

        return self.wdgt_spinbox_complete
    
    
    
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

    @QtCore.Slot(bool)
    def on_state_changed(self, value):
        """
        Value of chkbx_spinbox changed.
        """

        #spinbox
        self.spinbox.setEnabled(value)
        
        #emit value_changed
        self.state_changed.emit(value)

    
    @QtCore.Slot(float)
    def on_value_changed(self, value):
        """
        Value of spinbox changed.
        """
        
        #emit value_changed
        self.value_changed.emit(value)

    


