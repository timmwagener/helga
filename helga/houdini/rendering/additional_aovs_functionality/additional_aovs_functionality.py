




#

"""
additional_aovs_functionality
==========================================

Module that offers possibilities to adjust parameters on the additional_aovs hda globally from one node.
The content of this module is ment to be copied into the hdaModule section of the additional_aovs_control
HDA.

-----------------------

**Author:** `Timm Wagener <mailto:wagenertimm@gmail.com>`_
"""





#Add tool root path
#------------------------------------------------------------------

#import
import sys
import os

#tool_root_path
tool_root_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(tool_root_path)





#Import
#------------------------------------------------------------------
#python
import functools
import logging
import time

#houdini
import hou





#Import variable
do_reload = True

#helga

#global_variables
from helga.general.setup.global_variables import global_variables
if(do_reload):reload(global_variables)

#global_functions
from helga.general.setup.global_functions import global_functions
if(do_reload):reload(global_functions)


#additional_aovs_functionality

#lib

#additional_aovs_functionality_logging_handler
from lib import additional_aovs_functionality_logging_handler
if(do_reload):reload(additional_aovs_functionality_logging_handler)







#Globals
#------------------------------------------------------------------

ADDITIONAL_AOVS_NODE_TYPE = "additional_aovs"











#AdditionalAOVsFunctionality class
#------------------------------------------------------------------
class AdditionalAOVsFunctionality(object):
    """
    AdditionalAOVsFunctionality
    """


    def __new__(cls, *args, **kwargs):
        """
        AdditionalAOVsFunctionality instance factory.
        """

        #additional_aovs_functionality_instance
        additional_aovs_functionality_instance = super(AdditionalAOVsFunctionality, cls).__new__(cls, args, kwargs)

        return additional_aovs_functionality_instance

    
    def __init__(self,
                node = None,
                parm = None,
                logging_level = logging.DEBUG):
        """
        Customize instance.
        """

        #super
        self.parent_class = super(AdditionalAOVsFunctionality, self)
        self.parent_class.__init__()


        #logger
        #------------------------------------------------------------------
        
        #logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logging_level = logging_level
        self.logger.setLevel(self.logging_level)
        self.logger.handlers = []

        #status_handler
        self.status_handler = additional_aovs_functionality_logging_handler.PrintStreamHandler(self)
        self.logger.addHandler(self.status_handler)


        #instance variables
        #------------------------------------------------------------------
        
        #node
        self.node = node

        #parm
        self.parm = parm

        


        #init procedure
        #------------------------------------------------------------------

        





    #Methods
    #------------------------------------------------------------------

    def set_additional_aovs_parm(self):
        """
        Set additional aov parm.
        """


        #parm_tuple
        parm_tuple = self.parm.tuple()

        #parm_name
        parm_name = parm_tuple.name()

        #tuple_length
        tuple_length = len(parm_tuple)

        #value
        if(tuple_length < 2):
            value = parm_tuple.eval()[0]
        else:
            value = parm_tuple.eval()
        


        #iterate hda instances
        for hda_instance in self.get_node_instances():

            #parm_hda_instance
            parm_hda_instance = hda_instance.parm(parm_name)
            #tuple
            if not (parm_hda_instance):
                #parm_hda_instance
                parm_hda_instance = hda_instance.parmTuple(parm_name)

            #parm None
            if not (parm_hda_instance):
                #log
                self.logger.debug('{0} does not exist on {1}'.format(parm_name, hda_instance.path()))
                continue
            

            #set
            parm_hda_instance.set(value)

            #log
            self.logger.debug('{0}/{1}:{2}'.format(hda_instance.name(), parm_hda_instance.name(), value))


    

    #Utillity Methods
    #------------------------------------------------------------------

    def get_node_instances(self, type_name = ADDITIONAL_AOVS_NODE_TYPE):
        """
        Return list of all node instances in the scene with type type_name.
        """

        #node_type
        node_type = hou.nodeType(hou.vopNodeTypeCategory(), type_name)
        #check
        if not (node_type):
            #log
            self.logger.debug('Wrong node_type {0}. Could not set aov attributes.'.format(type_name))
            return []

        #node_instances_list
        node_instances_list = list(node_type.instances())

        #return
        return node_instances_list

    









    

#hdaModule
#------------------------------------------------------------------

def set_additional_aovs_parm(node, parm):
    """
    Set value of given parm on all instances of the additional_aovs HDA in the scene.
    """
    
    #node None
    if not (node):
        #log
        print('No node passed, not setting aov values.')
        return

    #parm None
    if not (parm):
        #log
        print('No parm passed, not setting aov values.')
        return

    
    #import
    from helga.houdini.rendering.additional_aovs_functionality import additional_aovs_functionality
    reload(additional_aovs_functionality)
    
    
    #additional_aovs_functionality_instance
    additional_aovs_functionality_instance = additional_aovs_functionality.AdditionalAOVsFunctionality(node = node, parm = parm)

    #set_additional_aov_parm
    additional_aovs_functionality_instance.set_additional_aovs_parm()


def set_all_aov_hda_instance_parms(node):
    """
    Set all AOV HDA instances in the scene to the values of this node.
    """

    #parm_list
    parm_list =  node.parms()

    #iterate and set
    for parm in parm_list:

        #import
        from helga.houdini.rendering.additional_aovs_functionality import additional_aovs_functionality
        reload(additional_aovs_functionality)

        #set
        additional_aovs_functionality.set_additional_aovs_parm(node, parm)








    







#Test
#------------------------------------------------------------------

if (__name__ == '__main__'):

    pass