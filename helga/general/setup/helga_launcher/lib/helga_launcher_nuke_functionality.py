

"""
helga_launcher_nuke_functionality
==========================================

Methods to set nuke env. variables and launch nuke.

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

    return 'nuke'

def get_env_vars():
    """
    Set complete pipeline env. vars. from global_variables module.
    This function depends on the correctly set base env. vars.
    """


    #import global_variables
    #------------------------------------------------------------------
    
    
    #Import variable
    do_reload = True

    #global_variables
    from helga.general.setup.global_variables import global_variables
    if(do_reload):reload(global_variables)



    #Environment variables
    #------------------------------------------------------------------

    #environment_pathes_dict
    environment_pathes_dict = {'NUKE_PATH': global_variables.NUKE_INIT_PATH}

    return environment_pathes_dict


def run(file_path = None, nuke_flavour = '--nukex'):
    """
    Start Nuke from subprocess
    """


    #Nuke exe
    #------------------------------------------------------------------

    #NUKE_EXE
    NUKE_EXE = os.getenv('HELGA_NUKE_EXE', False)
    


    #Assemble command line
    #------------------------------------------------------------------
    
    #command
    command = r'"{0}"'.format(NUKE_EXE)
    #file_path
    if(file_path):
        command += r' "{0}"'.format(file_path)
    #nuke_flavour
    if(nuke_flavour):
        command += r' {0}'.format(nuke_flavour)

    print('Command: {0}'.format(command))

    #Maya exe
    #------------------------------------------------------------------
    
    #DETACHED_PROCESS
    DETACHED_PROCESS = 0x00000008

    try:
        #start
        subprocess.Popen(r'{0}'.format(command), shell = True, creationflags = DETACHED_PROCESS)

    except:

        #log
        print('Detached process not supported on current operating system.')

        #start
        subprocess.Popen(r'{0}'.format(command), shell = True)







#Run if not imported
#------------------------------------------------------------------
if (__name__ == '__main__'):

    pass
    
    
    
    
        

        