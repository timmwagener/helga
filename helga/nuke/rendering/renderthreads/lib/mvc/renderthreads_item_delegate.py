
"""
renderthreads_item_delegate
==========================================

Subclass of QStyledItemDelegate to format view
"""


# Import
# ------------------------------------------------------------------
# python
import logging
# PySide
from PySide import QtGui
from PySide import QtCore
# nuke
import nuke

#  Import variable
do_reload = True


#  renderthreads

#  lib

#  renderthreads_globals
from .. import renderthreads_globals
if(do_reload):
    reload(renderthreads_globals)

#  renderthreads_logging
from .. import renderthreads_logging
if(do_reload):
    reload(renderthreads_logging)


# Globals
# ------------------------------------------------------------------


# RenderThreadsItemDelegate
# ------------------------------------------------------------------
class RenderThreadsItemDelegate(QtGui.QStyledItemDelegate):
    """
    Subclass of QStyledItemDelegate.
    """

    # Creation and Initialization
    # ------------------------------------------------------------------

    def __new__(cls, *args, **kwargs):
        """
        RenderThreadsItemDelegate instance factory.
        """

        # renderthreads_item_delegate_instance
        renderthreads_item_delegate_instance = super(RenderThreadsItemDelegate, cls).__new__(cls, args, kwargs)

        return renderthreads_item_delegate_instance

    
    def __init__(self, 
                logging_level = logging.DEBUG,
                parent=None):
        """
        Customize instance.
        """
        
        # super and objectName
        # ------------------------------------------------------------------
        
        # parent_class
        self.parent_class = super(RenderThreadsItemDelegate, self)
        self.parent_class.__init__(parent=parent)

        # setObjectName
        self.setObjectName(self.__class__.__name__)

        # instance variables
        # ------------------------------------------------------------------
        
        # logger
        self.logger = renderthreads_logging.get_logger(self.__class__.__name__)


    # Size Hint
    # ------------------------------------------------------------------

    def sizeHint(self, option, index):
        """
        Returns the size for a type a certain index represents.
        -----------------------

        Types handled:
        #. Lists
        #. nuke.Node
        """
        
        # index invalid
        if not(index.isValid()):

            # parent_class sizeHint
            return self.parent_class.sizeHint(option, index)
            
        # data
        data = index.data(QtCore.Qt.DisplayRole)

        # row & col
        row = index.row()
        col = index.column()


        # check types

        # list
        if(type(data) is list):
            
            # value_string
            value_string = ''
            for index, value in enumerate(data):
                
                # last value
                if(index == len(data) - 1):
                    value_string += str(value)
                    continue
                
                # append
                value_string += str(value + ';\n')

            # text_size
            q_font_metrics = QtGui.QFontMetrics(QtGui.QApplication.font())
            text_size = q_font_metrics.size(0, value_string)
            return text_size

        # nuke.Node
        elif(type(data) is nuke.Node):

            #value_string
            value_string = data.fullName()

            # text_size
            q_font_metrics = QtGui.QFontMetrics(QtGui.QApplication.font())
            text_size = q_font_metrics.size(0, value_string)
            return text_size
        
        # other type
        else:
            
            # parent_class sizeHint
            return self.parent_class.sizeHint(option, index)

    # Paint
    # ------------------------------------------------------------------

    def paint(self, painter, option, index):
        """
        Define the look of the current item based on its type.
        -----------------------

        Types handled:
        #. Lists
        #. nuke.Node
        """

        # index invalid
        if not(index.isValid()):
            
            # parent_class paint
            self.parent_class.paint(painter, option, index)
            return

        # data
        data = index.data(QtCore.Qt.DisplayRole)

        # row & col
        row = index.row()
        col = index.column()

        # list
        if(type(data) is list):

            # paint_list_as_string_with_lines
            self.paint_list_as_string_with_lines(painter, option, data)

        # nuke.Node
        elif(type(data) is nuke.Node):
            
            # paint_nuke_node
            self.paint_nuke_node(painter, option, data)

        # other type
        else:
            
            # parent_class paint
            self.parent_class.paint(painter, option, index)

    def paint_list_as_string_with_lines(self, painter, option, data):
        """
        Paint list as string with a seperate
        line for each list entry.
        """

        #save painter
        painter.save()
        
        #value_string
        value_string = ''
        for index, value in enumerate(data):
            
            #last value
            if(index == len(data) - 1):
                value_string += str(value)
                continue
            
            #append
            value_string += str(value + ';\n')


        #draw
        painter.drawText(option.rect, QtCore.Qt.AlignLeft, value_string)

        #restore painter
        painter.restore()

    def paint_nuke_node(self, painter, option, data):
        """
        Paint nuke.Node as string 
        consisting of nuke_node full name.
        """

        #save painter
        painter.save()
        
        #value_string
        value_string = str(data.fullName())

        #draw
        painter.drawText(option.rect, QtCore.Qt.AlignLeft, value_string)

        #restore painter
        painter.restore()