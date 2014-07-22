

"""
helga_launcher_favorites_functionality
==========================================

Methods to set/remove favorites.

-----------------------
"""





#Import
#------------------------------------------------------------------
#python
import sys
import os
import functools
import logging
import subprocess
import winshell
import time
import re
import shutil






#Globals
#------------------------------------------------------------------

def get_pipeline_icon_path():
    """
    Return pipeline icon path
    """

    #Import variable
    do_reload = True

    #global_variables
    from helga.general.setup.global_variables import global_variables
    if(do_reload):reload(global_variables)

    #pipeline_icon_path
    pipeline_icon_path = clean_path_for_favorites(global_variables.PIPELINE_ICON_PATH)

    return pipeline_icon_path




def clean_path_for_favorites(path):
    """
    Modify path to match favorite neccessities.
    """

    #remove forward slashes
    path = path.replace('/', '\\')

    return path


def get_favorites_dict():
    """
    Return favorites dict
    """
    
    #Import variable
    do_reload = True

    #global_variables
    from helga.general.setup.global_variables import global_variables
    if(do_reload):reload(global_variables)

    #pipeline_base_path_clean
    pipeline_base_path_clean = clean_path_for_favorites(global_variables.PIPELINE_BASE_PATH)


    #favorites_dict
    favorites_dict = dict(
    helga_rnd = '{0}\\Production\\rnd'.format(pipeline_base_path_clean),
    helga_scripts = '{0}\\Production\\scripts'.format(pipeline_base_path_clean),
    helga_2d = '{0}\\Production\\2d'.format(pipeline_base_path_clean),
    helga_3d = '{0}\\Production\\3d'.format(pipeline_base_path_clean),
    helga_assets = '{0}\\Production\\3d\\maya\\scenes\\assets'.format(pipeline_base_path_clean),
    helga_assets_work = '{0}\\Production\\3d\\maya\\scenes\\assets\\work'.format(pipeline_base_path_clean),
    helga_shots = '{0}\\Production\\3d\\maya\\scenes\\shots'.format(pipeline_base_path_clean),
    helga_tools = '{0}\\Production\\scripts\\deploy\\helga\\bin'.format(pipeline_base_path_clean)
    )


    return favorites_dict


def get_desktop_shortcuts_dict():
    """
    Return desktop shortcuts dict
    """
    
    #Import variable
    do_reload = True

    #global_variables
    from helga.general.setup.global_variables import global_variables
    if(do_reload):reload(global_variables)

    #pipeline_base_path_clean
    pipeline_base_path_clean = clean_path_for_favorites(global_variables.PIPELINE_BASE_PATH)


    #desktop_shortcuts_dict
    desktop_shortcuts_dict = dict(
    helga_launcher = '{0}\\Production\\scripts\\deploy\\helga\\bin\\HelgaLauncher\\batch\\helga_launcher.bat'.format(pipeline_base_path_clean),
    helga_launcher_maya = '{0}\\Production\\scripts\\deploy\\helga\\bin\\HelgaLauncher\\batch\\helga_launcher_maya.bat'.format(pipeline_base_path_clean),
    helga_launcher_nuke = '{0}\\Production\\scripts\\deploy\\helga\\bin\\HelgaLauncher\\batch\\helga_launcher_nuke.bat'.format(pipeline_base_path_clean),
    helga_launcher_houdini = '{0}\\Production\\scripts\\deploy\\helga\\bin\\HelgaLauncher\\batch\\helga_launcher_houdini.bat'.format(pipeline_base_path_clean)
    )


    return desktop_shortcuts_dict




#Favorites
#------------------------------------------------------------------

def get_favorite_directory():
    """
    Return favorite directory
    """
    
    return winshell.folder("Favorites")


def get_links_directory():
    """
    Return user Links directory. Despite its name, this method is used in add_favorites()
    """
    
    return os.path.join(winshell.folder("profile"), 'Links')


def add_favorites():
    """
    Add favorites.
    """

    #favorites_dict
    favorites_dict = get_favorites_dict()

    #favorites_dir
    favorites_dir = get_links_directory()

    #icons_dir
    icons_dir = get_pipeline_icon_path()

    #icon_path
    icon_path = os.path.join(icons_dir, 'iconhelgabright.ico')
    
    
    #iterate and set favorites
    for shortcut_name in sorted(favorites_dict.keys()):
        
        #target_path
        target_path = favorites_dict[shortcut_name]

        try:
            
            #create
            create_shortcut(favorites_dir, shortcut_name, target_path, '', icon_path)

            #append status
            print('Added favorite: {0} --> {1}'.format(shortcut_name, target_path))

        except:
            
            #append status
            print('Error adding favorite: {0} --> {1}'.format(shortcut_name, target_path))


#remove_favorites
def remove_favorites():
    """
    Remove favorites.
    """

    #favorites_dict
    favorites_dict = get_favorites_dict()
    

    #iterate and set favorites
    for shortcut_name, target_path in favorites_dict.iteritems():
        
        try:
            
            #shortcut_path
            shortcut_path = os.path.join(get_links_directory(), '{0}.lnk'.format(shortcut_name))

            #if isfile delete
            if(os.path.isfile(shortcut_path)):
                
                #delete
                os.remove(shortcut_path)

            #append status
            print('Deleted favorite: {0}'.format(shortcut_name))

        except:

            #append status
            print('Error deleting favorite: {0}'.format(shortcut_name))







#Desktop shortcuts
#------------------------------------------------------------------


#get_desktop_directory
def get_desktop_directory():
    """
    Return desktop directory
    """
    
    return winshell.desktop()


def create_desktop_shortcuts():
    """
    Create shortcuts to the helga_launcher on the desktop
    """

    #desktop_dir
    desktop_dir = get_desktop_directory()

    #desktop_shortcuts_dict
    desktop_shortcuts_dict = get_desktop_shortcuts_dict()

    #icons_dir
    icons_dir = get_pipeline_icon_path()

    #icon_path
    icon_path = os.path.join(icons_dir, 'iconhelgabright.ico')


    #iterate and set favorites
    for shortcut_name in sorted(desktop_shortcuts_dict.keys()):
        
        #target_path
        target_path = desktop_shortcuts_dict[shortcut_name]

        
        #icons matching GUI
        #maya
        if ('maya' in shortcut_name):
            icon_path = os.path.join(icons_dir, 'iconhelgaorange.ico')
        #maya
        if ('houdini' in shortcut_name):
            icon_path = os.path.join(icons_dir, 'iconhelgablue.ico')
        #nuke
        if ('nuke' in shortcut_name):
            icon_path = os.path.join(icons_dir, 'iconhelgayellow.ico')


        

        try:
            
            #create
            create_shortcut(desktop_dir, shortcut_name, target_path, '', icon_path)

            #append status
            print('Added desktop shortcut: {0} --> {1}'.format(shortcut_name, target_path))

        except:
            
            #append status
            print('Error adding desktop shortcut: {0} --> {1}'.format(shortcut_name, target_path))


def remove_desktop_shortcuts():
    """
    Remove desktop shortcuts
    """

    #desktop_shortcuts_dict
    desktop_shortcuts_dict = get_desktop_shortcuts_dict()
    

    #iterate and set favorites
    for shortcut_name, target_path in desktop_shortcuts_dict.iteritems():
        
        try:
            
            #shortcut_path
            shortcut_path = os.path.join(get_desktop_directory(), '{0}.lnk'.format(shortcut_name))

            #if isfile delete
            if(os.path.isfile(shortcut_path)):
                
                #delete
                os.remove(shortcut_path)

            #append status
            print('Deleted favorite: {0}'.format(shortcut_name))

        except:

            #append status
            print('Error deleting favorite: {0}'.format(shortcut_name))






#Create Shortcut
#------------------------------------------------------------------

#create_shortcut
def create_shortcut(shortcut_dir, shortcut_name, target_path, description = '', icon_path = ''):
    """
    Add shortcut
    """

    #shortcut_path
    shortcut_path = os.path.join(shortcut_dir, '{0}.lnk'.format(shortcut_name))


    #CreateShortcut
    winshell.CreateShortcut(Path = shortcut_path,
                            Target = target_path,
                            Icon = (icon_path, 0),
                            Description = description)

    #log
    print('Sucessfully created/updated shortcut: {0}'.format(shortcut_path))





#Run if not imported
#------------------------------------------------------------------
if (__name__ == '__main__'):

    pass
    
    
    
    
        

        