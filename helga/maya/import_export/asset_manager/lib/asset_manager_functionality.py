

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





#Import variable
do_reload = True


#asset_manager

#lib

#asset_manager_checks
from lib import asset_manager_checks
if(do_reload):reload(asset_manager_checks)






#AssetManagerFunctionality class
#------------------------------------------------------------------
class AssetManagerFunctionality(QtCore.QObject):

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

        #checks_functionality
        self.checks_functionality = asset_manager_checks.AssetManagerChecks()

        
        #logger
        #------------------------------------------------------------------
        #logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logging_level = logging_level
        self.logger.setLevel(self.logging_level)




    #Maya
    #------------------------------------------------------------------

    def plugin_loaded(self, plugin_name):
        """
        Check if plugin is loaded.
        """

        pass


    def save_scene(self):
        """
        Save scene.
        """

        #save
        pm.saveFile(force = True)

        #log
        self.logger.debug('Scene saved to: {0}'.format(self.get_maya_file()))


    def object_exists(self, pynode):
        """
        Check if the mobject that a pynode refers to
        still exists in the scene.
        """

        try:
            pm.PyNode(pynode.name())
            return True
        except:
            pass

        return False


    def get_maya_file(self):
        """
        Return path + name + extension of current maya file.
        """

        #maya_file
        maya_file = str(pm.system.sceneName())

        return maya_file


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


    def get_nodes_with_namespace_and_attr(self, pynode_list, attr_name):
        """
        Select nodes with a certain namespace
        that have given attribute.
        A namespace is mandatory. Operation will fail if
        namespace of node in pynode_list is empty.
        """

        #convert to list if not
        if not (type(pynode_list) is list):
            pynode_list = [pynode_list]

        #node_selection_list
        node_selection_list = []

        #iterate
        for pynode in pynode_list:

            #namespace
            namespace = pynode.namespace()
            #check
            if not (namespace):
                #log
                self.logger.debug('Node {0} does not have a namespace. Continuing'.format(pynode.name()))
                continue

            #namespace_node_list
            namespace_node_list = pm.namespaceInfo(namespace, lod = True, recurse = True)
            #check
            if not (namespace_node_list):
                #log
                self.logger.debug('Namespace node list for namespace: {0} and node {1} empty. Continuing'.format(namespace, pynode.name()))
                continue


            #append to node_selection_list
            node_selection_list += [namespace_node for
                                    namespace_node in 
                                    namespace_node_list if
                                    namespace_node.hasAttr(attr_name)]

        #return
        return node_selection_list


    def select_nodes_with_namespace_and_attr(self, pynode_list, attr_name):
        """
        Select nodes with a certain namespace
        that have given attribute.
        """

        #clear
        pm.select(cl = True)

        #node_list
        node_list = self.get_nodes_with_namespace_and_attr(pynode_list, attr_name)
        #check
        if not (node_list):
            #log
            self.logger.debug('Node list empty. No nodes to select.')
            return

        #select
        pm.select(node_list, r = True)


    def set_visibility_on_nodes_with_namespace_and_attr(self, pynode_list, attr_name, visibility = True):
        """
        Set visibility attr. on nodes with namespace and given
        attr. name to passed visibility parm.
        """

        #node_list
        node_list = self.get_nodes_with_namespace_and_attr(pynode_list, attr_name)
        #check
        if not (node_list):
            #log
            self.logger.debug('Node list empty. No nodes to set visibility on.')
            return

        
        #iterate
        for pynode in node_list:

            try:
                
                #check for visibility attr.
                if (pynode.hasAttr('visibility')):

                    #set
                    pynode.visibility.set(visibility)

                else:

                    #log
                    self.logger.debug('Node {0} doesnt have visibility attribute'.format(pynode.name()))

            except:

                #log
                self.logger.debug('Error setting visibility attribute on node {0}'.format(pynode.name()))


        

    
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










    #Attributes
    #------------------------------------------------------------------

    def add_attribute_to_node(self, node, attribute_name, attribute_type):
        """
        Add attribute to pynode and log success.
        """

        #check if attr already exists
        if (node.hasAttr(attribute_name)):
            
            #log
            self.logger.debug('Node {0} already has attr. {1}. Not adding attribute.'.format(node.name(), attribute_name))
            return

        try:
            
            #attribute_type string
            if (attribute_type == 'string'):
                
                #add
                node.addAttr(attribute_name, 
                                dt = attribute_type)

            #all other types
            else:
                
                #add
                node.addAttr(attribute_name, 
                                attributeType = attribute_type)

            #log
            self.logger.debug('Added attr: {0} to node {1}'.format(attribute_name,
                                                                    node.name()))

        except:

            #log
            self.logger.debug('Addition of attr: {0} to node {1} failed'.format(attribute_name,
                                                                                node.name()))


    def remove_attribute_from_node(self, node, attribute_name):
        """
        Add attribute to pynode and log success.
        """

        #check if attr exists on node
        if not(node.hasAttr(attribute_name)):
            
            #log
            self.logger.debug('Node {0} does not have attr. {1}. Not removing attribute.'.format(node.name(), attribute_name))
            return

        try:
            
            #remove
            pm.deleteAttr(node, attribute = attribute_name)

            #log
            self.logger.debug('Removed attr: {0} from node {1}'.format(attribute_name,
                                                                    node.name()))

        except:

            #log
            self.logger.debug('Removing of attr: {0} from node {1} failed'.format(attribute_name,
                                                                                node.name()))


    def add_attribute_to_selected_nodes(self, 
                                        attribute_name, 
                                        node_type_name, 
                                        shape_node_type_name = None,
                                        attribute_type = 'bool'):
        """
        Check if attribute_name not on nodes of selection and if so, add it.
        Only consider selected nodes of type node_type_name that have
        a shape of type shape_node_type_name. If shape_node_type_name is None
        dont perform shape check, directly use selected nodes of type node_type_name.
        The shape_node_type_name attribute here is what you get when you do type(object).__name__.
        It is NOT the type asked for by the et flag from the pm.sl() cmd.

        In short:
        1. node_type_name = pm.ls(et = node_type_name)
        2. shape_node_type_name = type(object).__name__ == shape_node_type_name
        """

        #node_list
        node_list = self.get_nodes_of_type(node_type_name, selection = True)
        #node_list empty
        if not(node_list):
            #log
            self.logger.debug('Node list empty.')
            return

        #check node list
        if not(self.checks_functionality.check_node_list_for_attribute_addition_or_removal(node_list, shape_node_type_name)):
            #log
            self.logger.debug('Not adding attributes.')
            return

        #checked_node_list
        checked_node_list = self.checks_functionality.check_node_list_for_attribute_addition_or_removal(node_list, shape_node_type_name)

        
        #iterate
        for node in checked_node_list:

            #add
            self.add_attribute_to_node(node, attribute_name, attribute_type)

            
    def remove_attribute_from_selected_nodes(self, 
                                                attribute_name, 
                                                node_type_name, 
                                                shape_node_type_name = None):
        """
        Check if attribute_name on nodes of selection and if so, remove it.
        Only consider selected nodes of type node_type_name that have
        a shape of type shape_node_type_name. If shape_node_type_name is None
        dont perform shape check, directly use selected nodes of type node_type_name.
        The shape_node_type_name attribute here is what you get when you do type(object).__name__.
        It is NOT the type asked for by the et flag from the pm.sl() cmd.

        In short:
        1. node_type_name = pm.ls(et = node_type_name)
        2. shape_node_type_name = type(object).__name__ == shape_node_type_name
        """

        #node_list
        node_list = self.get_nodes_of_type(node_type_name, selection = True)
        #node_list empty
        if not(node_list):
            #log
            self.logger.debug('Node list empty.')
            return

        #check node list
        if not(self.checks_functionality.check_node_list_for_attribute_addition_or_removal(node_list, shape_node_type_name)):
            #log
            self.logger.debug('Not removing attributes.')
            return

        #checked_node_list
        checked_node_list = self.checks_functionality.check_node_list_for_attribute_addition_or_removal(node_list, shape_node_type_name)

        
        #iterate
        for node in checked_node_list:

            #remove
            self.remove_attribute_from_node(node, attribute_name)


    def add_locator_attributes_to_selected_nodes(self,
                                                    node_type_name, 
                                                    shape_node_type_name = None):
        """
        Add helga locator attributes to selected nodes.
        The attributes for helga locator nodes are:

        #. helga_locator:bool
        #. helga_highpoly_rendergeo:string
        """

        #node_list
        node_list = self.get_nodes_of_type(node_type_name, selection = True)
        #node_list empty
        if not(node_list):
            #log
            self.logger.debug('Node list empty.')
            return

        #check node list
        if not(self.checks_functionality.check_node_list_for_attribute_addition_or_removal(node_list, shape_node_type_name)):
            #log
            self.logger.debug('Not adding attributes.')
            return

        #checked_node_list
        checked_node_list = self.checks_functionality.check_node_list_for_attribute_addition_or_removal(node_list, shape_node_type_name)

        
        #iterate
        for node in checked_node_list:

            #helga_locator
            self.add_attribute_to_node(node, 'helga_locator', 'bool')

            #helga_highpoly_rendergeo
            self.add_attribute_to_node(node, 'helga_highpoly_rendergeo', 'string')









    #Asset preparation
    #------------------------------------------------------------------

    @QtCore.Slot(str)
    def create_prop_base_setup(self, asset_name = 'example_asset'):
        """
        This is a convenience function to create the base setup for the prop assets
        in a consistent way (Groups, manips, locator).
        """

        #Locator error check
        #------------------------------------------------------------------

        if (pm.objExists('loc_{0}'.format(asset_name))):

            #log
            self.logger.debug('Locator of name {0} already exists. PyMEL will throw an error if the locator has the same name.\
\nPlease rename the prop. Not creating asset base setup.'.format('loc_{0}'.format(asset_name)))

            return


        #Create groups
        #------------------------------------------------------------------
        
        #grp_geo
        pm.select(cl = True)
        grp_geo = pm.group(name = 'grp_geo', empty = True)
        pm.select(cl = True)

        
        #grp_asset
        pm.select(cl = True)
        grp_asset = pm.group(name = 'grp_asset', empty = True)
        pm.select(cl = True)
        pm.parent(grp_asset, grp_geo)
        pm.select(cl = True)

        #grp_proxy
        pm.select(cl = True)
        grp_proxy = pm.group(name = 'grp_proxy', empty = True)
        pm.select(cl = True)
        pm.parent(grp_proxy, grp_geo)
        pm.select(cl = True)


        
        #grp_rig
        pm.select(cl = True)
        grp_rig = pm.group(name = 'grp_rig', empty = True)
        pm.select(cl = True)

        #grp_manips
        pm.select(cl = True)
        grp_manips = pm.group(name = 'grp_manips', empty = True)
        pm.select(cl = True)
        pm.parent(grp_manips, grp_rig)
        pm.select(cl = True)

        #grp_joints
        pm.select(cl = True)
        grp_joints = pm.group(name = 'grp_joints', empty = True)
        pm.select(cl = True)
        pm.parent(grp_joints, grp_rig)
        pm.select(cl = True)

        #grp_nodes
        pm.select(cl = True)
        grp_nodes = pm.group(name = 'grp_nodes', empty = True)
        pm.select(cl = True)
        pm.parent(grp_nodes, grp_rig)
        pm.select(cl = True)



        #Create manipulator
        #------------------------------------------------------------------

        #grp_manip_asset
        pm.select(cl = True)
        grp_manip_asset = pm.group(name = 'grp_manip_{0}'.format(asset_name), empty = True)
        pm.select(cl = True)
        pm.parent(grp_manip_asset, grp_manips)
        pm.select(cl = True)

        #manip_asset
        manip_asset = pm.circle(name = 'manip_{0}'.format(asset_name) , nr = (0,1,0), s = 16, ch = False)[0]
        pm.select(cl = True)
        pm.parent(manip_asset, grp_manip_asset)
        pm.select(cl = True)



        #Create joint
        #------------------------------------------------------------------

        #grp_joint_asset
        pm.select(cl = True)
        grp_joint_asset = pm.group(name = 'grp_joint_{0}'.format(asset_name), empty = True)
        pm.select(cl = True)
        pm.parent(grp_joint_asset, grp_joints)
        pm.select(cl = True)

        #joint_asset
        joint_asset = pm.joint(name = 'jnt_{0}'.format(asset_name))
        pm.select(cl = True)
        pm.parent(joint_asset, grp_joint_asset)
        pm.select(cl = True)



        #Create locator
        #------------------------------------------------------------------

        #grp_locator_asset
        pm.select(cl = True)
        grp_locator_asset = pm.group(name = 'grp_loc_{0}'.format(asset_name), empty = True)
        pm.select(cl = True)
        pm.parent(grp_locator_asset, grp_nodes)
        pm.select(cl = True)

        #locator_asset
        locator_asset = pm.spaceLocator(name = 'loc_{0}'.format(asset_name))
        pm.select(cl = True)
        pm.parent(locator_asset, grp_locator_asset)
        pm.select(cl = True)




        #Create constraints
        #------------------------------------------------------------------

        #pc_manip_to_grp_jnt
        pm.select(cl = True)
        pc_manip_to_grp_jnt = pm.parentConstraint(manip_asset, grp_joint_asset, mo = True)
        pm.select(cl = True)

        #sc_manip_to_grp_jnt
        pm.select(cl = True)
        sc_manip_to_grp_jnt = pm.scaleConstraint(manip_asset, grp_joint_asset, mo = True)
        pm.select(cl = True)


        #pc_manip_to_grp_loc
        pm.select(cl = True)
        pc_manip_to_grp_loc = pm.parentConstraint(manip_asset, grp_locator_asset, mo = True)
        pm.select(cl = True)

        #sc_manip_to_grp_loc
        pm.select(cl = True)
        sc_manip_to_grp_loc = pm.scaleConstraint(manip_asset, grp_locator_asset, mo = True)
        pm.select(cl = True)


