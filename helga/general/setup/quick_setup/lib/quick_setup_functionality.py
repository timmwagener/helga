

"""
quick_setup_functionality
==========================================

Module that holds the functionality for quick_setup.
"""










#Import
#------------------------------------------------------------------
#python
import sys
import os
import logging
import re
import shutil
import winshell
import time






#Functions
#------------------------------------------------------------------

#get_user
def get_user():
    """
    Get the currently logged on user or Unknown if False.
    """
    
    return os.getenv('USERNAME', 'Unknown')


#get_pipeline_base_path
def get_pipeline_base_path():
    """
    Get pipeline base path. Hardcoded or from environment variable.
    The environment variable has preference.
    """
    
    #PIPELINE_BASE_PATH
    PIPELINE_BASE_PATH = r'//bigfoot/grimmhelga'

    #if env. var. exists, replace
    if (os.getenv('HELGA_PIPELINE_BASE_PATH', False)):
        PIPELINE_BASE_PATH = os.getenv('HELGA_PIPELINE_BASE_PATH', False)

    return PIPELINE_BASE_PATH


#get_pipeline_scripts_base_path
def get_pipeline_scripts_base_path():
    """
    Get pipeline scripts base path.
    """
    
    #PIPELINE_BASE_PATH
    PIPELINE_BASE_PATH = get_pipeline_base_path()
    
    #PIPELINE_SCRIPTS_BASE_PATH
    PIPELINE_SCRIPTS_BASE_PATH = PIPELINE_BASE_PATH + r'/Production/scripts/deploy/helga'

    return PIPELINE_SCRIPTS_BASE_PATH


#copy_file
def copy_file(source_file, source_dir, destination_dir):
    """
    Copy file.
    """
    
    source = source_dir + '/' +source_file
    
    shutil.copy(source, destination_dir)


#get_time_string
def get_time_string():
    """
    Return time string.
    """

    #time_string
    time_string = ''
    
    try:
        
        #localtime
        localtime   = time.localtime()
        #assign time_string
        time_string  = time.strftime("%Y%m%d%H%M%S", localtime)
    
    except:

        print('Aquiring time string failed')
        return ''
    
    return time_string






#User Destination
#----------------------------------------------------

#get_user_setup_destination_dir
def get_user_setup_destination_dir(dcc, version = None):
    
    if (dcc == 'maya'):
        return get_user_setup_destination_dir_maya(version)
    elif (dcc == 'nuke'):
        return get_user_setup_destination_dir_nuke()
    elif (dcc == 'houdini'):
        return get_user_setup_destination_dir_houdini(version)


#get_user_setup_destination_dir_maya
def get_user_setup_destination_dir_maya(version):

    if (version == None):
        print('Could not aquire user setup directory for maya. Please supply a version')
        return None

    path_start = 'C:/Users/'
    username = get_user()
    path_end = '/Documents/maya/{0}/scripts'.format(version)
    
    return path_start + username + path_end


#get_user_setup_destination_dir_nuke
def get_user_setup_destination_dir_nuke():

    path_start = 'C:/Users/'
    username = get_user()
    path_end = '/.nuke'
    
    return path_start + username + path_end


#get_user_setup_destination_dir_houdini
def get_user_setup_destination_dir_houdini(version):

    if (version == None):
        print('Could not aquire user setup directory for maya. Please supply a version')
        return None

    path_start = 'C:/Users/'
    username = get_user()
    path_end = '/Documents/houdini{0}'.format(version)
    
    return path_start + username + path_end







#Pipeline Source
#----------------------------------------------------

#get_user_setup_source_dir
def get_user_setup_source_dir(dcc):
    
    if (dcc == 'maya'):
        return get_user_setup_source_dir_maya()
    elif (dcc == 'nuke'):
        return get_user_setup_source_dir_nuke()
    elif (dcc == 'houdini'):
        return get_user_setup_source_dir_houdini()


#get_user_setup_source_dir_maya
def get_user_setup_source_dir_maya():

    #maya_user_setup_source_dir
    maya_user_setup_source_dir = get_pipeline_scripts_base_path() + r'/helga/maya/setup/userSetup'

    return maya_user_setup_source_dir


#get_user_setup_source_dir_nuke
def get_user_setup_source_dir_nuke():

    #nuke_user_setup_source_dir
    nuke_user_setup_source_dir = get_pipeline_scripts_base_path() + r'/helga/nuke/setup/init'

    return nuke_user_setup_source_dir


#get_user_setup_source_dir_houdini
def get_user_setup_source_dir_houdini():

    #houdini_user_setup_source_dir
    houdini_user_setup_source_dir = get_pipeline_scripts_base_path() + r'/helga/houdini/setup/env'

    return houdini_user_setup_source_dir


#get_nuke_menu_source_dir
def get_nuke_menu_source_dir():

    #nuke_menu_source_dir
    nuke_menu_source_dir = get_pipeline_scripts_base_path() + r'/helga/nuke/setup/menu'

    return nuke_menu_source_dir







#Favorites
#----------------------------------------------------

#get_favorite_directory
def get_favorite_directory():
    """
    Return favorite directory
    """
    
    return winshell.folder("Favorites")


#get_links_directory
def get_links_directory():
    """
    Return user Links directory
    """
    
    return os.path.join(winshell.folder("profile"), 'Links')



#add_favorite
def add_favorite(shortcut_name, target_path, description = ''):
    """
    Add favorite shortcut. If shortcut already exists in Links, the
    shortcut will be updated with the given path.
    """

    #shortcut_path
    shortcut_path = os.path.join(get_links_directory(), '{0}.lnk'.format(shortcut_name))
    
    
    #create shortcut
    with winshell.shortcut(shortcut_path) as shortcut:
        shortcut.path = target_path
        shortcut.description = description

    #log
    print('Sucessfully created/updated favorite: {0}'.format(shortcut_path))





