

"""
helga_launcher_maya_functionality
==========================================

Methods to set maya env. variables and launch maya.

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










#Functions
#------------------------------------------------------------------

def get_app_name():
    """
    Return string with app name
    """

    return 'maya'

def get_env_vars():
    """
    Get dict. with all neccessary maya environment variables.
    The dict has the form {'variable_name:[variable_content, variable_content]'}.
    """

    #import global_variables
    #------------------------------------------------------------------
    
    
    #Import variable
    do_reload = True

    #global_variables
    from helga.general.setup.global_variables import global_variables
    if(do_reload):reload(global_variables)

    #set maya env. vars.
    #------------------------------------------------------------------

    #environment_pathes_dict
    environment_pathes_dict = {'MAYA_SCRIPT_PATH':global_variables.MAYA_SCRIPTS_PATH_LIST,
                                    'PYTHONPATH':global_variables.MAYA_PYTHONPATH_LIST,
                                    'XBMLANGPATH':global_variables.MAYA_ICONS_PATH_LIST,
                                    'MAYA_PLUG_IN_PATH':global_variables.MAYA_PLUGIN_PATH_LIST,
                                    'MAYA_SHELF_PATH':global_variables.MAYA_SHELF_PATH_LIST}

    return environment_pathes_dict


def run(file_path = None):
    """
    Start Maya from subprocess
    """

    #Maya exe
    #------------------------------------------------------------------

    #MAYA_EXE
    MAYA_EXE = os.getenv('HELGA_MAYA_EXE', False)


    #Assemble command line
    #------------------------------------------------------------------
    
    #command
    command = r'"{0}"'.format(MAYA_EXE)
    #file path
    if(file_path):
        command += r' -file "{0}"'.format(file_path)

    print('Command: {0}'.format(command))
    
    #Execute
    #------------------------------------------------------------------
    
    #DETACHED_PROCESS
    DETACHED_PROCESS = 0x00000008
    #start
    subprocess.Popen(r'{0}'.format(command), shell = True, creationflags = DETACHED_PROCESS)







#Run if not imported
#------------------------------------------------------------------
if (__name__ == '__main__'):

    pass
    
    
    
    
        

        