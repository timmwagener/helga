

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
        #remove duplicates and sort
        object_path_list = sorted(list(set(object_path_list)))

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





    #Hierarchy Methods
    #------------------------------------------------------------------

    def create_character_geo_node(self, parent_node, node_name):
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

    
    def create_character_hierarchy(self, parent_node):
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
        #remove duplicates and sort
        object_path_list = sorted(list(set(object_path_list)))

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
                geo_node = self.create_character_geo_node(parent_node, object_transform_name)
                
                #alembic_node
                alembic_node = self.create_character_alembic_node(parent_node, geo_node, alembic_path, object_path)



        #layout children
        parent_node.layoutChildren()


