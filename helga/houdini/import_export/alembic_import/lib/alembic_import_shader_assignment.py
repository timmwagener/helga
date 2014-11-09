

"""
alembic_import_shader_assignment
==========================================

Assign shaders to imported chars or scenes.
This module is specific to our pipeline.

Bitte sterbt alle ihr gottverdammten Huhrensoehne.
-----------------------

**Author:** `Timm Wagener <mailto:wagenertimm@gmail.com>`_
"""









#Import
#------------------------------------------------------------------
#python
import sys
import os
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
import alembic_import_globals
if(do_reload):reload(alembic_import_globals)

#alembic_import_logging_handler
import alembic_import_logging_handler
if(do_reload):reload(alembic_import_logging_handler)

#alembic_functionality
import alembic_functionality
if(do_reload):reload(alembic_functionality)







#Globals
#------------------------------------------------------------------
HELGA_MATERIAL_ATTRIBUTE_NAME = 'helga_material'
NETWORK_BOXES_OFFSET_X = 10










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

    
    def __init__(self, 
                    node = None,
                    logging_level = logging.DEBUG):
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

        #node
        self.node = node

        #alembic_functionality
        self.alembic_functionality = alembic_functionality.AlembicFunctionality()


        #init procedure
        #------------------------------------------------------------------

        pass







    #Main Methods
    #------------------------------------------------------------------

    def assign_materials(self):
        """
        Assign materials.
        Search the scene for a material of this name and assign it.
        """

        #all_nodes_list
        all_nodes_list = self.alembic_functionality.get_all_nodes()


        #geo_node_list
        geo_node_list = self.get_geo_node_list()
        #geo_alembic_node_list
        geo_alembic_node_list = self.get_geo_alembic_node_list(geo_node_list)
        #geo_alembic_material_list
        geo_alembic_material_list = self.get_geo_alembic_material_list(geo_alembic_node_list)


        #geo_alembic_material_list empty
        if not (geo_alembic_material_list):
            #log
            self.logger.debug('Geo_alembic_material_list empty. Check if you have any matching materials in the scene or if the assets need to be updated.')
            return

        
        #iterate and assign if name matches
        for geo_node, alembic_node, material_name in geo_alembic_material_list:

            #iterate all nodes list
            for node in all_nodes_list:

                #name matches
                if (node.name() == material_name):

                    try:
                        
                        #assign
                        geo_node.parm('shop_materialpath').set(node.path())

                        #log
                        self.logger.debug('Assigned {0} to node {1}'.format(node.path(), geo_node.name()))

                    except:

                        #log
                        self.logger.debug('Error assigning {0} to node {1}'.format(node.path(), geo_node.name()))

                    continue


    def create_network_boxes_from_materials(self):
        """
        Create network boxes for geo nodes based on helga_material
        attribute in alembic files.
        """

        #geo_node_list
        geo_node_list = self.get_geo_node_list()
        #geo_alembic_node_list
        geo_alembic_node_list = self.get_geo_alembic_node_list(geo_node_list)
        #geo_alembic_material_list
        geo_alembic_material_list = self.get_geo_alembic_material_list(geo_alembic_node_list)
        #material_name_geo_node_dict
        material_name_geo_node_dict = self.get_material_name_geo_node_dict(geo_alembic_material_list)


        #remove network boxes
        self.alembic_functionality.remove_network_boxes(self.node)

        #index
        index = 0

        #iterate and create
        for material_name, geo_node_list in material_name_geo_node_dict.iteritems():

            #position_x
            position_x = index * NETWORK_BOXES_OFFSET_X
            #position_y
            position_y = 0

            #create network box
            self.alembic_functionality.create_network_box(self.node, 
                                                            geo_node_list, 
                                                            network_box_name = material_name,
                                                            position_x = position_x,
                                                            position_y = position_y)

            #increment index
            index = index + 1



        


    




    #Utility Methods
    #------------------------------------------------------------------

    def get_geo_node_list(self):
        """
        Return list of geo nodes that are children of node.
        """

        return self.alembic_functionality.get_children_of_type(self.node, children_node_type = 'geo')


    def get_geo_alembic_node_list(self, geo_node_list):
        """
        Return list of type [[geo_node, alembic_node], [geo_node, alembic_node], ...].
        """

        #geo_node_list empty
        if not (geo_node_list):
            #log
            self.logger.debug('Geo_node_list empty. Returning empty list.')
            return []


        #geo_alembic_node_list
        geo_alembic_node_list = []

        #iterate and append
        for geo_node in geo_node_list:

            #alembic_node_list
            alembic_node_list = self.alembic_functionality.get_children_of_type(parent_node = geo_node, children_node_type = 'alembic')

            #if alembic node list
            if (alembic_node_list):

                #alembic_node
                alembic_node = alembic_node_list[0]

                #append
                geo_alembic_node_list.append([geo_node, alembic_node])



        #return
        return geo_alembic_node_list


    def get_geo_node_list_from_selection(self):
        """
        Return list of type [geo_node, geo_node, ...] from selected nodes.
        Valid selected node types are geo nodes, alembic_import_shot_highpoly,
        alembic_import_shot_proxy and alembic_import_char.
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


        #return
        return geo_node_list

    
    def get_geo_alembic_material_list(self, geo_alembic_node_list):
        """
        Return list of type [[geo_node, alembic_node, material_name], [geo_node, alembic_node, material_name], ...].
        The material_name is aquired from the alembic attribute helga_material on the asset transform nodes.
        An empty entry in this attr. or no attr. on the transform node at all means no addition to the
        geo_alembic_material_list.
        """

        #geo_alembic_node_list empty
        if not (geo_alembic_node_list):
            #log
            self.logger.debug('Geo_alembic_node_list empty. Returning empty list.')
            return []


        #geo_alembic_material_list
        geo_alembic_material_list = []

        #iterate
        for geo_node, alembic_node in geo_alembic_node_list:

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

    
    def get_material_name(self, alembic_path, object_path):
        """
        Get material name for alembic path and/or object_path within alembic.
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


    def get_material_name_geo_node_dict(self, geo_alembic_material_list):
        """
        Return dict of type {material_name:[geo_node, geo_node], material_name:[geo_node, geo_node], ...}
        """

        #material_name_geo_node_dict
        material_name_geo_node_dict = {}

        #iterate and assign if name matches
        for geo_node, alembic_node, material_name in geo_alembic_material_list:

            #material_name already key
            if (material_name in material_name_geo_node_dict.keys()):

                #append
                geo_node_list = material_name_geo_node_dict[material_name]
                material_name_geo_node_dict[material_name] = geo_node_list + [geo_node]

            #else
            else:

                #new
                material_name_geo_node_dict[material_name] = [geo_node]


        #return
        return material_name_geo_node_dict








#Test
#------------------------------------------------------------------
if (__name__ == '__main__'):

    pass