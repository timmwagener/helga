

"""
helga_launcher_ocio_functionality
==========================================

Methods to set ocio env. variables.

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

    return 'ocio'


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



    #Environment variables
    #------------------------------------------------------------------

    #environment_pathes_dict
    environment_pathes_dict = {'OCIO': global_variables.OCIO_PATH}

    return environment_pathes_dict


#Run if not imported
#------------------------------------------------------------------
if (__name__ == '__main__'):

    pass
    
    
    
    
        

        