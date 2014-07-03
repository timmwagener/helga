


#helga 456.py (startup procedures always executed)
#------------------------------------------------------------------




#Globals
#------------------------------------------------------------------
PIPELINE_SCRIPTS_BASE_PATH = r'//bigfoot/grimmhelga/Production/scripts/deploy'




#Append custom pathes
#------------------------------------------------------------------
import sys
sys.path.append(PIPELINE_SCRIPTS_BASE_PATH)










#Imports
#------------------------------------------------------------------

#python
import os
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















#Startup Procedures
#------------------------------------------------------------------
#------------------------------------------------------------------




#Copy houdini.env
#------------------------------------------------------------------

try:
    source_user_setup_dir = PIPELINE_SCRIPTS_BASE_PATH + r'/helga/houdini/setup/env'
    source_user_setup_file = 'houdini.env'

    user_setup_destination_dir = global_functions.get_user_setup_destination_dir('houdini')

    global_functions.copy_file(source_user_setup_file, source_user_setup_dir, user_setup_destination_dir)

    #SuccessMsg
    print('Successfully copied houdini.env')

except:
    
    #FailMsg
    print('Failed to copy houdini.env')










#Set Houdini Env. Variables
#------------------------------------------------------------------

#The variables in here can be expanded in Houdini
#For example: $HELGA_HDRI_PATH expands to //bigfoot/grimmhelga/Production/2d/hdri

try:
    #set variables
    os.environ['HELGA_SCRIPTS_BASE_PATH'] = PIPELINE_SCRIPTS_BASE_PATH
    os.environ['HELGA_HDRI_PATH'] = PIPELINE_HDRI_PATH


    #SuccessMsg
    print('Successfully set helga env. variables')

except:
    
    #FailMsg
    print('Error setting helga env. variables')









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














#Helga colorsettings
#------------------------------------------------------------------
'''
try:

    #default houdini startup when opened without hip file
    hou.hscript("colorsettings -g 1.0")
    hou.hscript("colorsettings -l c:/my/anus.lut")

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




#Print Environment
#------------------------------------------------------------------

#PRINT_ENVIRONMENT / off by default
PRINT_ENVIRONMENT = False

#print environment
if(PRINT_ENVIRONMENT):
    
    try:

        #Environment Variables
        print('\nEnvironment Variables:\n------------------------------------------------------------------')
        for environment_variable_key, environment_variable_value in os.environ.iteritems():
            print('{0} - {1}'.format(environment_variable_key, environment_variable_value))

        #Houdini Python Path
        for index, path in enumerate(sys.path):
            if not(index):
                print('\nHoudini path:\n------------------------------------------------------------------')
            print(path)

        #SuccessMsg
        print('Successfully printed Houdini Environment')

    except:
        
        #FailMsg
        print('Error printing Houdini Environment')












