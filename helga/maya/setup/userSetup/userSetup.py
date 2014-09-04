







#Imports
#------------------------------------------------------------------

#python
import sys
import os
import re
import shutil

#PySide
from PySide import QtGui
from PySide import QtCore

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
DIVIDERLINE = '-----------------------------------------------------------------------------------\n'









#Append MAYA_SCRIPT_PATH pathes to python interpreter sys.path
#------------------------------------------------------------------
#------------------------------------------------------------------
try:
    
    #get MAYA_SCRIPT_PATH pathes
    for path in mel.eval("getenv MAYA_SCRIPT_PATH").split(";"):

        #if path exists append
        if(os.path.exists(path)):
            
            #append
            sys.path.append(path)

            #SuccessMsg
            sys.__stdout__.write('->Successfully appended from MAYA_SCRIPT_PATH to sys.path: {0}\n'.format(path))

        else:

            #FailMsg
            sys.__stdout__.write('->Error appending {0} from MAYA_SCRIPT_PATH to sys.path. Path does not exist.\n'.format(path))

except:
    
    #FailMsg
    sys.__stdout__.write('Failed to append pathes to sys.path from MAYA_SCRIPT_PATH env. variable.\n')






#Dividerline
sys.__stdout__.write(DIVIDERLINE)

    
    


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
                sys.__stdout__.write('->Successfully loaded ' +plugin +' plugin\n')
            else:
                sys.__stdout__.write('->Skipped loading ' +plugin +' plugin. Plugin was already loaded.\n')
        except:
            sys.__stdout__.write('->Error loading ' +plugin +' plugin\n')

    #Dividerline
    sys.__stdout__.write(DIVIDERLINE)
            
    

    #Load deferred
    #------------------------------------------------------------------ 
    
      
    #load_plugins_deferred
    def load_plugins_deferred():
        
        #plugin_list
        plugin_list = ['vrayformaya.mll', 'rrSubmit_Maya_8.5+.py', 'helga_asset_metadata.py', 'helga_shots_metadata.py', 'AnimSchoolPicker.mll']
        

        #iterate plugin_list and load
        for plugin_name in plugin_list:
            try:
                
                if not(cmds.pluginInfo(plugin_name , query = True, loaded = True)):

                    try:
                        cmds.loadPlugin(plugin_name)
                        #Print to console instead of script editor
                        sys.__stdout__.write('->Successfully loaded ' +plugin_name +' deferred\n')
                    except:
                        sys.__stdout__.write('->Error loading ' +plugin_name +' deferred\n')
                
                else:
                    sys.__stdout__.write('->Skipped loading ' +plugin_name +' deferred. Plugin was already loaded\n')
            
            except:
                sys.__stdout__.write('->Error loading ' +plugin_name +' deferred\n')

        #Dividerline
        sys.__stdout__.write(DIVIDERLINE)
    
    #eval deferred
    cmds.evalDeferred(load_plugins_deferred)
    
    
    
except:
    
    #FailMsg
    print('->Failed to load Plugins')
    #Dividerline
    print(DIVIDERLINE)










#Set Project
#------------------------------------------------------------------
try:
    def load_project_deferred():
        
        #set project
        mel.eval('setProject "{0}"'.format(MAYA_PROJECT_DIR))

        #SuccessMsg
        sys.__stdout__.write('Successfully set Maya project deferred: {0}\n'.format(MAYA_PROJECT_DIR))
        #Dividerline
        sys.__stdout__.write(DIVIDERLINE)

    #set project deferred
    cmds.evalDeferred(load_project_deferred)

    

except:
    
    #FailMsg
    sys.__stdout__.write('Failed to set Maya project\n')
    #Dividerline
    sys.__stdout__.write(DIVIDERLINE)



    
    



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
        #Dividerline
        sys.__stdout__.write(DIVIDERLINE)
    
    #eval deferred
    cmds.evalDeferred(set_grid_default)
    

except:
    
    #FailMsg
    print('Failed to set standard grid\n')
    #Dividerline
    print(DIVIDERLINE)













#Source cometMenu deferred
#------------------------------------------------------------------

try:
    
    #source_comet_menu
    def source_comet_menu():
        
        #source menu
        pm.mel.eval('source "cometMenu.mel";')
        
        #Print to console instead of script editor
        sys.__stdout__.write('Successfully sourced comet menu\n')
        #Dividerline
        sys.__stdout__.write(DIVIDERLINE)
    
    #eval deferred
    cmds.evalDeferred(source_comet_menu)
    

except:
    
    #FailMsg
    print('Failed to source comet menu\n')
    #Dividerline
    print(DIVIDERLINE)











#GUI adjustments
#------------------------------------------------------------------

try:
    
    #adjust_gui
    def adjust_gui():
        
        try:

            #set global stylesheet
            QtGui.qApp.setStyleSheet(global_variables.MAYA_STYLESHEET)

            #style shelf background
            global_functions.style_maya_shelves()
            
            #Print to console instead of script editor
            sys.__stdout__.write('Successfully adjusted GUI\n')
            #Dividerline
            sys.__stdout__.write(DIVIDERLINE)

        except:

            #Print to console instead of script editor
            sys.__stdout__.write('Error adjusting GUI\n')
            #Dividerline
            sys.__stdout__.write(DIVIDERLINE)
    
    #eval deferred
    cmds.evalDeferred(adjust_gui)
    

except:
    
    #FailMsg
    print('Failed to adjust GUI\n')
    #Dividerline
    print(DIVIDERLINE)


