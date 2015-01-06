
"""
renderthreads_node
==========================================

This module holds the definition of node objects,
which are used in combination with the RenderThreads
MVC.
"""


# Import
# ------------------------------------------------------------------
# python
import os
import logging
# PySide
from PySide import QtCore
# nuke
import nuke


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



# RenderThreadsNode
# ------------------------------------------------------------------
class RenderThreadsNode(QtCore.QObject):
    """
    Non abstract base class for RenderThreads nodes.
    Inherits from QObject for signals, ObjeczName etc.
    This class can be used to instantiate RenderThreadNodes
    for each type of node. Concrete sub classes allow
    for explicit type checking.

    Supported interface:
    #. name:
        Returns self._nuke_node.name()
    #. setName:
        Returns self._nuke_node.setName()
    #. fullName:
        Returns self._nuke_node.fullName()
    #. Class:
        Returns self.__class__.__name__
    """

    # Signals
    # ------------------------------------------------------------------

    # Creation and Initialization
    # ------------------------------------------------------------------
    def __new__(cls, *args, **kwargs):
        """
        RenderThreadsNode instance factory.
        """

        # node_instance
        node_instance = super(RenderThreadsNode, cls).__new__(cls, args, kwargs)

        return node_instance

    
    def __init__(self,
                    nuke_node=None,
                    start_frame=None,
                    end_frame=None):
        """
        Customize instance.
        """

        # super and objectName
        # ------------------------------------------------------------------
        # parent_class
        self.parent_class = super(RenderThreadsNode, self)
        self.parent_class.__init__()

        self.setObjectName(self.__class__.__name__)

        # instance variables
        # ------------------------------------------------------------------
        # _nuke_node
        self.set_nuke_node(nuke_node)

        # _start_frame
        self.set_start_frame(start_frame)

        # _end_frame
        self.set_end_frame(end_frame)

        # container_protocol_index_size
        self.container_protocol_index_size = 3

        # logger
        self.logger = renderthreads_logging.get_logger(self.__class__.__name__)

    # Getter and Setter
    # ------------------------------------------------------------------

    def get_nuke_node(self):
        """
        Return self._nuke_node
        """

        return self._nuke_node

    def set_nuke_node(self, value):
        """
        Set self._nuke_node
        """

        self._nuke_node = value

    nuke_node = property(get_nuke_node, set_nuke_node)
    """Access for self._nuke_node"""

    def get_start_frame(self):
        """
        Return self._start_frame
        """

        return self._start_frame

    def set_start_frame(self, value):
        """
        Set self._start_frame
        """

        self._start_frame = value

    start_frame = property(get_start_frame, set_start_frame)
    """Access for self._start_frame"""

    def get_end_frame(self):
        """
        Return self._end_frame
        """

        return self._end_frame

    def set_end_frame(self, value):
        """
        Set self._end_frame
        """
        
        self._end_frame = value

    end_frame = property(get_end_frame, set_end_frame)
    """Access for self._end_frame"""

    def get_nuke_node_name(self):
        """
        Return Nuke Node Name.
        """

        try:
            nuke_node_name = self._nuke_node.name()
            return nuke_node_name

        except:
            # log
            self.logger.debug('Error aquiring nuke node name. Returning None')
            return None

    def set_nuke_node_name(self, value):
        """
        Calls self._nuke_node.setName().
        """

        try:
            self._nuke_node.setName(value)
        except:
            # log
            self.logger.debug('Error setting nuke node name')

    def name(self):
        """
        Wrapper for get_nuke_node_name to be consistent with
        nuke python API. This method return self._nuke_node.name().
        """

        return self.get_nuke_node_name()

    def setName(self, value):
        """
        Wrapper for get_nuke_node_name to be consistent with
        nuke python API. This method return self._nuke_node.name().
        """

        return self.set_nuke_node_name(value)

    def get_nuke_node_full_name(self):
        """
        Return Nuke Node full name. This
        is a unique identifier.
        """

        try:
            nuke_node_full_name = self._nuke_node.fullName()
            return nuke_node_full_name

        except:
            # log
            self.logger.debug('Error aquiring nuke node full name. Returning None')
            return None

    def fullName(self):
        """
        Wrapper for get_nuke_node_full_name to be consistent with
        nuke python API. This method return self._nuke_node.fullName().
        """

        return self.get_nuke_node_full_name()

    def get_nuke_node_type(self):
        """
        Return Nuke Node Type.
        This returns a string with the node type
        name like "Write" etc.
        """

        try:
            nuke_node_type = self._nuke_node.Class()
            return nuke_node_type

        except:
            # log
            self.logger.debug('Error aquiring nuke node type. Returning None')
            return None

    def Class(self):
        """
        Wrapper for get_nuke_node_type to be consistent with
        nuke python API. This method however return the type
        of renderthreads_node and NOT the nuke node type.
        """

        return self.__class__.__name__

    def get_frame_list(self):
        """
        Return frame list.
        This list consists of the integers that can
        be used as Frame numbers directly (for example
        in the -F flag).
        Example:
        self._start_frame = 10
        self._end_frame = 20
        frame_list = [10,11,12,......,20]
        """

        # frame_list
        frame_list = range(self._end_frame + 1)
        frame_list = frame_list[self._start_frame:]

        # return
        return frame_list


    # Operator overrides
    # ------------------------------------------------------------------
    def __eq__(self, other):
        """=="""
        return self.get_nuke_node_full_name() == other.get_nuke_node_full_name()
    def __ne__(self, other):
        """!="""
        return self.get_nuke_node_full_name() != other.get_nuke_node_full_name()
    def __hash__(self):
        return hash(self.get_nuke_node_full_name())
    def __len__(self):
        """
        Return number of properties.
        [0]_nuke_node
        [1]_start_frame
        [2]_end_frame
        """
        return self.container_protocol_index_size
    
    def __getitem__(self, key):
        """
        Return value accessed by one of the
        property object. See __len__ for a list.
        """

        # TypeError
        if not (type(key) == int):
            raise TypeError

        # KeyError
        if (key < 0 and
            key > self.container_protocol_index_size - 1):
            raise KeyError

        # 0
        if (key == 0): 
            return self.get_nuke_node()
        # 1
        elif (key == 1): 
            return self.get_start_frame()
        # 2
        elif (key == 2): 
            return self.get_end_frame()


    # Misc
    # ------------------------------------------------------------------
    
    def nuke_node_exists(self):
        """
        Return True or False whether or not
        nuke node exists.
        """
        
        try:
            full_name = self.get_nuke_node_full_name()
            return nuke.exists(full_name)
        except:
            return False


# RenderThreadsNodeWrite
# ------------------------------------------------------------------
class RenderThreadsNodeWrite(RenderThreadsNode):
    """
    Concrete subclass of RenderThreadsNode explicitly for
    write node types.
    """

    # Signals
    # ------------------------------------------------------------------

    # Creation and Initialization
    # ------------------------------------------------------------------
    def __new__(cls, *args, **kwargs):
        """
        RenderThreadsNodeWrite instance factory.
        """

        # node_instance
        node_instance = super(RenderThreadsNodeWrite, cls).__new__(cls, args, kwargs)

        return node_instance

    
    def __init__(self,
                    nuke_node=None,
                    start_frame=None,
                    end_frame=None):
        """
        Customize instance.
        """

        # super and objectName
        # ------------------------------------------------------------------
        # parent_class
        self.parent_class = super(RenderThreadsNodeWrite, self)
        self.parent_class.__init__(nuke_node = nuke_node,
                                    start_frame = start_frame,
                                    end_frame = end_frame)

        self.setObjectName(self.__class__.__name__)

        # instance variables
        # ------------------------------------------------------------------
        # logger
        self.logger = renderthreads_logging.get_logger(self.__class__.__name__)