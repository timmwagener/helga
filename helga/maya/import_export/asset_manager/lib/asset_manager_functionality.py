

"""
asset_manager_functionality
==========================================

AssetManager functionality. This module separates most of the functionality
from the UI. It encompasses functions used with Maya or other.
"""




#Import
#------------------------------------------------------------------
#python
import logging
#PySide
from PySide import QtGui
from PySide import QtCore
#maya
import pymel.core as pm







#AssetManagerFunctionality class
#------------------------------------------------------------------
class AssetManagerFunctionality(object):

    def __new__(cls, *args, **kwargs):
        """
        AssetManagerFunctionality instance factory.
        """

        #asset_manager_functionality_instance
        asset_manager_functionality_instance = super(AssetManagerFunctionality, cls).__new__(cls, args, kwargs)

        return asset_manager_functionality_instance

    
    def __init__(self, logging_level = logging.DEBUG):
        """
        Customize instance.
        """

        #super
        self.parent_class = super(AssetManagerFunctionality, self)
        self.parent_class.__init__()


        #instance variables
        #------------------------------------------------------------------

        
        #logger
        #------------------------------------------------------------------
        #logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logging_level = logging_level
        self.logger.setLevel(self.logging_level)




    #Maya
    #------------------------------------------------------------------

    def create_node(self, node_type):
        """
        Create node of given type. Node type is given as string.
        """
        
        #select
        new_node = pm.createNode(node_type)

        return new_node


    def select_nodes(self, pynode_list):
        """
        Select all pynodes from pynode_list.
        """
        
        #clear
        pm.select(cl = True)

        #select
        pm.select(pynode_list, r = True)


    def delete_nodes(self, pynode_list):
        """
        Delete all pynodes from pynode_list.
        """
        
        #clear
        pm.select(cl = True)

        #iterate and delete
        for pynode in pynode_list:
            
            try:
                pm.delete(pynode)
            except:
                self.logger.debug('Error deleting node {0}'.format(pynode.name()))


    def get_nodes_of_type(self, node_type, selection = False):
        """
        Return list of asset metadata nodes.
        """
        try:
            #node_list
            node_list = pm.ls(sl = selection, et = node_type)

            return node_list
        
        except:
            pass

        return []


    def get_current_frame(self):
        """
        Return current frame.
        """

        return pm.animation.currentTime()


    def get_current_framerange_start(self):
        """
        Return start of current framerange. (Not complete range)
        """

        return pm.playbackOptions(q = True, min = True)


    def get_current_framerange_end(self):
        """
        Return end of current framerange. (Not complete range)
        """

        return pm.playbackOptions(q = True, max = True)


    def get_complete_framerange_start(self):
        """
        Return start of complete framerange.
        """

        return pm.playbackOptions(q = True, ast = True)


    def get_complete_framerange_end(self):
        """
        Return end of complete framerange.
        """

        return pm.playbackOptions(q = True, aet = True)


    def remove_duplicate_pynodes(self, pynode_list):
        """
        Remove duplicate pynodes from list and return corrected list.
        This does NOT detect several PyNodes pointing to the same object,
        it only detects references to the same PyNode.
        """

        #pynode_id_list
        pynode_id_list = []

        #clean_pynode_list
        clean_pynode_list = []

        #iterate
        for pynode in pynode_list:

            #pynode_id
            pynode_id = id(pynode)

            #pynode already in list, continue
            if (pynode_id in pynode_id_list):
                continue

            #else append
            pynode_id_list.append(pynode_id)
            clean_pynode_list.append(pynode)

        return clean_pynode_list


