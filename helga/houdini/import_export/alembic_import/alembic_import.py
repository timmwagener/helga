

"""
alembic_import
==========================================

GUI to import Alembics according to our pipeline standards.

It takes care of:

#. Characters

In the future it will also import props and directories of props.
Cameras (for our shotcam setup) dont need a special import.
They work out of the box.

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









    #Methods
    #------------------------------------------------------------------

    def base_data_check(self):
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



    def create_hierarchy(self, hierarchy_type = None):
        """
        Create hierarchy.
        """

        #base_data_check
        if not (self.base_data_check()):
            #log
            self.logger.debug('Base data check failed, not creating Hierarchy.')
            return

        

        #char
        if(hierarchy_type == 'char'):
            self.create_character_hierarchy()
        
        #prop
        elif(hierarchy_type == 'prop'):
            self.create_prop_hierarchy()


    def create_character_hierarchy(self):
        """
        Create character hierarchy.
        """

        #create_character_hierarchy
        self.alembic_functionality.create_character_hierarchy(self.node)


    def create_prop_hierarchy(self):
        """
        Create prop hierarchy.
        """

        pass


    def print_alembic_object_path_list(self):
        """
        Create hierarchy.
        """

        #base_data_check
        if not (self.base_data_check()):
            #log
            self.logger.debug('Base data check failed, not printing object path list.')
            return


        #alembic_path
        alembic_path = self.base_data_check()[0]

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


    









    












#Test
#------------------------------------------------------------------

if (__name__ == '__main__'):

    #run
    run()