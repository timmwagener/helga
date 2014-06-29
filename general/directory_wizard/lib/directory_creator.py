



"""
directory_creator
==========================================

Module to create directories.

-----------------------
"""







#Import
#------------------------------------------------------------------
#python
import sys
import os
import functools
import logging
#PySide
from PySide import QtGui
from PySide import QtCore
from PySide import QtUiTools


#Import variable
do_reload = True

#global_variables
from helga.general.setup.global_variables import global_variables
if(do_reload):reload(global_variables)

#global_functions
from helga.general.setup.global_functions import global_functions
if(do_reload):reload(global_functions)







#DirectoryCreator class
#------------------------------------------------------------------

class DirectoryCreator(object):
    
    #Constructor
    def __init__(self,
                asset_name, 
                root_directory,
                logging_level = logging.DEBUG):
        
        #super class init
        super(DirectoryCreator, self).__init__()

        #asset_name
        self.asset_name = asset_name
        #root_directory
        self.root_directory = root_directory
        #asset_directory
        self.asset_directory = os.path.join(self.root_directory, 
                                            self.asset_name)
        #directory_list
        self.directory_list = []
        #directory_type
        self.directory_type = 'base'

        
        #logger
        #------------------------------------------------------------------
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logging_level = logging_level
        self.logger.setLevel(self.logging_level)
        

    

    #Create Methods
    #------------------------------------------------------------------
    #------------------------------------------------------------------
    
    #create_directories
    def create_directories(self, name_list = None, parent_directory = None):
        """
            Recurse self.directory_list and create directories.
        """

        #name_list None
        if (name_list is None):
            name_list = self.directory_list

        #parent_directory None
        if (parent_directory is None):
            parent_directory = self.asset_directory




        #create parent_directory if non existant
        if not(os.path.isdir(parent_directory)):
            
            #create directory
            os.makedirs(parent_directory)

        #iterate name_list
        for index, name_entry in enumerate(name_list):

            #if directory_entry is string
            if(isinstance(name_entry, str)):

                #target_directory
                target_directory = os.path.join(parent_directory, name_entry)

                #create directory
                os.makedirs(target_directory)

                #log
                self.logger.debug(target_directory)
        
            #if directory_entry is list recurse
            elif(isinstance(name_entry, list)):

                #new_parent_directory
                new_parent_directory = os.path.join(parent_directory, name_list[index-1])

                #create_directories
                self.create_directories(name_entry, new_parent_directory)






    #Getter & Setter
    #------------------------------------------------------------------
    #------------------------------------------------------------------

    #get_asset_directory
    def get_asset_directory(self):
        """
            Return self.asset_directory
        """

        return self.asset_directory


    #get_directory_type
    def get_directory_type(self):
        """
            Return self.directory_type
        """

        return self.directory_type




#CharacterDirectoryCreator class
#------------------------------------------------------------------

class CharacterDirectoryCreator(DirectoryCreator):
    
    #Constructor
    def __init__(self,
                asset_name,
                root_directory,
                logging_level = logging.DEBUG):
        
        #super class init
        super(CharacterDirectoryCreator, self).__init__(asset_name, root_directory)


        #directory_list
        #------------------------------------------------------------------
        self.directory_list = global_variables.CHARACTER_DIRECTORY_LIST
        self.directory_type = 'character'


        #logger
        #------------------------------------------------------------------
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logging_level = logging_level
        self.logger.setLevel(self.logging_level)




#PropDirectoryCreator class
#------------------------------------------------------------------

class PropDirectoryCreator(DirectoryCreator):
    
    #Constructor
    def __init__(self,
                asset_name,
                root_directory,
                logging_level = logging.DEBUG):
        
        #super class init
        super(PropDirectoryCreator, self).__init__(asset_name, root_directory)


        #directory_list
        #------------------------------------------------------------------
        self.directory_list = global_variables.PROP_DIRECTORY_LIST
        self.directory_type = 'prop'


        #logger
        #------------------------------------------------------------------
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logging_level = logging_level
        self.logger.setLevel(self.logging_level)



#ShotDirectoryCreator class
#------------------------------------------------------------------

class ShotDirectoryCreator(DirectoryCreator):
    
    #Constructor
    def __init__(self,
                asset_name,
                root_directory,
                logging_level = logging.DEBUG):
        
        #super class init
        super(ShotDirectoryCreator, self).__init__(asset_name, root_directory)


        #directory_list
        #------------------------------------------------------------------
        self.directory_list = global_variables.SHOT_DIRECTORY_LIST
        self.directory_type = 'shot'


        #logger
        #------------------------------------------------------------------
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logging_level = logging_level
        self.logger.setLevel(self.logging_level)



#CompDirectoryCreator class
#------------------------------------------------------------------

class CompDirectoryCreator(DirectoryCreator):
    
    #Constructor
    def __init__(self,
                asset_name,
                root_directory,
                logging_level = logging.DEBUG):
        
        #super class init
        super(CompDirectoryCreator, self).__init__(asset_name, root_directory)


        #directory_list
        #------------------------------------------------------------------
        self.directory_list = global_variables.COMP_DIRECTORY_LIST
        self.directory_type = 'comp'


        #logger
        #------------------------------------------------------------------
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logging_level = logging_level
        self.logger.setLevel(self.logging_level)
    


#PhotoscanDirectoryCreator class
#------------------------------------------------------------------

class PhotoscanDirectoryCreator(DirectoryCreator):
    
    #Constructor
    def __init__(self,
                asset_name,
                root_directory,
                logging_level = logging.DEBUG):
        
        #super class init
        super(PhotoscanDirectoryCreator, self).__init__(asset_name, root_directory)


        #directory_list
        #------------------------------------------------------------------
        self.directory_list = global_variables.PHOTOSCAN_DIRECTORY_LIST
        self.directory_type = 'photoscan'


        #logger
        #------------------------------------------------------------------
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logging_level = logging_level
        self.logger.setLevel(self.logging_level)    
    
    
    






#Test
#------------------------------------------------------------------

if (__name__ == '__main__'):

    #test_root_dir
    test_root_dir = 'c:/symlinks/temp/directory_creator_test'
    #test_prop_asset_name
    test_prop_asset_name = 'table'
    #test_photoscan_asset_name
    test_photoscan_asset_name = 'stairs_horizontal'

    #divider
    global_functions.divider()

    #prop_directory_creator
    prop_directory_creator = PropDirectoryCreator(test_prop_asset_name, test_root_dir)
    prop_directory_creator.create_directories()
    print('Asset directory: {0}'.format(prop_directory_creator.get_asset_directory()))
        
    #divider
    global_functions.divider()

    #photoscan_directory_creator
    photoscan_directory_creator = PhotoscanDirectoryCreator(test_photoscan_asset_name, test_root_dir)
    photoscan_directory_creator.create_directories()
    print('Asset directory: {0}'.format(photoscan_directory_creator.get_asset_directory()))    
        

