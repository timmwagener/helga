

"""
asset_manager_menu
==========================================

This module encapsulates the creation of the menu. The creation of the menu has gotten so big
codewise that it made sense to move it out of the main asset_manager module.
This module has two main functions:

1. setup_menu
2. connect_menu 
"""




#Import
#------------------------------------------------------------------
#python
import subprocess
import logging
import functools
#PySide
from PySide import QtGui
from PySide import QtCore





#Import variable
do_reload = True

#helga

#global_variables
from helga.general.setup.global_variables import global_variables
if(do_reload):reload(global_variables)

#global_functions
from helga.general.setup.global_functions import global_functions
if(do_reload):reload(global_functions)


#asset_manager

#lib.gui

#asset_manager_slider_action
from lib.gui import asset_manager_slider_action
if(do_reload):reload(asset_manager_slider_action)

#asset_manager_doublespinbox_action
from lib.gui import asset_manager_doublespinbox_action
if(do_reload):reload(asset_manager_doublespinbox_action)

#asset_manager_doublespinbox_checkable_action
from lib.gui import asset_manager_doublespinbox_checkable_action
if(do_reload):reload(asset_manager_doublespinbox_checkable_action)

#asset_manager_line_edit_checkable_action
from lib.gui import asset_manager_line_edit_checkable_action
if(do_reload):reload(asset_manager_line_edit_checkable_action)

#asset_manager_pre_export_dialog
from lib.gui import asset_manager_pre_export_dialog
if(do_reload):reload(asset_manager_pre_export_dialog)






#Globals
#------------------------------------------------------------------







#Functions
#------------------------------------------------------------------

def setup_menu(wdgt, parent = None):
    """
    Create the main menu for the asset manager.
    The wdgt arg. expects the asset manager instance to operate on.
    """

    #mnubar_menu
    wdgt.mnubar_menu = QtGui.QMenuBar(parent = wdgt)
    wdgt.mnubar_menu.setObjectName('mnubar_menu')
    parent.layout().addWidget(wdgt.mnubar_menu)

    
    #setup_menu_threads
    setup_menu_threads(wdgt, wdgt.mnubar_menu)

    #setup_menu_gui
    setup_menu_gui(wdgt, wdgt.mnubar_menu)

    #setup_menu_alembic
    setup_menu_alembic(wdgt, wdgt.mnubar_menu)

    #setup_menu_assets
    setup_menu_assets(wdgt, wdgt.mnubar_menu)
    


def setup_menu_threads(wdgt, menubar):
    """
    Setup menu threads.
    """

    #Threads
    #------------------------------------------------------------------

    #mnu_threads
    wdgt.mnu_threads = QtGui.QMenu('Threads', parent = wdgt)
    wdgt.mnu_threads.setObjectName('mnu_threads')
    menubar.addMenu(wdgt.mnu_threads)


    #Threads logging
    #------------------------------------------------------------------

    #mnu_threads_logging
    wdgt.mnu_threads_logging = QtGui.QMenu('Threads Logging', parent = wdgt)
    wdgt.mnu_threads_logging.setObjectName('mnu_threads_logging')
    wdgt.mnu_threads.addMenu(wdgt.mnu_threads_logging)

    #acn_grp_threads_logging
    wdgt.acn_grp_threads_logging = QtGui.QActionGroup(wdgt)


    #acn_set_threads_logging_level_debug
    wdgt.acn_set_threads_logging_level_debug = QtGui.QAction('Debug', wdgt)
    wdgt.acn_set_threads_logging_level_debug.setObjectName('acn_set_threads_logging_level_debug')
    wdgt.acn_set_threads_logging_level_debug.setCheckable(True)
    #eventually set checked
    if (wdgt.threads_initial_logging_level == logging.DEBUG):
        wdgt.acn_set_threads_logging_level_debug.setChecked(True)
    #add to menu and actiongroup
    wdgt.mnu_threads_logging.addAction(wdgt.acn_set_threads_logging_level_debug)
    wdgt.acn_grp_threads_logging.addAction(wdgt.acn_set_threads_logging_level_debug)

    #acn_set_threads_logging_level_info
    wdgt.acn_set_threads_logging_level_info = QtGui.QAction('Info', wdgt)
    wdgt.acn_set_threads_logging_level_info.setObjectName('acn_set_threads_logging_level_info')
    wdgt.acn_set_threads_logging_level_info.setCheckable(True)
    #eventually set checked
    if (wdgt.threads_initial_logging_level == logging.INFO):
        wdgt.acn_set_threads_logging_level_info.setChecked(True)
    #add to menu and actiongroup
    wdgt.mnu_threads_logging.addAction(wdgt.acn_set_threads_logging_level_info)
    wdgt.acn_grp_threads_logging.addAction(wdgt.acn_set_threads_logging_level_info)

    #acn_set_threads_logging_level_warning
    wdgt.acn_set_threads_logging_level_warning = QtGui.QAction('Warning', wdgt)
    wdgt.acn_set_threads_logging_level_warning.setObjectName('acn_set_threads_logging_level_warning')
    wdgt.acn_set_threads_logging_level_warning.setCheckable(True)
    #eventually set checked
    if (wdgt.threads_initial_logging_level == logging.WARNING):
        wdgt.acn_set_threads_logging_level_warning.setChecked(True)
    #add to menu and actiongroup
    wdgt.mnu_threads_logging.addAction(wdgt.acn_set_threads_logging_level_warning)
    wdgt.acn_grp_threads_logging.addAction(wdgt.acn_set_threads_logging_level_warning)

    #acn_set_threads_logging_level_error
    wdgt.acn_set_threads_logging_level_error = QtGui.QAction('Error', wdgt)
    wdgt.acn_set_threads_logging_level_error.setObjectName('acn_set_threads_logging_level_error')
    wdgt.acn_set_threads_logging_level_error.setCheckable(True)
    #eventually set checked
    if (wdgt.threads_initial_logging_level == logging.ERROR):
        wdgt.acn_set_threads_logging_level_error.setChecked(True)
    #add to menu and actiongroup
    wdgt.mnu_threads_logging.addAction(wdgt.acn_set_threads_logging_level_error)
    wdgt.acn_grp_threads_logging.addAction(wdgt.acn_set_threads_logging_level_error)

    #acn_set_threads_logging_level_critical
    wdgt.acn_set_threads_logging_level_critical = QtGui.QAction('Critical', wdgt)
    wdgt.acn_set_threads_logging_level_critical.setObjectName('acn_set_threads_logging_level_critical')
    wdgt.acn_set_threads_logging_level_critical.setCheckable(True)
    #eventually set checked
    if (wdgt.threads_initial_logging_level == logging.CRITICAL):
        wdgt.acn_set_threads_logging_level_critical.setChecked(True)
    #add to menu and actiongroup
    wdgt.mnu_threads_logging.addAction(wdgt.acn_set_threads_logging_level_critical)
    wdgt.acn_grp_threads_logging.addAction(wdgt.acn_set_threads_logging_level_critical)




    

    #acn_start_threads
    wdgt.acn_start_threads = QtGui.QAction('Re/Start threads', wdgt)
    wdgt.acn_start_threads.setObjectName('acn_start_threads')
    wdgt.mnu_threads.addAction(wdgt.acn_start_threads)

    #acn_stop_threads
    wdgt.acn_stop_threads = QtGui.QAction('Stop threads', wdgt)
    wdgt.acn_stop_threads.setObjectName('acn_stop_threads')
    wdgt.mnu_threads.addAction(wdgt.acn_stop_threads)


    #separator
    wdgt.mnu_threads.addSeparator()


    #acn_print_queue_size
    wdgt.acn_print_queue_size = QtGui.QAction('Queue size', wdgt)
    wdgt.acn_print_queue_size.setObjectName('acn_print_queue_size')
    wdgt.mnu_threads.addAction(wdgt.acn_print_queue_size)

    #acn_reset_queue
    wdgt.acn_reset_queue = QtGui.QAction('Queue reset', wdgt)
    wdgt.acn_reset_queue.setObjectName('acn_reset_queue')
    wdgt.mnu_threads.addAction(wdgt.acn_reset_queue)

    #acn_add_tasks_to_queue
    wdgt.acn_add_tasks_to_queue = QtGui.QAction('Add tasks to queue', wdgt)
    wdgt.acn_add_tasks_to_queue.setObjectName('acn_add_tasks_to_queue')
    wdgt.mnu_threads.addAction(wdgt.acn_add_tasks_to_queue)

    
    #separator
    wdgt.mnu_threads.addSeparator()
    
    
    #acn_set_thread_timer_interval
    wdgt.acn_set_thread_timer_interval = asset_manager_slider_action.AssetManagerSliderAction(minimum = 1, 
                                                                                                maximum = wdgt.get_thread_interval() * 4,
                                                                                                initial_value = wdgt.get_thread_interval(),
                                                                                                text = 'Set thread interval:',
                                                                                                parent = wdgt)
    wdgt.acn_set_thread_timer_interval.setObjectName('acn_set_thread_timer_interval')
    wdgt.mnu_threads.addAction(wdgt.acn_set_thread_timer_interval)


    #separator
    wdgt.mnu_threads.addSeparator()
    
    
    #acn_set_export_thread_timeout
    wdgt.acn_set_export_thread_timeout = asset_manager_slider_action.AssetManagerSliderAction(minimum = 1, 
                                                                                                maximum = wdgt.get_export_thread_timeout() * 4,
                                                                                                initial_value = wdgt.get_export_thread_timeout(),
                                                                                                text = 'Set export thread timeout:',
                                                                                                parent = wdgt)
    wdgt.acn_set_export_thread_timeout.setObjectName('acn_set_export_thread_timeout')
    wdgt.mnu_threads.addAction(wdgt.acn_set_export_thread_timeout)


    #separator
    wdgt.mnu_threads.addSeparator()


    #acn_set_thread_count
    max_threads = wdgt.threads_functionality.get_max_threads()
    thread_count = wdgt.threads_functionality.get_thread_count()
    wdgt.acn_set_thread_count = asset_manager_slider_action.AssetManagerSliderAction(maximum = max_threads,
                                                                                        initial_value = thread_count,
                                                                                        text = 'Set active thread count:',
                                                                                        parent = wdgt)
    wdgt.acn_set_thread_count.setObjectName('acn_set_thread_count')
    wdgt.mnu_threads.addAction(wdgt.acn_set_thread_count)


def setup_menu_gui(wdgt, menubar):
    """
    Setup menu gui.
    """

    #GUI
    #------------------------------------------------------------------

    #mnu_gui
    wdgt.mnu_gui = QtGui.QMenu('GUI', parent = wdgt)
    wdgt.mnu_gui.setObjectName('mnu_gui')
    menubar.addMenu(wdgt.mnu_gui)


    #shot_metatada_view
    #------------------------------------------------------------------
    
    #mnu_shot_metatada_view
    wdgt.mnu_shot_metatada_view = QtGui.QMenu('Shot metadata view', parent = wdgt)
    wdgt.mnu_shot_metatada_view.setObjectName('mnu_shot_metatada_view')
    wdgt.mnu_gui.addMenu(wdgt.mnu_shot_metatada_view)

    #acn_toggle_column_alembic_path
    wdgt.acn_toggle_column_alembic_path = QtGui.QAction('Toggle column Alembic Path', wdgt)
    wdgt.acn_toggle_column_alembic_path.setObjectName('acn_toggle_column_alembic_path')
    wdgt.mnu_shot_metatada_view.addAction(wdgt.acn_toggle_column_alembic_path)


    #prop_metatada_view
    #------------------------------------------------------------------
    
    #mnu_prop_metatada_view
    wdgt.mnu_prop_metatada_view = QtGui.QMenu('Prop metadata view', parent = wdgt)
    wdgt.mnu_prop_metatada_view.setObjectName('mnu_prop_metatada_view')
    wdgt.mnu_gui.addMenu(wdgt.mnu_prop_metatada_view)

    #acn_toggle_column_export_proxy_for_prop_view
    wdgt.acn_toggle_column_export_proxy_for_prop_view = QtGui.QAction('Toggle column export proxy', wdgt)
    wdgt.acn_toggle_column_export_proxy_for_prop_view.setObjectName('acn_toggle_column_export_proxy_for_prop_view')
    wdgt.mnu_prop_metatada_view.addAction(wdgt.acn_toggle_column_export_proxy_for_prop_view)

    #acn_toggle_column_export_locator_for_prop_view
    wdgt.acn_toggle_column_export_locator_for_prop_view = QtGui.QAction('Toggle column export locator', wdgt)
    wdgt.acn_toggle_column_export_locator_for_prop_view.setObjectName('acn_toggle_column_export_locator_for_prop_view')
    wdgt.mnu_prop_metatada_view.addAction(wdgt.acn_toggle_column_export_locator_for_prop_view)


    #char_metatada_view
    #------------------------------------------------------------------
    
    #mnu_char_metatada_view
    wdgt.mnu_char_metatada_view = QtGui.QMenu('Char metadata view', parent = wdgt)
    wdgt.mnu_char_metatada_view.setObjectName('mnu_char_metatada_view')
    wdgt.mnu_gui.addMenu(wdgt.mnu_char_metatada_view)

    #acn_toggle_column_export_proxy_for_char_view
    wdgt.acn_toggle_column_export_proxy_for_char_view = QtGui.QAction('Toggle column export proxy', wdgt)
    wdgt.acn_toggle_column_export_proxy_for_char_view.setObjectName('acn_toggle_column_export_proxy_for_char_view')
    wdgt.mnu_char_metatada_view.addAction(wdgt.acn_toggle_column_export_proxy_for_char_view)

    #acn_toggle_column_export_locator_for_char_view
    wdgt.acn_toggle_column_export_locator_for_char_view = QtGui.QAction('Toggle column export locator', wdgt)
    wdgt.acn_toggle_column_export_locator_for_char_view.setObjectName('acn_toggle_column_export_locator_for_char_view')
    wdgt.mnu_char_metatada_view.addAction(wdgt.acn_toggle_column_export_locator_for_char_view)


    #separator
    wdgt.mnu_gui.addSeparator()


    #acn_progressbar_test_run
    wdgt.acn_progressbar_test_run = QtGui.QAction('Progressbar test run', wdgt)
    wdgt.acn_progressbar_test_run.setObjectName('acn_progressbar_test_run')
    wdgt.mnu_gui.addAction(wdgt.acn_progressbar_test_run)

    #acn_hide_export_shell
    wdgt.acn_hide_export_shell = QtGui.QAction('Hide export shell', wdgt)
    wdgt.acn_hide_export_shell.setObjectName('acn_hide_export_shell')
    wdgt.acn_hide_export_shell.setCheckable(True)
    wdgt.acn_hide_export_shell.setChecked(wdgt.hide_export_shell)
    wdgt.mnu_gui.addAction(wdgt.acn_hide_export_shell)



def setup_menu_alembic(wdgt, menubar):
    """
    Setup menu alembic.
    """

    #Alembic
    #------------------------------------------------------------------

    #mnu_alembic
    wdgt.mnu_alembic = QtGui.QMenu('Alembic', parent = wdgt)
    wdgt.mnu_alembic.setObjectName('mnu_alembic')
    menubar.addMenu(wdgt.mnu_alembic)

    
    #acn_set_help_enabled
    wdgt.acn_set_help_enabled = QtGui.QAction('help', wdgt)
    wdgt.acn_set_help_enabled.setObjectName('acn_set_help_enabled')
    wdgt.acn_set_help_enabled.setCheckable(True)
    wdgt.acn_set_help_enabled.setChecked(wdgt.alembic_functionality.get_help_enabled())
    wdgt.mnu_alembic.addAction(wdgt.acn_set_help_enabled)

    
    #acn_set_dontSkipUnwrittenFrames_enabled
    wdgt.acn_set_dontSkipUnwrittenFrames_enabled = QtGui.QAction('dontSkipUnwrittenFrames', wdgt)
    wdgt.acn_set_dontSkipUnwrittenFrames_enabled.setObjectName('acn_set_dontSkipUnwrittenFrames_enabled')
    wdgt.acn_set_dontSkipUnwrittenFrames_enabled.setCheckable(True)
    wdgt.acn_set_dontSkipUnwrittenFrames_enabled.setChecked(wdgt.alembic_functionality.get_dontSkipUnwrittenFrames_enabled())
    wdgt.mnu_alembic.addAction(wdgt.acn_set_dontSkipUnwrittenFrames_enabled)

    
    #acn_set_verbose_enabled
    wdgt.acn_set_verbose_enabled = QtGui.QAction('verbose', wdgt)
    wdgt.acn_set_verbose_enabled.setObjectName('acn_set_verbose_enabled')
    wdgt.acn_set_verbose_enabled.setCheckable(True)
    wdgt.acn_set_verbose_enabled.setChecked(wdgt.alembic_functionality.get_verbose_enabled())
    wdgt.mnu_alembic.addAction(wdgt.acn_set_verbose_enabled)


    #acn_set_eulerFilter_enabled
    wdgt.acn_set_eulerFilter_enabled = QtGui.QAction('eulerFilter', wdgt)
    wdgt.acn_set_eulerFilter_enabled.setObjectName('acn_set_eulerFilter_enabled')
    wdgt.acn_set_eulerFilter_enabled.setCheckable(True)
    wdgt.acn_set_eulerFilter_enabled.setChecked(wdgt.alembic_functionality.get_eulerFilter_enabled())
    wdgt.mnu_alembic.addAction(wdgt.acn_set_eulerFilter_enabled)


    #acn_set_noNormals_enabled
    wdgt.acn_set_noNormals_enabled = QtGui.QAction('noNormals', wdgt)
    wdgt.acn_set_noNormals_enabled.setObjectName('acn_set_noNormals_enabled')
    wdgt.acn_set_noNormals_enabled.setCheckable(True)
    wdgt.acn_set_noNormals_enabled.setChecked(wdgt.alembic_functionality.get_noNormals_enabled())
    wdgt.mnu_alembic.addAction(wdgt.acn_set_noNormals_enabled)


    #acn_set_renderableOnly_enabled
    wdgt.acn_set_renderableOnly_enabled = QtGui.QAction('renderableOnly', wdgt)
    wdgt.acn_set_renderableOnly_enabled.setObjectName('acn_set_renderableOnly_enabled')
    wdgt.acn_set_renderableOnly_enabled.setCheckable(True)
    wdgt.acn_set_renderableOnly_enabled.setChecked(wdgt.alembic_functionality.get_renderableOnly_enabled())
    wdgt.mnu_alembic.addAction(wdgt.acn_set_renderableOnly_enabled)


    #acn_set_selection_enabled
    wdgt.acn_set_selection_enabled = QtGui.QAction('selection', wdgt)
    wdgt.acn_set_selection_enabled.setObjectName('acn_set_selection_enabled')
    wdgt.acn_set_selection_enabled.setCheckable(True)
    wdgt.acn_set_selection_enabled.setChecked(wdgt.alembic_functionality.get_selection_enabled())
    wdgt.mnu_alembic.addAction(wdgt.acn_set_selection_enabled)


    #acn_set_stripNamespaces_enabled
    wdgt.acn_set_stripNamespaces_enabled = QtGui.QAction('stripNamespaces', wdgt)
    wdgt.acn_set_stripNamespaces_enabled.setObjectName('acn_set_stripNamespaces_enabled')
    wdgt.acn_set_stripNamespaces_enabled.setCheckable(True)
    wdgt.acn_set_stripNamespaces_enabled.setChecked(wdgt.alembic_functionality.get_stripNamespaces_enabled())
    wdgt.mnu_alembic.addAction(wdgt.acn_set_stripNamespaces_enabled)


    #acn_set_uvWrite_enabled
    wdgt.acn_set_uvWrite_enabled = QtGui.QAction('uvWrite', wdgt)
    wdgt.acn_set_uvWrite_enabled.setObjectName('acn_set_uvWrite_enabled')
    wdgt.acn_set_uvWrite_enabled.setCheckable(True)
    wdgt.acn_set_uvWrite_enabled.setChecked(wdgt.alembic_functionality.get_uvWrite_enabled())
    wdgt.mnu_alembic.addAction(wdgt.acn_set_uvWrite_enabled)


    #acn_set_writeColorSets_enabled
    wdgt.acn_set_writeColorSets_enabled = QtGui.QAction('writeColorSets', wdgt)
    wdgt.acn_set_writeColorSets_enabled.setObjectName('acn_set_writeColorSets_enabled')
    wdgt.acn_set_writeColorSets_enabled.setCheckable(True)
    wdgt.acn_set_writeColorSets_enabled.setChecked(wdgt.alembic_functionality.get_writeColorSets_enabled())
    wdgt.mnu_alembic.addAction(wdgt.acn_set_writeColorSets_enabled)


    #acn_set_writeFaceSets_enabled
    wdgt.acn_set_writeFaceSets_enabled = QtGui.QAction('writeFaceSets', wdgt)
    wdgt.acn_set_writeFaceSets_enabled.setObjectName('acn_set_writeFaceSets_enabled')
    wdgt.acn_set_writeFaceSets_enabled.setCheckable(True)
    wdgt.acn_set_writeFaceSets_enabled.setChecked(wdgt.alembic_functionality.get_writeFaceSets_enabled())
    wdgt.mnu_alembic.addAction(wdgt.acn_set_writeFaceSets_enabled)


    #acn_set_wholeFrameGeo_enabled
    wdgt.acn_set_wholeFrameGeo_enabled = QtGui.QAction('wholeFrameGeo', wdgt)
    wdgt.acn_set_wholeFrameGeo_enabled.setObjectName('acn_set_wholeFrameGeo_enabled')
    wdgt.acn_set_wholeFrameGeo_enabled.setCheckable(True)
    wdgt.acn_set_wholeFrameGeo_enabled.setChecked(wdgt.alembic_functionality.get_wholeFrameGeo_enabled())
    wdgt.mnu_alembic.addAction(wdgt.acn_set_wholeFrameGeo_enabled)


    #acn_set_worldSpace_enabled
    wdgt.acn_set_worldSpace_enabled = QtGui.QAction('worldSpace', wdgt)
    wdgt.acn_set_worldSpace_enabled.setObjectName('acn_set_worldSpace_enabled')
    wdgt.acn_set_worldSpace_enabled.setCheckable(True)
    wdgt.acn_set_worldSpace_enabled.setChecked(wdgt.alembic_functionality.get_worldSpace_enabled())
    wdgt.mnu_alembic.addAction(wdgt.acn_set_worldSpace_enabled)


    #acn_set_writeVisibility_enabled
    wdgt.acn_set_writeVisibility_enabled = QtGui.QAction('writeVisibility', wdgt)
    wdgt.acn_set_writeVisibility_enabled.setObjectName('acn_set_writeVisibility_enabled')
    wdgt.acn_set_writeVisibility_enabled.setCheckable(True)
    wdgt.acn_set_writeVisibility_enabled.setChecked(wdgt.alembic_functionality.get_writeVisibility_enabled())
    wdgt.mnu_alembic.addAction(wdgt.acn_set_writeVisibility_enabled)


    #separator
    wdgt.mnu_alembic.addSeparator()


    #acn_set_step
    wdgt.acn_set_step = asset_manager_doublespinbox_checkable_action.AssetManagerDoubleSpinBoxCheckableAction(text = 'step',
                                                                                                                initial_state = wdgt.alembic_functionality.get_step_enabled(),
                                                                                                                initial_value = wdgt.alembic_functionality.get_step(),
                                                                                                                parent = wdgt)
    wdgt.acn_set_step.setObjectName('acn_set_step')
    wdgt.mnu_alembic.addAction(wdgt.acn_set_step)


    #acn_set_frameRelativeSample
    wdgt.acn_set_frameRelativeSample = asset_manager_doublespinbox_checkable_action.AssetManagerDoubleSpinBoxCheckableAction(text = 'frameRelativeSample',
                                                                                                                            initial_state = wdgt.alembic_functionality.get_frameRelativeSample_enabled(),
                                                                                                                            initial_value = wdgt.alembic_functionality.get_frameRelativeSample(),
                                                                                                                            parent = wdgt)
    wdgt.acn_set_frameRelativeSample.setObjectName('acn_set_frameRelativeSample')
    wdgt.mnu_alembic.addAction(wdgt.acn_set_frameRelativeSample)


    #acn_set_preRollStartFrame
    wdgt.acn_set_preRollStartFrame = asset_manager_doublespinbox_checkable_action.AssetManagerDoubleSpinBoxCheckableAction(text = 'preRollStartFrame',
                                                                                                                            initial_state = wdgt.alembic_functionality.get_preRollStartFrame_enabled(),
                                                                                                                            initial_value = wdgt.alembic_functionality.get_preRollStartFrame(),
                                                                                                                            parent = wdgt)
    wdgt.acn_set_preRollStartFrame.setObjectName('acn_set_preRollStartFrame')
    wdgt.mnu_alembic.addAction(wdgt.acn_set_preRollStartFrame)


    #separator
    wdgt.mnu_alembic.addSeparator()


    #acn_set_attr
    wdgt.acn_set_attr = asset_manager_line_edit_checkable_action.AssetManagerLineEditCheckableAction(placeholder_text = 'attr',
                                                                                                        initial_state = wdgt.alembic_functionality.get_attr_enabled(),
                                                                                                        text = wdgt.alembic_functionality.get_attr(),
                                                                                                        parent = wdgt)
    wdgt.acn_set_attr.setObjectName('acn_set_attr')
    wdgt.mnu_alembic.addAction(wdgt.acn_set_attr)


    #acn_set_attrPrefix
    wdgt.acn_set_attrPrefix = asset_manager_line_edit_checkable_action.AssetManagerLineEditCheckableAction(placeholder_text = 'attrPrefix',
                                                                                                            initial_state = wdgt.alembic_functionality.get_attrPrefix_enabled(),
                                                                                                            text = wdgt.alembic_functionality.get_attrPrefix(),
                                                                                                            parent = wdgt)
    wdgt.acn_set_attrPrefix.setObjectName('acn_set_attrPrefix')
    wdgt.mnu_alembic.addAction(wdgt.acn_set_attrPrefix)


    #acn_set_userAttr
    wdgt.acn_set_userAttr = asset_manager_line_edit_checkable_action.AssetManagerLineEditCheckableAction(placeholder_text = 'userAttr',
                                                                                                            initial_state = wdgt.alembic_functionality.get_userAttr_enabled(),
                                                                                                            text = wdgt.alembic_functionality.get_userAttr(),
                                                                                                            parent = wdgt)
    wdgt.acn_set_userAttr.setObjectName('acn_set_userAttr')
    wdgt.mnu_alembic.addAction(wdgt.acn_set_userAttr)


    #acn_set_userAttrPrefix
    wdgt.acn_set_userAttrPrefix = asset_manager_line_edit_checkable_action.AssetManagerLineEditCheckableAction(placeholder_text = 'userAttrPrefix',
                                                                                                                initial_state = wdgt.alembic_functionality.get_userAttrPrefix_enabled(),
                                                                                                                text = wdgt.alembic_functionality.get_userAttrPrefix(),
                                                                                                                parent = wdgt)
    wdgt.acn_set_userAttrPrefix.setObjectName('acn_set_userAttrPrefix')
    wdgt.mnu_alembic.addAction(wdgt.acn_set_userAttrPrefix)


    #separator
    wdgt.mnu_alembic.addSeparator()


    #acn_print_export_command
    wdgt.acn_print_export_command = QtGui.QAction('Print .abc export command', wdgt)
    wdgt.acn_print_export_command.setObjectName('acn_print_export_command')
    wdgt.mnu_alembic.addAction(wdgt.acn_print_export_command)


def setup_menu_assets(wdgt, menubar):
    """
    Setup menu assets.
    """

    #Assets
    #------------------------------------------------------------------

    #mnu_assets
    wdgt.mnu_assets = QtGui.QMenu('Assets', parent = wdgt)
    wdgt.mnu_assets.setObjectName('mnu_assets')
    menubar.addMenu(wdgt.mnu_assets)


    #Attributes
    #------------------------------------------------------------------

    #mnu_attributes
    wdgt.mnu_attributes = QtGui.QMenu('Attributes', parent = wdgt)
    wdgt.mnu_attributes.setObjectName('mnu_attributes')
    wdgt.mnu_assets.addMenu(wdgt.mnu_attributes)


    #acn_add_proxy_attributes
    wdgt.acn_add_proxy_attributes = QtGui.QAction('Add proxy attributes to selected geo', wdgt)
    wdgt.acn_add_proxy_attributes.setObjectName('acn_add_proxy_attributes')
    wdgt.mnu_attributes.addAction(wdgt.acn_add_proxy_attributes)

    #acn_add_rendergeo_attributes
    wdgt.acn_add_rendergeo_attributes = QtGui.QAction('Add rendergeo attributes to selected geo', wdgt)
    wdgt.acn_add_rendergeo_attributes.setObjectName('acn_add_rendergeo_attributes')
    wdgt.mnu_attributes.addAction(wdgt.acn_add_rendergeo_attributes)

    #acn_add_locator_attributes
    wdgt.acn_add_locator_attributes = QtGui.QAction('Add locator attributes to selected locator', wdgt)
    wdgt.acn_add_locator_attributes.setObjectName('acn_add_locator_attributes')
    wdgt.mnu_attributes.addAction(wdgt.acn_add_locator_attributes)


    #separator
    wdgt.mnu_attributes.addSeparator()


    #acn_remove_proxy_attributes
    wdgt.acn_remove_proxy_attributes = QtGui.QAction('Remove proxy attributes from selected geo', wdgt)
    wdgt.acn_remove_proxy_attributes.setObjectName('acn_remove_proxy_attributes')
    wdgt.mnu_attributes.addAction(wdgt.acn_remove_proxy_attributes)

    #acn_remove_rendergeo_attributes
    wdgt.acn_remove_rendergeo_attributes = QtGui.QAction('Remove rendergeo attributes from selected geo', wdgt)
    wdgt.acn_remove_rendergeo_attributes.setObjectName('acn_remove_rendergeo_attributes')
    wdgt.mnu_attributes.addAction(wdgt.acn_remove_rendergeo_attributes)

    #acn_remove_locator_attributes
    wdgt.acn_remove_locator_attributes = QtGui.QAction('Remove locator attributes from selected locator', wdgt)
    wdgt.acn_remove_locator_attributes.setObjectName('acn_remove_locator_attributes')
    wdgt.mnu_attributes.addAction(wdgt.acn_remove_locator_attributes)


def connect_menu(wdgt):
    """
    Connect this menu.
    """

    #connect_menu_threads
    connect_menu_threads(wdgt)

    #connect_menu_gui
    connect_menu_gui(wdgt)

    #connect_menu_alembic
    connect_menu_alembic(wdgt)

    #connect_menu_assets
    connect_menu_assets(wdgt)

    
    

def connect_menu_threads(wdgt):
    """
    Connect menu threads actions with wdgt.
    """

    #acn_set_threads_logging_level_debug
    wdgt.acn_set_threads_logging_level_debug.triggered.connect(functools.partial(wdgt.threads_functionality.set_logging_level_for_threads, 
                                                                                    logging.DEBUG))
    #acn_set_threads_logging_level_info
    wdgt.acn_set_threads_logging_level_info.triggered.connect(functools.partial(wdgt.threads_functionality.set_logging_level_for_threads, 
                                                                                logging.INFO))
    #acn_set_threads_logging_level_warning
    wdgt.acn_set_threads_logging_level_warning.triggered.connect(functools.partial(wdgt.threads_functionality.set_logging_level_for_threads, 
                                                                                    logging.WARNING))
    #acn_set_threads_logging_level_error
    wdgt.acn_set_threads_logging_level_error.triggered.connect(functools.partial(wdgt.threads_functionality.set_logging_level_for_threads, 
                                                                                    logging.ERROR))
    #acn_set_threads_logging_level_critical
    wdgt.acn_set_threads_logging_level_critical.triggered.connect(functools.partial(wdgt.threads_functionality.set_logging_level_for_threads, 
                                                                                    logging.CRITICAL))


    #acn_start_threads
    wdgt.acn_start_threads.triggered.connect(wdgt.threads_functionality.start_threads)
    #acn_stop_threads
    wdgt.acn_stop_threads.triggered.connect(wdgt.threads_functionality.stop_threads)
    #acn_print_queue_size
    wdgt.acn_print_queue_size.triggered.connect(wdgt.threads_functionality.print_queue_size)
    #acn_reset_queue
    wdgt.acn_reset_queue.triggered.connect(wdgt.threads_functionality.reset_queue)
    #acn_add_tasks_to_queue
    wdgt.acn_add_tasks_to_queue.triggered.connect(wdgt.threads_functionality.test_setup)

    #acn_set_thread_timer_interval
    wdgt.acn_set_thread_timer_interval.value_changed.connect(wdgt.threads_functionality.set_interval)
    #acn_set_export_thread_timeout
    wdgt.acn_set_export_thread_timeout.value_changed.connect(wdgt.set_export_thread_timeout)
    #acn_set_thread_count
    wdgt.acn_set_thread_count.value_changed.connect(wdgt.threads_functionality.set_thread_count)


def connect_menu_gui(wdgt):
    """
    Connect menu gui actions with wdgt.
    """

    #acn_toggle_column_alembic_path
    wdgt.acn_toggle_column_alembic_path.triggered.connect(functools.partial(wdgt.shot_metadata_view.view_functionality.toggle_column_with_header_name, 
                                                                            'Alembic Path'))

    #acn_toggle_column_export_proxy_for_prop_view
    wdgt.acn_toggle_column_export_proxy_for_prop_view.triggered.connect(functools.partial(wdgt.prop_metadata_view.view_functionality.toggle_column_with_header_name, 
                                                                                            'ExportProxy'))
    
    #acn_toggle_column_export_locator_for_prop_view
    wdgt.acn_toggle_column_export_locator_for_prop_view.triggered.connect(functools.partial(wdgt.prop_metadata_view.view_functionality.toggle_column_with_header_name, 
                                                                                            'ExportLocator'))

    #acn_toggle_column_export_proxy_for_char_view
    wdgt.acn_toggle_column_export_proxy_for_char_view.triggered.connect(functools.partial(wdgt.char_metadata_view.view_functionality.toggle_column_with_header_name, 
                                                                                            'ExportProxy'))
    
    #acn_toggle_column_export_locator_for_char_view
    wdgt.acn_toggle_column_export_locator_for_char_view.triggered.connect(functools.partial(wdgt.char_metadata_view.view_functionality.toggle_column_with_header_name, 
                                                                                            'ExportLocator'))

    #acn_progressbar_test_run
    wdgt.acn_progressbar_test_run.triggered.connect(functools.partial(wdgt.progressbar_test_run, 0, 200))
    #acn_hide_export_shell
    wdgt.acn_hide_export_shell.toggled.connect(wdgt.set_hide_export_shell)
    

def connect_menu_alembic(wdgt):
    """
    Connect menu alembic actions with wdgt.
    """

    #acn_set_help_enabled
    wdgt.acn_set_help_enabled.toggled.connect(wdgt.alembic_functionality.sgnl_set_help_enabled)

    #acn_set_dontSkipUnwrittenFrames_enabled
    wdgt.acn_set_dontSkipUnwrittenFrames_enabled.toggled.connect(wdgt.alembic_functionality.sgnl_set_dontSkipUnwrittenFrames_enabled)

    #acn_set_verbose_enabled
    wdgt.acn_set_verbose_enabled.toggled.connect(wdgt.alembic_functionality.sgnl_set_verbose_enabled)

    #acn_set_eulerFilter_enabled
    wdgt.acn_set_eulerFilter_enabled.toggled.connect(wdgt.alembic_functionality.sgnl_set_eulerFilter_enabled)

    #acn_set_noNormals_enabled
    wdgt.acn_set_noNormals_enabled.toggled.connect(wdgt.alembic_functionality.sgnl_set_noNormals_enabled)

    #acn_set_renderableOnly_enabled
    wdgt.acn_set_renderableOnly_enabled.toggled.connect(wdgt.alembic_functionality.sgnl_set_renderableOnly_enabled)

    #acn_set_selection_enabled
    wdgt.acn_set_selection_enabled.toggled.connect(wdgt.alembic_functionality.sgnl_set_selection_enabled)

    #acn_set_stripNamespaces_enabled
    wdgt.acn_set_stripNamespaces_enabled.toggled.connect(wdgt.alembic_functionality.sgnl_set_stripNamespaces_enabled)

    #acn_set_uvWrite_enabled
    wdgt.acn_set_uvWrite_enabled.toggled.connect(wdgt.alembic_functionality.sgnl_set_uvWrite_enabled)

    #acn_set_writeColorSets_enabled
    wdgt.acn_set_writeColorSets_enabled.toggled.connect(wdgt.alembic_functionality.sgnl_set_writeColorSets_enabled)

    #acn_set_writeFaceSets_enabled
    wdgt.acn_set_writeFaceSets_enabled.toggled.connect(wdgt.alembic_functionality.sgnl_set_writeFaceSets_enabled)

    #acn_set_wholeFrameGeo_enabled
    wdgt.acn_set_wholeFrameGeo_enabled.toggled.connect(wdgt.alembic_functionality.sgnl_set_wholeFrameGeo_enabled)

    #acn_set_worldSpace_enabled
    wdgt.acn_set_worldSpace_enabled.toggled.connect(wdgt.alembic_functionality.sgnl_set_worldSpace_enabled)

    #acn_set_writeVisibility_enabled
    wdgt.acn_set_writeVisibility_enabled.toggled.connect(wdgt.alembic_functionality.sgnl_set_writeVisibility_enabled)



    #acn_set_step
    wdgt.acn_set_step.value_changed.connect(wdgt.alembic_functionality.sgnl_set_step)
    wdgt.acn_set_step.state_changed.connect(wdgt.alembic_functionality.sgnl_set_step_enabled)

    #acn_set_frameRelativeSample
    wdgt.acn_set_frameRelativeSample.value_changed.connect(wdgt.alembic_functionality.sgnl_set_frameRelativeSample)
    wdgt.acn_set_frameRelativeSample.state_changed.connect(wdgt.alembic_functionality.sgnl_set_frameRelativeSample_enabled)

    #acn_set_preRollStartFrame
    wdgt.acn_set_preRollStartFrame.value_changed.connect(wdgt.alembic_functionality.sgnl_set_preRollStartFrame)
    wdgt.acn_set_preRollStartFrame.state_changed.connect(wdgt.alembic_functionality.sgnl_set_preRollStartFrame_enabled)



    #acn_set_attr
    wdgt.acn_set_attr.text_changed.connect(wdgt.alembic_functionality.sgnl_set_attr)
    wdgt.acn_set_attr.state_changed.connect(wdgt.alembic_functionality.sgnl_set_attr_enabled)

    #acn_set_attrPrefix
    wdgt.acn_set_attrPrefix.text_changed.connect(wdgt.alembic_functionality.sgnl_set_attrPrefix)
    wdgt.acn_set_attrPrefix.state_changed.connect(wdgt.alembic_functionality.sgnl_set_attrPrefix_enabled)

    #acn_set_userAttr
    wdgt.acn_set_userAttr.text_changed.connect(wdgt.alembic_functionality.sgnl_set_userAttr)
    wdgt.acn_set_userAttr.state_changed.connect(wdgt.alembic_functionality.sgnl_set_userAttr_enabled)

    #acn_set_userAttrPrefix
    wdgt.acn_set_userAttrPrefix.text_changed.connect(wdgt.alembic_functionality.sgnl_set_userAttrPrefix)
    wdgt.acn_set_userAttrPrefix.state_changed.connect(wdgt.alembic_functionality.sgnl_set_userAttrPrefix_enabled)



    #acn_print_export_command
    wdgt.acn_print_export_command.triggered.connect(functools.partial(wdgt.export, dry_run = True))


def connect_menu_assets(wdgt):
    """
    Connect menu assets actions with wdgt.
    """

    #acn_add_proxy_attributes
    wdgt.acn_add_proxy_attributes.triggered.connect(functools.partial(wdgt.maya_functionality.add_attribute_to_selected_nodes, 
                                                                        'helga_proxy',
                                                                        'transform'))

    #acn_add_rendergeo_attributes
    wdgt.acn_add_rendergeo_attributes.triggered.connect(functools.partial(wdgt.maya_functionality.add_attribute_to_selected_nodes, 
                                                                        'helga_rendergeo',
                                                                        'transform'))

    #acn_add_locator_attributes
    wdgt.acn_add_locator_attributes.triggered.connect(functools.partial(wdgt.maya_functionality.add_attribute_to_selected_nodes, 
                                                                        'helga_locator',
                                                                        'transform'))



    #acn_remove_proxy_attributes
    wdgt.acn_remove_proxy_attributes.triggered.connect(functools.partial(wdgt.maya_functionality.remove_attribute_from_selected_nodes, 
                                                                        'helga_proxy',
                                                                        'transform'))

    #acn_remove_rendergeo_attributes
    wdgt.acn_remove_rendergeo_attributes.triggered.connect(functools.partial(wdgt.maya_functionality.remove_attribute_from_selected_nodes, 
                                                                        'helga_rendergeo',
                                                                        'transform'))

    #acn_remove_locator_attributes
    wdgt.acn_remove_locator_attributes.triggered.connect(functools.partial(wdgt.maya_functionality.remove_attribute_from_selected_nodes, 
                                                                        'helga_locator',
                                                                        'transform'))





