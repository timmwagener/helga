

"""
alembic_import_shot
==========================================

GUI to import Shot Alembics according to our pipeline standards.

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










#AlembicImportShot class
#------------------------------------------------------------------
class AlembicImportShot(object):
    """
    AlembicImportShot
    """


    def __new__(cls, *args, **kwargs):
        """
        AlembicImportShot instance factory.
        """

        #alembic_import_shot_instance
        alembic_import_shot_instance = super(AlembicImportShot, cls).__new__(cls, args, kwargs)

        return alembic_import_shot_instance

    
    def __init__(self,
                node = None,
                logging_level = logging.DEBUG):
        """
        Customize instance.
        """

        #super
        self.parent_class = super(AlembicImportShot, self)
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

    def base_data_check_shot(self):
        """
        Check base data from the node and return either False
        or the needed data. (Equivalent to True).
        The returned data is [alembic_path] 
        """

        pass


    def base_data_check_prop(self):
        """
        Check base data for props.
        The returned data is [alembic_path, alembic_highpoly_rendergeo_dir]
        """

        #alembic_highpoly_rendergeo_dir
        alembic_highpoly_rendergeo_dir = self.alembic_functionality.get_parm_value(self.node, 'alembic_highpoly_rendergeo_dir')
        
        #is False
        if not (alembic_highpoly_rendergeo_dir):
            #log
            self.logger.debug('Parameter alembic highpoly rendergeo dir empty.')
            return False

        #dir exists
        if not (os.path.isdir(alembic_highpoly_rendergeo_dir)):
            #log
            self.logger.debug('Alembic highpoly rendergeo dir {0} does not exist.'.format(alembic_highpoly_rendergeo_dir))
            return False



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
        return [alembic_path, alembic_highpoly_rendergeo_dir]



    #Creation
    #------------------------------------------------------------------

    def create_shot(self):
        """
        Create shot.
        """

        #base_data_check_shot
        if not (self.base_data_check_shot()):
            #log
            self.logger.debug('Base data check failed, not creating shot.')
            return

        #create_character_hierarchy
        self.alembic_functionality.create_shot(self.node)


    def create_prop(self):
        """
        Create prop.
        """

        #base_data_check_prop
        if not (self.base_data_check_prop()):
            #log
            self.logger.debug('Base data check failed, not creating prop.')
            return

        #create_character_hierarchy
        self.alembic_functionality.create_prop(self.node)


    
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

def create_shot(node):
    """
    Function to be used in the hdaModule of the Python operator.
    """

    #import
    from helga.houdini.import_export.alembic_import import alembic_import_shot
    reload(alembic_import_shot)

    #alembic_import_shot_instance
    alembic_import_shot_instance = alembic_import_shot.AlembicImportShot(node)

    #create_shot
    alembic_import_shot_instance.create_shot()


def create_prop(node):
    """
    Function to be used in the hdaModule of the Python operator.
    """

    #import
    from helga.houdini.import_export.alembic_import import alembic_import_shot
    reload(alembic_import_shot)

    #alembic_import_shot_instance
    alembic_import_shot_instance = alembic_import_shot.AlembicImportShot(node)

    #create_prop
    alembic_import_shot_instance.create_prop()









#Test
#------------------------------------------------------------------

if (__name__ == '__main__'):

    pass