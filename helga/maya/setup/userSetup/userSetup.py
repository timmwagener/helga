







#Imports
#------------------------------------------------------------------

#python
import sys
import os
import re
import shutil

#maya
import maya.mel as mel
import maya.cmds as cmds
import maya.utils
import pymel.core as pm


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
MAYA_PROJECT_DIR = global_variables.MAYA_PROJECT_PATH #r'//bigfoot/grimmhelga/Production/3d/maya'









    
    


#Load Plugins
#------------------------------------------------------------------
#------------------------------------------------------------------

try:

    #Load non-deferred
    #------------------------------------------------------------------
    
    #PlugIn List
    plugin_list = ['objExport.mll', 
    'AbcExport.mll', 
    'AbcImport.mll', 
    'OpenEXRLoader.mll', 
    'cvShapeInverter.py', 
    'poseDeformer.mll',
    'poseReader.mll',
    'resetSkinJoint.mll']
        
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
        plugin_list = ['vrayformaya.mll', 'rrSubmit_Maya_8.5+.py', 'metadata.py', 'helga_assets_props_metadata.py']
        
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
        sys.__stdout__.write('Successfully set Maya project deferred: {0}\n'.format(MAYA_PROJECT_DIR))

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







#Source cometMenu deferred
#------------------------------------------------------------------

try:
    
    #source_comet_menu
    def source_comet_menu():
        
        #source menu
        pm.mel.eval('source "cometMenu.mel";')
        
        #Print to console instead of script editor
        sys.__stdout__.write('Successfully sourced comet menu\n')
    
    #eval deferred
    cmds.evalDeferred(source_comet_menu)
    

except:
    
    #FailMsg
    print('Failed to source comet menu\n')
