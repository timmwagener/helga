

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
                dock_it=True,
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

        # dock_it
        self.dock_it = dock_it

        # logger
        self.logger = renderthreads_logging.get_logger(self.__class__.__name__)

        # Init procedure
        # ------------------------------------------------------------------

        # setupUi
        self.setupUi(self)

        # Add te_log_handler after creation of UI
        # ------------------------------------------------------------------
        self.te_log_handler = renderthreads_logging.get_handler(self.te_log)
        self.logger.addHandler(self.te_log_handler)

        # setup_additional_ui
        self.setup_additional_ui()

        # connect_ui
        self.connect_ui()

        # style_ui
        self.style_ui()

        # run_tests
        self.run_tests()

        # dock_it
        if (self.dock_it):
            renderthreads_gui_helper.make_dockable(self)

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

        # temp
        self.btn_menu_render.clicked.connect(functools.partial(self.dummy_method, 'G-Unit'))

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
        renderthreads_gui_helper.correct_styled_background_attribute(self)

        # set_margins_and_spacing
        renderthreads_gui_helper.set_margins_and_spacing_for_child_layouts(self)

        # set_stylesheet
        self.setStyleSheet(renderthreads_stylesheets.get_stylesheet())

    

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

    def dummy_method_silent(self):
        """
        Dummy method without output.
        """

        pass

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
