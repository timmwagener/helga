

"""
renderthreads
==========================================

GUI to start threaded nuke rendering.

To use it execute the following script in your Nuke
Script Editor.

.. code::

    from helga.nuke.rendering.renderthreads import renderthreads
    reload(renderthreads)

    #run
    renderthreads.run()

-----------------------

**Author:** `Timm Wagener <mailto:wagenertimm@gmail.com>`_
"""


# Add tool root path
# ------------------------------------------------------------------
# import
import sys
import os

# tool_root_path
tool_root_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(tool_root_path)


# Import
# ------------------------------------------------------------------
# python
import functools
import logging
# PySide
from PySide import QtGui
from PySide import QtCore
from PySide import QtUiTools


# Import variable
do_reload = True


# renderthreads

# lib

# renderthreads_globals
from lib import renderthreads_globals
if(do_reload):
    reload(renderthreads_globals)

# renderthreads_logging
from lib import renderthreads_logging
if(do_reload):
    reload(renderthreads_logging)

# lib.gui

# renderthreads_gui_helper
from lib.gui import renderthreads_gui_helper
if(do_reload):
    reload(renderthreads_gui_helper)

# renderthreads_stylesheets
from lib.gui import renderthreads_stylesheets
if(do_reload):
    reload(renderthreads_stylesheets)

# renderthreads_dock_widget
from lib.gui import renderthreads_dock_widget
if(do_reload):
    reload(renderthreads_dock_widget)


# Globals
# ------------------------------------------------------------------
# Version
VERSION = renderthreads_globals.VERSION
# Pathes
TOOL_ROOT_PATH = renderthreads_globals.TOOL_ROOT_PATH
ICONS_PATH = renderthreads_globals.ICONS_PATH
UI_PATH = renderthreads_globals.UI_PATH
# Icons
ICON_RENDERTHREADS = renderthreads_globals.ICON_RENDERTHREADS


# form_class, base_class
# ------------------------------------------------------------------
# ui_file
ui_file_name = 'renderthreads.ui'
ui_file = os.path.join(UI_PATH, ui_file_name)

# form_class, base_class
form_class, base_class = renderthreads_gui_helper.load_ui_type(ui_file)


# RenderThreads class
# ------------------------------------------------------------------
class RenderThreads(form_class, base_class):
    """
    RenderThreads class.
    """

    # Signals
    # ------------------------------------------------------------------

    # Create and initialize
    # ------------------------------------------------------------------
    def __new__(cls, *args, **kwargs):
        """
        RenderThreads instance factory.
        """

        # delete and cleanup old instances
        renderthreads_gui_helper.check_and_delete_wdgt_instances_with_class_name(cls.__name__)
        renderthreads_gui_helper.check_and_delete_wdgt_instances_with_class_name(renderthreads_dock_widget.RenderThreadsDockWidget.__name__)

        # renderthreads_instance
        renderthreads_instance = super(RenderThreads, cls).__new__(cls, args, kwargs)

        return renderthreads_instance

    def __init__(self,
                logging_level=logging.DEBUG,
                dock_it = True,
                thread_interval=2000,
                export_thread_timeout=300,
                hide_export_shell=True,
                threads_initial_logging_level=logging.CRITICAL,
                parent=renderthreads_gui_helper.get_nuke_main_window()):
        """
        Customize instance.
        """

        # super and objectName
        # ------------------------------------------------------------------
        # super
        self.parent_class = super(RenderThreads, self)
        self.parent_class.__init__(parent)

        # setObjectName
        self.setObjectName(self.__class__.__name__)

        # instance variables
        # ------------------------------------------------------------------
        # title
        self.title = self.__class__.__name__ + ' ' + str(VERSION)

        #dock_it
        self.dock_it = dock_it

        # logger
        # ------------------------------------------------------------------
        # logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logging_level = logging_level
        self.logger.setLevel(self.logging_level)

        # status_handler
        # self.status_handler = asset_manager_logging_handler.StatusStreamHandler(self)
        # self.logger.addHandler(self.status_handler)

        # Init procedure
        # ------------------------------------------------------------------

        # setupUi
        self.setupUi(self)

        # setup_additional_ui
        self.setup_additional_ui()

        # connect_ui
        self.connect_ui()

        # style_ui
        self.style_ui()

        # run_tests
        self.run_tests()

        #dock_it
        if (self.dock_it):
            self.make_dockable()

    # Additional UI
    # ------------------------------------------------------------------
    def setup_additional_ui(self):
        """
        Setup additional UI like mvc or helga tool header.
        """

        # make sure its floating intead of embedded
        self.setWindowFlags(QtCore.Qt.Window)

        # set title
        self.setWindowTitle(self.title)

    # Connections
    # ------------------------------------------------------------------
    def connect_ui(self):
        """
        Connect UI widgets with slots or functions.
        """

        # connect_signals
        self.connect_signals()

        # connect_buttons
        self.connect_buttons()

        # connect_widgets
        self.connect_widgets()

        # connect_threads
        self.connect_threads()

    def connect_signals(self):
        """
        Connect Signals for the ui.
        """

        pass

    def connect_buttons(self):
        """
        Connect buttons.
        """

        pass

    def connect_widgets(self):
        """
        Connect widgets.
        """

        pass

    def connect_threads(self):
        """
        Connect threads.
        """

        pass

    # Style
    # ------------------------------------------------------------------
    def style_ui(self):
        """
        Setup tool palette, tool stylesheet and specific widget stylesheets.
        """

        # correct_styled_background_attribute
        self.correct_styled_background_attribute()

        # set_margins_and_spacing
        self.set_margins_and_spacing()

        # set_stylesheet
        self.setStyleSheet(renderthreads_stylesheets.get_stylesheet())

    def correct_styled_background_attribute(self):
        """
        Set QtCore.Qt.WA_StyledBackground True for all widgets.
        Without this attr. set, the background-color stylesheet
        will have no effect on QWidgets. This should replace the
        need for palette settings.
        ToDo:
        Maybe add exclude list when needed.
        """

        # wdgt_list
        wdgt_list = self.findChildren(QtGui.QWidget)  # Return several types ?!?!

        # iterate and set
        for wdgt in wdgt_list:

            # check type
            if(type(wdgt) is QtGui.QWidget):

                # styled_background
                wdgt.setAttribute(QtCore.Qt.WA_StyledBackground, True)

    def set_margins_and_spacing(self):
        """
        Eliminate margin and spacing for all layout widgets.
        """

        # margin_list
        margin_list = [0, 0, 0, 0]

        # lyt_classes_list
        lyt_classes_list = [QtGui.QStackedLayout, QtGui.QGridLayout, QtGui.QFormLayout,
                            QtGui.QBoxLayout, QtGui.QVBoxLayout, QtGui.QHBoxLayout, QtGui.QBoxLayout]

        # lyt_list
        lyt_list = []
        for lyt_class in lyt_classes_list:
            lyt_list += [wdgt for wdgt in self.findChildren(lyt_class)]

        # set margin and spacing
        for lyt in lyt_list:

            # check type
            if(type(lyt) in lyt_classes_list):

                # set
                lyt.setContentsMargins(*margin_list)
                lyt.setSpacing(0)

    # Getter & Setter
    # ------------------------------------------------------------------

    # Misc
    # ------------------------------------------------------------------
    def dummy_method(self, msg='dummy'):
        """
        Dummy method.
        """

        # log
        self.logger.debug('{0}'.format(msg))
        # print
        print('{0}'.format(msg))

    def dummy_method_silent(self):
        """
        Dummy method without output.
        """

        # log
        self.logger.debug('{0}'.format(msg))
        # print
        print('{0}'.format(msg))

    # Test
    # ------------------------------------------------------------------
    def run_tests(self):
        """
        Suite of test methods.
        """

        # log
        self.logger.debug('\n\nExecute test methods:\n-----------------------------')

        # test methods start here
        # ------------------------------------------------------------------
        # ------------------------------------------------------------------

        # dummy_method
        self.dummy_method()

        # ------------------------------------------------------------------
        # ------------------------------------------------------------------
        # test methods end here

        # log
        self.logger.debug('\n\n-----------------------------\nFinished test methods.')

    # Docking
    #------------------------------------------------------------------
    def make_dockable(self):
        """
        Make this window dockable.
        """

        # nuke_main_window
        nuke_main_window = renderthreads_gui_helper.get_nuke_main_window()

        # q_main_window_list
        q_main_window_list = nuke_main_window.findChildren(QtGui.QMainWindow)
        # check
        if not (q_main_window_list):
            # log
            self.logger.debug('Current Nuke configuration has no QMainWindow instance which is needed for docking\
Not performing dock behaviour.')
            return

        # q_main_window
        q_main_window = q_main_window_list[0]

        # wdgt_dock
        self.wdgt_dock = renderthreads_dock_widget.RenderThreadsDockWidget(parent=q_main_window)
        self.wdgt_dock.setAllowedAreas(QtCore.Qt.AllDockWidgetAreas)

        # set title
        #self.wdgt_dock.setWindowTitle(self.title)

        # set wdgt
        self.wdgt_dock.setWidget(self)
        
        # add to maya main window
        q_main_window.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.wdgt_dock)

    # Events
    # ------------------------------------------------------------------
    def closeEvent(self, event):
        """
        Customized closeEvent.
        """

        # log
        self.logger.debug('Close Event')

        # stop_all_threads_and_timer
        # self.stop_all_threads_and_timer()

        # parent close event
        self.parent_class.closeEvent(event)


# Run
# ------------------------------------------------------------------
def run():
    """
    Standardized run() method.
    """

    # renderthreads_instance
    renderthreads_instance = RenderThreads()
    renderthreads_instance.show()
