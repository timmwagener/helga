
"""
char_metadata_model
==========================================

Subclass of QAbstractTableModel to display and edit char metadata.
"""




#Import
#------------------------------------------------------------------
#python
import os
import logging
import re
#PySide
from PySide import QtGui
from PySide import QtCore




#Import variable
do_reload = True

#asset_manager

#lib

#asset_manager_functionality
from lib import asset_manager_functionality
if(do_reload):reload(asset_manager_functionality)









#CharMetadataModel class
#------------------------------------------------------------------
class CharMetadataModel(QtCore.QAbstractTableModel):
    """
    Class customized to display char metadata.
    -----------------------------

    **Expects the following format:**
    .. info::

        data_list = [[pynode], [pynode], [pynode], [pynode], ......]
    """

    def __new__(cls, *args, **kwargs):
        """
        CharMetadataModel instance factory.
        """

        #char_metadata_model_instance
        char_metadata_model_instance = super(CharMetadataModel, cls).__new__(cls, args, kwargs)

        return char_metadata_model_instance
    
    
    def __init__(self, 
                logging_level = logging.DEBUG,
                parent=None):
        """
        Customize instance.
        """
        
        #super class init
        super(CharMetadataModel, self).__init__(parent)


        #instance variables
        #------------------------------------------------------------------

        #header_name_list
        self.header_name_list = ['Assetname', 'Namespace', 'ExportProxy', 'ExportRendergeo', 'ExportLocator']

        #data_list
        self.data_list = [[]]

        #maya_functionality
        self.maya_functionality = asset_manager_functionality.AssetManagerFunctionality()
        
        
        #logger
        #------------------------------------------------------------------
        #logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logging_level = logging_level
        self.logger.setLevel(self.logging_level)
        
    
    def headerData(self, section, orientation, role = QtCore.Qt.DisplayRole):
        """
        Return header description for section.
        """
        
        #horizontal
        if(orientation == QtCore.Qt.Horizontal):
            
            #DisplayRole
            if (role == QtCore.Qt.DisplayRole):
                return self.header_name_list[section]

        #vertical
        elif(orientation == QtCore.Qt.Vertical):
            
            #DisplayRole
            if (role == QtCore.Qt.DisplayRole):
                return section
        
        return QtCore.QAbstractTableModel.headerData(self, section, orientation, role)

    
    def rowCount(self, parent):
        """
        Return row count.
        """

        #if any item in list return len
        if (any(self.data_list)):
            return len(self.data_list) 

        #else 0
        return 0

    
    def columnCount(self, parent):
        """
        Return column count.
        """

        return len(self.header_name_list) 

    
    def data(self, index, role = QtCore.Qt.DisplayRole):
        """
        Return data for current index. The returned data is
        rendered by QItemDelegate.
        """

        #index invalid
        if not(index.isValid()):
            #log
            self.logger.debug('Index {0} not valid.'.format(index))
            #evaluate in superclass
            return super(CharMetadataModel, self).data(self, index, role)
        
        
        #row & col
        row = index.row()
        col = index.column()

        #current_header
        current_header = self.header_name_list[col]

        #pynode
        pynode = self.data_list[row][0]

        #pynode mobject exists
        if not(self.maya_functionality.object_exists(pynode)):
            return None
        
        #DisplayRole and EditRole (return identical in most cases,
        #if not then do recheck later in this function)
        if (role == QtCore.Qt.DisplayRole or
            role == QtCore.Qt.ToolTipRole or
            role == QtCore.Qt.EditRole):

            
            #column Assetname
            if (current_header == self.header_name_list[0]):
                
                #asset_name
                asset_name = pynode.asset_name.get()
                
                return asset_name

            
            #column Namespace
            elif (current_header == self.header_name_list[1]):
                
                #namespace
                namespace = pynode.namespace()
                
                return namespace

            
            #column ExportProxy
            elif (current_header == self.header_name_list[2]):
                
                #proxy_export
                proxy_export = pynode.proxy_export.get()
                
                return proxy_export


            #column ExportRendergeo
            elif (current_header == self.header_name_list[3]):
                
                #rendergeo_export
                rendergeo_export = pynode.rendergeo_export.get()
                
                return rendergeo_export


            #column ExportLocator
            elif (current_header == self.header_name_list[4]):
                
                #locator_export
                locator_export = pynode.locator_export.get()
                
                return locator_export

            else:
                return None
        
        else:
            return None


    def setData(self, index, value, role = QtCore.Qt.EditRole):
        """
        Set data method for model.
        """

        #index invalid
        if not(index.isValid()):
            #log
            self.logger.debug('Index {0} not valid.'.format(index))
            #evaluate in superclass
            return False
        
        
        #row & col
        row = index.row()
        col = index.column()

        #current_header
        current_header = self.header_name_list[col]

        #pynode
        pynode = self.data_list[row][0]

        #pynode mobject exists
        if not(self.maya_functionality.object_exists(pynode)):
            return False

        #EditRole
        if (role == QtCore.Qt.EditRole):

            
            #column Assetname
            if (current_header == self.header_name_list[0]):
                
                #validate
                if(self.validate_value_for_asset_name(value)):
                    
                    #set value
                    pynode.asset_name.set(value)
                    #data changed signal
                    self.dataChanged.emit(index, index)
                
                    return True

                return False

            
            #column ExportProxy
            elif (current_header == self.header_name_list[2]):
                
                #set value
                pynode.proxy_export.set(value)
                #data changed signal
                self.dataChanged.emit(index, index)
                
                return True


            #column ExportRendergeo
            elif (current_header == self.header_name_list[3]):
                
                #set value
                pynode.rendergeo_export.set(value)
                #data changed signal
                self.dataChanged.emit(index, index)
                
                return True


            #column ExportLocator
            elif (current_header == self.header_name_list[4]):
                
                #set value
                pynode.locator_export.set(value)
                #data changed signal
                self.dataChanged.emit(index, index)
                
                return True

            
            else:
                return False
        
        else:
            return False



    
    def flags(self, index):
        """
        Return flags for indices.
        """

        #index invalid
        if not(index.isValid()):
            #log
            self.logger.debug('Index {0} not valid.'.format(index))
            #evaluate in superclass
            return super(CharMetadataModel, self).flags(self, index)
        
        
        #row & col
        row = index.row()
        col = index.column()

        #current_header
        current_header = self.header_name_list[col]


        #check cases

        #column Namespace
        if (current_header == self.header_name_list[1]):
            
            #not editable
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

        
        #default case
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsSelectable

    
    def update(self, data_list):
        #set data_list
        self.data_list = data_list
        #reset
        self.reset()

    
    def clear(self):
        #set data_list
        self.data_list = [[]]
        #reset
        self.reset()








    #Custom data methods
    #------------------------------------------------------------------

    def get_data_list(self):
        """
        Return self.data_list
        """

        return self.data_list


    def get_data_list_flat(self):
        """
        Return self.data_list pynodes as flat list.
        [[pynode], [pynode]] >> [pynode, pynode, pynode]
        """

        #data_list_flat
        data_list_flat = []

        #iterate
        for pynode_list in self.data_list:
            
            #check if index exists
            try:
                pynode = pynode_list[0]
            except:
                continue

            #append
            data_list_flat.append(pynode)


        #return
        return data_list_flat




    #Custom setData methods
    #------------------------------------------------------------------

    def validate_value_for_asset_name(self, value):
        """
        Validate the value that should be set on the asset_name attr. of the pynode.
        Return True or False.
        """

        try:
            
            #pattern_object
            pattern_object = re.compile(r'^[a-z]{1}[0-9a-z_]+')
            #match_string
            match_string = pattern_object.match(value).group()

            #compare
            if(len(value) == len(match_string)):
                return True

            else:
                pass
        
        except:
            pass
        
        return False

