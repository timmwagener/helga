

"""
helga_rig_functionality
==========================================

Rig helper functionality. This module separates the functionality of interacting with the Helga rigs
from any UI. It encompasses functions used with Maya modules.
There is no import of PySide in here. All UI tools that let you work with
the rigs import this module.
"""




#Import
#------------------------------------------------------------------
#python
import sys
import os
import logging
#maya
import pymel.core as pm



#Import variable
do_reload = True

#helga

#global_variables
from helga.general.setup.global_variables import global_variables
if(do_reload):reload(global_variables)

#global_functions
from helga.general.setup.global_functions import global_functions
if(do_reload):reload(global_functions)


#helga_rig_functionality

#helga_rig_globals
import helga_rig_globals as helga_rig_globals
if(do_reload): reload(helga_rig_globals)






#Globals
#------------------------------------------------------------------









#HelgaRigFunctionality class
#------------------------------------------------------------------
class HelgaRigFunctionality(object):
    """
    Class that exposes functionality to interact programmaticaly with the rigs.
    """
    
    def __init__(self, 
                    namespace = None, 
                    logging_level = logging.DEBUG):
        """
        Customize instance.
        """

        #super
        self.parent_class = super(HelgaRigFunctionality, self)
        self.parent_class.__init__()


        #instance variables
        #------------------------------------------------------------------

        #namespace
        self.namespace = namespace

        
        #logger
        #------------------------------------------------------------------
        #logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logging_level = logging_level
        self.logger.setLevel(self.logging_level)




    #Methods
    #------------------------------------------------------------------

    def reset_rig(self, namespace = None):
        """
        Reset the rig to T-Pose and complete factory defaults.
        If you set a keyframe after this, you have the valid preroll
        T-Pose.
        """
        
        #namespace from module
        if not (namespace):
            namespace = self.namespace

        pass

    
    def get_all_manipulators(self, namespace = None):
        """
        Return a dictionary with the following form:

        {manipulator_name : {attribute_name : attribute_value,
                                attribute_name : attribute_value,
                                attribute_name : attribute_value},
        manipulator_name : {attribute_name : attribute_value,
                                attribute_name : attribute_value,
                                attribute_name : attribute_value}
        }

        manipulator_name: Every manipulator for the rig of the given namespace.
        attribute_name: Each keyframeable attribute of the manipulator ('translateX', 'scaleY' ...).
        attribute_value: The factory default (T-Pose) value.
        """
        
        #namespace from module
        if not (namespace):
            namespace = self.namespace

        pass


    def get_dynamics_manipulators(self, namespace = None):
        """
        Same as above, but this time only return dictionary for manipulators
        that control dynamics attributes.
        """
        
        #namespace from module
        if not (namespace):
            namespace = self.namespace

        pass



    #Getter & Setter
    #------------------------------------------------------------------

    def set_namespace(self, namespace):
        """
        Set self.namespace
        """

        self.namespace = namespace

    
    def get_namespace(self):
        """
        Get self.namespace
        """

        return self.namespace