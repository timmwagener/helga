

"""
asset_manager_mayapy
==========================================

AssetManager mayapy. This module is running the whole export
procedure in mayapy.
"""




#Import
#------------------------------------------------------------------

#initialize standalone maya
import maya.standalone as standalone
standalone.initialize(name='python')

#python
import sys
import os

#maya
#scripting
import maya.cmds as cmds
import pymel.core as pm
#api 1
import maya.OpenMaya as open_maya
import maya.OpenMayaAnim as open_maya_anim
import maya.OpenMayaFX as open_maya_fx
import maya.OpenMayaRender as open_maya_render
import maya.OpenMayaUI as open_maya_ui
#api 2
import maya.api.OpenMaya as open_maya_2


#Import variable
do_reload = True

#helga

#global_variables
from helga.general.setup.global_variables import global_variables
if(do_reload):reload(global_variables)

#global_functions
from helga.general.setup.global_functions import global_functions
if(do_reload):reload(global_functions)



#Functions
#------------------------------------------------------------------

def open_file_and_export():
    """
    Get the env. vars., open the file and export.
    """

    #abc_command
    abc_command = os.environ.get('HELGA_ABC_COMMAND', None)

    #maya_file
    maya_file = os.environ.get('HELGA_ABC_MAYA_FILE', None)



    #open file
    try:
        pm.openFile(maya_file)
    except:
        print('Error opening {0}'.format(maya_file))

    #export abc
    try:
        pm.mel.eval(abc_command)
    except:
        print('Error exporting Alembic.\nAbc cmd: {0}'.format(abc_command))


def run():
    """
    Execute the export.
    """

    #open_file_and_export
    open_file_and_export()













