


#userSetup.py
#------------------------------------------------------------------
#------------------------------------------------------------------





#Helga pipeline exceptions
#------------------------------------------------------------------

#MissingEnvironmentVariableException
class MissingEnvironmentVariableException(Exception):
	"""
	Exception to be thrown when os.getenv('HELGA_PIPELINE_BASE_PATH', False) return False.
	This exception means that PIPELINE_BASE_PATH variable has not been set.
	"""

	def __init__(self):

		#log_message
		self.log_message = 'HELGA_PIPELINE_BASE_PATH environment variable is not set. Helga pipeline not loaded. Please set this environment variable to point to: //bigfoot/grimmhelga/Production/scripts/deploy'
		#super
		super(MissingEnvironmentVariableException, self).__init__(self, self.log_message)


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
PIPELINE_BASE_PATH = os.getenv('HELGA_PIPELINE_BASE_PATH', False) #r'//bigfoot/grimmhelga/Production/scripts/deploy/helga'


#env. var. doesnt exist
if not (PIPELINE_BASE_PATH):
	#raise custom exception and abort execution of module
	raise MissingEnvironmentVariableException

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

#maya
import maya.mel as mel
import maya.cmds as cmds
import maya.utils


#Import variable
do_reload = True

#global_variables
from helga.general.setup.global_variables import global_variables
if(do_reload):reload(global_variables)

#global_functions
from helga.general.setup.global_functions import global_functions
if(do_reload):reload(global_functions)












#userSetup Globals
#------------------------------------------------------------------
#------------------------------------------------------------------

#helga filmaka project globals
PIPELINE_SCRIPTS_BASE_PATH = global_variables.PIPELINE_SCRIPTS_BASE_PATH #r'//bigfoot/grimmhelga/Production/scripts/deploy/helga'
MAYA_PROJECT_DIR = global_variables.MAYA_PROJECT_PATH #r'//bigfoot/grimmhelga/Production/3d/maya'
MAYA_VERSION = global_variables.MAYA_VERSION #'2014-x64'








#Methods
#------------------------------------------------------------------
#------------------------------------------------------------------

#get_shelf_destination_dir
def get_shelf_destination_dir():
	
	path_start = 'C:/Users/'
	username = global_functions.get_user()
	path_end = '/Documents/maya/{0}/prefs/shelves'.format(MAYA_VERSION)
	
	return path_start + username + path_end

	
	


	

	


#Startup Procedures
#------------------------------------------------------------------
#------------------------------------------------------------------



#Copy userSetup.py
#------------------------------------------------------------------
#------------------------------------------------------------------

try:
	source_user_setup_dir = PIPELINE_SCRIPTS_BASE_PATH + r'/helga/maya/setup/userSetup'
	source_user_setup_file = 'userSetup.py'

	user_setup_destination_dir = global_functions.get_user_setup_destination_dir('maya')

	global_functions.copy_file(source_user_setup_file, source_user_setup_dir, user_setup_destination_dir)

	#SuccessMsg
	print('Successfully copied userSetup.py')

except:
	
	#FailMsg
	print('Failed to copy userSetup.py')
	






#Copy Shelf
#------------------------------------------------------------------
#------------------------------------------------------------------

try:
	source_shelf_dir = PIPELINE_SCRIPTS_BASE_PATH + r'/helga/maya/setup/shelf'
	source_shelf_name_list = ['shelf_helga.mel', 'shelf_advancedSkeleton.mel']

	shelf_destination_dir = get_shelf_destination_dir()

	#iterate and copy
	for source_shelf_name in source_shelf_name_list:
		global_functions.copy_file(source_shelf_name, source_shelf_dir, shelf_destination_dir)

		#SuccessMsg
		print('Successfully copied shelf: {0}'.format(source_shelf_name))

except:
	
	#FailMsg
	print('Failed to copy shelf')








#Add Project Scripts Location
#------------------------------------------------------------------
#------------------------------------------------------------------

try:
	script_path_list = [PIPELINE_SCRIPTS_BASE_PATH, PIPELINE_SCRIPTS_BASE_PATH + r'/helga/maya/setup/scripts']
	
	#Add custom test path if user is twagener
	if(global_functions.get_user() == 'twagener'): 
		script_path_list.append('C:/symlinks/maya/maya2014x64_scripts')

	for script_path in script_path_list:
		
		#Python
		sys.path.append(script_path)
		#MEL
		os.environ['MAYA_SCRIPT_PATH'] = os.environ['MAYA_SCRIPT_PATH'] +';' + script_path

		#SuccessMsg
		print('Added to scripts path: {0}'.format(script_path))

	#SuccessMsg
	print('Successfully added scriptpath list')

except:
	
	#FailMsg
	print('Failed to add scriptpath list')
	
	

	




#Add Icons Path
#------------------------------------------------------------------
#------------------------------------------------------------------

try:
	icons_path_list = [PIPELINE_SCRIPTS_BASE_PATH + r'/helga/maya/setup/icons']
	
	#Add custom test path if user is twagener
	if(global_functions.get_user() == 'twagener'):
		icons_path_list.append('C:/symlinks/maya/maya2014x64_icons')

	for icon_path in icons_path_list:
		os.environ['XBMLANGPATH'] = os.environ['XBMLANGPATH'] +';' + icon_path
	
	#SuccessMsg
	print('Successfully added Icons Path list')
	
	
except:
	
	#FailMsg
	print('Failed to add Icons Path list')

	
	



	

	

#Add PlugIn Path
#------------------------------------------------------------------
#------------------------------------------------------------------

try:
	plugin_path_list = [PIPELINE_SCRIPTS_BASE_PATH + r'/helga/maya/setup/plugins']
	
	#Add custom test path if user is twagener
	if(global_functions.get_user() == 'twagener'):
		plugin_path_list.append('C:/symlinks/maya/maya2014x64_plugins')
	
	for plugin_path in plugin_path_list:
		os.environ['MAYA_PLUG_IN_PATH'] = os.environ['MAYA_PLUG_IN_PATH'] +';' + plugin_path

	
	#SuccessMsg
	print('Successfully added PlugIn Path list')
	
	
except:
	
	#FailMsg
	print('Failed to add PlugIn Path list')
	
	

	
	


#Load Plugins
#------------------------------------------------------------------
#------------------------------------------------------------------

try:

	#Load non-deferred
	#------------------------------------------------------------------
	
	#PlugIn List
	plugin_list = ['objExport.mll', 'AbcExport.mll', 'AbcImport.mll', 'OpenEXRLoader.mll', 'cvShapeInverter.py']
		
	#iterate plugin_list and load plugin shouldnt it be already loaded
	for plugin in plugin_list:
			
		try:
			if not(cmds.pluginInfo(plugin , query = True, loaded = True)):
				cmds.loadPlugin(plugin)
				print('->Successfully loaded ' +plugin +' plugin')
			else:
				print('->Skipped loading ' +plugin +' plugin. Plugin was already loaded.')
		except:
			print('->Error loading ' +plugin +' plugin')
			
	

	#Load deferred
	#------------------------------------------------------------------	
		
	#load_plugins_deferred
	def load_plugins_deferred():
		
		#plugin_list
		plugin_list = ['vrayformaya.mll', 'rrSubmit_Maya_8.5+.py', 'metadata.py']
		
		#Add custom test path if user is twagener
		if(global_functions.get_user() == 'twagener'):
			plugin_list.append('ocio_maya.mll')

		#iterate plugin_list and load
		for plugin_name in plugin_list:
			try:
				if not(cmds.pluginInfo(plugin_name , query = True, loaded = True)):
					cmds.loadPlugin(plugin_name)
					#Print to console instead of script editor
					sys.__stdout__.write('->Successfully loaded ' +plugin_name +' deferred\n')
				else:
					sys.__stdout__.write('->Skipped loading ' +plugin_name +' deferred. Plugin was already loaded\n')
			except:
				sys.__stdout__.write('->Error loading ' +plugin_name +' deferred\n')
	
	#eval deferred
	cmds.evalDeferred(load_plugins_deferred)
	
	
except:
	
	#FailMsg
	print('->Failed to load Plugins')





#Set Project
#------------------------------------------------------------------
try:
	def load_project_deferred():
		
		#set project
		mel.eval('setProject "{0}"'.format(MAYA_PROJECT_DIR))

		#SuccessMsg
		sys.__stdout__.write('Successfully set Maya project deferred\n')

	#set project deferred
	cmds.evalDeferred(load_project_deferred)

	

except:
	
	#FailMsg
	sys.__stdout__.write('Failed to set Maya project\n')
	
	



#Set Grid
#------------------------------------------------------------------

try:
	
	#setGrid
	def set_grid_default():
		
		#set correct grid units and display settings
		cmds.grid(spacing = 5, divisions = 5, size = 10)
		cmds.displayColor( 'gridHighlight', 12, dormant=True )
		cmds.displayColor( 'grid', 3, dormant=True )
		
		#Turn grid on by default
		gridState = cmds.grid( toggle=True, q=True )
		if not(gridState): cmds.grid( toggle = True )
		
		#Print to console instead of script editor
		sys.__stdout__.write('Successfully set standard grid deferred\n')
	
	#eval deferred
	cmds.evalDeferred(set_grid_default)
	

except:
	
	#FailMsg
	print('Failed to set standard grid\n')





