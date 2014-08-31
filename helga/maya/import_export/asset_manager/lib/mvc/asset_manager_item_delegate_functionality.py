

"""
asset_manager_item_delegate_functionality
==========================================

AssetManager item delegate functionality. This module extends the item delegate modules
of the Asset Manager MVCs for common functionality.
"""




#Import
#------------------------------------------------------------------
#python
import subprocess
import logging
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

#asset_manager_globals
from lib import asset_manager_globals
if(do_reload):reload(asset_manager_globals)








#Globals
#------------------------------------------------------------------

#AssetManager Icons
ICON_TRUE = asset_manager_globals.ICON_TRUE
ICON_FALSE = asset_manager_globals.ICON_FALSE

#Colors
RED = asset_manager_globals.RED







#AssetManagerItemDelegateFunctionality class
#------------------------------------------------------------------
class AssetManagerItemDelegateFunctionality(object):
    """
    AssetManagerItemDelegateFunctionality class.
    """


    def __new__(cls, *args, **kwargs):
        """
        AssetManagerItemDelegateFunctionality instance factory.
        """

        #asset_manager_item_delegate_functionality_instance
        asset_manager_item_delegate_functionality_instance = super(AssetManagerItemDelegateFunctionality, cls).__new__(cls, args, kwargs)

        return asset_manager_item_delegate_functionality_instance

    
    def __init__(self, 
                    logging_level = logging.DEBUG,
                    item_delegate = None,
                    parent = None):
        """
        Customize instance.
        """

        #super
        self.parent_class = super(AssetManagerItemDelegateFunctionality, self)
        self.parent_class.__init__()

        
        #logger
        #------------------------------------------------------------------
        #logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logging_level = logging_level
        self.logger.setLevel(self.logging_level)


        
        #instance variables
        #------------------------------------------------------------------

        #item_delegate
        self.item_delegate = item_delegate

        #pxm_bool_true
        self.pxm_bool_true = QtGui.QPixmap(ICON_TRUE)
        #pxm_bool_false
        self.pxm_bool_false = QtGui.QPixmap(ICON_FALSE)


        



    



    #Getter & Setter
    #------------------------------------------------------------------

    def set_item_delegate(self, item_delegate):
        """
        Set self.item_delegate
        """

        self.item_delegate = item_delegate


    def get_item_delegate(self):
        """
        Get self.item_delegate
        """

        return self.item_delegate







    #Methods
    #------------------------------------------------------------------

    def get_column_data_dict_for_index(self, index):
        """
        Return a list with all data values for the column
        of index.
        """

        #index valid?
        if not(index.isValid()):
            #log
            self.logger.debug('Index invalid. Returning empty list')
            return []

        #model
        model = index.model()
        #row_count
        row_count = model.rowCount(None)

        #col
        col = index.column()

        #column_data_dict
        column_data_dict = {}
        #iterate
        for row in range(row_count):

            #current_index
            current_index = model.index(row, col)

            #current_index valid?
            if not(current_index.isValid()):
                #log
                self.logger.debug('Index invalid. Continuing')
                continue

            #data
            data = current_index.data(QtCore.Qt.DisplayRole)

            #append
            column_data_dict.setdefault(row, data)

        #return
        return column_data_dict


    def get_row_data_dict_for_index(self, index):
        """
        Return a list with all data values for the column
        of index.
        """

        #index valid?
        if not(index.isValid()):
            #log
            self.logger.debug('Index invalid. Returning empty list')
            return []

        #model
        model = index.model()
        #column_count
        column_count = model.columnCount(None)

        #row
        row = index.row()

        #row_data_dict
        row_data_dict = {}
        #iterate
        for col in range(column_count):

            #current_index
            current_index = model.index(row, col)

            #current_index valid?
            if not(current_index.isValid()):
                #log
                self.logger.debug('Index invalid. Continuing')
                continue

            #data
            data = current_index.data(QtCore.Qt.DisplayRole)

            #append
            row_data_dict.setdefault(col, data)

        #return
        return row_data_dict

    
    def duplicates_in_column(self, index):
        """
        Check wether or not the data value of index is
        unique in the column of index.
        Return True if there are duplicates and False
        if there are none OR if the index is invalid.
        """

        #index valid?
        if not(index.isValid()):
            #log
            self.logger.debug('Index invalid. Returning False.')
            return False

        
        #column_data_dict
        column_data_dict = self.get_column_data_dict_for_index(index)
        #check len
        if not (column_data_dict):
            #log
            self.logger.debug('Column data dict empty. Returning False.')
            return False


        #data
        data = index.data(QtCore.Qt.DisplayRole)

        #iterate
        for row, column_data in column_data_dict.iteritems():
            #check
            if (column_data == data and
                row != index.row()):
                return True

        #return
        return False


    def duplicates_in_row(self, index):
        """
        Check wether or not the data value of index is
        unique in the row of index.
        Return True if there are duplicates and False
        if there are none OR if the index is invalid.
        """

        #index valid?
        if not(index.isValid()):
            #log
            self.logger.debug('Index invalid. Returning False.')
            return False

        
        #row_data_dict
        row_data_dict = self.get_row_data_dict_for_index(index)
        #check len
        if not (row_data_dict):
            #log
            self.logger.debug('Row data dict empty. Returning False.')
            return False


        #data
        data = index.data(QtCore.Qt.DisplayRole)

        #iterate
        for col, row_data in row_data_dict.iteritems():
            #check
            if (row_data == data and
                col != index.column()):
                return True

        #return
        return False


    def paint_background_with_color(self, painter, option, index, color = RED):
        """
        Paint background in given color.
        The default color is red since this is often used to flag
        indices with errors.
        """

        #save painter
        painter.save()

        #set background color
        painter.setPen(QtGui.QPen(QtCore.Qt.NoPen))
        painter.setBrush(QtGui.QBrush(color))
        painter.drawRect(option.rect)

        #restore painter
        painter.restore()








    #Paint Datatypes
    #------------------------------------------------------------------

    def paint_bool_as_icon(self, painter, option, data):
        """
        Paint boolean values as icons.
        """

        #save painter
        painter.save()

        #width, height, center
        option_rect = option.rect
        width = option_rect.width()
        height = option_rect.height()
        center = option_rect.center()

        #margin
        margin = 5

        #pxm_bool
        if (data):
            pxm_bool = self.pxm_bool_true.scaledToHeight(height - (margin * 2))
        else:
            pxm_bool = self.pxm_bool_false.scaledToHeight(height - (margin * 2))

        #correct center to accomodate image in the center
        center.setX(center.x() - (pxm_bool.width() / 2))
        center.setY(center.y() - (pxm_bool.height() / 2))

        #draw pixmap
        painter.drawPixmap(center, pxm_bool)

        #restore painter
        painter.restore()


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

    

    
