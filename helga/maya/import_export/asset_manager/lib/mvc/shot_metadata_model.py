
"""
shot_metadata_model
==========================================

Subclass of QAbstractTableModel to display and edit shot_metadata.
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
#maya
import maya.cmds as cmds
import pymel.core as pm







#ShotMetadataModel class
#------------------------------------------------------------------
class ShotMetadataModel(QtCore.QAbstractTableModel):
    """
    Class customized to display shot metadata.
    -----------------------------

    **Expects the following format:**
    .. info::

        data_list = [[pynode], [pynode], [pynode], [pynode], ......]
    """

    def __new__(cls, *args, **kwargs):
        """
        ShotMetadataModel instance factory.
        """

        #shot_metadata_model_instance
        shot_metadata_model_instance = super(ShotMetadataModel, cls).__new__(cls, args, kwargs)

        return shot_metadata_model_instance
    
    
    def __init__(self, 
                logging_level = logging.DEBUG,
                parent=None):
        """
        Customize instance.
        """
        
        #super class init
        super(ShotMetadataModel, self).__init__(parent)


        #instance variables
        #------------------------------------------------------------------

        #header_name_list
        self.header_name_list = ['Shotname', 'Alembic Path', 'Shotcam', 'Start', 'End']

        #data_list
        self.data_list = [[]]
        
        
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

        #if any item in list return len
        if (any(self.data_list)):
            return len(self.data_list) 

        #else 0
        return 0

    
    def columnCount(self, parent):
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
            return super(ShotMetadataModel, self).data(self, index, role)
        
        
        #row & col
        row = index.row()
        col = index.column()

        #current_header
        current_header = self.header_name_list[col]

        #pynode
        pynode = self.data_list[row][0]

        #pynode mobject exists
        if not(pm.objExists(pynode.name())):
            return None
        
        #DisplayRole and EditRole (return identical in most cases,
        #if not then do recheck later...as with shot_cam attr.)
        if (role == QtCore.Qt.DisplayRole or
            role == QtCore.Qt.EditRole):

            #column Shotname
            if (current_header == self.header_name_list[0]):
                
                #shotname
                shotname = pynode.shot_name.get()
                
                return shotname

            #column Alembic Path
            elif (current_header == self.header_name_list[1]):
                
                #alembic_path
                alembic_path = pynode.alembic_path.get()
                
                return alembic_path

            #column Shotcam
            elif (current_header == self.header_name_list[2]):
                
                #DisplayRole
                if (role == QtCore.Qt.DisplayRole):
                    
                    #shot_cam
                    shot_cam = pynode.shot_cam.get()
                    return shot_cam

                
                #EditRole
                elif (role == QtCore.Qt.EditRole):
                    
                    #selected_cam_name
                    selected_cam_name = self.get_name_for_first_selection_if_shapetype_matches(pm.nodetypes.Camera)
                    #if true return
                    if(selected_cam_name):
                        return selected_cam_name
                    
                    #else return pynode attr
                    shot_cam = pynode.shot_cam.get()
                    return shot_cam

            #column Start
            elif (current_header == self.header_name_list[3]):
                
                #shot_start
                shot_start = pynode.shot_start.get()
                
                return shot_start

            #column End
            elif (current_header == self.header_name_list[4]):
                
                #shot_end
                shot_end = pynode.shot_end.get()
                
                return shot_end

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
        if not(pm.objExists(pynode.name())):
            return False

        #EditRole
        if (role == QtCore.Qt.EditRole):

            #column Shotname
            if (current_header == self.header_name_list[0]):
                
                #validate
                if(self.validate_value_for_shotname(value)):
                    
                    #set value
                    pynode.shot_name.set(value)
                    #data changed signal
                    self.dataChanged.emit(index, index)
                
                    return True

                return False

            #column Alembic Path
            elif (current_header == self.header_name_list[1]):
                
                #validate
                if(self.validate_value_for_alembic_path(value)):
                    
                    #set value
                    pynode.alembic_path.set(value)
                    #data changed signal
                    self.dataChanged.emit(index, index)
                
                    return True

                return False

            #column Shotcam
            elif (current_header == self.header_name_list[2]):
                
                #validate
                if(self.validate_value_for_shotcam(value)):
                    
                    #set value
                    pynode.shot_cam.set(value)
                    #data changed signal
                    self.dataChanged.emit(index, index)

                    return True

                return False

            #column Start
            elif (current_header == self.header_name_list[3]):
                
                #set value
                pynode.shot_start.set(value)
                #data changed signal
                self.dataChanged.emit(index, index)
                
                return True

            #column End
            elif (current_header == self.header_name_list[4]):
                
                #set value
                pynode.shot_end.set(value)
                #data changed signal
                self.dataChanged.emit(index, index)
                
                return True

            else:
                return False
        
        else:
            return False



    
    def flags(self, index):
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

    def get_name_for_first_selection_if_shapetype_matches(self, class_to_match):
        """
        **What it does:**

        #. Get first node of selection_list
        #. Get shape node for it
        #. Check shape node against class_to_match
        #. If all passed, return selected node name (**Not shape node name!**)
        """

        #check selected_node
        try:
            #selected_node
            selected_node = pm.ls(sl = True, et = 'transform')[0]
        except:
            return None
        
        #check node_shape
        try:
            node_shape = pm.PyNode(selected_node.getShape())
        except:
            return None
        
        #if not shape == class_to_match
        if not(type(node_shape) is class_to_match):
            return None


        #return
        return selected_node.name()





    #Custom setData methods
    #------------------------------------------------------------------

    def validate_value_for_shotname(self, value):
        """
        Validate the value that should be set on the shot_name attr. of the pynode.
        Return True or False.
        """

        try:
            
            #pattern_object
            pattern_object = re.compile(r'^[0-9]{3}[_]{1}[a-z]{1}([_a-z])+')
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


    def validate_value_for_alembic_path(self, value):
        """
        Validate the value that should be set on the alembic_path attr. of the pynode.
        Return True or False.
        """

        if(os.path.isdir(value)):
            return True
        
        return False

    
    def validate_value_for_shotcam(self, value):
        """
        Validate the value that should be set on the shot_cam attr. of the pynode.
        Return True or False.
        """

        #check if node for value exists
        try:
            #value_node
            value_node = pm.PyNode(value)
            
            #value_node_shape
            value_node_shape = pm.PyNode(value_node.getShape())
            
            #check correct type
            if(type(value_node_shape) is pm.nodetypes.Camera):

                return True

            else:
                pass

        except:
            pass
        
        return False
