
"""
create_manipulator_in_center
============================

Little helper module that does exactly what it states. It creates a manipulator and a joint
in the center of the selected object.
This module may be exposed as part of a general helper UI or used alone as is.

-----------------------

**Author:** `Timm Wagener <mailto:wagenertimm@gmail.com>`_
"""








#Import
#------------------------------------------------------------------
#python
import logging
#maya
import pymel.core as pm







#Globals
#------------------------------------------------------------------











#CreateManipulatorInCenter class
#------------------------------------------------------------------
class CreateManipulatorInCenter(object):
    """
    CreateManipulatorInCenter
    """

    
    def __new__(cls, *args, **kwargs):
        """
        CreateManipulatorInCenter instance factory.
        """

        #create_manipulator_in_center_instance
        create_manipulator_in_center_instance = super(CreateManipulatorInCenter, cls).__new__(cls, args, kwargs)

        return create_manipulator_in_center_instance

    
    def __init__(self, 
                logging_level = logging.DEBUG):
        """
        Customize instance.
        """


        #instance variables
        #------------------------------------------------------------------
        
        
        #logger
        #------------------------------------------------------------------
        #logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logging_level = logging_level
        self.logger.setLevel(self.logging_level)


        #Init procedure
        #------------------------------------------------------------------




    #Main Methods
    #------------------------------------------------------------------

    def run(self):
        """
        Create a manipulator in the center of the selected object.
        """

        #check
        if not (self.check()):

            #log
            self.logger.debug('Initial check failed. Not creating manipulator')
            return


        #selected_node
        selected_node = self.get_selected_node()

        #create_manipulator
        manipulator_node = self.create_manipulator(selected_node)

        #create_joint
        joint_node = self.create_joint(selected_node)

        #create_constraints
        self.create_constraints(manipulator_node, joint_node.getParent())

        #move_to_center
        self.move_to_center(selected_node, manipulator_node.getParent())



    #Methods
    #------------------------------------------------------------------

    def check(self):
        """
        Initial checks to prevent from some problems.
        This is not a guarantee for the procedure to run smoothly,
        but a big hint that it will.
        """

        #selected_node
        selected_node = self.get_selected_node()

        #check selected node exists
        if not (selected_node):

            #log
            self.logger.debug('Selected node is None.')
            return False

        
        #check if node is transform
        if not (pm.nodeType(selected_node) == 'transform'):

            #log
            self.logger.debug('Selected node {0} is not of type transform'.format(selected_node.name()))
            return False


        #return
        return True

    
    def get_selected_node(self):
        """
        Get the selected node or None
        """

        #selected_node_list
        selected_node_list = pm.ls(sl = True, fl = True)
        #check
        if not (selected_node_list):

            #log
            self.logger.debug('Selected node list empty or None')
            return

        try:
            #selected_node
            selected_node = selected_node_list[0]

        except:

            #log
            self.logger.debug('Selected node list has no first item')
            return

        #return valid
        return selected_node


    def create_manipulator(self, selected_node):
        """
        Create manipulator for given node.
        """

        #selected_node_name
        selected_node_name = selected_node.name()

        #grp_manipulator_node
        grp_manipulator_node = pm.group(em = True, n = 'grp_manip_{0}'.format(selected_node_name))
        pm.select(cl = True)

        #manipulator_node
        manipulator_node = pm.circle(nr=(0, 1, 0), c=(0, 0, 0), s = 32, ch = False, n = 'manip_{0}'.format(selected_node_name))[0]
        pm.select(cl = True)

        #parent
        pm.parent(manipulator_node, grp_manipulator_node)
        pm.select(cl = True)

        #return
        return manipulator_node


    def create_joint(self, selected_node):
        """
        Create joint for given node.
        """

        #selected_node_name
        selected_node_name = selected_node.name()

        #grp_joint_node
        grp_joint_node = pm.group(em = True, n = 'grp_jnt_{0}'.format(selected_node_name))
        pm.select(cl = True)

        #joint_node
        joint_node = pm.joint(n = 'jnt_{0}'.format(selected_node_name))
        pm.select(cl = True)

        #parent
        pm.parent(joint_node, grp_joint_node)
        pm.select(cl = True)

        #return
        return joint_node


    def create_constraints(self, master, slave):
        """
        Constrain the slave to the master with parent and scale constraints.
        """

        #parent_constraint
        parent_constraint = pm.parentConstraint(master, slave, mo = True, n = 'parent_con_{0}_to_{1}'.format(master.name(), slave.name()))
        pm.select(cl = True)

        #scale_constraint
        scale_constraint = pm.scaleConstraint(master, slave, mo = True, n = 'scale_con_{0}_to_{1}'.format(master.name(), slave.name()))
        pm.select(cl = True)


    def move_to_center(self, master, slave):
        """
        Move the slave to the center of the master.
        """

        #bbox_master
        bbox_master = master.getBoundingBox()

        #center_bbox_master
        center_bbox_master = bbox_master.center()

        #move
        slave.translate.set(center_bbox_master)