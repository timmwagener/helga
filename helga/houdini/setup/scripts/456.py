


#helga 456.py (startup procedures always executed)
#------------------------------------------------------------------




#Helga pipeline exceptions
#------------------------------------------------------------------

#PipelineBasePathNonExistentException
class PipelineBasePathNonExistentException(Exception):
    """
    Exception to be thrown when os.isdir(HELGA_PIPELINE_BASE_PATH) is False.
    """

    def __init__(self):

        #log_message
        self.log_message = 'HELGA_PIPELINE_BASE_PATH does not exist. Helga pipeline not loaded.'
        #super
        super(PipelineBasePathNonExistentException, self).__init__(self, self.log_message)






#Pipeline base path
#------------------------------------------------------------------
import os

#PIPELINE_BASE_PATH
PIPELINE_BASE_PATH = r'//bigfoot/grimmhelga'

#if env. var. exists, replace
if (os.getenv('HELGA_PIPELINE_BASE_PATH', False)):
    PIPELINE_BASE_PATH = os.getenv('HELGA_PIPELINE_BASE_PATH', False) #r'//bigfoot/grimmhelga/Production/scripts/deploy'


#pipeline path doesnt exist
if not (os.path.isdir(PIPELINE_BASE_PATH)):
    #raise custom exception and abort execution of module
    raise PipelineBasePathNonExistentException

#log
print('Pipeline base path: {0}'.format(PIPELINE_BASE_PATH))




#Append pipeline script path
#------------------------------------------------------------------
import sys

#PIPELINE_SCRIPTS_BASE_PATH
PIPELINE_SCRIPTS_BASE_PATH = PIPELINE_BASE_PATH + r'/Production/scripts/deploy/helga'

#append
sys.path.append(PIPELINE_SCRIPTS_BASE_PATH)










#Imports
#------------------------------------------------------------------

#python
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
HOUDINI_ENV_FILE = global_variables.HOUDINI_ENV_FILE
HOUDINI_SETUP_PATH = global_variables.HOUDINI_SETUP_PATH
HOUDINI_DIGITAL_ASSETS_PATH = global_variables.HOUDINI_DIGITAL_ASSETS_PATH













#Startup Procedures
#------------------------------------------------------------------
#------------------------------------------------------------------



#Write houdini.env
#------------------------------------------------------------------

try:

    #clear and write file
    with open(HOUDINI_ENV_FILE, 'w') as houdini_env_file:

        #houdini_env_content
        houdini_env_content = ''

        #Houdini Path
        houdini_env_content += 'HOUDINI_PATH = "{0};{1};&"'.format(HOUDINI_SETUP_PATH, HOUDINI_DIGITAL_ASSETS_PATH)
        
        #write
        houdini_env_file.write(houdini_env_content)

    #SuccessMsg
    print('Successfully written houdini.env')

except:
    
    #FailMsg
    print('Failed to write houdini.env')





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












