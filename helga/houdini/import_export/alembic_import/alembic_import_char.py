

"""
alembic_import_char
==========================================

GUI to import Character Alembics according to our pipeline standards.

This module is mainly needed because of the weird Alembic
import in Houdini, that generates all these Alembic xform nodes
and geometry nodes without all the usual parameters for subdiving etc.

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










#AlembicImportChar class
#------------------------------------------------------------------
class AlembicImportChar(object):
    """
    AlembicImportChar
    """


    def __new__(cls, *args, **kwargs):
        """
        AlembicImportChar instance factory.
        """

        #alembic_import_char_instance
        alembic_import_char_instance = super(AlembicImportChar, cls).__new__(cls, args, kwargs)

        return alembic_import_char_instance

    
    def __init__(self,
                node = None,
                logging_level = logging.DEBUG):
        """
        Customize instance.
        """

        #super
        self.parent_class = super(AlembicImportChar, self)
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









    #Methods
    #------------------------------------------------------------------

    def base_data_check_char(self):
        """
        Check base data from the node and return either False
        or the needed data. (Equivalent to True).
        The returned data is [alembic_path] 
        """

        #alembic_path
        alembic_path = self.alembic_functionality.get_parm_value(self.node, 'alembic_path')
        
        #is False
        if not (alembic_path):
            #log
            self.logger.debug('Alembic path empty.')
            return False
        
        #path exists
        if not (os.path.isfile(alembic_path)):
            #log
            self.logger.debug('Alembic path {0} does not exist.'.format(alembic_path))
            return False


        #return
        return [alembic_path]


    def create_char(self):
        """
        Create hierarchy.
        """

        #base_data_check_char
        if not (self.base_data_check_char()):
            #log
            self.logger.debug('Base data check failed, not creating char.')
            return

        #create_char
        self.alembic_functionality.create_char(self.node)


    def print_alembic_object_path_list(self):
        """
        Create hierarchy.
        """

        #base_data_check_char
        if not (self.base_data_check_char()):
            #log
            self.logger.debug('Base data check failed, not printing object path list.')
            return


        #alembic_path
        alembic_path = self.base_data_check_char()[0]

        #print_alembic_object_path_list
        self.alembic_functionality.print_alembic_object_path_list(alembic_path)

        

        

        
        
        

        

        



        

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

def create_char(node):
    """
    Create character hierarchy. Callback for node button.
    ------------------------------------------------------------------
    kwargs['node'].hdaModule().create_char(kwargs['node'])
    """
    
    #node None
    if not (node):
        #log
        print('No node passed, not building character hierarchy.')
        return

    #import
    from helga.houdini.import_export.alembic_import import alembic_import_char
    reload(alembic_import_char)
    
    
    #alembic_import_char_instance
    alembic_import_char_instance = alembic_import_char.AlembicImportChar(node = node)

    #create_char
    alembic_import_char_instance.create_char()


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
    from helga.houdini.import_export.alembic_import import alembic_import_shader_assignment
    reload(alembic_import_shader_assignment)
    
    
    #alembic_import_shader_assignment_instance
    alembic_import_shader_assignment_instance = alembic_import_shader_assignment.AlembicImportShaderAssignment(node = node)

    #assign materials
    alembic_import_shader_assignment_instance.assign_materials()


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
    from helga.houdini.import_export.alembic_import import alembic_import_shader_assignment
    reload(alembic_import_shader_assignment)
    
    
    #alembic_import_shader_assignment_instance
    alembic_import_shader_assignment_instance = alembic_import_shader_assignment.AlembicImportShaderAssignment(node = node)

    #create_network_boxes_from_materials
    alembic_import_shader_assignment_instance.create_network_boxes_from_materials()



def print_alembic_object_path_list(node):
    """
    Print Alembic object pathes and object types in the console.
    ------------------------------------------------------------------
    kwargs['node'].hdaModule().print_alembic_object_path_list(kwargs['node'])
    """
    
    #node None
    if not (node):
        #log
        print('No node passed, not printing alembic pathes.')
        return


    #import
    from helga.houdini.import_export.alembic_import import alembic_import_char
    reload(alembic_import_char)
    
    
    #alembic_import_char_instance
    alembic_import_char_instance = alembic_import_char.AlembicImportChar(node = node)

    #print_alembic_object_path_list
    alembic_import_char_instance.print_alembic_object_path_list()






#OnCreated callback (copy this in the HDAs OnCreated callback)
#------------------------------------------------------------------

'''
def set_expressions_on_subnet_parameters(node):
    """
    Set expressions on parameters.
    """

    #expression_frame
    expression_frame = '$FF'
    #set expression
    parm_frame = node.parm('frame')
    #set expression
    parm_frame.setExpression(expression_frame, language = hou.exprLanguage.Hscript)


    #expression_fps
    expression_fps = '$FPS'
    #set expression
    parm_fps = node.parm('fps')
    #set expression
    parm_fps.setExpression(expression_fps, language = hou.exprLanguage.Hscript)


def on_created():
    """
    Initialize node.
    """

    #node
    node = kwargs['node']
    
    #set_expressions_on_subnet_parameters
    set_expressions_on_subnet_parameters(node)


#on_created
on_created()

'''




    







#Test
#------------------------------------------------------------------

if (__name__ == '__main__'):

    pass