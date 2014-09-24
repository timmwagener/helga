

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

    def delete_content(self, node):
        """
        Delete all children of node.
        """

        #Delete parent_node content
        for child in node.children():
            child.destroy()


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
        Return tuple of type (object_name, object_type, children).
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


    def create_character_alembic_node(self, top_node, parent_node, alembic_path, object_path):
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


        #create expressions
        self.create_character_alembic_node_expressions(alembic_node, top_node)


        #return
        return alembic_node


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
                alembic_node = self.create_character_alembic_node(parent_node, geo_node, alembic_path, object_path)



        #layout children
        parent_node.layoutChildren()



    #Shot/Prop Highpoly Methods
    #------------------------------------------------------------------

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
        expression = 'prim("{0}", 0, "parentRot", 0)'.format(locator_alembic_node.name())
        #parm
        parm = locator_geo_node.parm('rx')
        #set expression
        parm.setExpression(expression, language = hou.exprLanguage.Hscript)

        #ry
        #expression
        expression = 'prim("{0}", 0, "parentRot", 1)'.format(locator_alembic_node.name())
        #parm
        parm = locator_geo_node.parm('ry')
        #set expression
        parm.setExpression(expression, language = hou.exprLanguage.Hscript)

        #rz
        #expression
        expression = 'prim("{0}", 0, "parentRot", 2)'.format(locator_alembic_node.name())
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


    def create_prop_highpoly_rendergeo_alembic_node(self, parent_node, alembic_path):
        """
        Return parm value for parm with parm_name on node.
        """

        #alembic_node
        alembic_node = parent_node.createNode('alembic', 'test')


        #set viewportlod
        parm_viewportlod = alembic_node.parm('viewportlod')
        parm_viewportlod.set(2)

        #set fileName
        parm_file_name = alembic_node.parm('fileName')
        parm_file_name.set(alembic_path)

        #return
        return alembic_node

    
    def create_prop_highpoly_rendergeo(self, parent_node):
        """
        Create a prop hierarchy according to our pipeline standards.
        """

        #alembic_path
        alembic_path = self.get_parm_value(parent_node, 'alembic_path')

        #alembic_file_name
        alembic_file_name = os.path.splitext(os.path.basename(alembic_path))[0]

        #alembic_highpoly_rendergeo_dir
        alembic_highpoly_rendergeo_dir = self.get_parm_value(parent_node, 'alembic_highpoly_rendergeo_dir')

        #object_path_list
        object_path_list = self.get_alembic_object_path_list(alembic_path)
        
        
        #object_path_to_rendergeo_list
        object_path_to_rendergeo_list = []

        #iterate and get type
        for object_path in object_path_list:

            #helga_highpoly_rendergeo
            helga_highpoly_rendergeo = self.get_alembic_attribute_value(alembic_path, object_path, 'helga_highpoly_rendergeo')
            
            #check attribute
            if not (helga_highpoly_rendergeo):
                #log
                self.logger.debug('helga_highpoly_rendergeo attribute could not be aquired for {0}. Not creating prop'.format(object_path))
                continue

            #highpoly_rendergeo_path
            highpoly_rendergeo_path = os.path.join(alembic_highpoly_rendergeo_dir, helga_highpoly_rendergeo[0] + '.abc')
            
            #check highpoly_rendergeo_path
            if not (os.path.isfile(highpoly_rendergeo_path)):
                #log
                self.logger.debug('Highpoly rendergeo at path {0} does not exist. Not creating prop'.format(highpoly_rendergeo_path))
                continue

            #create
            object_path_to_rendergeo_list.append([object_path, highpoly_rendergeo_path])


        #iterate and create props
        for object_path, highpoly_rendergeo_path in object_path_to_rendergeo_list:

            #locator_geo_node
            locator_geo_node = self.create_locator_geo_node(parent_node, alembic_file_name)
            locator_geo_node.moveToGoodPosition()

            #locator_alembic_node
            locator_alembic_node = self.create_locator_alembic_node(locator_geo_node, alembic_path, object_path)

            #create_locator_geo_node_expressions
            self.create_locator_geo_node_expressions(locator_geo_node, locator_alembic_node)


            #geo_node
            geo_node = self.create_geo_node(parent_node, alembic_file_name)
            geo_node.moveToGoodPosition()

            #alembic_node
            alembic_node = self.create_prop_highpoly_rendergeo_alembic_node(geo_node, highpoly_rendergeo_path)


            #connect
            geo_node.setFirstInput(locator_geo_node)



        


    def create_shot_highpoly_rendergeo(self, parent_node):
        """
        Create a shot hierarchy according to our pipeline standards.
        """

        print (parent_node.path())


