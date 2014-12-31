

"""
renderthreads_gui_helper
==========================================

This module encapsulates global ui related
helper functions
"""


# Import
# ------------------------------------------------------------------
# PySide
from PySide import QtGui
from PySide import QtCore


# Globals
# ------------------------------------------------------------------


# Cleanup
# ------------------------------------------------------------------
def get_widget_by_class_name_closure(wdgt_class_name):
    """
    Practicing closures. Doesnt really make sense here, or could at least
    be done much simpler/better.
    Want to try it with filter in order to get more into the builtins.
    """

    def get_widget_by_class_name(wdgt):
        """
        Function that is closed in. Accepts and checks all
        widgets against wdgt_class_name from enclosing function.
        All this mess to be able to use it with filter.
        """
        try:
            if (type(wdgt).__name__ == wdgt_class_name):
                return True
        except:
            pass
        return False

    return get_widget_by_class_name


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
            if (wdgt.objectName() == wdgt_name):
                return True
        except:
            pass
        return False

    return get_widget_by_name


def check_and_delete_wdgt_instances_with_class_name(wdgt_class_name):
    """
    Search for all occurences with wdgt_class_name and delete them.
    """

    # get_wdgt_closure
    get_wdgt_closure = get_widget_by_class_name_closure(wdgt_class_name)

    # wdgt_list
    wdgt_list = filter(get_wdgt_closure, QtGui.QApplication.allWidgets())

    # iterate and delete
    for index, wdgt in enumerate(wdgt_list):

        # Enable when threads are in.
        """
        # try to stop threads (wdgt == AssetManager)
        try:
            print('Stop threads for wdgt {0}'.format(wdgt.objectName()))
            wdgt.stop_all_threads_and_timer()
        except:
            pass
        """

        # schedule widget for deletion
        try:
            # log
            print('Scheduled widget {0} for deletion'.format(wdgt.objectName()))
            # delete
            wdgt.deleteLater()
        except:
            pass

    return wdgt_list


def check_and_delete_wdgt_instances_with_name(wdgt_name):
    """
    Search for all occurences with wdgt_name and delete them.
    """

    # get_wdgt_closure
    get_wdgt_closure = get_widget_by_name_closure(wdgt_name)

    # wdgt_list
    wdgt_list = filter(get_wdgt_closure, QtGui.QApplication.allWidgets())

    # iterate and delete
    for index, wdgt in enumerate(wdgt_list):

        # schedule widget for deletion
        try:
            # log
            print('Scheduled widget {0} for deletion'.format(wdgt.objectName()))
            # delete
            wdgt.deleteLater()
        except:
            pass

    return wdgt_list


# PySide
# ------------------------------------------------------------------
def load_ui_type(ui_file):
    """
    Pyside lacks the "loadUiType" command, so we have to convert the ui file to py code in-memory first
    and then execute it in a special frame to retrieve the form_class.
    This function return the form and base classes for the given qtdesigner ui file.
    """

    # lazy import

    try:

        # PySide
        from PySide import QtGui
        from PySide import QtCore
        from PySide import QtUiTools
        import pysideuic

    except Exception as exception_instance:
        # log
        print('Import failed: {0}'.format(exception_instance))
        # return None
        return None

    # compile ui

    parsed = xml.parse(ui_file)
    widget_class = parsed.find('widget').get('class')
    form_class = parsed.find('class').text

    with open(ui_file, 'r') as f:
        o = StringIO()
        frame = {}

        pysideuic.compileUi(f, o, indent=0)
        pyc = compile(o.getvalue(), '<string>', 'exec')
        exec pyc in frame

        # Fetch the base_class and form class based on their type in the xml from designer
        form_class = frame['Ui_%s' % form_class]
        base_class = eval('QtGui.%s' % widget_class)

    return form_class, base_class


def get_nuke_main_window():
    """
    Return the Maya main window.
    """

    try:
        # PySide
        from PySide import QtGui
        from PySide import QtCore

    except Exception as exception_instance:

        # log
        print('Import failed: {0}'.format(exception_instance))
        # return None
        return None

    # ptr_main_window
    ptr_main_window = QtGui.QApplication.activeWindow()

    # if True
    if (ptr_main_window):
        return ptr_main_window

    return None
