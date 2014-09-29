

"""
alembic_import_shot_proxy
==========================================

GUI to import Shot Proxy Alembics according to our pipeline standards.

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










#AlembicImportShotProxy class
#------------------------------------------------------------------
class AlembicImportShotProxy(object):
    """
    AlembicImportShotProxy
    """


    def __new__(cls, *args, **kwargs):
        """
        AlembicImportShotProxy instance factory.
        """

        #alembic_import_shot_proxy_instance
        alembic_import_shot_proxy_instance = super(AlembicImportShotProxy, cls).__new__(cls, args, kwargs)

        return alembic_import_shot_proxy_instance

    
    def __init__(self,
                node = None,
                logging_level = logging.DEBUG):
        """
        Customize instance.
        """

        #super
        self.parent_class = super(AlembicImportShotProxy, self)
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









    #Checks
    #------------------------------------------------------------------

    def base_data_check_prop(self):
        """
        Check base data for props.
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


    def base_data_check_shot(self):
        """
        Check base data from the node and return either False
        or the needed data. (Equivalent to True).
        The returned data is [alembic_path_list].
        """

        #alembic_dir
        alembic_dir = self.alembic_functionality.get_parm_value(self.node, 'alembic_dir')
        
        #is False
        if not (alembic_dir):
            #log
            self.logger.debug('Parameter alembic dir empty.')
            return False

        #dir exists
        if not (os.path.isdir(alembic_dir)):
            #log
            self.logger.debug('Alembic dir {0} does not exist.'.format(alembic_dir))
            return False


        #alembic_path_list
        alembic_path_list = [os.path.join(alembic_dir, file).replace('\\', '/') for 
                            file in 
                            os.listdir(alembic_dir) if 
                            (os.path.isfile(os.path.join(alembic_dir, file)) and file.split('.')[-1] == 'abc')]
        #alembic_path_list empty
        if not (alembic_path_list):
            #log
            self.logger.debug('alembic_path_list empty. Alembic dir {0} does not seem to contain alembic files.'.format(alembic_dir))
            return False


        #return
        return [alembic_path_list]



    #Creation
    #------------------------------------------------------------------

    def create_prop(self):
        """
        Create prop.
        """

        #base_data_check_prop
        if not (self.base_data_check_prop()):
            #log
            self.logger.debug('Base data check failed, not creating prop.')
            return

        #alembic_path, alembic_highpoly_rendergeo_dir
        alembic_path = self.base_data_check_prop()[0]

        #log
        self.logger.debug('\n\n-------------------------\n{0}\n-------------------------\n\n'.format(alembic_path))

        #create_prop_proxy
        self.alembic_functionality.create_prop_proxy(self.node, alembic_path)


    def create_shot(self):
        """
        Create shot.
        """

        #base_data_check_shot
        if not (self.base_data_check_shot()):
            #log
            self.logger.debug('Base data check failed, not creating shot.')
            return

        #alembic_path_list
        alembic_path_list = self.base_data_check_shot()[0]

        #delete_content
        self.alembic_functionality.delete_content(self.node)

        #iterate
        for alembic_path in alembic_path_list:

            #log
            self.logger.debug('\n\n-------------------------\n{0}\n-------------------------\n\n'.format(alembic_path))

            #create_prop_proxy
            self.alembic_functionality.create_prop_proxy(self.node, alembic_path)

        #layout children
        self.node.layoutChildren()

    


    
    #Utillity methods
    #------------------------------------------------------------------

    def print_alembic_object_path_list(self):
        """
        Print object path list.
        """

        pass

        

        

        
        
        

        

        



        

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

def create_prop(node):
    """
    Function to be used in the hdaModule of the Python operator.
    """

    #import
    from helga.houdini.import_export.alembic_import import alembic_import_shot_proxy
    reload(alembic_import_shot_proxy)

    #alembic_import_shot_instance
    alembic_import_shot_instance = alembic_import_shot_proxy.AlembicImportShotProxy(node)

    #create_prop
    alembic_import_shot_instance.create_prop()


def create_shot(node):
    """
    Function to be used in the hdaModule of the Python operator.
    """

    #import
    from helga.houdini.import_export.alembic_import import alembic_import_shot_proxy
    reload(alembic_import_shot_proxy)

    #alembic_import_shot_instance
    alembic_import_shot_instance = alembic_import_shot_proxy.AlembicImportShotProxy(node)

    #create_shot
    alembic_import_shot_instance.create_shot()






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