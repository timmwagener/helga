
"""
renderthreads_model
==========================================

Subclass of QAbstractTableModel to display 
and edit renderthreads nodes.
"""


# Import
# ------------------------------------------------------------------
# python
import os
import logging
import re
# PySide
from PySide import QtGui
from PySide import QtCore


# Import variable
do_reload = True


# renderthreads

# lib

# renderthreads_globals
from .. import renderthreads_globals
if(do_reload):
    reload(renderthreads_globals)

# renderthreads_logging
from .. import renderthreads_logging
if(do_reload):
    reload(renderthreads_logging)


# RenderThreadsModel
# ------------------------------------------------------------------
class RenderThreadsModel(QtCore.QAbstractTableModel):
    """
    Class customized to display 
    renderthreads nodes.
    ------------------------------------------

    **Expects the following format:**
    .. info::

        data_list = [[renderthreads_node], [renderthreads_node], 
                        [renderthreads_node], [renderthreads_node],
                        ......]
    """

    def __new__(cls, *args, **kwargs):
        """
        RenderThreadsModel instance factory.
        """

        # renderthreads_model_instance
        renderthreads_model_instance = super(RenderThreadsModel, cls).__new__(cls, args, kwargs)

        return renderthreads_model_instance
    
    
    def __init__(self, parent=None):
        """
        Customize instance.
        """
        
        # super and objectName
        # ------------------------------------------------------------------
        self.parent_class = super(RenderThreadsModel, self)
        self.parent_class.__init__(parent)

        # setObjectName
        self.setObjectName(self.__class__.__name__)


        # instance variables
        # ------------------------------------------------------------------
        # header_name_list
        self.header_name_list = ['name', 'start_frame', 'end_frame', 'additional_args']

        # data_list
        self.data_list = [[]]
        
        # logger
        self.logger = renderthreads_logging.get_logger(self.__class__.__name__)
        
    
    def headerData(self, section, orientation, role = QtCore.Qt.DisplayRole):
        """
        Return header description for section.
        """
        
        # horizontal
        if(orientation == QtCore.Qt.Horizontal):
            
            # DisplayRole
            if (role == QtCore.Qt.DisplayRole):
                return self.format_string(self.header_name_list[section])

        # vertical
        elif(orientation == QtCore.Qt.Vertical):
            
            # DisplayRole
            if (role == QtCore.Qt.DisplayRole):
                return section
        
        return QtCore.QAbstractTableModel.headerData(self, section, orientation, role)

    
    def rowCount(self, parent):

        # if any item in list return len
        if (any(self.data_list)):
            return len(self.data_list) 

        # else 0
        return 0

    
    def columnCount(self, parent):
        return len(self.header_name_list) 

    
    def data(self, index, role = QtCore.Qt.DisplayRole):
        """
        Return data for current index. The returned data is
        rendered by QItemDelegate.
        """

        # index invalid
        if not(index.isValid()):
            # log
            self.logger.debug('Index {0} not valid.'.format(index))
            # evaluate in superclass
            return self.parent_class.data(index, role)
        
        
        # row & col
        row = index.row()
        col = index.column()

        # current_header
        current_header = self.header_name_list[col]

        # renderthreads_node
        renderthreads_node = self.data_list[row][0]

        # nuke_node exists
        if not(renderthreads_node.nuke_node_exists()):
            return None
        
        # DisplayRole and EditRole (return identical in most cases,
        # if not then do recheck later)
        if (role == QtCore.Qt.DisplayRole or
            role == QtCore.Qt.ToolTipRole or
            role == QtCore.Qt.EditRole):

            # column name
            if (current_header == self.header_name_list[0]):
                
                # name
                name = renderthreads_node.name
                return name

            # column start_frame
            elif (current_header == self.header_name_list[1]):
                
                # start_frame
                start_frame = renderthreads_node.start_frame
                return start_frame

            # column end_frame
            elif (current_header == self.header_name_list[2]):
                
                # end_frame
                end_frame = renderthreads_node.end_frame
                return end_frame

            # column additional_args
            elif (current_header == self.header_name_list[3]):
                
                # additional_args
                additional_args = pynode.additional_args
                
                return additional_args

            else:
                # evaluate in superclass
                return self.parent_class.data(index, role)
        
        else:
            # evaluate in superclass
            return self.parent_class.data(index, role)


    def setData(self, index, value, role = QtCore.Qt.EditRole):
        """
        Set data method for model.
        """

        # index invalid
        if not(index.isValid()):
            # log
            self.logger.debug('Index {0} not valid.'.format(index))
            # evaluate in superclass
            return self.parent_class.setData(index, value, role)
        
        
        # row & col
        row = index.row()
        col = index.column()

        # current_header
        current_header = self.header_name_list[col]

        # renderthreads_node
        renderthreads_node = self.data_list[row][0]

        # nuke_node exists
        if not(renderthreads_node.nuke_node_exists()):
            return False

        # EditRole
        if (role == QtCore.Qt.EditRole):

            # column name
            if (current_header == self.header_name_list[0]):
                
                # validate
                if(self.validate_value_for_name(value)):
                    
                    # set value
                    renderthreads_node.name = value
                    # data changed signal
                    self.dataChanged.emit(index, index)
                
                    return True

                return False

            # column start_frame
            elif (current_header == self.header_name_list[1]):
                
                # validate
                if(self.validate_value_for_start_frame(value)):
                    
                    # set value
                    renderthreads_node.start_frame = value
                    # data changed signal
                    self.dataChanged.emit(index, index)
                
                    return True

                return False

            # column end_frame
            elif (current_header == self.header_name_list[2]):
                
                # validate
                if(self.validate_value_for_end_frame(value)):
                    
                    # set value
                    renderthreads_node.end_frame = value
                    # data changed signal
                    self.dataChanged.emit(index, index)
                
                    return True

                return False

            # column additional_args
            elif (current_header == self.header_name_list[3]):
                
                # validate
                if(self.validate_value_for_additional_args(value)):
                    
                    # set value
                    renderthreads_node.additional_args = value
                    # data changed signal
                    self.dataChanged.emit(index, index)
                
                    return True

                return False

            else:
                # evaluate in superclass
                return self.parent_class.setData(index, value, role)
        
        else:
            # evaluate in superclass
            return self.parent_class.setData(index, value, role)

    def flags(self, index):
        """
        Return flags for indices.
        """
        
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsSelectable

    def update(self, data_list):
        """
        Set data_list and reset display.
        """

        # set data_list
        self.data_list = data_list
        # reset
        self.reset()

    def clear(self):
        """
        Set empty data_list to model.
        """

        # set data_list
        self.data_list = [[]]
        # reset
        self.reset()

    def get_data_list(self):
        """
        Return self.data_list
        """

        return self.data_list

    def get_data_list_flat(self):
        """
        Return self.data_list entries as flat list.
        [[data], [data]] >> [data, data, data]
        """

        # data_list_flat
        data_list_flat = []

        # iterate
        for inner_data_list in self.data_list:
            
            # check if index exists
            try:
                data = inner_data_list[0]
            except:
                continue

            # append
            data_list_flat.append(data)

        # return
        return data_list_flat

    # Validation
    # ------------------------------------------------------------------

    def validate_value_for_name(self, value):
        """
        Validate the value that should be set on the attr. of the data object.
        Return True or False.
        """

        return True


    def validate_value_for_start_frame(self, value):
        """
        Validate the value that should be set on the attr. of the data object.
        Return True or False.
        """

        return True

    
    def validate_value_for_end_frame(self, value):
        """
        Validate the value that should be set on the attr. of the data object.
        Return True or False.
        """

        return True

    def validate_value_for_additional_args(self, value):
        """
        Validate the value that should be set on the attr. of the data object.
        Return True or False.
        """

        return True


    # Misc
    # ------------------------------------------------------------------

    def format_string(self, string_value):
        """
        Return a pretty version of string. This method is
        catered towards my naming habits.
        """
        
        try:
            # First letter uppercase
            formatted_string_value = string_value[0].upper() + string_value[1:]

            # replace _
            formatted_string_value = formatted_string_value.replace('_', ' ')
        
        except:
            # log
            self.logger.debug('Error formatting {0}. Returning empty string'.format(string_value))
            return ''

        return formatted_string_value
