
"""
asset_manager_line_edit_and_button_action
============================================

Subclass of QWidgetAction to allow for QLineEdit in menu which has
a button to execute something.
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









#AssetManagerLineEditAndButtonAction class
#------------------------------------------------------------------
class AssetManagerLineEditAndButtonAction(QtGui.QWidgetAction):
    """
    Subclass of QWidgetAction to allow for QLineEdit to be added as
    an action to a menu. The Action Widget has a button to execute
    something that possibly grabs and uses the data from the line edit 
    widget.
    """

    #Signals
    #------------------------------------------------------------------

    sgnl_button_pressed = QtCore.Signal(str)


    def __new__(cls, *args, **kwargs):
        """
        AssetManagerLineEditAndButtonAction instance factory.
        """

        #asset_manager_line_edit_and_button_action_instance
        asset_manager_line_edit_and_button_action_instance = super(AssetManagerLineEditAndButtonAction, cls).__new__(cls, args, kwargs)

        return asset_manager_line_edit_and_button_action_instance

    
    def __init__(self, 
                    logging_level = logging.DEBUG,
                    button_text = 'DoIt',
                    placeholder_text = 'PlaceHolder',
                    line_edit_text = '',
                    parent = None):
        """
        AssetManagerLineEditAndButtonAction instance customization.
        """

        #parent_class
        self.parent_class = super(AssetManagerLineEditAndButtonAction, self)
        #super class constructor
        self.parent_class.__init__(parent)

        #objectName
        self.setObjectName(self.__class__.__name__)


        #logger
        #------------------------------------------------------------------
        #logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logging_level = logging_level
        self.logger.setLevel(self.logging_level)

        
        #instance variables
        #------------------------------------------------------------------
        
        #button_text
        self.button_text = button_text

        #placeholder_text
        self.placeholder_text = placeholder_text

        #line_edit_text
        self.line_edit_text = line_edit_text

        
        


        

        









    #UI setup methods
    #------------------------------------------------------------------
    
    def setup_additional_ui(self, parent = None):
        """
        Setup additional UI.
        """
        
        #wdgt_line_edit_and_btn_complete
        self.wdgt_line_edit_and_btn_complete = QtGui.QWidget(parent = parent)
        self.wdgt_line_edit_and_btn_complete.setObjectName(self.__class__.__name__ + 
                                                    type(self.wdgt_line_edit_and_btn_complete).__name__)

        #lyt_line_edit_and_btn_complete
        self.lyt_line_edit_and_btn_complete = QtGui.QHBoxLayout(self.wdgt_line_edit_and_btn_complete)


        #line_edit
        self.line_edit = QtGui.QLineEdit()
        self.line_edit.setObjectName(self.__class__.__name__ + 
                                        type(self.line_edit).__name__)
        
        self.line_edit.setPlaceholderText(self.placeholder_text)
        self.line_edit.setText(self.line_edit_text)
        self.lyt_line_edit_and_btn_complete.addWidget(self.line_edit)


        #btn
        self.btn = QtGui.QPushButton()
        self.btn.setObjectName(self.__class__.__name__ + 
                                        type(self.btn).__name__)
        self.btn.setFlat(True)
        self.btn.setText(self.button_text)
        self.lyt_line_edit_and_btn_complete.addWidget(self.btn)


    def connect_ui(self):
        """
        Connect UI widgets with slots or functions.
        """

        #on_button_pressed
        self.btn.clicked.connect(self.on_button_pressed)


    def style_ui(self):
        """
        Setup tool palette, tool stylesheet and specific widget stylesheets.
        """

        #correct_styled_background_attribute
        self.correct_styled_background_attribute()

        #set_margins_and_spacing
        self.set_margins_and_spacing()

        #adjust size (Shrink to minimum size)
        self.wdgt_line_edit_and_btn_complete.adjustSize()

        




    #Getter & Setter
    #------------------------------------------------------------------

    def get_line_edit(self):
        """
        Return self.line_edit text.
        """

        #text
        text = self.line_edit.text()

        #return
        return text




    


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

        

        return self.wdgt_line_edit_and_btn_complete
    
    
    
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

    @QtCore.Slot()
    def on_button_pressed(self):
        """
        Catch self.btn.pressed and forward it to button_pressed signal for
        more convenient connecting with passing of a string.
        """

        #text
        text = self.get_line_edit()

        #emit
        self.sgnl_button_pressed.emit(text)

    


