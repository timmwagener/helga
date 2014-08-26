

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
            
            
            #alembic_path
            alembic_path = pynode_shot_metadata.alembic_path.get()

            #shot_start
            shot_start = pynode_shot_metadata.shot_start.get()

            #shot_end
            shot_end = pynode_shot_metadata.shot_end.get()


            #check alembic_path existence
            if not(os.path.isdir(alembic_path)):

                #log
                self.logger.debug('Alembic path {0} does not exist.')
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


    




    


