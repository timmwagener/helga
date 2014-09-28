


#Imports
#------------------------------------------------------------------

#python
import os
import sys
import re
import shutil
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

#Assign all global variables to only use local ones later on
PIPELINE_SCRIPTS_BASE_PATH = global_variables.PIPELINE_SCRIPTS_BASE_PATH
PIPELINE_HDRI_PATH = global_variables.PIPELINE_HDRI_PATH
OCIO_LIN_TO_SRGB_SPI_LUT_HOUDINI = global_variables.OCIO_LIN_TO_SRGB_SPI_LUT_HOUDINI
HOUDINI_OTL_PATH = global_variables.HOUDINI_OTL_PATH
PIPELINE_ALEMBIC_PATH = global_variables.PIPELINE_ALEMBIC_PATH
PIPELINE_FUR_PATH = global_variables.PIPELINE_FUR_PATH
PIPELINE_TEXTURES_PATH = global_variables.PIPELINE_TEXTURES_PATH
PIPELINE_RENDER_PATH = global_variables.PIPELINE_RENDER_PATH













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
    #set variables
    os.environ['HELGA_SCRIPTS_BASE_PATH'] = PIPELINE_SCRIPTS_BASE_PATH
    os.environ['HELGA_HDRI_PATH'] = PIPELINE_HDRI_PATH
    os.environ['HELGA_OTL_PATH'] = HOUDINI_OTL_PATH
    os.environ['HELGA_FUR_PATH'] = PIPELINE_FUR_PATH
    os.environ['HELGA_ALEMBIC_PATH'] = PIPELINE_ALEMBIC_PATH
    os.environ['HELGA_TEXTURES_PATH'] = PIPELINE_TEXTURES_PATH
    os.environ['HELGA_RENDER_PATH'] = PIPELINE_RENDER_PATH


    #SuccessMsg
    print('Successfully set helga env. variables')

except:
    
    #FailMsg
    print('Error setting helga env. variables')











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
try:
    
    #default houdini startup when opened without hip file
    hou.hscript("unitlength 0.01")

    #SuccessMsg
    print('Successfully set unitlength to cm')

except:
    
    #FailMsg
    print('Failed setting unitlength to cm')



