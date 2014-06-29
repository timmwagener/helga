




#helga init.py (startup procedures)
#------------------------------------------------------------------





#Imports
#------------------------------------------------------------------

#python
import sys
import os
import shutil






#Globals
#------------------------------------------------------------------
SCRIPTS_ROOT_PATH = r'//bigfoot/grimmhelga/Production/scripts/deploy'





#Methods
#------------------------------------------------------------------

#get_user
def get_user():
    return os.environ.get('USERNAME')


#get_user_setup_destination_dir
def get_user_setup_destination_dir():
    
    path_start = 'C:/Users/'
    username = get_user()
    path_end = '/.nuke'
    
    return path_start + username + path_end


#copy_file
def copy_file(source_file, source_dir, destination_dir):
    
    source = source_dir + '/' +source_file
    
    shutil.copy(source, destination_dir)

    










#Startup Routine
#------------------------------------------------------------------



#Copy init.py
#------------------------------------------------------------------

try:
    source_user_setup_dir = SCRIPTS_ROOT_PATH + r'/helga/nuke/setup/init'
    source_user_setup_file = 'init.py'

    user_setup_destination_dir = get_user_setup_destination_dir()

    copy_file(source_user_setup_file, source_user_setup_dir, user_setup_destination_dir)

    #SuccessMsg
    print('Successfully copied init.py')

except:
    
    #FailMsg
    print('Failed to copy init.py')





#Copy menu.py
#------------------------------------------------------------------

try:
    source_user_setup_dir = SCRIPTS_ROOT_PATH + r'/helga/nuke/setup/menu'
    source_user_setup_file = 'menu.py'

    user_setup_destination_dir = get_user_setup_destination_dir()

    copy_file(source_user_setup_file, source_user_setup_dir, user_setup_destination_dir)

    #SuccessMsg
    print('Successfully copied menu.py')

except:
    
    #FailMsg
    print('Failed to copy menu.py')













#Set plugins and scripts path
#------------------------------------------------------------------
try:
    plugin_path_list = [SCRIPTS_ROOT_PATH, SCRIPTS_ROOT_PATH + r'/helga/nuke/setup/plugins']
    
    for plugin_path in plugin_path_list:
        nuke.pluginAppendPath(plugin_path)
    
    #SuccessMsg
    print('Successfully set Helga Plugin Pathes')
    
except:
    
    #FailMsg
    print('Error setting Helga plugin pathes')
