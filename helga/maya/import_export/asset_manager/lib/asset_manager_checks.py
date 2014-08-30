

"""
asset_manager_checks
==========================================

AssetManager checks. This module separates test from the main module.
"""




#Import
#------------------------------------------------------------------
#python
import os
import sys
import logging
#maya
import pymel.core as pm




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

PIPELINE_ALEMBIC_PATH = global_variables.PIPELINE_ALEMBIC_PATH






#AssetManagerChecks class
#------------------------------------------------------------------
class AssetManagerChecks(object):

    def __new__(cls, *args, **kwargs):
        """
        AssetManagerChecks instance factory.
        """

        #asset_manager_checks_instance
        asset_manager_checks_instance = super(AssetManagerChecks, cls).__new__(cls, args, kwargs)

        return asset_manager_checks_instance

    
    def __init__(self, logging_level = logging.DEBUG):
        """
        Customize instance.
        """

        #super
        self.parent_class = super(AssetManagerChecks, self)
        self.parent_class.__init__()


        #instance variables
        #------------------------------------------------------------------

        
        #logger
        #------------------------------------------------------------------
        #logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logging_level = logging_level
        self.logger.setLevel(self.logging_level)




    #Big Checks
    #------------------------------------------------------------------

    def check_base_data(self, pynode_shot_metadata):
        """
        Check export base data.
        Return False or the needed data as list when True.
        """

        try:

            #check object existence
            if not(self.check_object_existence(pynode_shot_metadata)):
                
                #log
                self.logger.debug('Shot Metadata object is not existent anymore.')
                return False
            
            #shotname
            shotname = pynode_shot_metadata.shot_name.get()
            #no shotname
            if not(shotname):

                #log
                self.logger.debug('Shot Metadata object has no shotname.')
                return False



            #alembic_path
            alembic_path = self.get_alembic_path(pynode_shot_metadata)

            #shot_start
            shot_start = pynode_shot_metadata.shot_start.get()

            #shot_end
            shot_end = pynode_shot_metadata.shot_end.get()


            #check alembic_path existence
            if not(os.path.isdir(alembic_path)):

                #log
                self.logger.debug('Alembic path {0} does not exist.'.format(alembic_path))
                return False


            #check alembic_path subdirs existence
            alembic_subdir_name_list = ['cameras', 'props', 'chars']
            #iterate
            for alembic_subdir_name in alembic_subdir_name_list:

                #alembic_path_with_subdir
                alembic_path_with_subdir = os.path.join(alembic_path, alembic_subdir_name).replace('\\', '/')

                #check
                if not(os.path.isdir(alembic_path_with_subdir)):

                    #log
                    self.logger.debug('Alembic path subdirectory {0} does not exist.'.format(alembic_subdir_name))
                    self.logger.debug('Please make sure an alembic shot directory has the following subdirectories:\n\
{0}.'.format(alembic_subdir_name_list))
                    return False


            #check framerange
            if (shot_end < shot_start):

                #log
                self.logger.debug('Shot end frame {0} is smaller than shot start frame {1}'.format(shot_end, shot_start))
                return False

        except:

            return False


        return [alembic_path, shot_start, shot_end]


    def check_shot_data(self, pynode_shot_metadata):
        """
        Check metadata and data needed for shotcam export.
        Return False or the needed data (shotcam name) when True.
        """

        try:

            #check object existence (shotmetadata node)
            if not(self.check_object_existence(pynode_shot_metadata)):
                
                #log
                self.logger.debug('Shot Metadata object is not existent anymore.')
                return False
            
            
            #shot_cam
            shot_cam = pynode_shot_metadata.shot_cam.get()


            #check shotcam object existence (camera node)
            if not(self.check_object_existence(shot_cam)):
                
                #log
                self.logger.debug('Shot cam object {0} is not existent.'.format(shot_cam))
                return False


            #pynode_shot_cam
            pynode_shot_cam = pm.PyNode(shot_cam)

            #pynode_shot_cam_shape
            pynode_shot_cam_shape = pynode_shot_cam.getShape()

            #check shotcam shape exists
            if not(pynode_shot_cam_shape):
                
                #log
                self.logger.debug('Shot cam object {0} has no shape and is therefore probably not a Camera node.'.format(shot_cam))
                return False


            #check shotcam shape object is of type camera
            if not(type(pynode_shot_cam_shape) is pm.nodetypes.Camera):
                
                #log
                self.logger.debug('Shot cam object {0} is not of type Camera. It is of type {1}.'.format(shot_cam, type(pynode_shot_cam_shape).__name__))
                return False

        except:

            return False


        return shot_cam


    def check_prop_data(self, pynode_prop_metadata):
        """
        Check metadata and data needed for prop export.
        Return False or the needed data (asset_name, namespace) when True.
        """

        try:

            #check object existence (pynode_prop_metadata)
            if not(self.check_object_existence(pynode_prop_metadata)):
                
                #log
                self.logger.debug('Prop Metadata object is not existent anymore.')
                return False
            
            
            #asset_name
            asset_name = pynode_prop_metadata.asset_name.get()
            #check
            if not (asset_name):
                
                #log
                self.logger.debug('Prop metadata node {0} has no asset_name.'.format(pynode_prop_metadata.name()))
                return False

            
            #namespace
            namespace = pynode_prop_metadata.namespace()
            #check
            if not (namespace):
                
                #log
                self.logger.debug('Prop metadata node {0} has no namespace.'.format(pynode_prop_metadata.name()))
                return False

        except:

            return False


        return [asset_name, namespace]


    def check_char_data(self, pynode_char_metadata):
        """
        Check metadata and data needed for char export.
        Return False or the needed data (asset_name, namespace) when True.
        """

        try:

            #check object existence (pynode_char_metadata)
            if not(self.check_object_existence(pynode_char_metadata)):
                
                #log
                self.logger.debug('Char Metadata object is not existent anymore.')
                return False
            
            
            #asset_name
            asset_name = pynode_char_metadata.asset_name.get()
            #check
            if not (asset_name):
                
                #log
                self.logger.debug('Char metadata node {0} has no asset_name.'.format(pynode_char_metadata.name()))
                return False

            
            #namespace
            namespace = pynode_char_metadata.namespace()
            #check
            if not (namespace):
                
                #log
                self.logger.debug('Char metadata node {0} has no namespace.'.format(pynode_char_metadata.name()))
                return False

        except:

            return False


        return [asset_name, namespace]


    #Atomic Checks
    #------------------------------------------------------------------

    def check_object_existence(self, object_to_test):
        """
        Check if MObject for object_to_test still exists.
        Can be a string, unicode or PyNode
        """

        #string or unicode
        if (type(object_to_test) is str or
            type(object_to_test) is unicode):

            return self.check_object_existence_for_name(object_to_test)

        #PyNode
        else:

            return self.check_object_existence_for_pynode(object_to_test)


    def check_object_existence_for_pynode(self, pynode):
        """
        Check if MObject for PyNode still exists.
        """

        try:
            pm.PyNode(pynode.name())
        except:
            return False

        return True


    def check_object_existence_for_name(self, object_name):
        """
        Check if MObject for PyNode still exists.
        """

        return pm.objExists(object_name)


    #Methods
    #------------------------------------------------------------------

    def get_alembic_path(self, pynode_shot_metadata):
        """
        Return alembic path either from alembic_path attribute
        on pynode_shot_metadata if set, or build it from shot_name
        and globals (default).
        """

        #alembic_path_from_attribute
        alembic_path_from_attribute = pynode_shot_metadata.alembic_path.get()

        #if true return
        if(alembic_path_from_attribute):
            return alembic_path_from_attribute


        #build path from shot_name and globals (THIS IS THE DEFAULT)

        #shotname
        shotname = pynode_shot_metadata.shot_name.get()

        #alembic_path
        alembic_path = os.path.join(PIPELINE_ALEMBIC_PATH, shotname).replace('\\', '/')

        #return
        return alembic_path


    




    


