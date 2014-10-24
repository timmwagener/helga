

"""
alembic_import_shader_assignment
==========================================

Assign shaders to imported chars or scenes.
This module is specific to our pipeline.

Bitte sterbt alle ihr gottverdammten Huhrensoehne.
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




#Import variable
do_reload = True

#helga

#global_variables
from helga.general.setup.global_variables import global_variables
if(do_reload):reload(global_variables)

#global_functions
from helga.general.setup.global_functions import global_functions
if(do_reload):reload(global_functions)


#alembic_import

#lib

#alembic_import_globals
from lib import alembic_import_globals
if(do_reload):reload(alembic_import_globals)

#alembic_import_logging_handler
from lib import alembic_import_logging_handler
if(do_reload):reload(alembic_import_logging_handler)

#alembic_functionality
from lib import alembic_functionality
if(do_reload):reload(alembic_functionality)







#Globals
#------------------------------------------------------------------

#Pathes
TOOL_ROOT_PATH = alembic_import_globals.TOOL_ROOT_PATH
#Attributes
HELGA_MATERIAL_ATTRIBUTE_NAME = 'helga_material'










#AlembicImportShaderAssignment class
#------------------------------------------------------------------
class AlembicImportShaderAssignment(object):
    """
    AlembicImportShaderAssignment
    """


    def __new__(cls, *args, **kwargs):
        """
        AlembicImportShaderAssignment instance factory.
        """

        #alembic_import_shader_assignment_instance
        alembic_import_shader_assignment_instance = super(AlembicImportShaderAssignment, cls).__new__(cls, args, kwargs)

        return alembic_import_shader_assignment_instance

    
    def __init__(self, logging_level = logging.DEBUG):
        """
        Customize instance.
        """

        #super
        self.parent_class = super(AlembicImportShaderAssignment, self)
        self.parent_class.__init__()


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


        #instance variables
        #------------------------------------------------------------------

        #alembic_functionality
        self.alembic_functionality = alembic_functionality.AlembicFunctionality()


        #init procedure
        #------------------------------------------------------------------

        pass





    #Methods
    #------------------------------------------------------------------

    def get_material_name(self, alembic_path, object_path):
        """
        Get material for alembic path and/or object_path within alembic.
        """

        #material_name
        material_name = None

        #no object_path
        if not (object_path):

            #material_name
            material_name = self.get_material_name_for_alembic_path(alembic_path)
            

        #object_path
        else:

            #material_name
            material_name = self.get_material_name_for_alembic_path_and_object_path(alembic_path, object_path)


        #check if list
        #(parameter are return as list by get_alembic_attribute_value() method)
        if (isinstance(material_name, list)):
            material_name = material_name[0]
        
        #return
        return material_name


    def get_material_name_for_alembic_path(self, alembic_path):
        """
        Get material name for alembic path without considering object path.
        This method loops through all object pathes of the alembic file and
        returns the value of the first occurence of helga_metarial attr.
        that it finds. (Assuming props always only have one material).
        """

        #object_path_list
        object_path_list = self.alembic_functionality.get_alembic_object_path_list(alembic_path)

        #material_name
        material_name = None

        #iterate
        for object_path in object_path_list:

            #material_name
            material_name = self.alembic_functionality.get_alembic_attribute_value(alembic_path, object_path, HELGA_MATERIAL_ATTRIBUTE_NAME)

            #if True return
            if (material_name):

                #return
                return material_name

        
        #return
        return material_name


    def get_material_name_for_alembic_path_and_object_path(self, alembic_path, object_path):
        """
        Get material name for alembic path and object path.
        The material name attr. is always on the transform node,
        meaning that you always have to try the parent path when
        the type of an object path is a polymesh.
        """

        #object_type
        object_type = self.alembic_functionality.get_alembic_object_type(alembic_path, object_path)

        #if object_type == polymesh get parent
        if (object_type == 'polymesh'):

            try:

                #object_path
                object_path = os.path.dirname(object_path)
                #object_type
                object_type = self.alembic_functionality.get_alembic_object_type(alembic_path, object_path)

            except:

                #log
                self.logger.debug('Error getting parent path of polymesh: {0} - {1}'.format(alembic_path, object_path))


        
        #material_name
        material_name = None

        #material_name
        material_name = self.alembic_functionality.get_alembic_attribute_value(alembic_path, object_path, HELGA_MATERIAL_ATTRIBUTE_NAME)

        #return
        return material_name

        

    
    def get_geo_alembic_material_list(self, geo_alembic_node_dict):
        """
        Return helga_material attribute value from alembic.
        """

        #geo_alembic_material_list
        geo_alembic_material_list = []

        #iterate
        for geo_node, alembic_node in geo_alembic_node_dict.iteritems():

            #alembic_path
            alembic_path = self.alembic_functionality.get_parm_value(alembic_node, 'fileName')
            #alembic_path exists
            if not (os.path.isfile(alembic_path)):
                #log
                self.logger.debug('Alembic path does not exist. Continuing...')
                continue


            #object_path
            object_path = self.alembic_functionality.get_parm_value(alembic_node, 'objectPath')

            #material_name
            material_name = self.get_material_name(alembic_path, object_path)

            #if material_name then append
            if (material_name):

                #append
                geo_alembic_material_list.append([geo_node, alembic_node, material_name])


        #return
        return geo_alembic_material_list


    def assign_materials(self, geo_alembic_material_list):
        """
        Assign materials.
        Search the scene for a material of this name and assign it.
        """

        #all_nodes_list
        all_nodes_list = self.alembic_functionality.get_all_nodes()

        #iterate and assign if name matches
        for geo_node, alembic_node, material_name in geo_alembic_material_list:

            #iterate all nodes list
            for node in all_nodes_list:

                #name matches
                if (node.name() == material_name):

                    #assign
                    geo_node.parm('shop_materialpath').set(node.path())

                    #log
                    self.logger.debug('Assigned {0} to node {1}'.format(node.path(), geo_node.name()))

                    continue





    def get_geo_alembic_node_dict_from_selection(self):
        """
        Return dict {geo_node:alembic_sop_node, geo_node:alembic_sop_node, ...} for selected geo
        or helga pipeline alembic import nodes.
        """

        #selected_nodes_list
        selected_nodes_list = self.alembic_functionality.get_selected_nodes()

        #node_type_filter_list
        node_type_filter_list = ['alembic_import_shot_highpoly', 
                                    'alembic_import_shot_proxy',
                                    'alembic_import_char',
                                    'geo']
        #alembic_import_and_geo_node_list
        alembic_import_and_geo_node_list = self.alembic_functionality.filter_node_list(selected_nodes_list, node_type_filter_list)

        #geo_node_list
        geo_node_list = []
        #iterate and append
        for node in alembic_import_and_geo_node_list:

            #node is geo
            if (node.type().name() == 'geo'):

                #append
                geo_node_list.append(node)
                continue

            #node of type alembic_import_x
            if (node.type().name() in node_type_filter_list[:-1]):

                #children_geo_list
                children_geo_list = self.alembic_functionality.get_children_of_type(parent_node = node, children_node_type = 'geo')

                #add
                geo_node_list = geo_node_list + children_geo_list


        #geo_alembic_node_dict
        geo_alembic_node_dict = {}

        #iterate and append
        for geo_node in geo_node_list:

            #alembic_node_list
            alembic_node_list = self.alembic_functionality.get_children_of_type(parent_node = geo_node, children_node_type = 'alembic')

            #if alembic node list
            if (alembic_node_list):

                #set in dict
                geo_alembic_node_dict[geo_node] = alembic_node_list[0]



        #return
        return geo_alembic_node_dict









#Test
#------------------------------------------------------------------

def test():
    """
    Test method.
    """

    #import
    from helga.houdini.import_export.alembic_import import alembic_import_shader_assignment
    reload(alembic_import_shader_assignment)

    #alembic_import_shader_assignment_instance
    alembic_import_shader_assignment_instance = alembic_import_shader_assignment.AlembicImportShaderAssignment()

    #get_geo_alembic_node_dict_from_selection
    geo_alembic_node_dict = alembic_import_shader_assignment_instance.get_geo_alembic_node_dict_from_selection()

    #get_geo_alembic_material_list
    geo_alembic_material_list = alembic_import_shader_assignment_instance.get_geo_alembic_material_list(geo_alembic_node_dict)

    #assign_materials
    alembic_import_shader_assignment_instance.assign_materials(geo_alembic_material_list)





#import guard
if (__name__ == '__main__'):

    pass