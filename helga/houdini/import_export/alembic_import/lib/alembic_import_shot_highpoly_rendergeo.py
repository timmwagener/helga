

"""
alembic_import_shot_highpoly_rendergeo
==========================================

GUI to import Shot Highpoly Alembics according to our pipeline standards.

This module is mainly needed because of the weird Alembic
import in Houdini, that generates all these Alembic xform nodes
and geometry nodes without all the usual parameters for subdiving etc.

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











#AlembicImportShotHighpolyRendergeo class
#------------------------------------------------------------------
class AlembicImportShotHighpolyRendergeo(object):
    """
    AlembicImportShotHighpolyRendergeo
    """


    def __new__(cls, *args, **kwargs):
        """
        AlembicImportShotHighpolyRendergeo instance factory.
        """

        #alembic_import_shot_highpoly_rendergeo_instance
        alembic_import_shot_highpoly_rendergeo_instance = super(AlembicImportShotHighpolyRendergeo, cls).__new__(cls, args, kwargs)

        return alembic_import_shot_highpoly_rendergeo_instance

    
    def __init__(self,
                node = None,
                logging_level = logging.DEBUG):
        """
        Customize instance.
        """

        #super
        self.parent_class = super(AlembicImportShotHighpolyRendergeo, self)
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
        The returned data is [alembic_path, alembic_highpoly_rendergeo_dir]
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


        #return
        return [alembic_path, alembic_highpoly_rendergeo_dir]


    def base_data_check_shot(self):
        """
        Check base data from the node and return either False
        or the needed data. (Equivalent to True).
        The returned data is [checked_alembic_path_list, alembic_highpoly_rendergeo_dir].
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


        #checked_alembic_path_list
        checked_alembic_path_list = []

        #iterate
        for alembic_path in alembic_path_list:

            #object_path_list
            object_path_list = self.alembic_functionality.get_alembic_object_path_list(alembic_path)
            #object_path_list empty
            if not (object_path_list):
                #log
                self.logger.debug('Object path list for alembic {0} empty. Continuing'.format(alembic_path))
                continue

            #iterate, check and create
            for object_path in object_path_list:

                #helga_locator_attr_exists
                helga_locator_attr_exists = self.alembic_functionality.alembic_attribute_exists(alembic_path, object_path, 'helga_locator')

                #helga_highpoly_rendergeo_attr_exists
                helga_highpoly_rendergeo_attr_exists = self.alembic_functionality.alembic_attribute_exists(alembic_path, object_path, 'helga_highpoly_rendergeo')

                #if attr exists append and break
                if (helga_locator_attr_exists and helga_highpoly_rendergeo_attr_exists):

                    #append
                    checked_alembic_path_list.append(alembic_path)
                    break

        #checked_alembic_path_list empty
        if not (checked_alembic_path_list):
            #log
            self.logger.debug('checked_alembic_path_list empty. Alembic dir {0} does not seem to contain alembic files with helga_highpoly_rendergeo attribute.'.format(alembic_dir))
            return False


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


        #return
        return [checked_alembic_path_list, alembic_highpoly_rendergeo_dir]



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
        alembic_path, alembic_highpoly_rendergeo_dir = self.base_data_check_prop()

        #log
        self.logger.debug('\n\n-------------------------\n{0}\n-------------------------\n\n'.format(alembic_path))

        #create_prop_highpoly_rendergeo
        self.alembic_functionality.create_prop_highpoly_rendergeo(self.node, 
                                                                    alembic_path, 
                                                                    alembic_highpoly_rendergeo_dir)


    def create_shot(self):
        """
        Create shot.
        """

        #base_data_check_shot
        if not (self.base_data_check_shot()):
            #log
            self.logger.debug('Base data check failed, not creating shot.')
            return

        #alembic_path_list, alembic_highpoly_rendergeo_dir
        alembic_path_list, alembic_highpoly_rendergeo_dir = self.base_data_check_shot()


        #iterate
        for alembic_path in alembic_path_list:

            #log
            self.logger.debug('\n\n-------------------------\n{0}\n-------------------------\n\n'.format(alembic_path))

            #create_prop_highpoly_rendergeo
            self.alembic_functionality.create_prop_highpoly_rendergeo(self.node, 
                                                                        alembic_path, 
                                                                        alembic_highpoly_rendergeo_dir)

        #layout children
        self.node.layoutChildren()

    


    
    
        
        
        

        

        



        

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

    pass