




#

"""
image_plane_functionality
==========================================

Module that offers possibilities to work with the image planes on the mantra nodes.
Current functionality is to set the helga pipeline image planes.

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










#Globals
#------------------------------------------------------------------

VARIABLE_NAME_LIST = ["direct_comp", 
"direct_emission", 
"indirect_comp", 
"indirect_emission",
"P",
"Pz",
"surface_color",
"sss",
"velocity",
"stmap",
"amb_occ",
"tangent_normals",
"world_normals",
"render_id",
"render_id_integer",
"fresnel_one",
"fresnel_two",
"fur_gradient"
]


TYPE_FLOAT_LIST = ["Af", "Pz", "Render_Time", "Shading_Samples", "Pixel_Samples"]
QUANTIZE_32F_LIST = ["P", "Pz"]
PER_LIGHT_EXPORT_LIST = []
SAMPLE_FILTER_LIST = ["direct_emission"]
EXPORT_VAR_FOR_EACH_COMPONENT_LIST = ["direct_comp", "indirect_comp"]


VM_FILENAME_PLANE_EXPRESSION = r"""
import os

#vex_variable
vex_variable = "%(vex_variable)s"

#node
node = hou.pwd()
#picture_path
picture_path = node.evalParm("vm_picture")
#picture_directory, picture_name
picture_directory, picture_name = os.path.split(picture_path)
#picture_basename, picture_padding, picture_ext
picture_basename, picture_padding, picture_ext = picture_name.split(".")
#new_picture_name
new_picture_name = "{0}_{1}.{2}.{3}".format(picture_basename, vex_variable, picture_padding, picture_ext)
#new_picture_path
new_picture_path = "{0}/{1}".format(picture_directory, new_picture_name)

#return
return new_picture_path
"""






#ImagePlane class
#------------------------------------------------------------------
class ImagePlane(object):
    """
    Class that holds the data belonging to an image
    """

    def __init__(self, variable_name):
        """
        Customize ImagePlane
        """

        #intristic attrs
        self.vm_variable_plane = variable_name
        self.vm_disable_plane = False
        self.vm_vextype_plane = "vector"
        self.vm_channel_plane = ""
        self.vm_quantize_plane = "half"
        self.vm_sfilter_plane = "alpha"
        self.vm_componentexport = False
        self.vm_lightexport = False
        self.vm_lightexport_scope = "*"
        self.vm_lightexport_select = "*"
        self.vm_filename_plane = ""
        self.vm_usefile_plane = False



#ImagePlaneCreator class
#------------------------------------------------------------------
class ImagePlaneCreator(object):
    """
    ImagePlane Factory
    """
    
    def create_image_plane(self, variable_name):
        """
        Create image plane.
        """

        #image_plane
        image_plane = ImagePlane(variable_name)
        
        #customize basic
        self.customize_basic(image_plane)

        #customize specific
        self.customize_specific(image_plane)
        
        
        #return
        return image_plane


    def customize_basic(self, image_plane):
        """
        Basic customizations
        """

        #variable_name
        variable_name = image_plane.vm_variable_plane

        
        #TYPE_FLOAT_LIST
        if (variable_name in TYPE_FLOAT_LIST):
            image_plane.vm_vextype_plane = "float"
        
        #QUANTIZE_32F_LIST
        if (variable_name in QUANTIZE_32F_LIST):
            image_plane.vm_quantize_plane = "float"
        
        #SAMPLE_FILTER_LIST
        if (variable_name in SAMPLE_FILTER_LIST):
            image_plane.vm_sfilter_plane = "fullopacity"
        
        #EXPORT_VAR_FOR_EACH_COMPONENT_LIST
        if (variable_name in EXPORT_VAR_FOR_EACH_COMPONENT_LIST):
            image_plane.vm_componentexport = True


    def customize_specific(self, image_plane):
        """
        Specific customizations
        """

        #variable_name
        variable_name = image_plane.vm_variable_plane

        
        #direct_comp
        if (variable_name == 'direct_comp'):

            #vm_channel_plane
            image_plane.vm_channel_plane = 'direct'

        
        #indirect_comp
        if (variable_name == 'indirect_comp'):

            #vm_channel_plane
            image_plane.vm_channel_plane = 'indirect'






#ImagePlaneFunctionality class
#------------------------------------------------------------------
class ImagePlaneFunctionality(object):
    """
    ImagePlaneFunctionality
    """


    def __new__(cls, *args, **kwargs):
        """
        ImagePlaneFunctionality instance factory.
        """

        #image_plane_functionality_instance
        image_plane_functionality_instance = super(ImagePlaneFunctionality, cls).__new__(cls, args, kwargs)

        return image_plane_functionality_instance

    
    def __init__(self):
        """
        Customize instance.
        """

        #super
        self.parent_class = super(ImagePlaneFunctionality, self)
        self.parent_class.__init__()


        #instance variables
        #------------------------------------------------------------------
        
        


        #init procedure
        #------------------------------------------------------------------

        









    #Main Methods
    #------------------------------------------------------------------

    def add_image_planes(self):
        """
        Add helga pipeline image planes to selected mantra nodes.
        """

        #mantra_nodes_list
        mantra_nodes_list = self.get_selected_nodes_of_type(node_type = 'ifd')
        #check
        if not (mantra_nodes_list):
            #log
            print('No Mantra nodes selected. Please select a Mantra node and try again.')
            return


        #iterate mantra nodes and set pathes
        for mantra_node in mantra_nodes_list:

            #log
            print('\n\n\n----------------------------------\n{0}\n----------------------------------'.format(mantra_node.path()))

            #iterate image planes
            for variable_name in VARIABLE_NAME_LIST:

                #add_image_plane
                self.add_image_plane(mantra_node, variable_name)






    #Methods
    #------------------------------------------------------------------

    def add_image_plane(self, mantra_node, variable_name, different_file = True):
        """
        Check if image plane with variable of t
        """

        #image plane already exists?
        if (self.image_plane_exists(mantra_node, variable_name)):
            #log
            print('{0} - {1}: Failed because image plane already exists'.format(variable_name, mantra_node.path()))
            return

        #image_plane_count
        image_plane_count = self.get_image_plane_count(mantra_node)

        #target_index
        target_index = image_plane_count + 1
        
        #add empty plane
        mantra_node.parm("vm_numaux").set(target_index)

        #image_plane
        image_plane = ImagePlaneCreator().create_image_plane(variable_name)

        #iterate ImagePlane members
        for key, value in image_plane.__dict__.iteritems():
            
            #parm_name
            parm_name = "{0}{1}".format(key, target_index)
            #parm
            parm = mantra_node.parm(parm_name)
            
            #if exists, set
            if (parm):
                parm.set(value)

        #different_file
        if (different_file):

            #set_different_file_expression
            self.set_different_file_expression(mantra_node, target_index)


        #log
        print('{0} - {1}'.format(variable_name, mantra_node.path()))


    def set_different_file_expression(self, node, target_index):
        """
        Enable and set the property that exports the image plane
        at given target index with the correct file path.
        """

        #vex_variable_parm
        vex_variable_parm = node.parm("{0}{1}".format('vm_variable_plane', target_index))
        #vex_variable_value
        vex_variable_value = vex_variable_parm.eval()

        #parm_vm_usefile_plane
        parm_vm_usefile_plane = node.parm("{0}{1}".format('vm_usefile_plane', target_index))
        parm_vm_usefile_plane.set(True)

        
        #parm_vm_filename_plane
        parm_vm_filename_plane = node.parm("{0}{1}".format('vm_filename_plane', target_index))

        #set expression
        parm_vm_filename_plane.setExpression(VM_FILENAME_PLANE_EXPRESSION % {'vex_variable': vex_variable_value}, language = hou.exprLanguage.Python)

    
    def get_image_plane_count(self, mantra_node):
        """
        Return number of image planes of the mantra rop.
        """

        #image_plane_count
        image_plane_count = self.get_parm_value(mantra_node, 'vm_numaux')

        return image_plane_count


    def image_plane_exists(self, mantra_node, plane_to_match):
        """
        Return list of all variable names that match plane_to_match.
        An empty list evals to False.
        """

        #image_plane_count
        image_plane_count = self.get_image_plane_count(mantra_node)

        #existing_image_plane_list
        existing_image_plane_list = []

        #iterate
        for index in range(image_plane_count):

            #image_plane_index
            image_plane_index = index + 1

            #vm_variable_plane
            vm_variable_plane = self.get_parm_value(mantra_node, 'vm_variable_plane{0}'.format(image_plane_index))
            
            #check
            if (vm_variable_plane == plane_to_match):
                existing_image_plane_list.append(vm_variable_plane)

        #return
        return existing_image_plane_list

    



    #Utility Methods
    #------------------------------------------------------------------

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


    def get_parm_value(self, node, parm_name):
        """
        Return parm value for parm with parm_name on node.
        """

        #parm
        parm = node.parm(parm_name)
        #check
        if not (parm):
            #log
            print('Node {0} does not have a parm with name {1}. Returning None'.format(node.name(), parm_name))
            return None

        #return
        return parm.eval()


    def set_parm_value(self, node, parm_name, value):
        """
        Set value for parm with parm_name on node.
        """

        #parm
        parm = node.parm(parm_name)
        #check
        if not (parm):
            #log
            print('Node {0} does not have a parm with name {1}. Not setting value'.format(node.name(), parm_name))
            return

        #set
        parm.set(value)




        

        
        
        

        

        



        

    #Test
    #------------------------------------------------------------------

    def dummy_method(self, msg = 'dummy'):
        """
        Dummy method
        """

        #print
        print('{0}'.format(msg))


    









    












#Test
#------------------------------------------------------------------

if (__name__ == '__main__'):

    pass