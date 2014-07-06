
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

#PIPELINE_BASE_PATH
PIPELINE_BASE_PATH = r'//bigfoot/grimmhelga'
"""Helga pipeline base path"""

#if env. var. exists, replace
if (os.getenv('HELGA_PIPELINE_BASE_PATH', False)):
    PIPELINE_BASE_PATH = os.getenv('HELGA_PIPELINE_BASE_PATH', False)



PIPELINE_SCRIPTS_BASE_PATH = PIPELINE_BASE_PATH + r'/Production/scripts/deploy/helga'
"""Pipeline scripts base path. You can import helga from here."""

PIPELINE_ASSETS_PATH = PIPELINE_BASE_PATH + r'/Production/3d/maya/scenes/assets'
"""Pipeline Assets path. Below this directory you find all assets for the show."""

PIPELINE_SHOTS_PATH = PIPELINE_BASE_PATH + r'/Production/3d/maya/scenes/shots'
"""Pipeline Shots path. Below this directory you find all shots for the show."""

PIPELINE_WORK_PROPS_PATH = PIPELINE_BASE_PATH + r'/Production/3d/maya/scenes/assets/work/props'
"""Pipeline work/props path. Below this directory you find all workfiles of props for the show."""

PIPELINE_RND_PATH = PIPELINE_BASE_PATH + r'/Production/rnd'
"""Pipeline rnd path. Personal RnD folders for all team members."""

PIPELINE_HDRI_PATH = PIPELINE_BASE_PATH + r'/Production/2d/hdri'
"""Pipeline HDRI path. Below here are all HDRIs for helga."""

PIPELINE_DOCUMENTATION_URL = r'http://helga-docs.readthedocs.org/'
"""Default URL constant. Points to pipeline documentation"""




#Directory Wizard
#----------------------------------------------------

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





#Maya
#----------------------------------------------------

MAYA_PROJECT_PATH = PIPELINE_BASE_PATH + r'/Production/3d/maya'
"""Helga pipeline Maya project path"""

MAYA_VERSION = r'2014-x64'
"""Helga pipeline Maya version"""





#Nuke
#----------------------------------------------------
NUKE_INIT_PATH = PIPELINE_SCRIPTS_BASE_PATH + r'/helga/nuke/setup/init'
"""Default nuke init path"""

NUKE_MENU_PATH = PIPELINE_SCRIPTS_BASE_PATH + r'/helga/nuke/setup/menu'
"""Default nuke menu path"""

NUKE_ICONS_PATH = PIPELINE_SCRIPTS_BASE_PATH + r'/helga/nuke/setup/icons'
"""Default nuke icons path"""

NUKE_PLUGIN_PATH = PIPELINE_SCRIPTS_BASE_PATH + r'/helga/nuke/setup/plugins'
"""Default nuke plugin path"""





#Houdini
#----------------------------------------------------

HOUDINI_VERSION = r'13.0'
"""Helga pipeline HOUDINI version"""

HOUDINI_ENV_FILE = PIPELINE_SCRIPTS_BASE_PATH + r'/helga/houdini/setup/env/houdini.env'
"""Helga pipeline HOUDINI houdini.env file"""

HOUDINI_SETUP_PATH = PIPELINE_SCRIPTS_BASE_PATH + r'/helga/houdini/setup'
"""Helga pipeline HOUDINI setup path"""

HOUDINI_DIGITAL_ASSETS_PATH = MAYA_PROJECT_PATH + r'/scenes/assets'
"""Helga pipeline HOUDINI digital assets path"""


    

