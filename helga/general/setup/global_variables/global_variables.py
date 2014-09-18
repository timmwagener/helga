
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



PIPELINE_BASE_PATH = os.getenv('HELGA_PIPELINE_BASE_PATH', False)
"""Helga pipeline base path"""

#import protection
#everything from here on will fail if the ancor PIPELINE_BASE_PATH fails
if (PIPELINE_BASE_PATH):

    HELGA_PIPELINE_FLAVOUR = os.getenv('HELGA_PIPELINE_FLAVOUR', False)
    """Pipeline flavour. Can be sandbox or deploy."""

    PIPELINE_SCRIPTS_BASE_PATH = PIPELINE_BASE_PATH + r'/Production/scripts/' + HELGA_PIPELINE_FLAVOUR + r'/helga'
    """Pipeline scripts base path. You can import helga from here."""

    PIPELINE_LIBRARIES_PATH_GENERAL = PIPELINE_BASE_PATH + r'/Production/scripts/libraries/general/python2.7libs'
    PIPELINE_LIBRARIES_PATH_GENERAL_FOR_HOUDINI = PIPELINE_BASE_PATH + r'/Production/scripts/libraries/general' #HOUDINI_PATH searches for python2.7libs folder automatically
    """General libraries to be used with all our DCCs. All DCCs have a Python 2.7.x interpreter."""

    PIPELINE_LIBRARIES_PATH_HOUDINI = PIPELINE_BASE_PATH + r'/Production/scripts/libraries/houdini'
    """Specific third party libraries to be used with Houdini."""

    PIPELINE_LIBRARIES_PATH_MAYA = PIPELINE_BASE_PATH + r'/Production/scripts/libraries/maya'
    """Specific third party libraries to be used with Maya."""

    PIPELINE_LIBRARIES_PATH_NUKE = PIPELINE_BASE_PATH + r'/Production/scripts/libraries/nuke'
    """Specific third party libraries to be used with Nuke."""


    
    OCIO_PATH = PIPELINE_SCRIPTS_BASE_PATH + r'/helga/general/setup/ocio/nuke_modified/config.ocio'
    """Helga pipeline OCIO path"""

    OCIO_LIN_TO_SRGB_SPI_LUT_HOUDINI = PIPELINE_SCRIPTS_BASE_PATH + r'/helga/general/setup/ocio/nuke_modified/luts/srgb_s_curve.lut'
    """Lin to srgb_spi lut in Houdinis LUT format .lut"""



    PIPELINE_ICON_PATH = PIPELINE_SCRIPTS_BASE_PATH + r'/helga/general/setup/icons'
    """Helga pipeline icon path"""

    PIPELINE_ASSETS_PATH = PIPELINE_BASE_PATH + r'/Production/3d/maya/scenes/assets'
    """Pipeline Assets path. Below this directory you find all assets for the show."""

    PIPELINE_ALEMBIC_PATH = PIPELINE_BASE_PATH + r'/Production/3d/maya/cache/alembic'
    """Pipeline Alembic path. Below this directory you find all alembic caches for the show."""

    PIPELINE_FUR_PATH = PIPELINE_BASE_PATH + r'/Production/3d/maya/cache/fur'
    """Pipeline fur path. Below this directory you find all fur caches for the show."""

    PIPELINE_TEXTURES_PATH = PIPELINE_ASSETS_PATH + r'/textures'
    """Pipeline textures path. Below this directory you find all published textures for the show."""

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

    MAYA_EXE = os.getenv('HELGA_MAYA_EXE', False)
    """Helga pipeline Maya exe"""

    MAYA_PY = os.path.abspath(os.path.join(os.path.dirname(MAYA_EXE), 'mayapy.exe')).replace('\\', '/')
    """Helga pipeline Maya Python interpreter path"""


    MAYA_PROJECT_PATH = PIPELINE_BASE_PATH + r'/Production/3d/maya'
    """Helga pipeline Maya project path"""


    MAYA_VERSION = r'2014-x64'
    """Helga pipeline Maya version"""

    MAYA_USERSETUP_PATH = PIPELINE_SCRIPTS_BASE_PATH + r'/helga/maya/setup/userSetup'
    """Path to userSetup.py and userSetup.mel"""


    MAYA_SCRIPTS_PATH_LIST = [MAYA_USERSETUP_PATH,
                                PIPELINE_SCRIPTS_BASE_PATH + r'/helga/maya/setup/scripts',
                                PIPELINE_SCRIPTS_BASE_PATH + r'/helga/maya/setup/scripts/cometScripts',
                                PIPELINE_SCRIPTS_BASE_PATH + r'/helga/maya/setup/scripts/ae_templates',
                                PIPELINE_LIBRARIES_PATH_GENERAL,
                                PIPELINE_LIBRARIES_PATH_MAYA]
    """Helga pipeline Maya scripts pathes"""


    MAYA_PYTHONPATH_LIST = [PIPELINE_SCRIPTS_BASE_PATH]
    """Helga pipeline Maya python pathes"""


    MAYA_ICONS_PATH_LIST = [PIPELINE_SCRIPTS_BASE_PATH + r'/helga/maya/setup/icons',
                            PIPELINE_SCRIPTS_BASE_PATH + r'/helga/maya/setup/icons/plugin_images']
    """Helga pipeline Maya icons pathes"""


    MAYA_PLUGIN_PATH_LIST = [PIPELINE_SCRIPTS_BASE_PATH + r'/helga/maya/setup/plugins']
    """Helga pipeline Maya plugins pathes"""


    MAYA_SHELF_PATH_LIST = [PIPELINE_SCRIPTS_BASE_PATH + r'/helga/maya/setup/shelf']
    """Helga pipeline Maya shelf pathes"""






    #Nuke
    #----------------------------------------------------

    NUKE_EXE = os.getenv('HELGA_NUKE_EXE', False)
    """Helga pipeline Nuke exe"""


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

    HOUDINI_EXE = os.getenv('HELGA_HOUDINI_EXE', False)
    """Helga pipeline Houdini exe"""


    HOUDINI_VERSION = r'13.0'
    """Helga pipeline HOUDINI version"""


    HOUDINI_SETUP_PATH = PIPELINE_SCRIPTS_BASE_PATH + r'/helga/houdini/setup'
    """Helga pipeline HOUDINI setup path"""


    HOUDINI_DIGITAL_ASSETS_PATH = MAYA_PROJECT_PATH + r'/scenes/assets'
    """Helga pipeline HOUDINI digital assets path"""

    HOUDINI_OTL_PATH = HOUDINI_DIGITAL_ASSETS_PATH + r'/otls'
    """Helga pipeline HOUDINI otl path"""

    HOUDINI_PATH = [HOUDINI_SETUP_PATH,
                    HOUDINI_DIGITAL_ASSETS_PATH,
                    PIPELINE_LIBRARIES_PATH_GENERAL_FOR_HOUDINI,
                    PIPELINE_LIBRARIES_PATH_HOUDINI,
                    '&']
    """Helga Houdini path"""








    #Stylesheets
    #----------------------------------------------------


    #Maya
    #----------------------------------------------------

    MAYA_STYLESHEET_DICT = {'tab_selected_background_color' : '#b13b00' if(HELGA_PIPELINE_FLAVOUR == 'deploy') else '#006cbf',
                            'tab_hover_background_color' : '#f9661e' if(HELGA_PIPELINE_FLAVOUR == 'deploy') else '#008df9'}
    """Dictionary to format Maya stylesheet string"""

    MAYA_STYLESHEET = "\
\
\
/* QLineEdit#A3FGXfield */\
QLineEdit#A3FGXfield { border-radius: 0; background-color: #222222; color: #ffbbbb } \
QLineEdit#A3FGYfield { border-radius: 0; background-color: #222222; color: #bbffbb } \
QLineEdit#A3FGZfield { border-radius: 0; background-color: #222222; color: #bbbbff } \
\
\
/* QTabBar */\
QTabBar::tab { background-color: rgba(255, 255, 255, 0); color: #dbdce0; alignment: center; }\
QTabBar::tab:selected { background-color: %(tab_selected_background_color)s; }\
QTabBar::tab:hover { background-color: %(tab_hover_background_color)s; }\
\
\
\
"%MAYA_STYLESHEET_DICT
    #----------------------------------------------------

    


    #Nuke
    #----------------------------------------------------

    NUKE_STYLESHEET_DICT = {'tab_selected_background_color' : '#b13b00' if(HELGA_PIPELINE_FLAVOUR == 'deploy') else '#006cbf',
                            'tab_hover_background_color' : '#f9661e' if(HELGA_PIPELINE_FLAVOUR == 'deploy') else '#008df9'}
    """Dictionary to format Nuke stylesheet string"""

    NUKE_STYLESHEET = "\
\
\
/* QTabBar */\
QTabBar::tab { background-color: rgba(255, 255, 255, 0); color: #dbdce0; alignment: center; }\
QTabBar::tab:selected { background-color: %(tab_selected_background_color)s; }\
QTabBar::tab:hover { background-color: %(tab_hover_background_color)s; }\
\
\
\
"%NUKE_STYLESHEET_DICT
    #----------------------------------------------------


    

