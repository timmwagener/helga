


#Imports
#------------------------------------------------------------------

#python
import os
import sys
import re
import shutil
import getpass
#houdini
import hou



#Import variable
do_reload = True

#global_variables
from helga.general.setup.global_variables import global_variables
if(do_reload):reload(global_variables)

#global_functions
from helga.general.setup.global_functions import global_functions
if(do_reload):reload(global_functions)








#init Globals
#------------------------------------------------------------------

# USER
USER = getpass.getuser()

#Assign all global variables to only use local ones later on
PIPELINE_SCRIPTS_BASE_PATH = global_variables.PIPELINE_SCRIPTS_BASE_PATH
PIPELINE_HDRI_PATH = global_variables.PIPELINE_HDRI_PATH
OCIO_LIN_TO_SRGB_SPI_LUT_HOUDINI = global_variables.OCIO_LIN_TO_SRGB_SPI_LUT_HOUDINI
HOUDINI_OTL_PATH = global_variables.HOUDINI_OTL_PATH
PIPELINE_ALEMBIC_PATH = global_variables.PIPELINE_ALEMBIC_PATH
PIPELINE_FUR_PATH = global_variables.PIPELINE_FUR_PATH
PIPELINE_TEXTURES_PATH = global_variables.PIPELINE_TEXTURES_PATH
PIPELINE_RENDER_PATH = global_variables.PIPELINE_RENDER_PATH

# FX specific
FX_USER_LIST = ['jfranz']









#Print USER
#------------------------------------------------------------------

print('User: {0}'.format(USER))







#Run houdini 456 default setup
#------------------------------------------------------------------

try:
    
    #default houdini startup when opened without hip file
    hou.hscript("source 456.cmd")

    #SuccessMsg
    print('Successfully executed 456.cmd')

except:
    
    #FailMsg
    print('Failed to execute 456.cmd')









#Set Houdini Env. Variables
#------------------------------------------------------------------

#The variables in here can be expanded in Houdini
#For example: $HELGA_HDRI_PATH expands to //bigfoot/grimmhelga/Production/2d/hdri

try:

    """
    #set variables
    os.environ['HELGA_SCRIPTS_BASE_PATH'] = PIPELINE_SCRIPTS_BASE_PATH
    os.environ['HELGA_HDRI_PATH'] = PIPELINE_HDRI_PATH
    os.environ['HELGA_OTL_PATH'] = HOUDINI_OTL_PATH
    os.environ['HELGA_FUR_PATH'] = PIPELINE_FUR_PATH
    os.environ['HELGA_ALEMBIC_PATH'] = PIPELINE_ALEMBIC_PATH
    os.environ['HELGA_TEXTURES_PATH'] = PIPELINE_TEXTURES_PATH
    os.environ['HELGA_RENDER_PATH'] = PIPELINE_RENDER_PATH
    """


    #set global in houdini
    hou.hscript("set -g HELGA_SCRIPTS_BASE_PATH = {0}".format(PIPELINE_SCRIPTS_BASE_PATH))
    hou.hscript("set -g HELGA_HDRI_PATH = {0}".format(PIPELINE_HDRI_PATH))
    hou.hscript("set -g HELGA_OTL_PATH = {0}".format(HOUDINI_OTL_PATH))
    hou.hscript("set -g HELGA_FUR_PATH = {0}".format(PIPELINE_FUR_PATH))
    hou.hscript("set -g HELGA_ALEMBIC_PATH = {0}".format(PIPELINE_ALEMBIC_PATH))
    hou.hscript("set -g HELGA_TEXTURES_PATH = {0}".format(PIPELINE_TEXTURES_PATH))
    hou.hscript("set -g HELGA_RENDER_PATH = {0}".format(PIPELINE_RENDER_PATH))


    #SuccessMsg
    print('Successfully set helga env. variables')

except:
    
    #FailMsg
    print('Error setting helga env. variables')





#Check if $HELGA_SHOT_NAME variable exists and if not, set it
#------------------------------------------------------------------

# HELGA_SHOT_NAME
HELGA_SHOT_NAME = '$HELGA_SHOT_NAME'

# check if variable exists
try:
    
    # check
    hou.hscriptExpression('{0}'.format(HELGA_SHOT_NAME))

    # variable_value
    variable_value = hou.expandString('{0}'.format(HELGA_SHOT_NAME))
    
    # SuccessMsg
    print('Variable {0} is set to {1}'.format(HELGA_SHOT_NAME, variable_value))

except:

    # FailMsg
    print('Variable {0} does not exist. Setting it to empty value.'.format(HELGA_SHOT_NAME))

    #set $HELGA_SHOT_NAME
    hou.hscript("set -g HELGA_SHOT_NAME = {0}".format(''))






#Helga colorsettings
#------------------------------------------------------------------

#Disabled since we are doing normal linear light workflow again with sRGB
#But we are still using OCIO in Nuke

'''
try:

    #default houdini startup when opened without hip file
    hou.hscript("colorsettings -g 1.0 -l {0} -c -r".format(OCIO_LIN_TO_SRGB_SPI_LUT_HOUDINI))

    #SuccessMsg
    print('Successfully set colorsettings')

except:
    
    #FailMsg
    print('Failed setting colorsettings')

'''











#Helga set cm
#------------------------------------------------------------------

class UnitlengthError(Exception):
    """
    Error to be raised when setting unitlength to cm is not desired.
    """
    
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

try:

    # check if fx user
    if (USER in FX_USER_LIST):
        
        # modal_return_value
        modal_return_value = hou.ui.displayMessage("{0} has been detected as an FX user. Do you want to keep the unitlength to its default value (m) to aid simulations?".format(USER), buttons =("Yes" ,"No"))

        # if 0 raise
        if (modal_return_value == 0):

            # raise
            raise UnitlengthError(USER) 
    
    #default houdini startup when opened without hip file
    hou.hscript("unitlength 0.01")

    #SuccessMsg
    print('Successfully set unitlength to cm')

except UnitlengthError as error:
    
    #FailMsg
    print('FX User {0}. Not setting unitlength.'.format(error.value))

except:
    
    #FailMsg
    print('Failed setting unitlength to cm')



