

"""
asset_manager_view_functionality
==========================================

AssetManager view functionality. This module extends the view modules
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










#Globals
#------------------------------------------------------------------









#AssetManagerViewFunctionality class
#------------------------------------------------------------------
class AssetManagerViewFunctionality(object):
    """
    AssetManagerViewFunctionality class.
    """


    def __new__(cls, *args, **kwargs):
        """
        AssetManagerViewFunctionality instance factory.
        """

        #asset_manager_view_functionality_instance
        asset_manager_view_functionality_instance = super(AssetManagerViewFunctionality, cls).__new__(cls, args, kwargs)

        return asset_manager_view_functionality_instance

    
    def __init__(self, 
                    logging_level = logging.DEBUG,
                    view = None,
                    parent = None):
        """
        Customize instance.
        """

        #super
        self.parent_class = super(AssetManagerViewFunctionality, self)
        self.parent_class.__init__()

        
        #logger
        #------------------------------------------------------------------
        #logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logging_level = logging_level
        self.logger.setLevel(self.logging_level)


        
        #instance variables
        #------------------------------------------------------------------

        #view
        self.view = view



    



    #Getter & Setter
    #------------------------------------------------------------------

    def set_view(self, view):
        """
        Set self.view
        """

        self.view = view


    def get_view(self):
        """
        Get self.view
        """

        return self.view







    #Methods
    #------------------------------------------------------------------

    def get_column_with_header_name(self, header_name):
        """
        Get column index for given header name.
        """

        #check if view has model
        if not(self.view.model()):
            #log
            self.logger.debug('View does not have model. Returning None instead of column index.')
            return None

        #section_count
        section_count = self.view.horizontalHeader().count()

        #iterate header_data
        for index in range(section_count):

            #header_data
            header_data = self.view.model().headerData(index, QtCore.Qt.Horizontal)

            #if match get index
            if (header_data == header_name):
                
                #return
                return index

        #no match return None
        return None


    def is_column_with_header_name_hidden(self, header_name):
        """
        Return True or False if the column with given header_name is hidden.
        Return None if the column doesnt exist.
        """

        #column_index
        column_index = self.get_column_with_header_name(header_name)
        #header_name not found
        if (column_index is None):
            #log
            self.logger.debug('Header name {0} not found in model. Not getting hidden status.'.format(header_name))
            return None

        #column_hidden_status
        column_hidden_status = self.view.isColumnHidden(column_index)

        #log
        self.logger.debug('Column for header {0} hidden status is {1}.'.format(header_name, column_hidden_status))

        #return
        return column_hidden_status


    def hide_column_with_header_name(self, header_name, visibility):
        """
        Set hidden status for column with given header name.
        """

        #column_index
        column_index = self.get_column_with_header_name(header_name)
        #header_name not found
        if (column_index is None):
            #log
            self.logger.debug('Header name {0} not found in model. Not setting visibility.'.format(header_name))
            return None

        #set hidden
        self.view.setColumnHidden(column_index, visibility)

        #log
        self.logger.debug('Set header {0} hidden status to {1}.'.format(header_name, visibility))


    def toggle_column_with_header_name(self, header_name):
        """
        Return True or False if the column with given header_name is hidden.
        Return None if the column doesnt exist.
        """

        #column_index
        column_index = self.get_column_with_header_name(header_name)
        #header_name not found
        if (column_index is None):
            #log
            self.logger.debug('Header name {0} not found in model. Not toggling hidden status.'.format(header_name))
            return None

        #column_hidden_status
        column_hidden_status = self.view.isColumnHidden(column_index)

        #make visible
        if (column_hidden_status):

            #set hidden
            self.view.setColumnHidden(column_index, False)

        #hide
        else:

            #set hidden
            self.view.setColumnHidden(column_index, True)


        #log
        self.logger.debug('Set header {0} hidden status to {1}.'.format(header_name, 
                                                                        self.view.isColumnHidden(column_index)))

        



    

    
