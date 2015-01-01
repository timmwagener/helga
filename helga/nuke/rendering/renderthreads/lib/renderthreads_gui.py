

"""
renderthreads_gui
==========================================

This module encapsulates the creation/connection of the
additional specific ui.
"""


#  Import
#  ------------------------------------------------------------------
#  Python
import logging
import functools
#  PySide
from PySide import QtGui
from PySide import QtCore


#  Import variable
do_reload = True

#  renderthreads

#  lib

#  renderthreads_globals
import renderthreads_globals
if(do_reload):
    reload(renderthreads_globals)

#  renderthreads_logging
import renderthreads_logging
if(do_reload):
    reload(renderthreads_logging)

#  renderthreads_nuke
import renderthreads_nuke
if(do_reload):
    reload(renderthreads_nuke)

#  lib.gui

#  renderthreads_gui_helper
from gui import renderthreads_gui_helper
if(do_reload):
    reload(renderthreads_gui_helper)

#  renderthreads_stylesheets
from gui import renderthreads_stylesheets
if(do_reload):
    reload(renderthreads_stylesheets)


#  Globals
#  ------------------------------------------------------------------
TITLE = renderthreads_globals.TITLE
VERSION = renderthreads_globals.VERSION


#  logger (Module Level)
#  ------------------------------------------------------------------
logger = renderthreads_logging.get_logger(__name__)


#  Globals
#  ------------------------------------------------------------------


#  Functions
#  ------------------------------------------------------------------

#  Setup
#  ------------------------------------------------------------------
def setup_additional_ui(wdgt):
    """
    Main method that sets up the entire additional ui.
    """

    #  log
    logger.debug('create_additional_ui')
    # create_additional_ui
    create_additional_ui(wdgt)

    #  log
    logger.debug('connect_ui')
    # connect_ui
    connect_ui(wdgt)

    #  log
    logger.debug('style_ui')
    # style_ui
    style_ui(wdgt)


#  Create
#  ------------------------------------------------------------------
def create_additional_ui(wdgt):
    """
    Create the main menu for the asset manager.
    The wdgt arg. expects the asset manager instance to operate on.
    """

    #  make sure its floating intead of embedded
    wdgt.setWindowFlags(QtCore.Qt.Window)

    #  set title
    wdgt.setWindowTitle(TITLE + ' ' + str(VERSION))

    #  create_stkwdgt_menu
    create_stkwdgt_menu(wdgt)

    #  create_pbar_render
    create_pbar_render(wdgt)

    # dev
    if (wdgt.is_dev()):
        # create_dev_ui
        create_dev_ui(wdgt)


def create_stkwdgt_menu(wdgt):
    """
    Fake menu consisting of buttons that are
    switching the stkwdgt containing all the content.
    """

    #  lyt_stkwdgt_menu
    lyt_stkwdgt_menu = wdgt.wdgt_stkwdgt_menu.layout()

    # mnubar_stkwdgt
    wdgt.mnubar_stkwdgt = QtGui.QMenuBar(parent = wdgt)
    wdgt.mnubar_stkwdgt.setObjectName('mnubar_stkwdgt')
    lyt_stkwdgt_menu.addWidget(wdgt.mnubar_stkwdgt)

    # acn_render
    wdgt.acn_render = wdgt.mnubar_stkwdgt.addAction('Render')
    wdgt.acn_render.setObjectName('acn_render')

    # acn_threads
    wdgt.acn_threads = wdgt.mnubar_stkwdgt.addAction('Threads')
    wdgt.acn_threads.setObjectName('acn_threads')


def create_pbar_render(wdgt):
    """
    Setup progressbar for rendering.
    """

    #  lyt_pbar_render
    lyt_pbar_render = wdgt.wdgt_pbar_render.layout()

    #  pbar_render
    wdgt.pbar_render = QtGui.QProgressBar()
    wdgt.pbar_render.setOrientation(QtCore.Qt.Horizontal)
    wdgt.pbar_render.setMinimum(0)
    wdgt.pbar_render.setMaximum(99)
    wdgt.pbar_render.setValue(50)
    #  add
    lyt_pbar_render.addWidget(wdgt.pbar_render)


def create_dev_ui(wdgt):
    """
    Create additional ui when wdgt.is_dev() is True.
    """

    # add_dev_menu
    add_dev_menu(wdgt)


def add_dev_menu(wdgt):
    """
    Create dev wdgt and add it to the stkdgt_content.
    This is only happening when in dev mode.
    """

    # mnu_dev
    wdgt.mnu_dev = QtGui.QMenu('Dev', parent = wdgt)
    wdgt.mnu_dev.setObjectName('mnu_dev')
    wdgt.mnubar_stkwdgt.addMenu(wdgt.mnu_dev)

    # mnu_dev_nuke
    wdgt.mnu_dev_nuke = QtGui.QMenu('Nuke', parent = wdgt)
    wdgt.mnu_dev_nuke.setObjectName('mnu_dev_nuke')
    wdgt.mnu_dev.addMenu(wdgt.mnu_dev_nuke)

    #acn_print_all_write_nodes
    wdgt.acn_print_all_write_nodes = QtGui.QAction('Print all write nodes', wdgt)
    wdgt.acn_print_all_write_nodes.setObjectName('acn_print_all_write_nodes')
    wdgt.mnu_dev_nuke.addAction(wdgt.acn_print_all_write_nodes)

    #acn_print_selected_write_nodes
    wdgt.acn_print_selected_write_nodes = QtGui.QAction('Print selected write nodes', wdgt)
    wdgt.acn_print_selected_write_nodes.setObjectName('acn_print_selected_write_nodes')
    wdgt.mnu_dev_nuke.addAction(wdgt.acn_print_selected_write_nodes)

    # mnu_dev_threads
    wdgt.mnu_dev_threads = QtGui.QMenu('Threads', parent = wdgt)
    wdgt.mnu_dev_threads.setObjectName('mnu_dev_threads')
    wdgt.mnu_dev.addMenu(wdgt.mnu_dev_threads)

    #acn_test_threads
    wdgt.acn_test_threads = QtGui.QAction('Test threads', wdgt)
    wdgt.acn_test_threads.setObjectName('acn_test_threads')
    wdgt.mnu_dev_threads.addAction(wdgt.acn_test_threads)


#  Connect
#  ------------------------------------------------------------------
def connect_ui(wdgt):
    """
    Connect UI widgets with slots or functions.
    """

    #  connect_signals
    connect_signals(wdgt)

    #  connect_buttons
    connect_buttons(wdgt)

    #  connect_widgets
    connect_widgets(wdgt)

    #  connect_threads
    connect_threads(wdgt)

    # dev
    if (wdgt.is_dev()):
        # connect_dev_ui
        connect_dev_ui(wdgt)


def connect_signals(wdgt):
    """
    Connect Signals for the ui.
    """

    pass


def connect_buttons(wdgt):
    """
    Connect buttons.
    """

    pass


def connect_widgets(wdgt):
    """
    Connect widgets.
    """

    # acn_render
    wdgt.acn_render.triggered.connect(functools.partial(wdgt.stkwdgt_content.setCurrentIndex, 0))
    # acn_threads
    wdgt.acn_threads.triggered.connect(functools.partial(wdgt.stkwdgt_content.setCurrentIndex, 1))


def connect_threads(self):
    """
    Connect threads.
    """

    pass


def connect_dev_ui(wdgt):
    """
    Connect dev UI widgets with slots or functions.
    """

    # acn_print_all_write_nodes
    wdgt.acn_print_all_write_nodes.triggered.connect(functools.partial(renderthreads_nuke.get_write_nodes))
    # acn_print_selected_write_nodes
    wdgt.acn_print_selected_write_nodes.triggered.connect(functools.partial(renderthreads_nuke.get_selected_write_nodes))
    # acn_test_threads
    wdgt.acn_test_threads.triggered.connect(wdgt.thread_manager.test_setup)


#  Style
#  ------------------------------------------------------------------
def style_ui(wdgt):
    """
    Setup tool palette, tool stylesheet and specific widget stylesheets.
    """

    #  correct_styled_background_attribute
    renderthreads_gui_helper.correct_styled_background_attribute(wdgt)

    #  set_margins_and_spacing
    renderthreads_gui_helper.set_margins_and_spacing_for_child_layouts(wdgt)

    #  set_stylesheet
    wdgt.setStyleSheet(renderthreads_stylesheets.get_stylesheet())
