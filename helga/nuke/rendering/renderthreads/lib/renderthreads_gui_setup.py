

"""
renderthreads_gui_setup
==========================================

This module encapsulates the creation/connection of the
additional specific ui.
"""


#  Import
#  ------------------------------------------------------------------
#  Python
import logging
import functools
import multiprocessing
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

#  renderthreads_command_line_engine
import renderthreads_command_line_engine
if(do_reload):
    reload(renderthreads_command_line_engine)

#  lib.gui

#  renderthreads_gui_helper
from gui import renderthreads_gui_helper
if(do_reload):
    reload(renderthreads_gui_helper)

#  renderthreads_slider_widget
from gui import renderthreads_slider_widget
if(do_reload):
    reload(renderthreads_slider_widget)

#  renderthreads_command_line_flag_widget
from gui import renderthreads_command_line_flag_widget
if(do_reload):
    reload(renderthreads_command_line_flag_widget)

#  renderthreads_signal_remapper
from gui import renderthreads_signal_remapper
if(do_reload):
    reload(renderthreads_signal_remapper)

#  renderthreads_stylesheets
from gui import renderthreads_stylesheets
if(do_reload):
    reload(renderthreads_stylesheets)


#  Globals
#  ------------------------------------------------------------------
TITLE = renderthreads_globals.TITLE
VERSION = renderthreads_globals.VERSION

ICON_RENDERTHREADS = renderthreads_globals.ICON_RENDERTHREADS

INITIAL_LOGGING_LEVEL = renderthreads_globals.INITIAL_LOGGING_LEVEL

TEXT_DIVIDER = renderthreads_globals.TEXT_DIVIDER

COMMAND_LINE_FLAG_SPACING = renderthreads_globals.COMMAND_LINE_FLAG_SPACING

WRITE_NODE_REPLACEMENT_TEMPLATE = renderthreads_globals.WRITE_NODE_REPLACEMENT_TEMPLATE


#  logger (Module Level)
#  ------------------------------------------------------------------
logger = renderthreads_logging.get_logger(__name__)


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

    #  set icon
    wdgt.setWindowIcon(QtGui.QIcon(ICON_RENDERTHREADS))

    #  create_stkwdgt_menu
    create_stkwdgt_menu(wdgt)

    # create_threads_menu
    create_threads_menu(wdgt)

    # create_command_line_menu
    create_command_line_menu(wdgt)

    # create_options_menu
    create_options_menu(wdgt)

    #  create_pbar_render
    create_pbar_render(wdgt)

    #  create_signal_remapper
    create_signal_remapper(wdgt)

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

    # acn_command_line
    wdgt.acn_command_line = wdgt.mnubar_stkwdgt.addAction('Cmd. Line')
    wdgt.acn_command_line.setObjectName('acn_command_line')

    # acn_options
    wdgt.acn_options = wdgt.mnubar_stkwdgt.addAction('Options')
    wdgt.acn_options.setObjectName('acn_options')


def create_threads_menu(wdgt):
    """
    Menu for threads. This function
    creates not a QMenu but the entire optons
    content for the stackwidget threads page.
    """

    # create_sub_threads_menu
    create_sub_threads_menu(wdgt)

    # create_queue_menu
    create_queue_menu(wdgt)

    # add stretch
    lyt_sawdgt_threads_options = wdgt.sawdgt_threads_options.layout()
    lyt_sawdgt_threads_options.addStretch()


def create_sub_threads_menu(wdgt):
    """
    Menu for threads that use the the custom
    renderthreads slider widget.
    """

    #  frm_threads
    frm_threads = wdgt.frm_threads.layout()

    # sldr_threadcount
    wdgt.sldr_threadcount = renderthreads_slider_widget.Slider(header = 'Threadcount',
                                                                minimum = 1,
                                                                maximum = wdgt.thread_manager.get_max_threads(),
                                                                initial_value = wdgt.thread_manager.get_thread_count())
    wdgt.sldr_threadcount.set_tick_position(QtGui.QSlider.TicksBelow)
    wdgt.sldr_threadcount.set_tick_interval(1)
    frm_threads.addWidget(wdgt.sldr_threadcount)

    # sldr_thread_interval
    wdgt.sldr_thread_interval = renderthreads_slider_widget.Slider(header = 'Thread interval',
                                                                minimum = 100,
                                                                maximum = 10000,
                                                                initial_value = 2000)
    wdgt.sldr_thread_interval.set_tick_position(QtGui.QSlider.TicksBelow)
    wdgt.sldr_thread_interval.set_tick_interval(100)
    frm_threads.addWidget(wdgt.sldr_thread_interval)

    # btn_start_threads
    wdgt.btn_start_threads = QtGui.QPushButton('Re/Start threads')
    wdgt.btn_start_threads.setFlat(True)
    frm_threads.addWidget(wdgt.btn_start_threads)

    # btn_stop_threads
    wdgt.btn_stop_threads = QtGui.QPushButton('Stop threads')
    wdgt.btn_stop_threads.setFlat(True)
    frm_threads.addWidget(wdgt.btn_stop_threads)


def create_queue_menu(wdgt):
    """
    Menu for thread queue.
    """

    #  lyt_frm_queue
    lyt_frm_queue = wdgt.frm_queue.layout()

    # btn_print_queue_size
    wdgt.btn_print_queue_size = QtGui.QPushButton('Print queue size')
    wdgt.btn_print_queue_size.setFlat(True)
    lyt_frm_queue.addWidget(wdgt.btn_print_queue_size)

    # btn_reset_queue
    wdgt.btn_reset_queue = QtGui.QPushButton('Reset queue')
    wdgt.btn_reset_queue.setFlat(True)
    lyt_frm_queue.addWidget(wdgt.btn_reset_queue)


def create_command_line_menu(wdgt):
    """
    Menu for command line. This function
    creates not a QMenu but the entire optons
    content for the stackwidget command line page.
    """

    # create_command_line
    create_command_line(wdgt)

    # create_flags_menu
    create_flags_menu(wdgt)

    # create_constants_menu
    create_constants_menu(wdgt)

    # update_command_line
    update_command_line(wdgt)


def create_command_line(wdgt):
    """
    Create wdgt.lbl_command_line which displays
    the current command line.
    """

    # tooltip
    tooltip = 'This is the current command line that will be used for the render process.\n\
{0}\n\
PLEASE KEEP IN MIND:\n\
Not all the command line flags make sense together. Some settings and combinations\n\
might be invalid and cause the render to fail.'.format(TEXT_DIVIDER)
    wdgt.frm_command_line.setToolTip(tooltip)

    #  lyt_frm_command_line
    lyt_frm_command_line = wdgt.frm_command_line.layout()

    # lbl_command_line
    wdgt.lbl_command_line = QtGui.QLabel(parent = wdgt)
    wdgt.lbl_command_line.setObjectName('lbl_command_line')
    wdgt.lbl_command_line.setText('temp')
    wdgt.lbl_command_line.setWordWrap(True)
    lyt_frm_command_line.addWidget(wdgt.lbl_command_line)


def create_flags_menu(wdgt):
    """
    Menu for command line options.
    """

    # command_line_flag_list
    wdgt.command_line_flag_list = []

    #  lyt_frm_command_line_options
    lyt_frm_command_line_options = wdgt.frm_command_line_options.layout()

    
    # flg_a
    tooltip = 'Formats default to anamorphic.'
    wdgt.flg_a = renderthreads_command_line_flag_widget.CommandLineFlag(flag = '-a',
                                                                        state = False,
                                                                        tooltip = tooltip,
                                                                        checkable = True,
                                                                        parent = wdgt)
    lyt_frm_command_line_options.addWidget(wdgt.flg_a)
    # command_line_flag_list
    wdgt.command_line_flag_list.append(wdgt.flg_a)
    # spacer widget
    renderthreads_gui_helper.insert_spacer_widget(lyt_frm_command_line_options, 0, COMMAND_LINE_FLAG_SPACING, wdgt)


    # flg_nukeassist
    tooltip = 'Run in Nuke Assist mode.'
    wdgt.flg_nukeassist = renderthreads_command_line_flag_widget.CommandLineFlag(flag = '--nukeassist',
                                                                                    state = False,
                                                                                    tooltip = tooltip,
                                                                                    checkable = True,
                                                                                    parent = wdgt)
    lyt_frm_command_line_options.addWidget(wdgt.flg_nukeassist)
    # command_line_flag_list
    wdgt.command_line_flag_list.append(wdgt.flg_nukeassist)
    # spacer widget
    renderthreads_gui_helper.insert_spacer_widget(lyt_frm_command_line_options, 0, COMMAND_LINE_FLAG_SPACING, wdgt)

    
    # flg_b
    tooltip = 'Start in background.'
    wdgt.flg_b = renderthreads_command_line_flag_widget.CommandLineFlag(flag = '-b',
                                                                        state = False,
                                                                        tooltip = tooltip,
                                                                        checkable = True,
                                                                        parent = wdgt)
    lyt_frm_command_line_options.addWidget(wdgt.flg_b)
    # command_line_flag_list
    wdgt.command_line_flag_list.append(wdgt.flg_b)
    # spacer widget
    renderthreads_gui_helper.insert_spacer_widget(lyt_frm_command_line_options, 0, COMMAND_LINE_FLAG_SPACING, wdgt)


    # flg_c
    tooltip = 'Limit cache memory usage. Size is in bytes\nor append k, M, G or T'
    wdgt_parameter = QtGui.QLineEdit(parent = wdgt)
    wdgt.flg_c = renderthreads_command_line_flag_widget.CommandLineFlag(flag = '-c',
                                                                        state = False,
                                                                        tooltip = tooltip,
                                                                        checkable = True,
                                                                        wdgt_parameter = wdgt_parameter,
                                                                        parent = wdgt)
    lyt_frm_command_line_options.addWidget(wdgt.flg_c)
    # command_line_flag_list
    wdgt.command_line_flag_list.append(wdgt.flg_c)
    # spacer widget
    renderthreads_gui_helper.insert_spacer_widget(lyt_frm_command_line_options, 0, COMMAND_LINE_FLAG_SPACING, wdgt)


    # flg_cont
    tooltip = 'Attempt to render subsequent frames in the range after an error.\n\
If not specified, the application will stop on the first error.'
    wdgt.flg_cont = renderthreads_command_line_flag_widget.CommandLineFlag(flag = '--cont',
                                                                            state = False,
                                                                            tooltip = tooltip,
                                                                            checkable = True,
                                                                            parent = wdgt)
    lyt_frm_command_line_options.addWidget(wdgt.flg_cont)
    # command_line_flag_list
    wdgt.command_line_flag_list.append(wdgt.flg_cont)
    # spacer widget
    renderthreads_gui_helper.insert_spacer_widget(lyt_frm_command_line_options, 0, COMMAND_LINE_FLAG_SPACING, wdgt)


    # flg_d
    tooltip = 'Set X display name.'
    wdgt.flg_d = renderthreads_command_line_flag_widget.CommandLineFlag(flag = '-d',
                                                                        state = False,
                                                                        tooltip = tooltip,
                                                                        checkable = True,
                                                                        parent = wdgt)
    lyt_frm_command_line_options.addWidget(wdgt.flg_d)
    # command_line_flag_list
    wdgt.command_line_flag_list.append(wdgt.flg_d)
    # spacer widget
    renderthreads_gui_helper.insert_spacer_widget(lyt_frm_command_line_options, 0, COMMAND_LINE_FLAG_SPACING, wdgt)


    # flg_f
    tooltip = 'Render at full size (turns off proxy).'
    wdgt.flg_f = renderthreads_command_line_flag_widget.CommandLineFlag(flag = '-f',
                                                                        state = False,
                                                                        tooltip = tooltip,
                                                                        checkable = True,
                                                                        parent = wdgt)
    lyt_frm_command_line_options.addWidget(wdgt.flg_f)
    # command_line_flag_list
    wdgt.command_line_flag_list.append(wdgt.flg_f)
    # spacer widget
    renderthreads_gui_helper.insert_spacer_widget(lyt_frm_command_line_options, 0, COMMAND_LINE_FLAG_SPACING, wdgt)


    # flg_F
    tooltip = 'Frame numbers to execute the script at.\n\
A range can be one of:\n\
"A"        single frame number A\n\
"A-B"      all frames from A through B\n\
"A-BxC"    every Cth frame from A to last one less or equal to B.\n\
{0}\n\
THIS FLAG IS NOT AVAILABLE FOR USER INPUT\n\
SINCE IT IS HANDLED BY THE TOOL INTERNALLY.'.format(TEXT_DIVIDER)
    wdgt_parameter = QtGui.QSpinBox(parent = wdgt)
    wdgt_parameter.setValue(1)
    wdgt.flg_F = renderthreads_command_line_flag_widget.CommandLineFlag(flag = '-F',
                                                                        tooltip = tooltip,
                                                                        checkable = False,
                                                                        wdgt_parameter = wdgt_parameter,
                                                                        parent = wdgt)
    lyt_frm_command_line_options.addWidget(wdgt.flg_F)
    # force parameter enabled
    wdgt.flg_F.force_parameter_enabled(False)
    # command_line_flag_list
    wdgt.command_line_flag_list.append(wdgt.flg_F)
    # spacer widget
    renderthreads_gui_helper.insert_spacer_widget(lyt_frm_command_line_options, 0, COMMAND_LINE_FLAG_SPACING, wdgt)


    # flg_gpu
    tooltip = 'Enables GPU usage when in terminal mode with an optional gpu index argument\n\
that defaults to 0 if none given. Will override preferences when in interactive mode.'
    wdgt_parameter = QtGui.QLineEdit(text = '0', parent = wdgt)
    wdgt.flg_gpu = renderthreads_command_line_flag_widget.CommandLineFlag(flag = '--gpu',
                                                                            state = False,
                                                                            tooltip = tooltip,
                                                                            checkable = True,
                                                                            wdgt_parameter = wdgt_parameter,
                                                                            parent = wdgt)
    lyt_frm_command_line_options.addWidget(wdgt.flg_gpu)
    # command_line_flag_list
    wdgt.command_line_flag_list.append(wdgt.flg_gpu)
    # spacer widget
    renderthreads_gui_helper.insert_spacer_widget(lyt_frm_command_line_options, 0, COMMAND_LINE_FLAG_SPACING, wdgt)


    # flg_gpulist
    tooltip = 'Print the selectable gpus and their index.'
    wdgt.flg_gpulist = renderthreads_command_line_flag_widget.CommandLineFlag(flag = '--gpulist',
                                                                                state = False,
                                                                                tooltip = tooltip,
                                                                                checkable = True,
                                                                                parent = wdgt)
    lyt_frm_command_line_options.addWidget(wdgt.flg_gpulist)
    # command_line_flag_list
    wdgt.command_line_flag_list.append(wdgt.flg_gpulist)
    # spacer widget
    renderthreads_gui_helper.insert_spacer_widget(lyt_frm_command_line_options, 0, COMMAND_LINE_FLAG_SPACING, wdgt)


    # flg_h
    tooltip = 'Print help and exit.'
    wdgt.flg_h = renderthreads_command_line_flag_widget.CommandLineFlag(flag = '-h',
                                                                                state = False,
                                                                                tooltip = tooltip,
                                                                                checkable = True,
                                                                                parent = wdgt)
    lyt_frm_command_line_options.addWidget(wdgt.flg_h)
    # command_line_flag_list
    wdgt.command_line_flag_list.append(wdgt.flg_h)
    # spacer widget
    renderthreads_gui_helper.insert_spacer_widget(lyt_frm_command_line_options, 0, COMMAND_LINE_FLAG_SPACING, wdgt)


    # flg_hiero
    tooltip = 'License against a Hiero license instead of a Nuke one.'
    wdgt.flg_hiero = renderthreads_command_line_flag_widget.CommandLineFlag(flag = '--hiero',
                                                                                state = False,
                                                                                tooltip = tooltip,
                                                                                checkable = True,
                                                                                parent = wdgt)
    lyt_frm_command_line_options.addWidget(wdgt.flg_hiero)
    # command_line_flag_list
    wdgt.command_line_flag_list.append(wdgt.flg_hiero)
    # spacer widget
    renderthreads_gui_helper.insert_spacer_widget(lyt_frm_command_line_options, 0, COMMAND_LINE_FLAG_SPACING, wdgt)


    # flg_i
    tooltip = 'With -x or -t use interactive, not render, license.'
    wdgt.flg_i = renderthreads_command_line_flag_widget.CommandLineFlag(flag = '-i',
                                                                        state = False,
                                                                        tooltip = tooltip,
                                                                        checkable = True,
                                                                        parent = wdgt)
    lyt_frm_command_line_options.addWidget(wdgt.flg_i)
    # command_line_flag_list
    wdgt.command_line_flag_list.append(wdgt.flg_i)
    # spacer widget
    renderthreads_gui_helper.insert_spacer_widget(lyt_frm_command_line_options, 0, COMMAND_LINE_FLAG_SPACING, wdgt)


    # flg_l
    tooltip = 'Apply linear transfer to the file read in.'
    wdgt.flg_l = renderthreads_command_line_flag_widget.CommandLineFlag(flag = '-l',
                                                                        state = False,
                                                                        tooltip = tooltip,
                                                                        checkable = True,
                                                                        parent = wdgt)
    lyt_frm_command_line_options.addWidget(wdgt.flg_l)
    # command_line_flag_list
    wdgt.command_line_flag_list.append(wdgt.flg_l)
    # spacer widget
    renderthreads_gui_helper.insert_spacer_widget(lyt_frm_command_line_options, 0, COMMAND_LINE_FLAG_SPACING, wdgt)


    # flg_m
    tooltip = 'Set threads count.'
    cpu_count = multiprocessing.cpu_count()
    wdgt_parameter = QtGui.QSpinBox(parent = wdgt)
    wdgt_parameter.setMinimum(1)
    wdgt_parameter.setMaximum(cpu_count)
    wdgt_parameter.setValue(cpu_count)
    wdgt.flg_m = renderthreads_command_line_flag_widget.CommandLineFlag(flag = '-m',
                                                                        state = False,
                                                                        tooltip = tooltip,
                                                                        checkable = True,
                                                                        wdgt_parameter = wdgt_parameter,
                                                                        parent = wdgt)
    lyt_frm_command_line_options.addWidget(wdgt.flg_m)
    # command_line_flag_list
    wdgt.command_line_flag_list.append(wdgt.flg_m)
    # spacer widget
    renderthreads_gui_helper.insert_spacer_widget(lyt_frm_command_line_options, 0, COMMAND_LINE_FLAG_SPACING, wdgt)


    # flg_n
    tooltip = 'Don\'t run postagestamps and don\'t open windows.'
    wdgt.flg_n = renderthreads_command_line_flag_widget.CommandLineFlag(flag = '-n',
                                                                        state = False,
                                                                        tooltip = tooltip,
                                                                        checkable = True,
                                                                        parent = wdgt)
    lyt_frm_command_line_options.addWidget(wdgt.flg_n)
    # command_line_flag_list
    wdgt.command_line_flag_list.append(wdgt.flg_n)
    # spacer widget
    renderthreads_gui_helper.insert_spacer_widget(lyt_frm_command_line_options, 0, COMMAND_LINE_FLAG_SPACING, wdgt)


    # flg_nukex
    tooltip = 'Run as NukeX instead of standard Nuke.'
    wdgt.flg_nukex = renderthreads_command_line_flag_widget.CommandLineFlag(flag = '--nukex',
                                                                            state = True,
                                                                            tooltip = tooltip,
                                                                            checkable = True,
                                                                            parent = wdgt)
    lyt_frm_command_line_options.addWidget(wdgt.flg_nukex)
    # command_line_flag_list
    wdgt.command_line_flag_list.append(wdgt.flg_nukex)
    # spacer widget
    renderthreads_gui_helper.insert_spacer_widget(lyt_frm_command_line_options, 0, COMMAND_LINE_FLAG_SPACING, wdgt)


    # flg_p
    tooltip = 'Turn on proxy mode (use -f to force full size).'
    wdgt.flg_p = renderthreads_command_line_flag_widget.CommandLineFlag(flag = '-p',
                                                                        state = False,
                                                                        tooltip = tooltip,
                                                                        checkable = True,
                                                                        parent = wdgt)
    lyt_frm_command_line_options.addWidget(wdgt.flg_p)
    # command_line_flag_list
    wdgt.command_line_flag_list.append(wdgt.flg_p)
    # spacer widget
    renderthreads_gui_helper.insert_spacer_widget(lyt_frm_command_line_options, 0, COMMAND_LINE_FLAG_SPACING, wdgt)


    # flg_P
    tooltip = 'Measure performance metrics and show in DAG.'
    wdgt.flg_P = renderthreads_command_line_flag_widget.CommandLineFlag(flag = '-P',
                                                                        state = False,
                                                                        tooltip = tooltip,
                                                                        checkable = True,
                                                                        parent = wdgt)
    lyt_frm_command_line_options.addWidget(wdgt.flg_P)
    # command_line_flag_list
    wdgt.command_line_flag_list.append(wdgt.flg_P)
    # spacer widget
    renderthreads_gui_helper.insert_spacer_widget(lyt_frm_command_line_options, 0, COMMAND_LINE_FLAG_SPACING, wdgt)


    # flg_pause
    tooltip = 'Initial viewers in script specified on command line should be paused'
    wdgt.flg_pause = renderthreads_command_line_flag_widget.CommandLineFlag(flag = '--pause',
                                                                            state = False,
                                                                            tooltip = tooltip,
                                                                            checkable = True,
                                                                            parent = wdgt)
    lyt_frm_command_line_options.addWidget(wdgt.flg_pause)
    # command_line_flag_list
    wdgt.command_line_flag_list.append(wdgt.flg_pause)
    # spacer widget
    renderthreads_gui_helper.insert_spacer_widget(lyt_frm_command_line_options, 0, COMMAND_LINE_FLAG_SPACING, wdgt)


    # flg_safe
    tooltip = 'Stops any scripts or plugins in ~/.nuke, $NUKE_PATH being executed\n\
as well as stopping any Ofx plugins being loaded (including FurnaceCore)'
    wdgt.flg_safe = renderthreads_command_line_flag_widget.CommandLineFlag(flag = '--safe',
                                                                            state = False,
                                                                            tooltip = tooltip,
                                                                            checkable = True,
                                                                            parent = wdgt)
    lyt_frm_command_line_options.addWidget(wdgt.flg_safe)
    # command_line_flag_list
    wdgt.command_line_flag_list.append(wdgt.flg_safe)
    # spacer widget
    renderthreads_gui_helper.insert_spacer_widget(lyt_frm_command_line_options, 0, COMMAND_LINE_FLAG_SPACING, wdgt)


    # flg_ple
    tooltip = 'Run in Personal Learning Edition mode (see user guide)'
    wdgt.flg_ple = renderthreads_command_line_flag_widget.CommandLineFlag(flag = '--ple',
                                                                            state = False,
                                                                            tooltip = tooltip,
                                                                            checkable = True,
                                                                            parent = wdgt)
    lyt_frm_command_line_options.addWidget(wdgt.flg_ple)
    # command_line_flag_list
    wdgt.command_line_flag_list.append(wdgt.flg_ple)
    # spacer widget
    renderthreads_gui_helper.insert_spacer_widget(lyt_frm_command_line_options, 0, COMMAND_LINE_FLAG_SPACING, wdgt)


    # flg_priority
    tooltip = 'Run the application with a different priority.\n\
Choose from:\n\
high (only available to super user on Linux/OS X)\n\
medium\n\
low'
    wdgt_parameter = QtGui.QComboBox(parent = wdgt)
    wdgt_parameter.insertItems(0, ['high', 'medium', 'low'])
    wdgt.flg_priority = renderthreads_command_line_flag_widget.CommandLineFlag(flag = '--priority',
                                                                                state = False,
                                                                                tooltip = tooltip,
                                                                                checkable = True,
                                                                                wdgt_parameter = wdgt_parameter,
                                                                                parent = wdgt)
    lyt_frm_command_line_options.addWidget(wdgt.flg_priority)
    # command_line_flag_list
    wdgt.command_line_flag_list.append(wdgt.flg_priority)
    # spacer widget
    renderthreads_gui_helper.insert_spacer_widget(lyt_frm_command_line_options, 0, COMMAND_LINE_FLAG_SPACING, wdgt)


    # flg_q
    tooltip = 'Quiet (don\'t print stuff).'
    wdgt.flg_q = renderthreads_command_line_flag_widget.CommandLineFlag(flag = '-q',
                                                                            state = False,
                                                                            tooltip = tooltip,
                                                                            checkable = True,
                                                                            parent = wdgt)
    lyt_frm_command_line_options.addWidget(wdgt.flg_q)
    # command_line_flag_list
    wdgt.command_line_flag_list.append(wdgt.flg_q)
    # spacer widget
    renderthreads_gui_helper.insert_spacer_widget(lyt_frm_command_line_options, 0, COMMAND_LINE_FLAG_SPACING, wdgt)


    # flg_s
    tooltip = 'Sets the minimum stack size for each thread in bytes;\n\
this defaults to 16777216 (16MB) the smallest allowed value is 1048576 (1MB).'
    wdgt_parameter = QtGui.QSpinBox(parent = wdgt)
    wdgt_parameter.setMinimum(1048576)
    wdgt_parameter.setMaximum(1048576 * 1000)
    wdgt_parameter.setValue(16777216)
    wdgt.flg_s = renderthreads_command_line_flag_widget.CommandLineFlag(flag = '-s',
                                                                            state = False,
                                                                            tooltip = tooltip,
                                                                            checkable = True,
                                                                            wdgt_parameter = wdgt_parameter,
                                                                            parent = wdgt)
    lyt_frm_command_line_options.addWidget(wdgt.flg_s)
    # command_line_flag_list
    wdgt.command_line_flag_list.append(wdgt.flg_s)
    # spacer widget
    renderthreads_gui_helper.insert_spacer_widget(lyt_frm_command_line_options, 0, COMMAND_LINE_FLAG_SPACING, wdgt)


    # flg_sro
    tooltip = 'Force the application to obey the render order of Write\n\
nodes such that Reads can use files created by earlier Write nodes'
    wdgt.flg_sro = renderthreads_command_line_flag_widget.CommandLineFlag(flag = '--sro',
                                                                            state = False,
                                                                            tooltip = tooltip,
                                                                            checkable = True,
                                                                            parent = wdgt)
    lyt_frm_command_line_options.addWidget(wdgt.flg_sro)
    # command_line_flag_list
    wdgt.command_line_flag_list.append(wdgt.flg_sro)
    # spacer widget
    renderthreads_gui_helper.insert_spacer_widget(lyt_frm_command_line_options, 0, COMMAND_LINE_FLAG_SPACING, wdgt)


    # flg_t
    tooltip = 'Terminal only (no gui).\n\
If <script> is a .py file it will be executed.'
    wdgt.flg_t = renderthreads_command_line_flag_widget.CommandLineFlag(flag = '-t',
                                                                            state = False,
                                                                            tooltip = tooltip,
                                                                            checkable = True,
                                                                            parent = wdgt)
    lyt_frm_command_line_options.addWidget(wdgt.flg_t)
    # command_line_flag_list
    wdgt.command_line_flag_list.append(wdgt.flg_t)
    # spacer widget
    renderthreads_gui_helper.insert_spacer_widget(lyt_frm_command_line_options, 0, COMMAND_LINE_FLAG_SPACING, wdgt)


    # flg_tg
    tooltip = 'Terminal mode, but starting a QApplication so PySide/\n\
PyQt can be used. Needs an X session.'
    wdgt.flg_tg = renderthreads_command_line_flag_widget.CommandLineFlag(flag = '--tg',
                                                                            state = False,
                                                                            tooltip = tooltip,
                                                                            checkable = True,
                                                                            parent = wdgt)
    lyt_frm_command_line_options.addWidget(wdgt.flg_tg)
    # command_line_flag_list
    wdgt.command_line_flag_list.append(wdgt.flg_tg)
    # spacer widget
    renderthreads_gui_helper.insert_spacer_widget(lyt_frm_command_line_options, 0, COMMAND_LINE_FLAG_SPACING, wdgt)


    # flg_V
    tooltip = 'Print more stuff, choose level from:\n\
0 (not verbose)\n\
1 (output nuke script load and save)\n\
2 (output loading plugins, python, tcl, nuke scripts, progress and buffer report).'
    wdgt_parameter = QtGui.QSpinBox(parent = wdgt)
    wdgt_parameter.setMinimum(0)
    wdgt_parameter.setMaximum(2)
    wdgt_parameter.setValue(0)
    wdgt.flg_V = renderthreads_command_line_flag_widget.CommandLineFlag(flag = '-V',
                                                                            state = False,
                                                                            tooltip = tooltip,
                                                                            checkable = True,
                                                                            wdgt_parameter = wdgt_parameter,
                                                                            parent = wdgt)
    lyt_frm_command_line_options.addWidget(wdgt.flg_V)
    # command_line_flag_list
    wdgt.command_line_flag_list.append(wdgt.flg_V)
    # spacer widget
    renderthreads_gui_helper.insert_spacer_widget(lyt_frm_command_line_options, 0, COMMAND_LINE_FLAG_SPACING, wdgt)


    # flg_view
    tooltip = 'Only execute these views (comma-separated list: e.g. \'left,right\').'
    wdgt_parameter = QtGui.QLineEdit(text = '', parent = wdgt)
    wdgt.flg_view = renderthreads_command_line_flag_widget.CommandLineFlag(flag = '--view',
                                                                            state = False,
                                                                            tooltip = tooltip,
                                                                            checkable = True,
                                                                            wdgt_parameter = wdgt_parameter,
                                                                            parent = wdgt)
    lyt_frm_command_line_options.addWidget(wdgt.flg_view)
    # command_line_flag_list
    wdgt.command_line_flag_list.append(wdgt.flg_view)
    # spacer widget
    renderthreads_gui_helper.insert_spacer_widget(lyt_frm_command_line_options, 0, COMMAND_LINE_FLAG_SPACING, wdgt)


    # flg_version
    tooltip = 'Print version information and exit.'
    wdgt.flg_version = renderthreads_command_line_flag_widget.CommandLineFlag(flag = '--version',
                                                                            state = False,
                                                                            tooltip = tooltip,
                                                                            checkable = True,
                                                                            parent = wdgt)
    lyt_frm_command_line_options.addWidget(wdgt.flg_version)
    # command_line_flag_list
    wdgt.command_line_flag_list.append(wdgt.flg_version)
    # spacer widget
    renderthreads_gui_helper.insert_spacer_widget(lyt_frm_command_line_options, 0, COMMAND_LINE_FLAG_SPACING, wdgt)

    
    # flg_x
    tooltip = 'Execute the script (rather than edit it).\n\
{0}\n\
THIS FLAG IS NOT AVAILABLE FOR USER INPUT\n\
SINCE IT IS HANDLED BY THE TOOL INTERNALLY.'.format(TEXT_DIVIDER)
    wdgt.flg_x = renderthreads_command_line_flag_widget.CommandLineFlag(flag = '-x',
                                                                        tooltip = tooltip,
                                                                        checkable = False,
                                                                        parent = wdgt)
    lyt_frm_command_line_options.addWidget(wdgt.flg_x)
    # command_line_flag_list
    wdgt.command_line_flag_list.append(wdgt.flg_x)
    # spacer widget
    renderthreads_gui_helper.insert_spacer_widget(lyt_frm_command_line_options, 0, COMMAND_LINE_FLAG_SPACING, wdgt)


    # flg_X
    tooltip = 'Only execute these nodes (comma-separated list).\n\
{0}\n\
THIS FLAG IS NOT AVAILABLE FOR USER INPUT\n\
SINCE IT IS HANDLED BY THE TOOL INTERNALLY.'.format(TEXT_DIVIDER)
    wdgt_parameter = QtGui.QLineEdit(text = WRITE_NODE_REPLACEMENT_TEMPLATE, parent = wdgt)
    wdgt.flg_X = renderthreads_command_line_flag_widget.CommandLineFlag(flag = '-X',
                                                                        tooltip = tooltip,
                                                                        checkable = False,
                                                                        wdgt_parameter = wdgt_parameter,
                                                                        parent = wdgt)
    lyt_frm_command_line_options.addWidget(wdgt.flg_X)
    # force parameter enabled
    wdgt.flg_X.force_parameter_enabled(False)
    # command_line_flag_list
    wdgt.command_line_flag_list.append(wdgt.flg_X)
    # spacer widget
    renderthreads_gui_helper.insert_spacer_widget(lyt_frm_command_line_options, 0, COMMAND_LINE_FLAG_SPACING, wdgt)


    # flg_remap
    tooltip = 'For terminal mode, sets path remappings from a comma separated list.\n\
The remappings will be read as pairs, where the first path in each pair will\n\
map to the second path in each pair e.g. -remap "X:/path,B:/,Y:/,Z:/foo"\n\
The path X:/path/file.nk will be mapped to B:/file.nk\n\
The path Y:/bar/something.nk will be mapped to Z:/foo/bar/something.nk\n\
This option will cause an error if there are not an equal number of \'map froms\' and \'map to\' entries in the list.'
    wdgt_parameter = QtGui.QLineEdit(text = '', parent = wdgt)
    wdgt.flg_remap = renderthreads_command_line_flag_widget.CommandLineFlag(flag = '--remap',
                                                                            state = False,
                                                                            tooltip = tooltip,
                                                                            checkable = True,
                                                                            wdgt_parameter = wdgt_parameter,
                                                                            parent = wdgt)
    lyt_frm_command_line_options.addWidget(wdgt.flg_remap)
    # command_line_flag_list
    wdgt.command_line_flag_list.append(wdgt.flg_remap)
    # spacer widget
    renderthreads_gui_helper.insert_spacer_widget(lyt_frm_command_line_options, 0, COMMAND_LINE_FLAG_SPACING, wdgt)


    # flg_crashhandling
    tooltip = 'Specify 1 or 0 for whether the crash handler should be started or not.\n\
By default it only starts in GUI mode.\n\
This can also be controlled by using the environment variable NUKE_CRASH_HANDLING.'
    wdgt_parameter = QtGui.QSpinBox(parent = wdgt)
    wdgt_parameter.setMinimum(0)
    wdgt_parameter.setMaximum(1)
    wdgt_parameter.setValue(0)
    wdgt.flg_crashhandling = renderthreads_command_line_flag_widget.CommandLineFlag(flag = '--crashhandling',
                                                                                    state = False,
                                                                                    tooltip = tooltip,
                                                                                    checkable = True,
                                                                                    wdgt_parameter = wdgt_parameter,
                                                                                    parent = wdgt)
    lyt_frm_command_line_options.addWidget(wdgt.flg_crashhandling)
    # command_line_flag_list
    wdgt.command_line_flag_list.append(wdgt.flg_crashhandling)
    # spacer widget
    renderthreads_gui_helper.insert_spacer_widget(lyt_frm_command_line_options, 0, COMMAND_LINE_FLAG_SPACING, wdgt)


    # flg_nocrashprompt
    tooltip = 'Disable the crash prompt, so crashes are automatically submitted in GUI mode.\n\
This is the standard behavior in terminal mode. This can also be controlled\n\
by using the NUKE_NO_CRASH_PROMPT environment variable.'
    wdgt.flg_nocrashprompt = renderthreads_command_line_flag_widget.CommandLineFlag(flag = '--nocrashprompt',
                                                                                    state = False,
                                                                                    tooltip = tooltip,
                                                                                    checkable = True,
                                                                                    parent = wdgt)
    lyt_frm_command_line_options.addWidget(wdgt.flg_nocrashprompt)
    # command_line_flag_list
    wdgt.command_line_flag_list.append(wdgt.flg_nocrashprompt)


def create_constants_menu(wdgt):
    """
    Menu for constants.
    """

    #  lyt_frm_constants
    lyt_frm_constants = wdgt.frm_constants.layout()

    # nuke_script_path
    nuke_script_path = renderthreads_nuke.get_script_path()
    # nuke_path
    nuke_path = renderthreads_nuke.get_nuke_path()


    # lbl_script_path
    wdgt.lbl_script_path = QtGui.QLabel(text = 'Nuke Script', parent = wdgt)
    wdgt.lbl_script_path.setObjectName('lbl_script_path')
    lyt_frm_constants.addWidget(wdgt.lbl_script_path)
    
    # le_script_path
    wdgt.le_script_path = QtGui.QLineEdit(parent = wdgt)
    wdgt.le_script_path.setObjectName('le_script_path')
    wdgt.le_script_path.setText(nuke_script_path)
    wdgt.le_script_path.setReadOnly(True)
    lyt_frm_constants.addWidget(wdgt.le_script_path)


    # spacer widget
    renderthreads_gui_helper.insert_spacer_widget(lyt_frm_constants, 0, COMMAND_LINE_FLAG_SPACING, wdgt)

    
    # lbl_nuke_path
    wdgt.lbl_nuke_path = QtGui.QLabel(text = 'Nuke Executable', parent = wdgt)
    wdgt.lbl_nuke_path.setObjectName('lbl_nuke_path')
    lyt_frm_constants.addWidget(wdgt.lbl_nuke_path)

    # wdgt_nuke_path
    wdgt.wdgt_nuke_path = QtGui.QWidget(parent = wdgt)
    wdgt.wdgt_nuke_path.setObjectName('wdgt_nuke_path')
    wdgt.wdgt_nuke_path.setLayout(QtGui.QHBoxLayout())
    lyt_frm_constants.addWidget(wdgt.wdgt_nuke_path)

    # lyt_nuke_path
    lyt_nuke_path = wdgt.wdgt_nuke_path.layout()

    # le_nuke_path
    wdgt.le_nuke_path = QtGui.QLineEdit(parent = wdgt)
    wdgt.le_nuke_path.setObjectName('le_nuke_path')
    wdgt.le_nuke_path.setText(nuke_path)
    lyt_nuke_path.addWidget(wdgt.le_nuke_path)

    # btn_nuke_path
    wdgt.btn_nuke_path = QtGui.QPushButton(text = 'Pick', parent = wdgt)
    wdgt.btn_nuke_path.setObjectName('btn_nuke_path')
    lyt_nuke_path.addWidget(wdgt.btn_nuke_path)


def create_options_menu(wdgt):
    """
    Menu for options. This function
    creates not a QMenu but the entire options
    content for the stackwidget options page.
    """

    # create_general_options_menu
    create_general_options_menu(wdgt)
    
    # Add stretch for main layout at end
    lyt_sawdgt_options = wdgt.sawdgt_options.layout()
    lyt_sawdgt_options.addStretch()


def create_general_options_menu(wdgt):
    """
    Menu for general options like
    logging etc.
    """

    #  lyt_frm_general_options
    lyt_frm_general_options = wdgt.frm_general_options.layout()

    # sldr_logging_level
    wdgt.sldr_logging_level = renderthreads_slider_widget.Slider(header = 'Logging level',
                                                                    minimum = 1,
                                                                    maximum = 5,
                                                                    initial_value = INITIAL_LOGGING_LEVEL / 10)
    wdgt.sldr_logging_level.set_tick_position(QtGui.QSlider.TicksBelow)
    wdgt.sldr_logging_level.set_tick_interval(1)
    lyt_frm_general_options.addWidget(wdgt.sldr_logging_level)

    # sldr_display_shell
    wdgt.sldr_display_shell = renderthreads_slider_widget.Slider(header = 'Display render shell',
                                                                    minimum = 0,
                                                                    maximum = 1,
                                                                    initial_value = 1)
    wdgt.sldr_display_shell.set_tick_position(QtGui.QSlider.TicksBelow)
    wdgt.sldr_display_shell.set_tick_interval(1)
    lyt_frm_general_options.addWidget(wdgt.sldr_display_shell)


def create_pbar_render(wdgt):
    """
    Setup progressbar for rendering.
    """

    #  lyt_pbar_render
    lyt_pbar_render = wdgt.frm_pbar_render.layout()

    #  pbar_render
    wdgt.pbar_render = QtGui.QProgressBar()
    wdgt.pbar_render.setOrientation(QtCore.Qt.Horizontal)
    wdgt.pbar_render.setMinimum(0)
    wdgt.pbar_render.setMaximum(99)
    wdgt.pbar_render.setValue(50)
    #  add
    lyt_pbar_render.addWidget(wdgt.pbar_render)


def create_signal_remapper(wdgt):
    """
    Setup signal remapper instance.
    """

    # signal_remapper
    wdgt.signal_remapper = renderthreads_signal_remapper.SignalRemapper()


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

    #acn_print_all_converted_write_nodes
    wdgt.acn_print_all_converted_write_nodes = QtGui.QAction('Print all converted write nodes', wdgt)
    wdgt.acn_print_all_converted_write_nodes.setObjectName('acn_print_all_converted_write_nodes')
    wdgt.mnu_dev_nuke.addAction(wdgt.acn_print_all_converted_write_nodes)

    #acn_print_selected_converted_write_nodes
    wdgt.acn_print_selected_converted_write_nodes = QtGui.QAction('Print selected converted write nodes', wdgt)
    wdgt.acn_print_selected_converted_write_nodes.setObjectName('acn_print_selected_converted_write_nodes')
    wdgt.mnu_dev_nuke.addAction(wdgt.acn_print_selected_converted_write_nodes)

    
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

    #  connect_actions
    connect_actions(wdgt)

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

    # iterate flags
    # state and parameter
    for flag in wdgt.command_line_flag_list:

        # state_changed
        flag.state_changed.connect(functools.partial(update_command_line, wdgt))
        # parameter_changed
        flag.parameter_changed.connect(functools.partial(update_command_line, wdgt))

    # le_script_path
    wdgt.le_script_path.textChanged.connect(functools.partial(update_command_line, wdgt))

    # le_nuke_path
    wdgt.le_nuke_path.textChanged.connect(functools.partial(update_command_line, wdgt))


    # sgnl_set_logging
    wdgt.signal_remapper.sgnl_set_logging.connect(renderthreads_logging.set_logging_level)


def connect_actions(wdgt):
    """
    Connect actions.
    """

    # acn_render
    wdgt.acn_render.triggered.connect(functools.partial(wdgt.stkwdgt_content.setCurrentIndex, 0))
    # acn_threads
    wdgt.acn_threads.triggered.connect(functools.partial(wdgt.stkwdgt_content.setCurrentIndex, 1))
    # acn_command_line
    wdgt.acn_command_line.triggered.connect(functools.partial(wdgt.stkwdgt_content.setCurrentIndex, 2))
    # acn_options
    wdgt.acn_options.triggered.connect(functools.partial(wdgt.stkwdgt_content.setCurrentIndex, 3))


def connect_widgets(wdgt):
    """
    Connect widgets.
    """

    # sldr_threadcount
    wdgt.sldr_threadcount.value_changed.connect(wdgt.thread_manager.set_thread_count)
    # sldr_thread_interval
    wdgt.sldr_thread_interval.value_changed.connect(wdgt.thread_manager.set_interval)


    # btn_start_threads
    wdgt.btn_start_threads.clicked.connect(wdgt.thread_manager.start_threads)
    # btn_stop_threads
    wdgt.btn_stop_threads.clicked.connect(wdgt.thread_manager.stop_threads)

    
    # btn_print_queue_size
    wdgt.btn_print_queue_size.clicked.connect(wdgt.thread_manager.print_queue_size)
    # btn_reset_queue
    wdgt.btn_reset_queue.clicked.connect(wdgt.thread_manager.reset_queue)

    
    # btn_nuke_path
    wdgt.btn_nuke_path.clicked.connect(functools.partial(renderthreads_gui_helper.pick_file,
                                                            wdgt.le_nuke_path,
                                                            'Executables (*.exe)'))

    # sldr_logging_level
    wdgt.sldr_logging_level.value_changed.connect(wdgt.signal_remapper.remap_logging)


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
    wdgt.acn_print_all_write_nodes.triggered.connect(functools.partial(renderthreads_nuke.print_nodes, 'Write'))
    # acn_print_selected_write_nodes
    wdgt.acn_print_selected_write_nodes.triggered.connect(functools.partial(renderthreads_nuke.print_nodes, 'Write', True))

    # acn_print_all_converted_write_nodes
    wdgt.acn_print_all_converted_write_nodes.triggered.connect(functools.partial(renderthreads_nuke.print_nodes,
                                                                                    'Write',
                                                                                    False,
                                                                                    True))
    # acn_print_selected_converted_write_nodes
    wdgt.acn_print_selected_converted_write_nodes.triggered.connect(functools.partial(renderthreads_nuke.print_nodes,
                                                                                        'Write',
                                                                                        True,
                                                                                        True))
    
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


#  Slots
#  ------------------------------------------------------------------

def update_script_path(wdgt):
    """
    Update wdgt.le_script_path with current
    nuke script path. This function is triggered
    by script_check service.
    """

    # nuke_script_path
    nuke_script_path = renderthreads_nuke.get_script_path()

    # set
    wdgt.le_script_path.setText(nuke_script_path)


def update_command_line(wdgt, *args):
    """
    Update lbl_command_line when state or
    parameter of flag are changed.
    """

    # nuke_script_path
    nuke_script_path = wdgt.le_script_path.text()
    
    # nuke_script_path_word_wrap
    nuke_script_path_word_wrap = renderthreads_gui_helper.prepare_string_for_word_wrap(nuke_script_path)

    # nuke_path
    nuke_path = wdgt.le_nuke_path.text()

    # flag_list
    flag_list = wdgt.command_line_flag_list

    # command_line_string
    command_line_string = renderthreads_command_line_engine.get_command_line_string(flag_list,
                                                                                    nuke_path,
                                                                                    nuke_script_path)

    # command_line_string_word_wrap
    command_line_string_word_wrap = renderthreads_command_line_engine.get_command_line_string(flag_list,
                                                                                                nuke_path,
                                                                                                nuke_script_path_word_wrap)

    # set lbl_command_line
    wdgt.lbl_command_line.setText(command_line_string_word_wrap)

    # log
    logger.debug('{0}'.format(command_line_string))

    # return
    return command_line_string
