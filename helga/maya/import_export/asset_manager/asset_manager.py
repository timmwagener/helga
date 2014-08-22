

"""
asset_manager
==========================================

GUI to export Alembics from Maya. Building atop of our asset based pipeline.

It takes care of:

#. Cameras
#. Characters
#. Props


-----------------------

Idea list:

#. Queue/Threadpool for alembic export
#. Feed closures to Queue
#. Export chars, props and cameras
#. Use descriptor protocol
#. Take care of preroll for chars in code.

-----------------------

**Author:** `Timm Wagener <mailto:wagenertimm@gmail.com>`_
"""




#Add tool root path
#------------------------------------------------------------------

#import
import sys
import os

#tool_root_path
tool_root_path = os.path.abspath(__file__)
sys.path.append(tool_root_path)





#Import
#------------------------------------------------------------------
#python
import functools
import logging
import subprocess
import time
import shutil
import webbrowser
import yaml
import hashlib
#PySide
from PySide import QtGui
from PySide import QtCore
from PySide import QtUiTools
import shiboken
import pysideuic




#Import variable
do_reload = True

#helga

#global_variables
from helga.general.setup.global_variables import global_variables
if(do_reload):reload(global_variables)

#global_functions
from helga.general.setup.global_functions import global_functions
if(do_reload):reload(global_functions)

#doc_link
from helga.general.setup.doc_link import doc_link
if(do_reload): reload(doc_link)


#asset_manager

#asset_manager_globals
from lib import asset_manager_globals
if(do_reload):reload(asset_manager_globals)

#asset_manager_logging_handler
from lib import asset_manager_logging_handler
if(do_reload):reload(asset_manager_logging_handler)

#asset_manager_functionality
from lib import asset_manager_functionality
if(do_reload):reload(asset_manager_functionality)


#asset_manager_button
from lib.gui import asset_manager_button
if(do_reload):reload(asset_manager_button)

#asset_manager_stylesheet_widget
from lib.gui import asset_manager_stylesheet_widget
if(do_reload):reload(asset_manager_stylesheet_widget)

#asset_manager_stylesheets
from lib.gui import asset_manager_stylesheets
if(do_reload):reload(asset_manager_stylesheets)


#shot_metadata_model
from lib.mvc import shot_metadata_model
if(do_reload):reload(shot_metadata_model)

#shot_metadata_view
from lib.mvc import shot_metadata_view
if(do_reload):reload(shot_metadata_view)

#shot_metadata_item_delegate
from lib.mvc import shot_metadata_item_delegate
if(do_reload):reload(shot_metadata_item_delegate)

#shot_metadata_context_menu
from lib.mvc import shot_metadata_context_menu
if(do_reload):reload(shot_metadata_context_menu)








#Globals
#------------------------------------------------------------------

#Pathes
TOOL_ROOT_PATH = asset_manager_globals.TOOL_ROOT_PATH
MEDIA_PATH = asset_manager_globals.MEDIA_PATH
ICONS_PATH = asset_manager_globals.ICONS_PATH

#AssetManager Sizes
STACKEDWIDGET_DIVIDER_HEIGHT = asset_manager_globals.STACKEDWIDGET_DIVIDER_HEIGHT

#AssetManager colors
BRIGHT_ORANGE = asset_manager_globals.BRIGHT_ORANGE
DARK_ORANGE = asset_manager_globals.DARK_ORANGE
BRIGHT_GREY = asset_manager_globals.BRIGHT_GREY
GREY = asset_manager_globals.GREY
DARK_GREY = asset_manager_globals.DARK_GREY
DARK_BLUE = asset_manager_globals.DARK_BLUE
BRIGHT_BLUE = asset_manager_globals.BRIGHT_BLUE
WHITE = asset_manager_globals.WHITE


#AssetManager Icons
ICON_EXPORT = asset_manager_globals.ICON_EXPORT
ICON_CHAR = asset_manager_globals.ICON_CHAR
ICON_PROP = asset_manager_globals.ICON_PROP
ICON_SHOT = asset_manager_globals.ICON_SHOT
ICON_UPDATE = asset_manager_globals.ICON_UPDATE
ICON_DOCS = asset_manager_globals.ICON_DOCS

#Text
SHOT_METADATA_EXPLANATION_HEADER = asset_manager_globals.SHOT_METADATA_EXPLANATION_HEADER
SHOT_METADATA_EXPLANATION_TEXT = asset_manager_globals.SHOT_METADATA_EXPLANATION_TEXT
PROP_METADATA_EXPLANATION_HEADER = asset_manager_globals.PROP_METADATA_EXPLANATION_HEADER
PROP_METADATA_EXPLANATION_TEXT = asset_manager_globals.PROP_METADATA_EXPLANATION_TEXT
CHAR_METADATA_EXPLANATION_HEADER = asset_manager_globals.CHAR_METADATA_EXPLANATION_HEADER
CHAR_METADATA_EXPLANATION_TEXT = asset_manager_globals.CHAR_METADATA_EXPLANATION_TEXT


#UI Palette
WINDOW_COLOR = DARK_GREY#QtGui.QPalette.Window // A general background color.
BACKGROUND_COLOR = DARK_GREY#QtGui.QPalette.Background // This value is obsolete. Use Window instead.
WINDOWTEXT_COLOR = BRIGHT_GREY#QtGui.QPalette.WindowText // A general foreground color.
FOREGROUND_COLOR = GREY#QtGui.QPalette.Foreground // This value is obsolete. Use WindowText instead.
BASE_COLOR = DARK_GREY#QtGui.QPalette.Base // Used mostly as the background color for text entry widgets, but can also be used for other painting - such as the background of combobox drop down lists and toolbar handles. It is usually white or another light color.
ALTERNATEBASE_COLOR = DARK_GREY#QtGui.QPalette.AlternateBase // Used as the alternate background color in views with alternating row colors (see QAbstractItemView.setAlternatingRowColors() ).
TOOLTIPBASE_COLOR = DARK_GREY#QtGui.QPalette.ToolTipBase // Used as the background color for PySide.QtGui.QToolTip and PySide.QtGui.QWhatsThis . Tool tips use the Inactive color group of PySide.QtGui.QPalette , because tool tips are not active windows.
TOOLTIPTEXT_COLOR = BRIGHT_GREY#QtGui.QPalette.ToolTipText // Used as the foreground color for PySide.QtGui.QToolTip and PySide.QtGui.QWhatsThis . Tool tips use the Inactive color group of PySide.QtGui.QPalette , because tool tips are not active windows.
TEXT_COLOR = BRIGHT_GREY#QtGui.QPalette.Text // The foreground color used with Base. This is usually the same as the WindowText, in which case it must provide good contrast with Window and Base.
BUTTON_COLOR = QtGui.QColor(QtCore.Qt.black)#QtGui.QPalette.Button // The general button background color. This background can be different from Window as some styles require a different background color for buttons.
BUTTONTEXT_COLOR = BRIGHT_GREY#QtGui.QPalette.ButtonText // A foreground color used with the Button color.
BRIGHTTEXT_COLOR = QtGui.QColor(QtCore.Qt.black)#QtGui.QPalette.BrightText // A text color that is very different from WindowText, and contrasts well with e.g. Dark. Typically used for text that needs to be drawn where Text or WindowText would give poor contrast, such as on pressed push buttons. Note that text colors can be used for things other than just words
HIGHLIGHT_COLOR = BRIGHT_ORANGE#QtGui.QPalette.Highlight // A color to indicate a selected item or the current item. By default, the highlight color is Qt.darkBlue .
HIGHLIGHTEDTEXT_COLOR = BRIGHT_GREY#QtGui.QPalette.HighlightedText // A text color that contrasts with Highlight. By default, the highlighted text color is Qt.white .
LINK_COLOR = QtGui.QColor(QtCore.Qt.red)#QtGui.QPalette.Link // A text color used for unvisited hyperlinks. By default, the link color is Qt.blue .
LINKVISITED_COLOR = QtGui.QColor(QtCore.Qt.red)#QtGui.QPalette.LinkVisited // A text color used for already visited hyperlinks. By default, the linkvisited color is Qt.magenta .







#Cleanup old instances
#------------------------------------------------------------------

def get_widget_by_name_closure(wdgt_name):
    """
    Practicing closures. Doesnt really make sense here, or could at least
    be done much simpler/better.
    Want to try it with filter in order to get more into the builtins.
    """

    def get_widget_by_name(wdgt):
        """
        Function that is closed in. Accepts and checks all
        widgets against wdgt_name from enclosing function.
        ALl this mess to be able to use it with filter.
        """
        try:
            if (wdgt.__class__.__name__ == wdgt_name):
                return True
        except:
            pass
        return False

    return get_widget_by_name


def check_and_delete_wdgt_instances_with_name(wdgt_name):
    """
    Search for all occurences with wdgt_name and delete them.
    """

    #get_wdgt_closure
    get_wdgt_closure = get_widget_by_name_closure(wdgt_name)

    #wdgt_asset_manager_list
    wdgt_asset_manager_list = filter(get_wdgt_closure, QtGui.QApplication.allWidgets())

    #iterate and delete
    for index, wdgt_asset_manager in enumerate(wdgt_asset_manager_list):

        try:
            #mute logger
            wdgt_asset_manager.status_handler.wdgt_status = None
            #delete
            wdgt_asset_manager.deleteLater()
       
        except:
            pass

    return wdgt_asset_manager_list













#form_class, base_class
#------------------------------------------------------------------

#ui_file
ui_file_name = 'asset_manager.ui'
ui_file = os.path.join(MEDIA_PATH, ui_file_name)

#form_class, base_class
form_class, base_class = global_functions.load_ui_type(ui_file)








#AssetManager class
#------------------------------------------------------------------
class AssetManager(form_class, base_class):
    """
    AssetManager
    """

    #Signals
    #------------------------------------------------------------------
    stkwdgt_change_current = QtCore.Signal(int)
    explanation_header_set_text = QtCore.Signal(str)
    explanation_text_set_text = QtCore.Signal(str)


    
    def __new__(cls, *args, **kwargs):
        """
        AssetManager instance factory.
        """

        #delete old instances
        check_and_delete_wdgt_instances_with_name(cls.__name__)

        #asset_manager_instance
        asset_manager_instance = super(AssetManager, cls).__new__(cls, args, kwargs)

        return asset_manager_instance

    
    def __init__(self, 
                logging_level = logging.DEBUG,
                auto_update_models = True,
                parent = global_functions.get_main_window()):
        """
        Customize instance.
        """

        #super
        self.parent_class = super(AssetManager, self)
        self.parent_class.__init__(parent)

        #setObjectName
        self.setObjectName(self.__class__.__name__)


        #instance variables
        #------------------------------------------------------------------
        self.title_name = self.__class__.__name__
        self.version = 0.1
        self.title = self.title_name +' ' + str(self.version)
        self.icon_path = os.path.join(ICONS_PATH, 'icon_asset_manager.png')

        #asset_manager_functionality
        self.asset_manager_functionality = asset_manager_functionality.AssetManagerFunctionality()

        #auto_update_models
        self.auto_update_models = auto_update_models
        #auto_update_timer
        self.auto_update_timer = None

        #shot_metadata_list
        self.shot_metadata_list = []
        #prop_metadata_list
        self.prop_metadata_list = []
        #char_metadata_list
        self.char_metadata_list = []

        

        
        #logger
        #------------------------------------------------------------------
        #logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logging_level = logging_level
        self.logger.setLevel(self.logging_level)

        #status_handler
        self.status_handler = asset_manager_logging_handler.StatusStreamHandler(self)
        self.logger.addHandler(self.status_handler)
        

        #Init procedure
        #------------------------------------------------------------------
        
        #setupUi
        self.setupUi(self)

        #setup_additional_ui
        self.setup_additional_ui()

        #connect_ui
        self.connect_ui()

        #style_ui
        self.style_ui()

        #test_methods
        self.test_methods()

        



        

    

    
    
    
        
        
        
    
    
    
    #UI setup methods
    #------------------------------------------------------------------
    
    def setup_additional_ui(self):
        """
        Setup additional UI like mvc or helga tool header.
        """

        #make sure its floating intead of embedded
        self.setWindowFlags(QtCore.Qt.Window)

        #set title
        self.setWindowTitle(self.title)

        #setup_status_widget
        self.setup_status_widget()

        #setup_stacked_widget
        self.setup_stacked_widget() #buttons and widgets

        #setup_additional_buttons
        self.setup_additional_buttons()

        #setup_progressbar
        self.setup_progressbar()

        #setup_mvc
        self.setup_mvc()

        #auto_update_models
        if(self.auto_update_models):
            self.setup_auto_update_models()


    def connect_ui(self):
        """
        Connect UI widgets with slots or functions.
        """

        #Signals
        self.stkwdgt_change_current.connect(self.stkwdgt_metadata.setCurrentIndex)
        self.explanation_header_set_text.connect(self.lbl_explanation_header.setText)
        self.explanation_text_set_text.connect(self.lbl_explanation_text.setText)

        
        #Context Menus

        #shot_metadata_view
        self.shot_metadata_view.customContextMenuRequested.connect(self.display_shot_metadata_context_menu)

        
        #Widgets

        #btn_docs
        self.btn_docs.clicked.connect(doc_link.run)
        
        #btn_show_shot_metadata
        self.btn_show_shot_metadata.clicked.connect(functools.partial(self.set_active_stacked_widget, self.btn_show_shot_metadata))
        self.btn_show_shot_metadata.clicked.connect(functools.partial(self.set_explanation_text, self.btn_show_shot_metadata))
        #btn_show_prop_metadata
        self.btn_show_prop_metadata.clicked.connect(functools.partial(self.set_active_stacked_widget, self.btn_show_prop_metadata))
        self.btn_show_prop_metadata.clicked.connect(functools.partial(self.set_explanation_text, self.btn_show_prop_metadata))
        #btn_show_char_metadata
        self.btn_show_char_metadata.clicked.connect(functools.partial(self.set_active_stacked_widget, self.btn_show_char_metadata))
        self.btn_show_char_metadata.clicked.connect(functools.partial(self.set_explanation_text, self.btn_show_char_metadata))

        #btn_export
        self.btn_export.clicked.connect(functools.partial(self.dummy_method, 'Export'))

        #btn_update_models
        if not(self.auto_update_models):
            self.btn_update_models.clicked.connect(self.update_models)

    
    def style_ui(self):
        """
        Setup tool palette, tool stylesheet and specific widget stylesheets.
        """

        #correct_styled_background_attribute
        self.correct_styled_background_attribute()

        #set_margins_and_spacing
        self.set_margins_and_spacing()

        #setup_tool_palette_global
        #self.setup_tool_palette_global()

        #setup_tool_palette_specific
        #self.setup_tool_palette_specific()

        #set_active_stacked_widget 
        self.set_active_stacked_widget(self.btn_show_shot_metadata)

        #set_explanation_text
        self.set_explanation_text(self.btn_show_shot_metadata)

        #set_stylesheet
        self.setStyleSheet(asset_manager_stylesheets.get_stylesheet())

    
    def setup_status_widget(self):
        """
        Setup status widget for logging
        """

        #le_status
        self.le_status = QtGui.QLineEdit()
        self.le_status.setObjectName('le_status')
        #set in lyt
        self.lyt_status.addWidget(self.le_status)

    
    def setup_stacked_widget(self):
        """
        Setup stacked widget ui to test sweet ui design.
        """

        #setup_stacked_widget_pages
        self.setup_stacked_widget_pages()

        #setup_stacked_widget_buttons
        self.setup_stacked_widget_buttons()

    
    def setup_stacked_widget_pages(self):
        """
        Setup stacked widget pages
        """

        #wdgt_shot_metadata
        self.wdgt_shot_metadata = asset_manager_stylesheet_widget.AssetManagerStylesheetWidget(background_color_normal = DARK_GREY,
                                                                                                background_color_active = GREY,
                                                                                                parent = self)
        self.lyt_shot_metadata = QtGui.QVBoxLayout()
        self.wdgt_shot_metadata.setLayout(self.lyt_shot_metadata)
        

        #wdgt_prop_metadata
        self.wdgt_prop_metadata = asset_manager_stylesheet_widget.AssetManagerStylesheetWidget(background_color_normal = DARK_GREY,
                                                                                                background_color_active = GREY,
                                                                                                parent = self)
        self.lyt_prop_metadata = QtGui.QVBoxLayout()
        self.wdgt_prop_metadata.setLayout(self.lyt_prop_metadata)
        

        #wdgt_char_metadata
        self.wdgt_char_metadata = asset_manager_stylesheet_widget.AssetManagerStylesheetWidget(background_color_normal = DARK_GREY,
                                                                                                background_color_active = GREY,
                                                                                                parent = self)
        self.lyt_char_metadata = QtGui.QVBoxLayout()
        self.wdgt_char_metadata.setLayout(self.lyt_char_metadata)
        
        

        
        

        #stkwdgt_metadata
        self.stkwdgt_metadata =  QtGui.QStackedWidget()
        self.stkwdgt_metadata.addWidget(self.wdgt_shot_metadata)
        self.stkwdgt_metadata.addWidget(self.wdgt_prop_metadata)
        self.stkwdgt_metadata.addWidget(self.wdgt_char_metadata)
        
        #add stkwdgt_metadata to layout
        self.lyt_stacked_widget_container.addWidget(self.stkwdgt_metadata, 1, 1)


    def setup_stacked_widget_buttons(self):
        """
        Setup stacked widget buttons
        """

        #btn_show_shot_metadata
        self.btn_show_shot_metadata = asset_manager_button.AssetManagerButton( icon_name = ICON_SHOT,
                                                                                fixed_width = 64,
                                                                                fixed_height = 64,
                                                                                label_header_text = SHOT_METADATA_EXPLANATION_HEADER,
                                                                                label_text = SHOT_METADATA_EXPLANATION_TEXT,
                                                                                parent = self)
        self.btn_show_shot_metadata.setObjectName('btn_show_shot_metadata')
        self.lyt_metadata_buttons.addWidget(self.btn_show_shot_metadata)
        #btn_show_shot_metadata_divider
        self.btn_show_shot_metadata_divider = asset_manager_stylesheet_widget.AssetManagerStylesheetWidget(fixed_height = STACKEDWIDGET_DIVIDER_HEIGHT,
                                                                                                            fixed_width = 64,
                                                                                                            parent = self)
        self.btn_show_shot_metadata_divider.setObjectName('btn_show_shot_metadata_divider')
        self.lyt_metadata_buttons.addWidget(self.btn_show_shot_metadata_divider)
        

        

        #btn_show_prop_metadata
        self.btn_show_prop_metadata = asset_manager_button.AssetManagerButton(icon_name = ICON_PROP,
                                                                                fixed_width = 64,
                                                                                fixed_height = 64,
                                                                                label_header_text = PROP_METADATA_EXPLANATION_HEADER,
                                                                                label_text = PROP_METADATA_EXPLANATION_TEXT,
                                                                                parent = self)
        self.btn_show_prop_metadata.setObjectName('btn_show_prop_metadata')
        self.lyt_metadata_buttons.addWidget(self.btn_show_prop_metadata)
        #btn_show_prop_metadata_divider
        self.btn_show_prop_metadata_divider = asset_manager_stylesheet_widget.AssetManagerStylesheetWidget(fixed_height = STACKEDWIDGET_DIVIDER_HEIGHT,
                                                                                                            fixed_width = 64,
                                                                                                            parent = self)
        self.btn_show_prop_metadata_divider.setObjectName('btn_show_prop_metadata_divider')
        self.lyt_metadata_buttons.addWidget(self.btn_show_prop_metadata_divider)
        

        

        #btn_show_char_metadata
        self.btn_show_char_metadata = asset_manager_button.AssetManagerButton(icon_name = ICON_CHAR,
                                                                                fixed_width = 64,
                                                                                fixed_height = 64,
                                                                                label_header_text = CHAR_METADATA_EXPLANATION_HEADER,
                                                                                label_text = CHAR_METADATA_EXPLANATION_TEXT,
                                                                                parent = self)
        self.btn_show_char_metadata.setObjectName('btn_show_char_metadata')
        self.lyt_metadata_buttons.addWidget(self.btn_show_char_metadata)
        #btn_show_char_metadata_divider
        self.btn_show_char_metadata_divider = asset_manager_stylesheet_widget.AssetManagerStylesheetWidget(fixed_height = STACKEDWIDGET_DIVIDER_HEIGHT,
                                                                                                            fixed_width = 64,
                                                                                                            parent = self)
        self.btn_show_char_metadata_divider.setObjectName('btn_show_char_metadata_divider')
        self.lyt_metadata_buttons.addWidget(self.btn_show_char_metadata_divider)


    def set_active_stacked_widget(self, wdgt_sender):
        """
        Set active stacked widget based on wdgt_sender.
        """

        #wdgt_checklist
        wdgt_checklist = [(self.btn_show_shot_metadata, self.btn_show_shot_metadata_divider, self.wdgt_shot_metadata),
                            (self.btn_show_prop_metadata, self.btn_show_prop_metadata_divider, self.wdgt_prop_metadata),
                            (self.btn_show_char_metadata, self.btn_show_char_metadata_divider, self.wdgt_char_metadata)]

        #iterate and check
        for index, wdgt_list in enumerate(wdgt_checklist):
            
            for wdgt, wdgt_divider, wdgt_metadata in [wdgt_list]:
            
                #if match set  active
                if (wdgt is wdgt_sender):

                    #set_stylesheet
                    wdgt.set_stylesheet(role = 'active')
                    wdgt_divider.set_stylesheet(role = 'active')
                    wdgt_metadata.set_stylesheet(role = 'active')

                    #emit changed
                    self.stkwdgt_change_current.emit(index)

                #else normal
                else:

                    #set_stylesheet
                    wdgt.set_stylesheet(role = 'normal')
                    wdgt_divider.set_stylesheet(role = 'normal')
                    wdgt_metadata.set_stylesheet(role = 'normal')


    def set_explanation_text(self, wdgt_sender):
        """
        Set explanation text. Means setting the text for self.lbl_explanation_header
        and self.lbl_explanation_text.
        """

        #wdgt_checklist
        wdgt_checklist = [self.btn_show_shot_metadata, 
                            self.btn_show_prop_metadata, 
                            self.btn_show_char_metadata]

        #iterate and check
        for index, wdgt in enumerate(wdgt_checklist):
            
            #if match set text
            if (wdgt is wdgt_sender):

                #emit
                self.explanation_header_set_text.emit(wdgt_sender.label_header_text)
                self.explanation_text_set_text.emit(wdgt_sender.label_text)


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


    def setup_tool_palette_global(self):
        """
        Setup palette for tool and apply to all widgets.
        This should be applied before all unique customizations
        and stylesheets.
        """

        #wdgt_list
        wdgt_list = self.findChildren(QtCore.QObject)

        #customize palette
        for wdgt in wdgt_list:
            
            try:
                self.customize_palette(wdgt, QtGui.QPalette.Window, WINDOW_COLOR)
                self.customize_palette(wdgt, QtGui.QPalette.Background, BACKGROUND_COLOR)
                self.customize_palette(wdgt, QtGui.QPalette.WindowText, WINDOWTEXT_COLOR)
                self.customize_palette(wdgt, QtGui.QPalette.Foreground, FOREGROUND_COLOR)
                self.customize_palette(wdgt, QtGui.QPalette.Base, BASE_COLOR)
                self.customize_palette(wdgt, QtGui.QPalette.AlternateBase, ALTERNATEBASE_COLOR)
                self.customize_palette(wdgt, QtGui.QPalette.ToolTipBase, TOOLTIPBASE_COLOR)
                self.customize_palette(wdgt, QtGui.QPalette.ToolTipText, TOOLTIPTEXT_COLOR)
                self.customize_palette(wdgt, QtGui.QPalette.Text, TEXT_COLOR)
                self.customize_palette(wdgt, QtGui.QPalette.Button, BUTTON_COLOR)
                self.customize_palette(wdgt, QtGui.QPalette.ButtonText, BUTTONTEXT_COLOR)
                self.customize_palette(wdgt, QtGui.QPalette.BrightText, BRIGHTTEXT_COLOR)
                self.customize_palette(wdgt, QtGui.QPalette.Highlight, HIGHLIGHT_COLOR)
                self.customize_palette(wdgt, QtGui.QPalette.HighlightedText, HIGHLIGHTEDTEXT_COLOR)
                self.customize_palette(wdgt, QtGui.QPalette.Link, LINK_COLOR)
                self.customize_palette(wdgt, QtGui.QPalette.LinkVisited, LINKVISITED_COLOR)
            
            except:
                pass


    def setup_tool_palette_specific(self):
        """
        Setup the palette for specific widgets.
        Mostly needed for QWidgets that refuse to
        accepts background_color stylesheets
        """

        pass


    def setup_additional_buttons(self):
        """
        Setup additional buttons anywhere in the tool.
        """

        #setup_model_update_button
        if not(self.auto_update_models):
            self.setup_model_update_button()

        #setup_export_button
        self.setup_export_button()

        #setup_docs_button
        self.setup_docs_button()


    def setup_export_button(self):
        """
        Create self.btn_export
        """

        #btn_export
        self.btn_export = asset_manager_button.AssetManagerButton(icon_name = ICON_EXPORT,
                                                                    fixed_width = 64,
                                                                    fixed_height = 64,
                                                                    parent = self)
        self.btn_export.setObjectName('btn_export')
        self.lyt_metadata_buttons.addWidget(self.btn_export)
        #btn_export_divider
        self.btn_export_divider = asset_manager_stylesheet_widget.AssetManagerStylesheetWidget(fixed_height = STACKEDWIDGET_DIVIDER_HEIGHT,
                                                                                                fixed_width = 64,
                                                                                                parent = self)
        self.btn_export_divider.setObjectName('btn_export_divider')
        self.lyt_metadata_buttons.addWidget(self.btn_export_divider)


    def setup_model_update_button(self):
        """
        Create self.btn_update_models
        """

        #btn_update_models
        self.btn_update_models = asset_manager_button.AssetManagerButton(icon_name = ICON_UPDATE,
                                                                            fixed_width = 64,
                                                                            fixed_height = 64,
                                                                            parent = self)
        self.btn_update_models.setObjectName('btn_update_models')
        self.lyt_metadata_buttons.addWidget(self.btn_update_models)
        #btn_update_models_divider
        self.btn_update_models_divider = asset_manager_stylesheet_widget.AssetManagerStylesheetWidget(fixed_height = STACKEDWIDGET_DIVIDER_HEIGHT,
                                                                                                            fixed_width = 64,
                                                                                                            parent = self)
        self.btn_update_models_divider.setObjectName('btn_update_models_divider')
        self.lyt_metadata_buttons.addWidget(self.btn_update_models_divider)


    def setup_docs_button(self):
        """
        Create self.btn_docs
        """

        #btn_docs
        self.btn_docs = asset_manager_button.AssetManagerButton(icon_name = ICON_DOCS,
                                                                background_color_normal = DARK_ORANGE,
                                                                hover_radial_color_normal = WHITE,
                                                                hover_radial_radius = 0.4,
                                                                fixed_width = 64,
                                                                fixed_height = 64,
                                                                parent = self)
        self.btn_docs.setObjectName('btn_docs')
        self.lyt_docs.addWidget(self.btn_docs)
        


    def setup_progressbar(self):
        """
        Setup self.progressbar.
        """

        #progressbar
        self.progressbar = QtGui.QProgressBar()
        self.progressbar.setObjectName('progressbar')
        #customize
        self.progressbar.setTextVisible(False)
        self.progressbar.setValue(0)
        self.progressbar.setOrientation(QtCore.Qt.Vertical)
        self.progressbar.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)

        #add to lyt
        self.lyt_metadata_progress.addWidget(self.progressbar)
        
    
    def setup_mvc(self):
        """
        Setup all model-view controller.
        """

        #setup_mvc_shot_metadata
        self.setup_mvc_shot_metadata()


    def setup_mvc_shot_metadata(self):
        """
        Setup model-view controller for shot metadata.
        """
    
        #shot_metadata_view
        self.shot_metadata_view = shot_metadata_view.ShotMetadataView(self.logging_level)
        self.shot_metadata_view.setWordWrap(True)
        #set resize mode for horizontal header
        self.shot_metadata_view.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.shot_metadata_view.horizontalHeader().setStretchLastSection(False)
        self.shot_metadata_view.verticalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.shot_metadata_view.setAlternatingRowColors(True)
        #objectNames
        self.shot_metadata_view.setObjectName('shot_metadata_view')
        self.shot_metadata_view.horizontalHeader().setObjectName('shot_metadata_view_hor_header')
        self.shot_metadata_view.verticalHeader().setObjectName('shot_metadata_view_ver_header')
        #context menu
        self.shot_metadata_view.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        #add to ui
        self.lyt_shot_metadata.addWidget(self.shot_metadata_view)


        #shot_metadata_item_delegate
        self.shot_metadata_item_delegate = shot_metadata_item_delegate.ShotMetadataItemDelegate(self.logging_level)
        #set in view
        self.shot_metadata_view.setItemDelegate(self.shot_metadata_item_delegate)

        
        #shot_metadata_model
        self.shot_metadata_model = shot_metadata_model.ShotMetadataModel(self.logging_level)
        #set model in view
        self.shot_metadata_view.setModel(self.shot_metadata_model)

        #shot_metadata_selection_model
        self.shot_metadata_selection_model = QtGui.QItemSelectionModel(self.shot_metadata_model)
        self.shot_metadata_view.setSelectionModel(self.shot_metadata_selection_model)


    def display_shot_metadata_context_menu(self, pos):
        """
        Create and display shot metadata context menu.
        """
    
        menu = shot_metadata_context_menu.ShotMetadataContextMenu(parent = self)
        menu.set_view(self.shot_metadata_view)
        menu.popup(self.shot_metadata_view.mapToGlobal(pos))



    #MVC methods
    #------------------------------------------------------------------

    def convert_list_for_tablemodel(self, list_to_convert):
        """
        [obj, obj, obj] >> [[obj], [obj], [obj]]
        """

        #list false
        if not (list_to_convert):
            return [[]]

        #table_model_list
        table_model_list = [[pynode] for pynode in list_to_convert]

        return table_model_list


    def setup_auto_update_models(self, interval = 2000):
        """
        Create QTimer to automatically trigger update_models in intervals.
        """

        #auto_update_timer
        self.auto_update_timer = QtCore.QTimer(self)
        self.auto_update_timer.timeout.connect(self.update_models)
        self.auto_update_timer.start(interval)

    
    def update_models(self):
        """
        Update all models.
        """

        #update if neccessary
        if (self.update_models_necessary()):

            #log
            print('Update models: {0}'.format(time.time()))
            
            #update_shotmetadata_model
            self.update_shotmetadata_model()

            #update_propmetadata_model
            self.update_propmetadata_model()

            #update_charmetadata_model
            self.update_charmetadata_model()


    def get_hashstring_from_list(self, list_to_convert):
        """
        Convert a list to a hashable string.
        """

        #if list_to_convert empty
        if not (list_to_convert):
            return ''
        

        #sorted_list
        sorted_list = sorted([pynode.name() for pynode in list_to_convert])

        #hashable_string
        hashable_string = ''

        #iterate and concatenate
        for name in sorted_list:
            hashable_string += name

        return hashable_string


    def update_models_necessary(self):
        """
        Hash and check model metadata lists and 
        decide if update_models() is necessary.
        """

        #model data

        #shot_metadata_list_string
        shot_metadata_list_string = self.get_hashstring_from_list(self.shot_metadata_list)
        #prop_metadata_list_string
        prop_metadata_list_string = self.get_hashstring_from_list(self.prop_metadata_list)
        #char_metadata_list_string
        char_metadata_list_string = self.get_hashstring_from_list(self.char_metadata_list)

        #current_metadata_lists_string
        current_metadata_lists_string = shot_metadata_list_string + prop_metadata_list_string + char_metadata_list_string
        current_metadata_lists_string = str(current_metadata_lists_string)
        

        #current_metadata_lists_hash_object
        current_metadata_lists_hash_object = hashlib.sha1(bytearray(current_metadata_lists_string))
        current_model_lists_hex_digest = current_metadata_lists_hash_object.hexdigest()
        


        #scene data
        
        #new_shot_metadata_list
        new_shot_metadata_list = self.asset_manager_functionality.get_nodes_of_type('HelgaShotsMetadata')
        #new_prop_metadata_list
        new_prop_metadata_list = self.asset_manager_functionality.get_nodes_of_type('HelgaPropMetadata')
        #new_char_metadata_list
        new_char_metadata_list = self.asset_manager_functionality.get_nodes_of_type('HelgaCharacterMetadata')

        #new_shot_metadata_list_string
        new_shot_metadata_list_string = self.get_hashstring_from_list(new_shot_metadata_list)
        #new_prop_metadata_list_string
        new_prop_metadata_list_string = self.get_hashstring_from_list(new_prop_metadata_list)
        #new_char_metadata_list_string
        new_char_metadata_list_string = self.get_hashstring_from_list(new_char_metadata_list)

        #new_metadata_lists_string
        new_metadata_lists_string = new_shot_metadata_list_string + new_prop_metadata_list_string + new_char_metadata_list_string
        new_metadata_lists_string = str(new_metadata_lists_string)
        

        #new_metadata_lists_hash_object
        new_metadata_lists_hash_object = hashlib.sha1(bytearray(new_metadata_lists_string))
        new_model_lists_hex_digest = new_metadata_lists_hash_object.hexdigest()
        


        #compare and return
        if(new_model_lists_hex_digest == current_model_lists_hex_digest):
            return False

        return True


    def update_shotmetadata_model(self):
        """
        Update self.shot_metadata_model
        """

        #set_shot_metadata_list from scene
        self.set_shot_metadata_list()

        #list_for_tablemodel
        table_model_list = self.convert_list_for_tablemodel(self.shot_metadata_list)

        #set in model
        self.shot_metadata_model.update(table_model_list)


    def update_propmetadata_model(self):
        """
        Update self.prop_metadata_model
        """

        #set_prop_metadata_list from scene
        self.set_prop_metadata_list()

        '''
        #list_for_tablemodel
        table_model_list = self.convert_list_for_tablemodel(self.shot_metadata_list)

        #set in model
        self.shot_metadata_model.update(table_model_list)
        '''


    def update_charmetadata_model(self):
        """
        Update self.char_metadata_model
        """

        #set_char_metadata_list from scene
        self.set_char_metadata_list()

        '''
        #list_for_tablemodel
        table_model_list = self.convert_list_for_tablemodel(self.shot_metadata_list)

        #set in model
        self.shot_metadata_model.update(table_model_list)
        '''


    #Getter & Setter
    #------------------------------------------------------------------

    def set_status(self, new_value):
        """
        Set le_status text
        """
        try:
            
            #clear
            self.le_status.clear()
            #set text
            self.le_status.setText(new_value)

        except:

            pass
        

    def get_status(self):
        """
        Return content of le_status
        """

        try:
            return str(self.le_status.text())
        except:
            pass


    def customize_palette(self, wdgt, role, color):
        """
        Set background color for widget.
        """

        #setAutoFillBackground
        try:
            if(role == wdgt.backgroundRole()):
                wdgt.setAutoFillBackground(True)
        except:
            pass
        
        try:
            
            #palette_to_customize
            palette_to_customize = wdgt.palette()
            #set color
            palette_to_customize.setColor(role, color)
            wdgt.setPalette(palette_to_customize)
        
        except:

            #log
            self.logger.debug('Error setting palette for {0} - {1}'.format(wdgt.objectName(), wdgt))



    def set_shot_metadata_list(self):
        """
        Set self.shot_metadata_list
        """
        
        self.shot_metadata_list = self.asset_manager_functionality.get_nodes_of_type('HelgaShotsMetadata')


    def set_prop_metadata_list(self):
        """
        Set self.prop_metadata_list
        """
        
        self.prop_metadata_list = self.asset_manager_functionality.get_nodes_of_type('HelgaPropMetadata')


    def set_char_metadata_list(self):
        """
        Set self.char_metadata_list
        """
        
        self.char_metadata_list = self.asset_manager_functionality.get_nodes_of_type('HelgaCharacterMetadata')






    #Events
    #------------------------------------------------------------------

    def closeEvent(self, event):
        """
        Customized closeEvent
        """

        #stop timer
        if(self.auto_update_timer):
            self.auto_update_timer.stop()

        #parent close event
        self.parent_class.closeEvent(event)


    





    #Test
    #------------------------------------------------------------------

    def dummy_method(self, msg = 'dummy'):
        """
        Dummy method
        """

        #log
        self.logger.debug('{0}'.format(msg))
        #print
        print('{0}'.format(msg))
        

    def test_methods(self):
        """
        Suite of test methods to execute on startup.
        """

        #log
        self.logger.debug('\n\nExecute test methods:\n-----------------------------')


        
        #test methods here
        #------------------------------------------------------------------

        #dummy_method
        self.dummy_method()

        #asset_manager_functionality test
        print(self.asset_manager_functionality.get_nodes_of_type('HelgaShotsMetadata'))

        #------------------------------------------------------------------



        #log
        self.logger.debug('\n\n-----------------------------\nFinished test methods.')


    








#Run
#------------------------------------------------------------------

def run():
    """
    Standardized run() method
    """
    
    #asset_manager_instance
    asset_manager_instance = AssetManager()
    asset_manager_instance.show()










#Test setup home
#------------------------------------------------------------------

def asset_manager_run_home():
    """
    Copy and run @ home.
    Not to be used by anyone ever.
    """

    #Import
    #------------------------------------------------------------------
    #python
    import os
    import sys
    import shutil
    


    #Globals
    #------------------------------------------------------------------
    SOURCE_DIR = r'D:/filmaka/projects/helga/Production/scripts/work/helga/helga/maya/import_export'#dir to copy
    TARGET_DIR = r'D:/filmaka/projects/helga/Production/scripts/sandbox/helga/helga/maya/import_export'#source_dir is deleted from here if it exists and then copied in there

    

    #Delete existing
    #------------------------------------------------------------------
    try:
        if(os.path.isdir(TARGET_DIR)):
            print('Delete Dir: {0}'.format(TARGET_DIR))
            shutil.rmtree(TARGET_DIR)

    except:
        print('Delete Dir doesnt exist. Returning. - {0}'.format(TARGET_DIR))
        return


    #Copy
    #------------------------------------------------------------------
    
    try:
        if(os.path.isdir(SOURCE_DIR)):
            print('Copy {0} to {1}'.format(SOURCE_DIR, TARGET_DIR))
            shutil.copytree(SOURCE_DIR, TARGET_DIR)
            
    
    except:
        print('Copying failed. Returning. {0} to {1}'.format(SOURCE_DIR, TARGET_DIR))
        return
    





    #Run
    #------------------------------------------------------------------
    #helga
    from helga.maya.import_export.asset_manager import asset_manager
    reload(asset_manager)
    
    #asset_manager_instance
    asset_manager_instance = asset_manager.AssetManager()
    asset_manager_instance.show()



#asset_manager_run_home()




#Test
#------------------------------------------------------------------

if (__name__ == '__main__'):

    #run
    run()