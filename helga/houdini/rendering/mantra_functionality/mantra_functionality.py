




#

"""
mantra_functionality
==========================================

Module that offers possibilities to adjust render pathes, rendersettings etc.

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

RENDER_IMAGE_FORMAT = 'exr'
HELGA_RENDER_PATH = '$HELGA_RENDER_PATH'
HIP = '$HIP'
HIPNAME = '$HIPNAME:r'
FRAME_PADDING = '$F4'
OPERATOR_NAME = '$OS'
TAKE_NAME = '$ACTIVETAKE' #Not working yet or flacky. Therefore not used











#MantraFunctionality class
#------------------------------------------------------------------
class MantraFunctionality(object):
    """
    MantraFunctionality
    """


    def __new__(cls, *args, **kwargs):
        """
        MantraFunctionality instance factory.
        """

        #mantra_functionality_instance
        mantra_functionality_instance = super(MantraFunctionality, cls).__new__(cls, args, kwargs)

        return mantra_functionality_instance

    
    def __init__(self):
        """
        Customize instance.
        """

        #super
        self.parent_class = super(MantraFunctionality, self)
        self.parent_class.__init__()


        #instance variables
        #------------------------------------------------------------------
        
        


        #init procedure
        #------------------------------------------------------------------

        









    #Methods
    #------------------------------------------------------------------

    def set_renderpathes(self, testing = True):
        """
        Set the renderpathes for testing for the selected Mantra nodes.
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

            #set_ifd_path
            self.set_ifd_path(mantra_node, testing = testing)

            #set_picture_path
            self.set_picture_path(mantra_node, testing = testing)


    def set_ifd_path(self, node, testing = False):
        """
        Set path for ifd rendering. Ifd files are like .rib files and are consumed by
        Mantra.
        """

        #username
        username = global_functions.get_user()
        #check
        if not (username):
            #set unknown
            username = 'unknown'


        #take
        take = self.get_parm_value(node, 'take')


        #parm_soho_outputmode
        parm_soho_outputmode = node.parm('soho_outputmode')
        #parm_soho_diskfile
        parm_soho_diskfile = node.parm('soho_diskfile')


        #ifd_path

        #testing
        if (testing):
            
            #ifd_path
            ifd_path = '{0}/ifd/{1}/{2}/{3}/{4}/{2}_{3}.{5}.ifd'.format(HIP, 'testing', HIPNAME, OPERATOR_NAME, take, FRAME_PADDING)

        #comp
        else:

            #ifd_path
            ifd_path = '{0}/ifd/{1}/{2}/{3}/{4}/{2}_{3}.{5}.ifd'.format(HIP, 'comp', HIPNAME, OPERATOR_NAME, take, FRAME_PADDING)

        
        #set ifd path
        parm_soho_diskfile.set(ifd_path)

        #set outputmode
        parm_soho_outputmode.set(True)


        #log
        print('{0} --> ifd path'.format(node.path()))


    def set_picture_path(self, node, testing = False):
        """
        Set path for image rendering.
        """

        #username
        username = global_functions.get_user()
        #check
        if not (username):
            #set unknown
            username = 'unknown'


        #take
        take = self.get_parm_value(node, 'take')


        #parm_vm_picture
        parm_vm_picture = node.parm('vm_picture')


        #picture_path
        
        #testing
        if (testing):

            #picture_path
            picture_path = '{0}/{1}/{2}/{3}/{4}/{5}/{3}_{4}.{6}.{7}'.format(HELGA_RENDER_PATH, 'testing', username, HIPNAME, OPERATOR_NAME, take, FRAME_PADDING, RENDER_IMAGE_FORMAT)
        
        #comp
        else:

            #shot_name
            shot_name = self.get_shot_name()

            #picture_path
            picture_path = '{0}/{1}/{2}/{3}/{4}/{5}/{3}_{4}.{6}.{7}'.format(HELGA_RENDER_PATH, 'comp', shot_name, HIPNAME, OPERATOR_NAME, take, FRAME_PADDING, RENDER_IMAGE_FORMAT)

        #set ifd path
        parm_vm_picture.set(picture_path)


        #log
        print('{0} --> picture path'.format(node.path()))
        

    def apply_base_setup(self):
        """
        Apply rendering base setup for the selected Mantra nodes.
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

            try:
                #decouple_indirect_noise_parameters
                self.decouple_indirect_noise_parameters(mantra_node)
                #add_operator_id_render_property
                self.add_operator_id_render_property(mantra_node)
            
            except:
                #log
                print('Error adding indirect parameters. Maybe they already existed.')

            #set_mantra_base_parameters
            self.set_mantra_base_parameters(mantra_node)


    def decouple_indirect_noise_parameters(self, node):
        """
        Decouple indirect noise parameters on Mantra node.
        """

        #Create Parameters
        #------------------------------------------------------------------

        #parm_group
        parm_group = node.parmTemplateGroup()

        
        #folder_sampling
        folder_sampling = parm_group.containingFolder('vm_minraysamples')
        #vm_decoupleindirect
        hou_parm_template = hou.ToggleParmTemplate("vm_decoupleindirect", "Decouple Indirect Sample Limits", default_value=False)
        hou_parm_template.setHelp("None")
        hou_parm_template.setTags({"spare_category": "Sampling"})
        #append
        parm_group.appendToFolder(folder_sampling, hou_parm_template)
        #set in node
        node.setParmTemplateGroup(parm_group)

        #log
        parm = node.parm("vm_decoupleindirect")
        parm_name = parm.name()
        parm_value = parm.eval()
        print('Added parm. {0} - {1}'.format(parm_name, parm_value))


        #folder_sampling
        folder_sampling = parm_group.containingFolder('vm_minraysamples')
        #vm_minindirectraysamples
        hou_parm_template = hou.IntParmTemplate("vm_minindirectraysamples", "Min Indirect Ray Samples", 1, default_value=([1]), min=1, max=64, min_is_strict=False, max_is_strict=False, naming_scheme=hou.parmNamingScheme.Base1)
        hou_parm_template.setConditional( hou.parmCondType.DisableWhen, "{ vm_decoupleindirect == 0 }")
        hou_parm_template.setHelp("None")
        hou_parm_template.setTags({"spare_category": "Sampling"})
        #append
        parm_group.appendToFolder(folder_sampling, hou_parm_template)
        #set in node
        node.setParmTemplateGroup(parm_group)

        #log
        parm = node.parm("vm_minindirectraysamples")
        parm_name = parm.name()
        parm_value = parm.eval()
        print('Added parm. {0} - {1}'.format(parm_name, parm_value))


        #folder_sampling
        folder_sampling = parm_group.containingFolder('vm_minraysamples')
        #vm_maxindirectraysamples
        hou_parm_template = hou.IntParmTemplate("vm_maxindirectraysamples", "Max Indirect Ray Samples", 1, default_value=([9]), min=1, max=64, min_is_strict=False, max_is_strict=False, naming_scheme=hou.parmNamingScheme.Base1)
        hou_parm_template.setConditional( hou.parmCondType.DisableWhen, "{ vm_decoupleindirect == 0 } { vm_dorayvariance == 0 }")
        hou_parm_template.setHelp("None")
        hou_parm_template.setTags({"spare_category": "Sampling"})
        #append
        parm_group.appendToFolder(folder_sampling, hou_parm_template)
        #set in node
        node.setParmTemplateGroup(parm_group)

        #log
        parm = node.parm("vm_maxindirectraysamples")
        parm_name = parm.name()
        parm_value = parm.eval()
        print('Added parm. {0} - {1}'.format(parm_name, parm_value))

        
        #folder_sampling
        folder_sampling = parm_group.containingFolder('vm_minraysamples')
        #vm_indirectvariance
        hou_parm_template = hou.FloatParmTemplate("vm_indirectvariance", "Indirect Noise Level", 1, default_value=([0.05]), min=0, max=0.1, min_is_strict=False, max_is_strict=False, look=hou.parmLook.Regular, naming_scheme=hou.parmNamingScheme.Base1)
        hou_parm_template.setConditional( hou.parmCondType.DisableWhen, "{ vm_decoupleindirect == 0 } { vm_dorayvariance == 0 }")
        hou_parm_template.setHelp("None")
        hou_parm_template.setTags({"spare_category": "Sampling"})
        #append
        parm_group.appendToFolder(folder_sampling, hou_parm_template)
        #set in node
        node.setParmTemplateGroup(parm_group)

        #log
        parm = node.parm("vm_indirectvariance")
        parm_name = parm.name()
        parm_value = parm.eval()
        print('Added parm. {0} - {1}'.format(parm_name, parm_value))

        
        
        #Adjust Parameters
        #------------------------------------------------------------------

        # Code for /out/mantra1/vm_decoupleindirect parm 
        hou_parm = node.parm("vm_decoupleindirect")
        hou_parm.lock(False)
        hou_parm.setAutoscope(False)


        # Code for /out/mantra1/vm_minindirectraysamples parm 
        hou_parm = node.parm("vm_minindirectraysamples")
        hou_parm.lock(False)
        hou_parm.setAutoscope(False)


        # Code for /out/mantra1/vm_maxindirectraysamples parm 
        hou_parm = node.parm("vm_maxindirectraysamples")
        hou_parm.lock(False)
        hou_parm.setAutoscope(False)


        # Code for /out/mantra1/vm_indirectvariance parm 
        hou_parm = node.parm("vm_indirectvariance")
        hou_parm.lock(False)
        hou_parm.setAutoscope(False)



    def add_operator_id_render_property(self, node):
        """
        Add vm_generate_opid property to mantra node. This property ensures that
        the render_id passes work.
        """

        #Create Parameters
        #------------------------------------------------------------------

        #parm_group
        parm_group = node.parmTemplateGroup()

        
        #folder_output
        folder_output = parm_group.containingFolder('vm_picture')
        #vm_decoupleindirect
        hou_parm_template = hou.ToggleParmTemplate("vm_generate_opid", "Generate Operator IDs", default_value = True)
        hou_parm_template.setHelp("None")
        hou_parm_template.setTags({"spare_category": "Output"})
        #append
        parm_group.appendToFolder(folder_output, hou_parm_template)
        #set in node
        node.setParmTemplateGroup(parm_group)

        #log
        parm = node.parm("vm_generate_opid")
        parm_name = parm.name()
        parm_value = parm.eval()
        print('Added parm. {0} - {1}'.format(parm_name, parm_value))


        #Adjust Parameters
        #------------------------------------------------------------------

        #vm_generate_opid 
        hou_parm = node.parm("vm_generate_opid")
        hou_parm.lock(False)
        hou_parm.setAutoscope(False)


        


        

        


    def set_mantra_base_parameters(self, node):
        """
        Set mantra base parameters. This is the technically correct base setup.
        It is ment as a starting ground that gets things like exr compression etc. right.
        From this foundation you are ment to try and tweak the look.
        """

        #Main
        #------------------------------------------------------------------

        #soho_mkpath
        self.set_parm_value(node, 'soho_mkpath', True)
        #log
        print('{0} to {1}'.format('soho_mkpath', self.get_parm_value(node, 'soho_mkpath')))

        

        #Objects
        #------------------------------------------------------------------

        #soho_autoheadlight
        self.set_parm_value(node, 'soho_autoheadlight', False)
        #log
        print('{0} to {1}'.format('soho_autoheadlight', self.get_parm_value(node, 'soho_autoheadlight')))
        


        #Properties/Output
        #------------------------------------------------------------------

        #override_camerares
        self.set_parm_value(node, 'override_camerares', True)
        #log
        print('{0} to {1}'.format('override_camerares', self.get_parm_value(node, 'override_camerares')))

        #res_overridex
        self.set_parm_value(node, 'res_overridex', 1280)
        #log
        print('{0} to {1}'.format('res_overridex', self.get_parm_value(node, 'res_overridex')))

        #res_overridey
        self.set_parm_value(node, 'res_overridey', 720)
        #log
        print('{0} to {1}'.format('res_overridey', self.get_parm_value(node, 'res_overridey')))


        
        #Properties/Output Options
        #------------------------------------------------------------------

        #vm_image_exr_compression
        self.set_parm_value(node, 'vm_image_exr_compression', 'zips')
        #log
        print('{0} to {1}'.format('vm_image_exr_compression', self.get_parm_value(node, 'vm_image_exr_compression')))



        #Properties/Render
        #------------------------------------------------------------------

        #vm_renderengine
        self.set_parm_value(node, 'vm_renderengine', 'raytrace')
        #log
        print('{0} to {1}'.format('vm_renderengine', self.get_parm_value(node, 'vm_renderengine')))



        #Properties/Sampling
        #------------------------------------------------------------------

        #vm_samplelock
        self.set_parm_value(node, 'vm_samplelock', False)
        #log
        print('{0} to {1}'.format('vm_samplelock', self.get_parm_value(node, 'vm_samplelock')))

        #shutteroffset
        self.set_parm_value(node, 'shutteroffset', 0)
        #log
        print('{0} to {1}'.format('shutteroffset', self.get_parm_value(node, 'shutteroffset')))

        #vm_minraysamples
        self.set_parm_value(node, 'vm_minraysamples', 2)
        #log
        print('{0} to {1}'.format('vm_minraysamples', self.get_parm_value(node, 'vm_minraysamples')))

        #vm_maxraysamples
        self.set_parm_value(node, 'vm_maxraysamples', 9)
        #log
        print('{0} to {1}'.format('vm_maxraysamples', self.get_parm_value(node, 'vm_maxraysamples')))

        #vm_variance
        self.set_parm_value(node, 'vm_variance', 0.01)
        #log
        print('{0} to {1}'.format('vm_variance', self.get_parm_value(node, 'vm_variance')))

        
        #vm_decoupleindirect
        self.set_parm_value(node, 'vm_decoupleindirect', 0)
        #log
        print('{0} to {1}'.format('vm_decoupleindirect', self.get_parm_value(node, 'vm_decoupleindirect')))

        #vm_minindirectraysamples
        self.set_parm_value(node, 'vm_minindirectraysamples', 2)
        #log
        print('{0} to {1}'.format('vm_minindirectraysamples', self.get_parm_value(node, 'vm_minindirectraysamples')))

        #vm_maxindirectraysamples
        self.set_parm_value(node, 'vm_maxindirectraysamples', 9)
        #log
        print('{0} to {1}'.format('vm_maxindirectraysamples', self.get_parm_value(node, 'vm_maxindirectraysamples')))

        #vm_indirectvariance
        self.set_parm_value(node, 'vm_indirectvariance', 0.01)
        #log
        print('{0} to {1}'.format('vm_indirectvariance', self.get_parm_value(node, 'vm_indirectvariance')))



        #Properties/Shading
        #------------------------------------------------------------------

        #vm_reflectlimit
        self.set_parm_value(node, 'vm_reflectlimit', 4)
        #log
        print('{0} to {1}'.format('vm_reflectlimit', self.get_parm_value(node, 'vm_reflectlimit')))

        #vm_refractlimit
        self.set_parm_value(node, 'vm_refractlimit', 4)
        #log
        print('{0} to {1}'.format('vm_refractlimit', self.get_parm_value(node, 'vm_refractlimit')))

        #vm_diffuselimit
        self.set_parm_value(node, 'vm_diffuselimit', 1)
        #log
        print('{0} to {1}'.format('vm_diffuselimit', self.get_parm_value(node, 'vm_diffuselimit')))

        #vm_pbrreflectratio
        self.set_parm_value(node, 'vm_pbrreflectratio', 1)
        #log
        print('{0} to {1}'.format('vm_pbrreflectratio', self.get_parm_value(node, 'vm_pbrreflectratio')))

        #vm_colorlimit
        self.set_parm_value(node, 'vm_colorlimit', 5)
        #log
        print('{0} to {1}'.format('vm_colorlimit', self.get_parm_value(node, 'vm_colorlimit')))



        #Properties/Statistics
        #------------------------------------------------------------------

        #vm_verbose
        self.set_parm_value(node, 'vm_verbose', 4)
        #log
        print('{0} to {1}'.format('vm_verbose', self.get_parm_value(node, 'vm_verbose')))



        #vm_alfprogress
        self.set_parm_value(node, 'vm_alfprogress', True)
        #log
        print('{0} to {1}'.format('vm_alfprogress', self.get_parm_value(node, 'vm_alfprogress')))












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


    def get_shot_name(self):
        """
        Return parm value for parm with parm_name on node.
        """

        #hipfile_path
        hipfile_path = hou.hipFile.path()

        #check if path correct
        if not ('lighting' in hipfile_path):

            #log
            print('Hipfile path {0} does not match pipeline shots path because it is not under a folder called lighting. Returning unknown as shot name'.format(hipfile_path))
            return 'unknown'

        #hipfile_path_list
        hipfile_path_list = hipfile_path.split('/')

        #lighting_index
        lighting_index = hipfile_path_list.index('lighting')

        #check if lighting_index correct
        if not (lighting_index):

            #log
            print('lighting_index {0} for Hipfile path seems wrong. Returning unknown as shot name'.format(lighting_index))
            return 'unknown'


        #shot_name
        shot_name = hipfile_path_list[lighting_index - 1]


        return shot_name




        

        
        
        

        

        



        

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