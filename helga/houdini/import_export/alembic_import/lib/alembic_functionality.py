

"""
alembic_functionality
==========================================

Module that provides general functions to be used with the alembic_import module.
Encapsulates Houdini and Alembic from alembic_import.
"""




#Import
#------------------------------------------------------------------
#python
import os
import logging
#houdini
import hou
import _alembic_hom_extensions as abc





#Import variable
do_reload = True


#alembic_import

#lib

#alembic_import_globals
from lib import alembic_import_globals
if(do_reload):reload(alembic_import_globals)

#alembic_import_logging_handler
from lib import alembic_import_logging_handler
if(do_reload):reload(alembic_import_logging_handler)






#AlembicFunctionality class
#------------------------------------------------------------------
class AlembicFunctionality(object):

    def __new__(cls, *args, **kwargs):
        """
        AlembicFunctionality instance factory.
        """

        #alembic_functionality_instance
        alembic_functionality_instance = super(AlembicFunctionality, cls).__new__(cls, args, kwargs)

        return alembic_functionality_instance

    
    def __init__(self, logging_level = logging.DEBUG):
        """
        Customize instance.
        """

        #super
        self.parent_class = super(AlembicFunctionality, self)
        self.parent_class.__init__()


        #instance variables
        #------------------------------------------------------------------

        

        
        #logger
        #------------------------------------------------------------------
        
        #logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logging_level = logging_level
        self.logger.setLevel(self.logging_level)
        self.logger.handlers = []

        #status_handler
        self.status_handler = alembic_import_logging_handler.PrintStreamHandler(self)
        self.logger.addHandler(self.status_handler)







    #Utility Methods
    #------------------------------------------------------------------

    




    #Houdini Utility Methods
    #------------------------------------------------------------------

    def get_network_boxes(self, parent_node):
        """
        Return list of network boxes that are children of parent_node.
        """

        return parent_node.networkBoxes()


    def remove_network_boxes(self, parent_node):
        """
        Get all network boxes that are children of node and remove them.
        The nodes inside the network boxes are not deleted, just
        reparented.
        """

        #network_boxes_list
        network_boxes_list = self.get_network_boxes(parent_node)

        #iterate
        for network_box_node in network_boxes_list:

            #delete
            network_box_node.destroy()


    def create_network_box(self, 
                            parent_node, 
                            child_node_list, 
                            network_box_name = None, 
                            position_x = 0,
                            position_y = 0):
        """
        Create network box with children and optional name.
        """

        #network_box_node
        network_box_node = parent_node.createNetworkBox(network_box_name)

        #layout children
        parent_node.layoutChildren(child_nodes = child_node_list)

        #add children
        for child_node in child_node_list:

            #add
            network_box_node.addNode(child_node)

        #fit
        network_box_node.fitAroundContents()

        #setPosition
        vec_position = hou.Vector2((position_x, position_y))
        network_box_node.setPosition(vec_position)


    
    def get_all_nodes(self):
        """
        Get list of all nodes in the scene.
        """

        #all_nodes_list
        all_nodes_list = hou.node("/").allSubChildren()

        return all_nodes_list

    
    def get_selected_nodes(self, verbose = False):
        """
        Get list of selected nodes.
        """

        #selected_nodes_list
        selected_nodes_list = hou.selectedNodes()

        #verbose
        if (verbose):

            #iterate and print name and type
            for selected_node in selected_nodes_list:

                print('{0} - {1}'.format(selected_node.name(), 
                                            selected_node.type().name()))
        
        #return
        return selected_nodes_list


    def get_selected_nodes_of_type(self, node_type = None):
        """
        Get list of selected Mantra nodes.
        """

        #node_type None
        if not (node_type):
            #log
            print('No node type given. Returning empty list')
            return []

        #selected_nodes_list
        selected_nodes_list = hou.selectedNodes()

        #matching_nodes_list
        matching_nodes_list = []

        #iterate and append
        for selected_node in selected_nodes_list:

            #selected_node_type
            selected_node_type = selected_node.type().name()

            #type matching
            if (selected_node_type == node_type):

                #append
                matching_nodes_list.append(selected_node)

        
        #return
        return matching_nodes_list


    def filter_node_list(self, node_list, node_type_filter_list):
        """
        Return list of nodes that match a node_type in node_type_filter_list
        """

        #node_list_filtered
        node_list_filtered = []

        #iterate and append
        for node in node_list:

            #match
            if (node.type().name() in node_type_filter_list):

                #append
                node_list_filtered.append(node)


        #return
        return node_list_filtered


    def get_children_of_type(self, parent_node = None, children_node_type = None):
        """
        Get list of children of type.
        """

        #parent_node None
        if not (parent_node):
            #log
            print('No parent node given. Returning empty list')
            return []

        #children_node_type None
        if not (children_node_type):
            #log
            print('No children node type given. Returning empty list')
            return []


        #children_list
        children_list = parent_node.children()

        #children_list empty
        if not (children_list):
            #log
            print('Children list for node {0} empty. Returning empty list'.format(parent_node.name()))
            return []

        #children_node_type_list
        children_node_type_list = []

        #iterate and append
        for child_node in children_list:
            
            #if type matches append
            if (child_node.type().name() == children_node_type):

                #append
                children_node_type_list.append(child_node)


        #return
        return children_node_type_list
    

    def delete_content(self, node):
        """
        Delete all children of node.
        """

        #Delete parent_node content
        for child in node.children():
            child.destroy()

        #remove network boxes
        self.remove_network_boxes(node)


    def get_parm_value(self, node, parm_name):
        """
        Return parm value for parm with parm_name on node.
        """

        #parm
        parm = node.parm(parm_name)
        #check
        if not (parm):
            #log
            self.logger.debug('Node {0} does not have a parm with name {1}. Returning None'.format(node.name(), parm_name))
            return None

        #return
        return parm.eval()

    
    #Alembic Utility Methods
    #------------------------------------------------------------------

    def get_alembic_hierarchy_tuple(self, alembic_path, object_path = '/'):
        """
        Return tuple of type (object_name, object_type, children).
        Each tuple represents an object exported with -root in the Alembic
        job args.
        """

        #path exists
        if not (os.path.isfile(alembic_path)):
            #log
            self.logger.debug('Alembic path does not exist. Returning empty tuple')
            return ()

        try:
            #alembic_hierarchy_tuple
            alembic_hierarchy_tuple = abc.alembicGetSceneHierarchy(alembic_path, object_path)

        except:
            #return empty tuple
            return ()

        return alembic_hierarchy_tuple


    def get_alembic_object_path_list(self, alembic_path):
        """
        Return list of object pathes.
        """

        try:
            #alembic_object_path_list
            alembic_object_path_list = abc.alembicGetObjectPathListForMenu(alembic_path)
            #remove duplicates and sort
            alembic_object_path_list = sorted(list(set(alembic_object_path_list)))

            #return
            return alembic_object_path_list

        except:
            
            pass
        
        return []


    def print_alembic_object_path_list(self, alembic_path):
        """
        Return list of object pathes.
        """

        #path exists
        if not (os.path.isfile(alembic_path)):
            #log
            self.logger.debug('Alembic path does not exist. Not printing object path list')
            return

        
        #object_path_list
        object_path_list = self.get_alembic_object_path_list(alembic_path)

        #iterate and get type
        for object_path in object_path_list:

            #object_type
            object_type = self.get_alembic_object_type(alembic_path, object_path)
            
            #log
            print('{0} | {1}'.format(object_path, object_type))


    def get_alembic_object_type(self, alembic_path, object_path):
        """
        Return object type of tuple (object_name, object_type, children).
        Returned result is object_tuple[1].
        Each tuple represents an object exported with -root in the Alembic
        job args.
        """

        #path exists
        if not (os.path.isfile(alembic_path)):
            #log
            self.logger.debug('Alembic path does not exist. Returning empty tuple')
            return None

        try:
            #alembic_hierarchy_tuple
            alembic_hierarchy_tuple = self.get_alembic_hierarchy_tuple(alembic_path, object_path)

        except:
            #log
            self.logger.debug('Error aquiring Alembic hierarchy tuple. Returning None')
            return None


        #object_type
        object_type = alembic_hierarchy_tuple[1]
        
        #return
        return object_type


    def alembic_attribute_exists(self, alembic_path, object_path, attribute_name):
        """
        For object at object_path in alembic from alembic_path check if attribute exists.
        """

        #path exists
        if not (os.path.isfile(alembic_path)):
            #log
            self.logger.debug('Alembic file at path does not exist. Returning None')
            return False

        #alembic_query_result
        alembic_query_result = abc.alembicArbGeometry(alembic_path, object_path, attribute_name, 0)

        #object exists
        if not (alembic_query_result):
            #log
            self.logger.debug('Object path inside Alembic file does not exist. Returning False')
            return False


        #scope
        scope = alembic_query_result[2]
        
        #attr unknown
        if (scope == 'unknown'):
            #log
            self.logger.debug('Attribute for Object path inside Alembic file does not exist. Returning False')
            return False

        #return
        return True


    def get_alembic_attribute_value(self, alembic_path, object_path, attribute_name):
        """
        For object at object_path in alembic from alembic_path get attribute value.
        """

        #check
        if not (self.alembic_attribute_exists(alembic_path, object_path, attribute_name)):
            #log
            self.logger.debug('Attribute {0} on alembic {1} at path {2} can not be retrieved. Returning None'.format(attribute_name,
                                                                                                                        alembic_path, 
                                                                                                                        object_path))
            return None

        #alembic_query_result
        alembic_query_result = abc.alembicArbGeometry(alembic_path, object_path, attribute_name, 0)

        #return
        return alembic_query_result[0]





    #Character Methods
    #------------------------------------------------------------------

    def create_geo_node(self, parent_node, node_name):
        """
        Create character geo node. This node is used to assign materials
        and contains an alembic sop node that points to the geoShape object. 
        """

        #geo_node
        geo_node = parent_node.createNode('geo', node_name)
        #delete_content
        self.delete_content(geo_node)

        return geo_node


    def create_character_alembic_node(self, parent_node, object_path):
        """
        Return parm value for parm with parm_name on node.
        """

        #object_shape_name
        object_shape_name = object_path.split('/')[-2]

        #alembic_node
        alembic_node = parent_node.createNode('alembic', object_shape_name)


        #set objectPath
        alembic_node_object_path = alembic_node.parm('objectPath')
        alembic_node_object_path.set(object_path)


        #return
        return alembic_node


    def create_character_time_blend_node(self, parent_node, alembic_node):
        """
        Append timeblend sop to alembic sop to interpolate
        at fractions of a frame for velocity motionblur.
        """

        #time_blend_node
        time_blend_node = parent_node.createNode('timeblend')

        #uncheck clamp at first frame
        parm_holdfirst = time_blend_node.parm('holdfirst')
        parm_holdfirst.set(False)

        #connect to alembic sop
        time_blend_node.setFirstInput(alembic_node)

        #return
        return time_blend_node


    def create_character_trail_node(self, parent_node, time_blend_node):
        """
        Append trail sop to add v point attr. for velocity motionblur.
        """

        #trail_node
        trail_node = parent_node.createNode('trail')

        #result
        parm_result = trail_node.parm('result')
        parm_result.set(3)

        #velapproximation
        parm_velapproximation = trail_node.parm('velapproximation')
        parm_velapproximation.set(1)

        #connect to time_blend sop
        trail_node.setFirstInput(time_blend_node)

        #return
        return trail_node


    def create_character_alembic_node_expressions(self, alembic_node, top_node):
        """
        Create expressions for character alembic sop node.
        The character alembic sop nodes tend to be controlled by
        the top_node to make sure changes ripple through.
        """

        #relative_path
        relative_path = alembic_node.relativePathTo(top_node)
        

        #parm_name
        parm_name = 'frame'
        #expression
        expression = 'ch("{0}/{1}")'.format(relative_path, parm_name)
        #parm
        parm = alembic_node.parm('frame')
        #set expression
        parm.setExpression(expression, language = hou.exprLanguage.Hscript)


        #parm_name
        parm_name = 'fps'
        #expression
        expression = 'ch("{0}/{1}")'.format(relative_path, parm_name)
        #parm
        parm = alembic_node.parm('fps')
        #set expression
        parm.setExpression(expression, language = hou.exprLanguage.Hscript)


        #parm_name
        parm_name = 'loadmode'
        #expression
        expression = 'ch("{0}/{1}")'.format(relative_path, parm_name)
        #parm
        parm = alembic_node.parm('loadmode')
        #set expression
        parm.setExpression(expression, language = hou.exprLanguage.Hscript)


        #parm_name
        parm_name = 'alembic_path'
        #expression
        expression = 'chs("{0}/{1}")'.format(relative_path, parm_name)
        #parm
        parm = alembic_node.parm('fileName')
        #set expression
        parm.setExpression(expression, language = hou.exprLanguage.Hscript)


    def create_character_velocity_motionblur_expressions(self, geo_node, trail_node, top_node):
        """
        Create expressions for velocity motionblur.
        This add the ability to enable and scale velocity
        motionblur. This only works if the alembic
        is imported as Houdini Geometry (default for
        character imports)
        """

        #trail_node_relative_path
        trail_node_relative_path = trail_node.relativePathTo(top_node)

        #geo_node_relative_path
        geo_node_relative_path = geo_node.relativePathTo(top_node)


        #trail_node expressions

        #parm_name
        parm_name = 'velscale'
        #expression
        expression = 'ch("{0}/{1}")'.format(trail_node_relative_path, parm_name)
        #parm
        parm = trail_node.parm('velscale')
        #set expression
        parm.setExpression(expression, language = hou.exprLanguage.Hscript)



        #geo_node expressions

        #parm_name
        parm_name = 'geo_velocityblur'
        #expression
        expression = 'ch("{0}/{1}")'.format(geo_node_relative_path, parm_name)
        #parm
        parm = geo_node.parm('geo_velocityblur')
        #set expression
        parm.setExpression(expression, language = hou.exprLanguage.Hscript)

    
    def create_char(self, parent_node):
        """
        Create a character hierarchy according to our pipeline standards.
        This method expects an Alembic based on the Helga character standard,
        and might give undesired results on mismatch.

        The expected Alembic format is plain flat:
        root -> geo_1 -> geo_1_shape, geo_2 -> geo_2_shape, geo_3 -> geo_3_shape, geo_4 -> geo_4_shape...

        Minimal error checking is performed at this stage.

        ----------------------------------

        Future improvements could be to check for attributes to automate
        grouping in netboxes.
        """

        #delete_content
        self.delete_content(parent_node)
        #log
        self.logger.debug('Content of {0} deleted'.format(parent_node.path()))

        
        #alembic_path
        alembic_path = self.get_parm_value(parent_node, 'alembic_path')

        #object_path_list
        object_path_list = self.get_alembic_object_path_list(alembic_path)
        

        #iterate and get type
        for object_path in object_path_list:

            #object_type
            object_type = self.get_alembic_object_type(alembic_path, object_path)
            
            #if object_type == polymesh create geometry and alembic sop
            if (object_type == 'polymesh'):

                #object_transform_name
                object_transform_name = object_path.split('/')[1]

                #log
                self.logger.debug('Create geo node {0}'.format(object_transform_name))

                
                
                #geo_node
                geo_node = self.create_geo_node(parent_node, object_transform_name)
                
                #alembic_node
                alembic_node = self.create_character_alembic_node(geo_node, object_path)

                #time_blend_node
                time_blend_node = self.create_character_time_blend_node(geo_node, alembic_node)

                #trail_node
                trail_node = self.create_character_trail_node(geo_node, time_blend_node)
                trail_node.setDisplayFlag(True)
                trail_node.setRenderFlag(True)



                #create alembic expressions
                self.create_character_alembic_node_expressions(alembic_node, parent_node)

                #create velocity motionblur expressions
                self.create_character_velocity_motionblur_expressions(geo_node, trail_node, parent_node)

                #layout children geo node
                geo_node.layoutChildren()



        #layout children
        parent_node.layoutChildren()



    #Shot/Prop Highpoly Methods
    #------------------------------------------------------------------

    def create_prop_highpoly_rendergeo_nodes(self,
                                                parent_node,
                                                object_path, 
                                                alembic_path, 
                                                highpoly_rendergeo_path):
        """
        Create prop highpoly rendergeo node network.
        """

        #alembic_file_name
        alembic_file_name = os.path.splitext(os.path.basename(alembic_path))[0]

        #locator_geo_node
        locator_geo_node = self.create_locator_geo_node(parent_node, alembic_file_name)
        locator_geo_node.setDisplayFlag(False)
        locator_geo_node.moveToGoodPosition()

        #locator_alembic_node
        locator_alembic_node = self.create_locator_alembic_node(locator_geo_node, alembic_path, object_path)

        #create_locator_geo_node_expressions
        self.create_locator_geo_node_expressions(locator_geo_node, locator_alembic_node)


        #geo_node
        geo_node_name = alembic_file_name.replace('_locator', '')
        geo_node = self.create_geo_node(parent_node, geo_node_name)
        geo_node.moveToGoodPosition()

        #alembic_node
        alembic_node = self.create_prop_highpoly_rendergeo_alembic_node(geo_node, highpoly_rendergeo_path, node_name = geo_node.name())


        #connect
        geo_node.setFirstInput(locator_geo_node)


    def create_locator_geo_node(self, parent_node, node_name):
        """
        Create locator geo node. This node is used to assign materials
        and contains an alembic sop node that points to the geoShape object. 
        """

        #geo_node
        geo_node = parent_node.createNode('geo', node_name)
        #delete_content
        self.delete_content(geo_node)

        return geo_node


    def create_locator_alembic_node(self, parent_node, alembic_path, object_path):
        """
        Return parm value for parm with parm_name on node.
        """

        #object_shape_name
        object_shape_name = object_path.split('/')[-1]

        #alembic_node
        alembic_node = parent_node.createNode('alembic', object_shape_name)


        #set loadmode
        parm_loadmode = alembic_node.parm('loadmode')
        parm_loadmode.set(1)

        #set loadLocator
        parm_load_locator = alembic_node.parm('loadLocator')
        parm_load_locator.set(True)

        #set fileName
        parm_file_name = alembic_node.parm('fileName')
        parm_file_name.set(alembic_path)
        

        #return
        return alembic_node


    def create_locator_geo_node_expressions(self, locator_geo_node, locator_alembic_node):
        """
        Return parm value for parm with parm_name on node.
        """
        
        #tx
        #expression
        expression = 'prim("{0}", 0, "parentTrans", 0)'.format(locator_alembic_node.name())
        #parm
        parm = locator_geo_node.parm('tx')
        #set expression
        parm.setExpression(expression, language = hou.exprLanguage.Hscript)

        #ty
        #expression
        expression = 'prim("{0}", 0, "parentTrans", 1)'.format(locator_alembic_node.name())
        #parm
        parm = locator_geo_node.parm('ty')
        #set expression
        parm.setExpression(expression, language = hou.exprLanguage.Hscript)

        #tz
        #expression
        expression = 'prim("{0}", 0, "parentTrans", 2)'.format(locator_alembic_node.name())
        #parm
        parm = locator_geo_node.parm('tz')
        #set expression
        parm.setExpression(expression, language = hou.exprLanguage.Hscript)



        #rx
        #expression
        expression = 'deg(prim("{0}", 0, "parentRot", 0))'.format(locator_alembic_node.name())
        #parm
        parm = locator_geo_node.parm('rx')
        #set expression
        parm.setExpression(expression, language = hou.exprLanguage.Hscript)

        #ry
        #expression
        expression = 'deg(prim("{0}", 0, "parentRot", 1))'.format(locator_alembic_node.name())
        #parm
        parm = locator_geo_node.parm('ry')
        #set expression
        parm.setExpression(expression, language = hou.exprLanguage.Hscript)

        #rz
        #expression
        expression = 'deg(prim("{0}", 0, "parentRot", 2))'.format(locator_alembic_node.name())
        #parm
        parm = locator_geo_node.parm('rz')
        #set expression
        parm.setExpression(expression, language = hou.exprLanguage.Hscript)


        
        #sx
        #expression
        expression = 'prim("{0}", 0, "parentScale", 0)'.format(locator_alembic_node.name())
        #parm
        parm = locator_geo_node.parm('sx')
        #set expression
        parm.setExpression(expression, language = hou.exprLanguage.Hscript)

        #sy
        #expression
        expression = 'prim("{0}", 0, "parentScale", 1)'.format(locator_alembic_node.name())
        #parm
        parm = locator_geo_node.parm('sy')
        #set expression
        parm.setExpression(expression, language = hou.exprLanguage.Hscript)

        #sz
        #expression
        expression = 'prim("{0}", 0, "parentScale", 2)'.format(locator_alembic_node.name())
        #parm
        parm = locator_geo_node.parm('sz')
        #set expression
        parm.setExpression(expression, language = hou.exprLanguage.Hscript)


    def create_prop_highpoly_rendergeo_alembic_node(self, parent_node, alembic_path, node_name = 'unknown'):
        """
        Return parm value for parm with parm_name on node.
        """

        #alembic_node
        alembic_node = parent_node.createNode('alembic', node_name)


        #set viewportlod
        parm_viewportlod = alembic_node.parm('viewportlod')
        parm_viewportlod.set(2)

        #set fileName
        parm_file_name = alembic_node.parm('fileName')
        parm_file_name.set(alembic_path)

        #return
        return alembic_node


    def check_prop_highpoly_rendergeo(self, object_path, alembic_path, alembic_highpoly_rendergeo_dir):
        """
        Check the data needed for building a highpoly rendergeo alembic prop in Houdini.
        Return false if the needed data is insufficient or the needed data if True.
        The returned data is in the form of [highpoly_rendergeo_path].
        This should be all the data needed to build a prop.
        """
        
        #alembic_file_name
        alembic_file_name = os.path.splitext(os.path.basename(alembic_path))[0]
        #alembic_file_name empty
        if not (alembic_file_name):
            #log
            self.logger.debug('Could not aquire Alembic file name for path {0}.'.format(alembic_path))
            return False


        #helga_locator_attr_exists
        helga_locator_attr_exists = self.alembic_attribute_exists(alembic_path, object_path, 'helga_locator')
        #check attribute
        if not (helga_locator_attr_exists):
            #log
            self.logger.debug('helga_locator attribute could not be aquired for {0}. Not creating prop'.format(object_path))
            return False
        

        #helga_highpoly_rendergeo_attr
        helga_highpoly_rendergeo_attr = self.get_alembic_attribute_value(alembic_path, object_path, 'helga_highpoly_rendergeo')
        #check attribute
        if not (helga_highpoly_rendergeo_attr):
            #log
            self.logger.debug('helga_highpoly_rendergeo attribute could not be aquired for {0}. Not creating prop'.format(object_path))
            return False

        
        #helga_highpoly_rendergeo_value
        helga_highpoly_rendergeo_value = helga_highpoly_rendergeo_attr[0]

        #highpoly_rendergeo_path
        highpoly_rendergeo_path = os.path.join(alembic_highpoly_rendergeo_dir, helga_highpoly_rendergeo_value + '.abc')
        #check highpoly_rendergeo_path
        if not (os.path.isfile(highpoly_rendergeo_path)):
            #log
            self.logger.debug('Highpoly rendergeo at path {0} does not exist. Not creating prop'.format(highpoly_rendergeo_path))
            return False

        

        #return
        return [highpoly_rendergeo_path]


    def create_prop_highpoly_rendergeo(self, 
                                        parent_node, 
                                        alembic_path, 
                                        alembic_highpoly_rendergeo_dir):
        """
        Create a prop hierarchy according to our pipeline standards.
        """
        
        #object_path_list
        object_path_list = self.get_alembic_object_path_list(alembic_path)
        #object_path_list empty
        if not (object_path_list):
            #log
            self.logger.debug('Object path list for alembic {0} empty. Not creating prop, returning None'.format(alembic_path))
            return False


        #iterate, check and create
        for object_path in object_path_list:

            #log
            self.logger.debug('\n\n-------------------------\n{0}\n-------------------------\n\n'.format(object_path))

            #check
            if not (self.check_prop_highpoly_rendergeo(object_path, alembic_path, alembic_highpoly_rendergeo_dir)):
                #log
                self.logger.debug('Prop highpoly rendergeo check failed for {0}. Not building prop.'.format(object_path))
                continue

            #highpoly_rendergeo_path
            highpoly_rendergeo_path = self.check_prop_highpoly_rendergeo(object_path, 
                                                                            alembic_path, 
                                                                            alembic_highpoly_rendergeo_dir)[0]


            #create_prop_highpoly_rendergeo_nodes
            self.create_prop_highpoly_rendergeo_nodes(parent_node,
                                                        object_path, 
                                                        alembic_path, 
                                                        highpoly_rendergeo_path)


    #Shot/Prop Proxy Methods
    #------------------------------------------------------------------

    def create_prop_proxy_nodes(self, parent_node, alembic_path):
        """
        Create prop proxy node.
        """

        #alembic_file_name
        alembic_file_name = os.path.splitext(os.path.basename(alembic_path))[0]

        #geo_node
        geo_node = self.create_geo_node(parent_node, alembic_file_name)

        #alembic_node
        alembic_node = self.create_prop_proxy_alembic_node(geo_node, alembic_path)

        #create expressions
        self.create_prop_proxy_alembic_node_expressions(alembic_node, parent_node)


    def create_prop_proxy_alembic_node(self, parent_node, alembic_path):
        """
        Create Alembic node specifically for prop proxy.
        """

        #alembic_node
        alembic_node = parent_node.createNode('alembic', parent_node.name())

        #set fileName
        parm_file_name = alembic_node.parm('fileName')
        parm_file_name.set(alembic_path)

        #return
        return alembic_node


    def create_prop_proxy_alembic_node_expressions(self, alembic_node, top_node):
        """
        Create expressions for prop proxy alembic sop node.
        The character alembic sop nodes tend to be controlled by
        the top_node to make sure changes ripple through.
        """

        #relative_path
        relative_path = alembic_node.relativePathTo(top_node)
        

        #parm_name
        parm_name = 'frame'
        #expression
        expression = 'ch("{0}/{1}")'.format(relative_path, parm_name)
        #parm
        parm = alembic_node.parm('frame')
        #set expression
        parm.setExpression(expression, language = hou.exprLanguage.Hscript)


        #parm_name
        parm_name = 'fps'
        #expression
        expression = 'ch("{0}/{1}")'.format(relative_path, parm_name)
        #parm
        parm = alembic_node.parm('fps')
        #set expression
        parm.setExpression(expression, language = hou.exprLanguage.Hscript)


        #parm_name
        parm_name = 'loadmode'
        #expression
        expression = 'ch("{0}/{1}")'.format(relative_path, parm_name)
        #parm
        parm = alembic_node.parm('loadmode')
        #set expression
        parm.setExpression(expression, language = hou.exprLanguage.Hscript)


    def check_prop_proxy(self, alembic_path):
        """
        Check the data needed for building a proxy alembic prop in Houdini.
        Return false if the needed data is insufficient or the needed data if True.
        The returned data is in the form of [alembic_path].
        This should be all the data needed to build a prop.
        """
        
        #alembic_file_name
        alembic_file_name = os.path.splitext(os.path.basename(alembic_path))[0]
        #alembic_file_name empty
        if not (alembic_file_name):
            #log
            self.logger.debug('Could not aquire Alembic file name for path {0}.'.format(alembic_path))
            return False


        #object_path_list
        object_path_list = self.get_alembic_object_path_list(alembic_path)
        #object_path_list empty
        if not (object_path_list):
            #log
            self.logger.debug('Object path list for alembic {0} empty.'.format(alembic_path))
            return False
        

        #helga_proxy_attr_exists
        helga_proxy_attr_exists = False
        
        #iterate and check
        for object_path in object_path_list:
            
            #helga_proxy_attr
            helga_proxy_attr = self.alembic_attribute_exists(alembic_path, object_path, 'helga_proxy')
            
            #if True then break
            if (helga_proxy_attr):

                #set helga_proxy_attr_exists
                helga_proxy_attr_exists = True
                break

        #helga_proxy_attr_exists false
        if not (helga_proxy_attr_exists):
            #log
            self.logger.debug('Alembic has no helga_proxy attribute.'.format(alembic_path))
            return False

        
        #return
        return [alembic_path]


    def create_prop_proxy(self, 
                            parent_node, 
                            alembic_path):
        """
        Create a prop hierarchy according to our pipeline standards.
        """
        
        #check
        if not (self.check_prop_proxy(alembic_path)):
            #log
            self.logger.debug('Prop proxy check failed. Not creating prop')
            return

        #create
        self.create_prop_proxy_nodes(parent_node, alembic_path)

            



