
"""
global_variables
==========================================

Simple but hopefully helpful module to that bundles all
constants and pipeline variables in a central place.

-----------------------

Usage
-----

::
	
	from helga.general.setup.global_variables import global_variables
	reload(global_variables)

	#pipeline_base_path
	pipeline_base_path = global_variables.PIPELINE_BASE_PATH

-----------------------
"""



#Import
#----------------------------------------------------
#python
import os
import sys




#Globals
#----------------------------------------------------


#General
#----------------------------------------------------
PIPELINE_BASE_PATH = r'//bigfoot/grimmhelga'
"""Helga pipeline base path"""

PIPELINE_SCRIPTS_BASE_PATH = r'//bigfoot/grimmhelga/Production/scripts/deploy'
"""Pipeline scripts base path. You can import helga from here."""

MAYA_PROJECT_PATH = r'//bigfoot/grimmhelga/Production/3d/maya'
"""Helga pipeline Maya project path"""

PIPELINE_DOCUMENTATION_URL = r'http://www.kiiia.com/helga/documentation/build/html/index.html'
"""Default URL constant. Points to pipeline documentation"""


CHARACTER_DIRECTORY_LIST = ['model', ['export'], 'rig', ['last_published'], 'sculpt', ['export'], 'textures', 'temp']
"""Helga character directory structure"""

PROP_DIRECTORY_LIST = ['model', ['export'], 'photoscan', ['masks', 'out', 'photos', 'nuke'], 'rig', ['last_published'], 'sculpt', ['export'], 'textures', 'temp']
"""Helga prop directory structure"""

SHOT_DIRECTORY_LIST = ['animation', 'lighting', 'fx', ['cloth']]
"""Helga shot directory structure"""

COMP_DIRECTORY_LIST = ['2d_render', '3d_render', 'nuke', 'ae', 'mattepainting', 'footage', 'temp']
"""Helga comp directory structure"""

PHOTOSCAN_DIRECTORY_LIST = ['photos', 'masks', 'nuke', 'photoscan', ['out'], 'temp']
"""Helga photoscan directory structure"""



#Nuke
#----------------------------------------------------
NUKE_INIT_PATH = PIPELINE_SCRIPTS_BASE_PATH + r'/helga/nuke/setup/init/'
"""Default nuke init path"""

NUKE_MENU_PATH = PIPELINE_SCRIPTS_BASE_PATH + r'/helga/nuke/setup/menu/'
"""Default nuke menu path"""

NUKE_ICONS_PATH = PIPELINE_SCRIPTS_BASE_PATH + r'/helga/nuke/setup/icons/'
"""Default nuke icons path"""

NUKE_PLUGIN_PATH = PIPELINE_SCRIPTS_BASE_PATH + r'/helga/nuke/setup/plugins'
"""Default nuke plugin path"""



