

"""
alembic_import
==============

Module that wraps pur pipeline alembic import into Houdini.

This custom import was neccessary to avoid some of the downsides of the default
Alembic import that especially have an impact on lighting and shading.

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

#alembic_import_shot_highpoly_rendergeo
from lib import alembic_import_shot_highpoly_rendergeo
if(do_reload):(alembic_import_shot_highpoly_rendergeo)

#alembic_import_shot_rendergeo
from lib import alembic_import_shot_rendergeo
if(do_reload):(alembic_import_shot_rendergeo)

#alembic_import_shot_proxy
from lib import alembic_import_shot_proxy
if(do_reload):(alembic_import_shot_proxy)

#alembic_import_char
from lib import alembic_import_char
if(do_reload):(alembic_import_char)







#Globals
#------------------------------------------------------------------

#Pathes
TOOL_ROOT_PATH = alembic_import_globals.TOOL_ROOT_PATH










#AlembicImport class
#------------------------------------------------------------------
class AlembicImport(object):
    """
    AlembicImport
    """


    def __new__(cls, *args, **kwargs):
        """
        AlembicImport instance factory.
        """

        #alembic_import_instance
        alembic_import_instance = super(AlembicImport, cls).__new__(cls, args, kwargs)

        return alembic_import_instance

    
    def __init__(self,
                node = None,
                logging_level = logging.DEBUG):
        """
        Customize instance.
        """

        #super
        self.parent_class = super(AlembicImport, self)
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

        self.test_methods()


    

    #Creation
    #------------------------------------------------------------------

    def create_char(self):
        """
        Create character according to helga standards.
        """

        #alembic_import_char_instance
        alembic_import_char_instance = alembic_import_char.AlembicImportChar(self.node)

        #create_char
        alembic_import_char_instance.create_char()


    def print_alembic_object_path_list(self):
        """
        Print alembic object path list.
        """

        #alembic_import_char_instance
        alembic_import_char_instance = alembic_import_char.AlembicImportChar(self.node)

        #print_alembic_object_path_list
        alembic_import_char_instance.print_alembic_object_path_list()


    def create_prop(self, prop_type):
        """
        Create prop of prop_type. prop_type may be 'rendergeo' or 'proxy'.
        'rendergeo' has highpoly_rendergeo (which is locator based highpoly geometry)
        and 'rendergeo' flagged geometry which is displaced or just normal
        geometry ment for rendering.
        """

        #rendergeo
        if (prop_type == 'rendergeo'):

            #create_prop_rendergeo
            self.create_prop_rendergeo()

        #proxy
        elif (prop_type == 'proxy'):

            #create_prop_proxy
            self.create_prop_proxy()


    def create_prop_rendergeo(self):
        """
        Create prop that may be flagged with 'helga_highpoly_rendergeo' or 
        'helga_rendergeo' attr.
        """

        #alembic_import_shot_highpoly_rendergeo_instance
        alembic_import_shot_highpoly_rendergeo_instance = alembic_import_shot_highpoly_rendergeo.AlembicImportShotHighpolyRendergeo(self.node)
        #alembic_import_shot_rendergeo_instance
        alembic_import_shot_rendergeo_instance = alembic_import_shot_rendergeo.AlembicImportShotRendergeo(self.node)

        #create_prop
        alembic_import_shot_highpoly_rendergeo_instance.create_prop()
        #create_prop
        alembic_import_shot_rendergeo_instance.create_prop()


    def create_prop_proxy(self):
        """
        Create prop that is be flagged with 'helga_proxy' attr.
        """

        #alembic_import_shot_proxy_instance
        alembic_import_shot_proxy_instance = alembic_import_shot_proxy.AlembicImportShotProxy(self.node)

        #create_prop
        alembic_import_shot_proxy_instance.create_prop()


    def create_shot(self, shot_type):
        """
        Create shot of shot_type. shot_type may be 'rendergeo' or 'proxy'.
        'rendergeo' has highpoly_rendergeo (which is locator based highpoly geometry)
        and 'rendergeo' flagged geometry which is displaced or just normal
        geometry ment for rendering.
        """

        #rendergeo
        if (shot_type == 'rendergeo'):

            #create_shot_rendergeo
            self.create_shot_rendergeo()

        #proxy
        elif (shot_type == 'proxy'):

            #create_shot_proxy
            self.create_shot_proxy()


    def create_shot_rendergeo(self):
        """
        Create shot that may be flagged with 'helga_highpoly_rendergeo' or 
        'helga_rendergeo' attr.
        """

        #alembic_import_shot_highpoly_rendergeo_instance
        alembic_import_shot_highpoly_rendergeo_instance = alembic_import_shot_highpoly_rendergeo.AlembicImportShotHighpolyRendergeo(self.node)
        #alembic_import_shot_rendergeo_instance
        alembic_import_shot_rendergeo_instance = alembic_import_shot_rendergeo.AlembicImportShotRendergeo(self.node)

        #delete_content
        self.alembic_functionality.delete_content(self.node)

        #create_shot
        alembic_import_shot_highpoly_rendergeo_instance.create_shot()
        #create_shot
        alembic_import_shot_rendergeo_instance.create_shot()


    def create_shot_proxy(self):
        """
        Create shot that is be flagged with 'helga_proxy' attr.
        """

        #alembic_import_shot_proxy_instance
        alembic_import_shot_proxy_instance = alembic_import_shot_proxy.AlembicImportShotProxy(self.node)

        #delete_content
        self.alembic_functionality.delete_content(self.node)

        #create_shot
        alembic_import_shot_proxy_instance.create_shot()

    


    
    
        

        

        
        
        

        

        



        

    #Test
    #------------------------------------------------------------------

    def dummy_method(self, msg = 'dummy'):
        """
        Dummy method
        """

        #log
        self.logger.debug('{0}'.format(msg))
        #print
        print('{0}'.format(msg))


    def test_methods(self):
        """
        Suite of test methods to execute on startup.
        """

        #log
        self.logger.debug('\n\nExecute test methods:\n-----------------------------')


        
        #test methods here
        #------------------------------------------------------------------

        #dummy_method
        self.dummy_method()

        #------------------------------------------------------------------



        #log
        self.logger.debug('\n\n-----------------------------\nFinished test methods.')


    








#hdaModule
#------------------------------------------------------------------
#------------------------------------------------------------------


#char
#------------------------------------------------------------------

def create_char(node):
    """
    Create character hierarchy. Callback for node button.
    ------------------------------------------------------------------
    kwargs['node'].hdaModule().create_char(kwargs['node'])
    """

    #import
    from helga.houdini.import_export.alembic_import import alembic_import
    reload(alembic_import)

    #alembic_import_instance
    alembic_import_instance = alembic_import.AlembicImport(node)

    #create_prop
    alembic_import_instance.create_char()


def print_alembic_object_path_list(node):
    """
    Print Alembic object pathes and object types in the console.
    ------------------------------------------------------------------
    kwargs['node'].hdaModule().print_alembic_object_path_list(kwargs['node'])
    """

    #import
    from helga.houdini.import_export.alembic_import import alembic_import
    reload(alembic_import)

    #alembic_import_instance
    alembic_import_instance = alembic_import.AlembicImport(node)

    #create_prop
    alembic_import_instance.print_alembic_object_path_list()


#props
#------------------------------------------------------------------

def create_prop(node, prop_type):
    """
    Function to be used in the hdaModule of the Python operator.
    ------------------------------------------------------------------
    kwargs['node'].hdaModule().create_prop(kwargs['node'], 'rendergeo')
    -
    kwargs['node'].hdaModule().create_prop(kwargs['node'], 'proxy')
    """

    #import
    from helga.houdini.import_export.alembic_import import alembic_import
    reload(alembic_import)

    #alembic_import_instance
    alembic_import_instance = alembic_import.AlembicImport(node)

    #create_prop
    alembic_import_instance.create_prop(prop_type)


def create_shot(node, shot_type):
    """
    Function to be used in the hdaModule of the Python operator.
    ------------------------------------------------------------------
    kwargs['node'].hdaModule().create_shot(kwargs['node'], 'rendergeo')
    -
    kwargs['node'].hdaModule().create_shot(kwargs['node'], 'proxy')
    """

    #import
    from helga.houdini.import_export.alembic_import import alembic_import
    reload(alembic_import)

    #alembic_import_instance
    alembic_import_instance = alembic_import.AlembicImport(node)

    #create_shot
    alembic_import_instance.create_shot(shot_type)


#shader assignment and grouping
#------------------------------------------------------------------

def create_network_boxes_from_materials(node):
    """
    Try to create network boxes for the geo node children of this node.
    The network boxes are based on the helga_material attr. of alembic
    files within alembic sops under the geo nodes.
    ------------------------------------------------------------------
    kwargs['node'].hdaModule().create_network_boxes_from_materials(kwargs['node'])
    """
    
    #node None
    if not (node):
        #log
        print('No node passed, not assigning materials.')
        return

    #import
    from helga.houdini.import_export.alembic_import.lib import alembic_import_shader_assignment
    reload(alembic_import_shader_assignment)
    
    
    #alembic_import_shader_assignment_instance
    alembic_import_shader_assignment_instance = alembic_import_shader_assignment.AlembicImportShaderAssignment(node = node)

    #create_network_boxes_from_materials
    alembic_import_shader_assignment_instance.create_network_boxes_from_materials()


def assign_materials(node):
    """
    Try to assign materials for content of this node.
    ------------------------------------------------------------------
    kwargs['node'].hdaModule().assign_materials(kwargs['node'])
    """
    
    #node None
    if not (node):
        
        #log
        print('No node passed, not assigning materials.')
        return

    #import
    from helga.houdini.import_export.alembic_import.lib import alembic_import_shader_assignment
    reload(alembic_import_shader_assignment)
    
    
    #alembic_import_shader_assignment_instance
    alembic_import_shader_assignment_instance = alembic_import_shader_assignment.AlembicImportShaderAssignment(node = node)

    #assign materials
    alembic_import_shader_assignment_instance.assign_materials()












#Test
#------------------------------------------------------------------

if (__name__ == '__main__'):

    pass