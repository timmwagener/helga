

"""
quick_setup
==========================================

Simple but hopefully helpful module to automatically put the helga pipeline DCCs
into deployment or remove them from it.

-----------------------

The tool is available as precompiled binary under $PIPELINE_SCRIPTS_BASE_PATH/bin

-----------------------

**Author:** `Timm Wagener <mailto:wagenertimm@gmail.com>`_
"""





#FAVORITES_DICT
#------------------------------------------------------------------

import os


#clean_path_for_favorites (upfront definition)
def clean_path_for_favorites(path):
    """
    Modify path to match favorite neccessities.
    """

    #remove forward slashes
    path = path.replace('/', '\\')

    return path




#PIPELINE_BASE_PATH
PIPELINE_BASE_PATH = r'//bigfoot/grimmhelga'

#if env. var. exists, replace
if (os.getenv('HELGA_PIPELINE_BASE_PATH', False)):
    PIPELINE_BASE_PATH = os.getenv('HELGA_PIPELINE_BASE_PATH', False)


#clean base path
PIPELINE_BASE_PATH = clean_path_for_favorites(PIPELINE_BASE_PATH)


#FAVORITES_DICT
FAVORITES_DICT = dict(
helga_rnd = '{0}\\Production\\rnd'.format(PIPELINE_BASE_PATH),
helga_scripts = '{0}\\Production\\scripts'.format(PIPELINE_BASE_PATH),
helga_2d = '{0}\\Production\\2d'.format(PIPELINE_BASE_PATH),
helga_3d = '{0}\\Production\\3d'.format(PIPELINE_BASE_PATH),
helga_assets = '{0}\\Production\\3d\\maya\\scenes\\assets'.format(PIPELINE_BASE_PATH),
helga_assets_work = '{0}\\Production\\3d\\maya\\scenes\\assets\\work'.format(PIPELINE_BASE_PATH),
helga_shots = '{0}\\Production\\3d\\maya\\scenes\\shots'.format(PIPELINE_BASE_PATH),
helga_tools = '{0}\\Production\\scripts\\deploy\\helga\\bin'.format(PIPELINE_BASE_PATH)
)





#Add relative pathes
#------------------------------------------------------------------

#import
import sys


#tool_root_path
tool_root_path = os.path.dirname(__file__)
sys.path.append(tool_root_path)

#media_path
media_path = os.path.join(os.path.dirname(__file__), 'media')
media_path_py2exe = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'media'))
sys.path.append(media_path)
sys.path.append(media_path_py2exe)

#icons_path
icons_path = os.path.join(media_path, 'icons')
icons_path_py2exe = os.path.join(media_path_py2exe, 'icons')
sys.path.append(icons_path)
sys.path.append(icons_path_py2exe)







#Import
#------------------------------------------------------------------
#python
import functools
import logging
import subprocess
import time
#PyQt4
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import uic


#Import variable
do_reload = True

#quick_setup_logging_handler
from lib import quick_setup_logging_handler
if(do_reload):reload(quick_setup_logging_handler)

#quick_setup_functionality
from lib import quick_setup_functionality
if(do_reload):reload(quick_setup_functionality)





#UI classes
#------------------------------------------------------------------

#ui_file_path when run from interpreter
try:
    
    #ui_file_path
    ui_file_path = os.path.join(media_path, 'quick_setup.ui')
    classes_list = uic.loadUiType(ui_file_path)


#ui_file_path when run from distribution
except:
    
    #ui_file_path
    ui_file_path = os.path.join(media_path_py2exe, 'quick_setup.ui')
    classes_list = uic.loadUiType(ui_file_path)








#QuickSetup class
#------------------------------------------------------------------

class QuickSetup(classes_list[0], classes_list[1]):
    
    #Constructor
    def __init__(self, 
                logging_level = logging.DEBUG, 
                parent = None):
        
        #super class init
        super(QuickSetup, self).__init__(parent)


        #instance variables
        #------------------------------------------------------------------
        self.title_name = self.__class__.__name__
        self.version = 0.2
        self.title = self.title_name +' ' + str(self.version)

        #logger
        #------------------------------------------------------------------
        #status_handler
        self.status_handler = quick_setup_logging_handler.StatusStreamHandler(self)
        #logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logging_level = logging_level
        self.logger.setLevel(self.logging_level)
        self.logger.addHandler(self.status_handler)



        #Init procedure
        #------------------------------------------------------------------
        
        #setupUi
        self.setupUi(self)

        #setup_additional_ui
        self.setup_additional_ui()
        
        #connect_ui
        self.connect_ui()

        #show
        self.show()
        



    #UI Methods
    #------------------------------------------------------------------
    
    #setup_additional_ui
    def setup_additional_ui(self):
        """
        Setup additional ui elements.
        """

        #set header icon
        header_icon_path = ''
        header_icon_name = 'icon_quick_setup.png'
        #executed from python
        if (os.path.isdir(icons_path)):
            header_icon_path = os.path.join(icons_path, header_icon_name)
        #executed from distribution
        elif (os.path.isdir(icons_path_py2exe)):
            header_icon_path = os.path.join(icons_path_py2exe, header_icon_name)
        
        #set stylesheet header
        self.wdgt_header_icon.setStyleSheet("border-image: url({0});".format(header_icon_path.replace('\\', '/')))
        
        
        #set title
        self.setWindowTitle(self.title)
        #set header label
        self.lbl_header_text.setText(self.title)


        #set lbl_user
        self.lbl_user.setText(quick_setup_functionality.get_user())
        #set lbl_pipeline_base_path
        self.lbl_pipeline_base_path.setText(quick_setup_functionality.get_pipeline_base_path())


    #connect_ui
    def connect_ui(self):
        """
        Connect ui elements.
        """

        #btn_quick_setup
        self.btn_quick_setup.clicked.connect(functools.partial(self.quick_setup_pipeline))
        #btn_quick_remove
        self.btn_quick_remove.clicked.connect(functools.partial(self.quick_remove_pipeline))

        #btn_create_favorites
        self.btn_create_favorites.clicked.connect(functools.partial(self.add_favorites))
        #btn_remove_favorites
        self.btn_remove_favorites.clicked.connect(functools.partial(self.remove_favorites))






    #Pipeline Setup Methods
    #------------------------------------------------------------------

    #quick_setup_pipeline
    def quick_setup_pipeline(self):
        """
        Quick setup the pipeline (Copy DCC startup scripts).
        If startup scripts already exist, rename them in order to keep them.
        """

        #clear status
        self.clear_setup_status()

        
        #setup_maya_pipeline
        self.setup_maya_pipeline()
        #append status
        self.append_setup_status('---------------------------------')

        #setup_nuke_pipeline
        self.setup_nuke_pipeline()
        #append status
        self.append_setup_status('---------------------------------')

        #setup_houdini_pipeline
        self.setup_houdini_pipeline()
        #append status
        self.append_setup_status('---------------------------------')

        
        #append status
        self.append_setup_status('Quick setup of helga pipeline finished')
        #log
        self.logger.debug('Quick setup of helga pipeline finished')


    #setup_maya_pipeline
    def setup_maya_pipeline(self):
        """
        Setup maya pipeline.
        """

        #append status
        self.append_setup_status('Maya:')

        
        #user_setup_destination_dir
        user_setup_destination_dir = quick_setup_functionality.get_user_setup_destination_dir('maya', '2014-x64')

        #user setup dir non existent
        if not(os.path.isdir(user_setup_destination_dir)):
            #append status
            self.append_setup_status('User setup destination dir: {0} not found. Maybe you have never started Maya so far'.format(user_setup_destination_dir))
            self.append_setup_status('Aborting...')
            return None
        #append status
        self.append_setup_status('User setup destination dir: {0}.'.format(user_setup_destination_dir))


        #userSetup already exists at user destination
        if('userSetup.py' in os.listdir(user_setup_destination_dir)):
            
            #current_file_name
            current_file_name = os.path.join(user_setup_destination_dir, 'userSetup.py')
            #target_file_name
            target_file_name = os.path.join(user_setup_destination_dir, 'backup_helga_{0}_userSetup.py'.format(quick_setup_functionality.get_time_string()))

            #rename
            os.rename(current_file_name, target_file_name)
            
            #append status
            self.append_setup_status('Backuped existing userSetup: {0}.'.format(target_file_name))


        #pipeline_user_setup_source_dir
        pipeline_user_setup_source_dir = quick_setup_functionality.get_user_setup_source_dir('maya')

        #user setup dir non existent
        if not(os.path.isdir(pipeline_user_setup_source_dir)):
            #append status
            self.append_setup_status('Pipeline user setup source dir: {0} not found. Maybe you have not mounted the network path.'.format(pipeline_user_setup_source_dir))
            self.append_setup_status('Aborting...')
            return None
        #append status
        self.append_setup_status('Pipeline user setup source dir: {0}.'.format(pipeline_user_setup_source_dir))


        
        #pipeline_user_setup_source_file
        pipeline_user_setup_source_file = 'userSetup.py'
        #pipeline_user_setup_source_file_path
        pipeline_user_setup_source_file_path = os.path.join(pipeline_user_setup_source_dir, pipeline_user_setup_source_file)

        #user setup file non existent
        if not(os.path.isfile(pipeline_user_setup_source_file_path)):
            #append status
            self.append_setup_status('Pipeline user setup source file: {0} not found. Maybe you have not mounted the network path.'.format(pipeline_user_setup_source_file_path))
            self.append_setup_status('Aborting...')
            return None
        #append status
        self.append_setup_status('Pipeline user setup source file: {0}.'.format(pipeline_user_setup_source_file_path))


        
        #copy
        quick_setup_functionality.copy_file(pipeline_user_setup_source_file,
                                            pipeline_user_setup_source_dir,
                                            user_setup_destination_dir)
        #append status
        self.append_setup_status('{0} copied'.format(pipeline_user_setup_source_file))

        
        #append status
        self.append_setup_status('Maya setup successfull')


    #setup_nuke_pipeline
    def setup_nuke_pipeline(self):
        """
        Setup nuke pipeline.
        """

        #append status
        self.append_setup_status('Nuke:')

        
        #user_setup_destination_dir
        user_setup_destination_dir = quick_setup_functionality.get_user_setup_destination_dir('nuke')

        #user setup dir non existent
        if not(os.path.isdir(user_setup_destination_dir)):
            #append status
            self.append_setup_status('User setup destination dir: {0} not found. Maybe you have never started Maya so far'.format(user_setup_destination_dir))
            self.append_setup_status('Aborting...')
            return None
        #append status
        self.append_setup_status('User setup destination dir: {0}.'.format(user_setup_destination_dir))


        #init already exists at user destination
        if('init.py' in os.listdir(user_setup_destination_dir)):
            
            #current_file_name
            current_file_name = os.path.join(user_setup_destination_dir, 'init.py')
            #target_file_name
            target_file_name = os.path.join(user_setup_destination_dir, 'backup_helga_{0}_init.py'.format(quick_setup_functionality.get_time_string()))

            #rename
            os.rename(current_file_name, target_file_name)
            
            #append status
            self.append_setup_status('Backuped existing init.py: {0}.'.format(target_file_name))


        #menu already exists at user destination
        if('menu.py' in os.listdir(user_setup_destination_dir)):
            
            #current_file_name
            current_file_name = os.path.join(user_setup_destination_dir, 'menu.py')
            #target_file_name
            target_file_name = os.path.join(user_setup_destination_dir, 'backup_helga_{0}_menu.py'.format(quick_setup_functionality.get_time_string()))

            #rename
            os.rename(current_file_name, target_file_name)
            
            #append status
            self.append_setup_status('Backuped existing menu.py: {0}.'.format(target_file_name))


        
        #pipeline_user_setup_source_dir
        pipeline_user_setup_source_dir = quick_setup_functionality.get_user_setup_source_dir('nuke')

        #user setup dir non existent
        if not(os.path.isdir(pipeline_user_setup_source_dir)):
            #append status
            self.append_setup_status('Pipeline user setup source dir: {0} not found. Maybe you have not mounted the network path.'.format(pipeline_user_setup_source_dir))
            self.append_setup_status('Aborting...')
            return None
        #append status
        self.append_setup_status('Pipeline user setup source dir: {0}.'.format(pipeline_user_setup_source_dir))



        #pipeline_menu_source_dir
        pipeline_menu_source_dir = quick_setup_functionality.get_nuke_menu_source_dir()

        #user setup dir non existent
        if not(os.path.isdir(pipeline_menu_source_dir)):
            #append status
            self.append_setup_status('Pipeline menu source dir: {0} not found. Maybe you have not mounted the network path.'.format(pipeline_menu_source_dir))
            self.append_setup_status('Aborting...')
            return None
        #append status
        self.append_setup_status('Pipeline menu source dir: {0}.'.format(pipeline_menu_source_dir))


        
        #pipeline_user_setup_source_file
        pipeline_user_setup_source_file = 'init.py'
        #pipeline_user_setup_source_file_path
        pipeline_user_setup_source_file_path = os.path.join(pipeline_user_setup_source_dir, pipeline_user_setup_source_file)

        #user setup file non existent
        if not(os.path.isfile(pipeline_user_setup_source_file_path)):
            #append status
            self.append_setup_status('Pipeline user setup source file: {0} not found. Maybe you have not mounted the network path.'.format(pipeline_user_setup_source_file_path))
            self.append_setup_status('Aborting...')
            return None
        #append status
        self.append_setup_status('Pipeline user setup source file: {0}.'.format(pipeline_user_setup_source_file_path))




        #pipeline_menu_source_file
        pipeline_menu_source_file = 'menu.py'
        #pipeline_menu_source_file_path
        pipeline_menu_source_file_path = os.path.join(pipeline_menu_source_dir, pipeline_menu_source_file)

        #user setup file non existent
        if not(os.path.isfile(pipeline_menu_source_file_path)):
            #append status
            self.append_setup_status('Pipeline menu source file: {0} not found. Maybe you have not mounted the network path.'.format(pipeline_menu_source_file_path))
            self.append_setup_status('Aborting...')
            return None
        #append status
        self.append_setup_status('Pipeline menu source file: {0}.'.format(pipeline_menu_source_file_path))



        
        #copy init.py
        quick_setup_functionality.copy_file(pipeline_user_setup_source_file,
                                            pipeline_user_setup_source_dir,
                                            user_setup_destination_dir)
        #append status
        self.append_setup_status('{0} copied'.format(pipeline_user_setup_source_file))

        #copy menu.py
        quick_setup_functionality.copy_file(pipeline_menu_source_file,
                                            pipeline_menu_source_dir,
                                            user_setup_destination_dir)
        #append status
        self.append_setup_status('{0} copied'.format(pipeline_menu_source_file))

        
        

        #append status
        self.append_setup_status('Nuke setup successfull')


    #setup_houdini_pipeline
    def setup_houdini_pipeline(self):
        """
        Setup houdini pipeline.
        """

        #append status
        self.append_setup_status('Houdini:')

        
        #user_setup_destination_dir
        user_setup_destination_dir = quick_setup_functionality.get_user_setup_destination_dir('houdini', '13.0')

        #user setup dir non existent
        if not(os.path.isdir(user_setup_destination_dir)):
            #append status
            self.append_setup_status('User setup destination dir: {0} not found. Maybe you have never started Maya so far'.format(user_setup_destination_dir))
            self.append_setup_status('Aborting...')
            return None
        #append status
        self.append_setup_status('User setup destination dir: {0}.'.format(user_setup_destination_dir))


        #houdini already exists at user destination
        if('houdini.env' in os.listdir(user_setup_destination_dir)):
            
            #current_file_name
            current_file_name = os.path.join(user_setup_destination_dir, 'houdini.env')
            #target_file_name
            target_file_name = os.path.join(user_setup_destination_dir, 'backup_helga_{0}_houdini.env'.format(quick_setup_functionality.get_time_string()))

            #rename
            os.rename(current_file_name, target_file_name)
            
            #append status
            self.append_setup_status('Backuped existing houdini.env: {0}.'.format(target_file_name))


        #pipeline_user_setup_source_dir
        pipeline_user_setup_source_dir = quick_setup_functionality.get_user_setup_source_dir('houdini')

        #user setup dir non existent
        if not(os.path.isdir(pipeline_user_setup_source_dir)):
            #append status
            self.append_setup_status('Pipeline user setup source dir: {0} not found. Maybe you have not mounted the network path.'.format(pipeline_user_setup_source_dir))
            self.append_setup_status('Aborting...')
            return None
        #append status
        self.append_setup_status('Pipeline user setup source dir: {0}.'.format(pipeline_user_setup_source_dir))


        
        #pipeline_user_setup_source_file
        pipeline_user_setup_source_file = 'houdini.env'
        #pipeline_user_setup_source_file_path
        pipeline_user_setup_source_file_path = os.path.join(pipeline_user_setup_source_dir, pipeline_user_setup_source_file)

        #user setup file non existent
        if not(os.path.isfile(pipeline_user_setup_source_file_path)):
            #append status
            self.append_setup_status('Pipeline user setup source file: {0} not found. Maybe you have not mounted the network path.'.format(pipeline_user_setup_source_file_path))
            self.append_setup_status('Aborting...')
            return None
        #append status
        self.append_setup_status('Pipeline user setup source file: {0}.'.format(pipeline_user_setup_source_file_path))


        
        #copy
        quick_setup_functionality.copy_file(pipeline_user_setup_source_file,
                                            pipeline_user_setup_source_dir,
                                            user_setup_destination_dir)
        #append status
        self.append_setup_status('{0} copied'.format(pipeline_user_setup_source_file))

        
        #append status
        self.append_setup_status('Houdini setup successfull')





    #Pipeline Remove Methods
    #------------------------------------------------------------------

    #quick_remove_pipeline
    def quick_remove_pipeline(self):
        """
        Quick remove the pipeline (Remove DCC startup scripts).
        """

        #clear status
        self.clear_setup_status()

        
        #remove_maya_pipeline
        self.remove_maya_pipeline()
        #append status
        self.append_setup_status('---------------------------------')

        #remove_nuke_pipeline
        self.remove_nuke_pipeline()
        #append status
        self.append_setup_status('---------------------------------')

        #remove_houdini_pipeline
        self.remove_houdini_pipeline()
        #append status
        self.append_setup_status('---------------------------------')


        #append status
        self.append_setup_status('Quick removal of helga pipeline finished')
        #log
        self.logger.debug('Quick removal of helga pipeline finished')


    #remove_maya_pipeline
    def remove_maya_pipeline(self):
        """
        Remove maya pipeline.
        """

        try:
            #user_setup_destination_dir
            user_setup_destination_dir = quick_setup_functionality.get_user_setup_destination_dir('maya', '2014-x64')
            #user_setup_file
            user_setup_file = os.path.join(user_setup_destination_dir, 'userSetup.py')

            #delete
            os.remove(user_setup_file)
        
        except:
            #append status
            self.append_setup_status('Error removing Maya userSetup file. Maybe no userSetup file or directory existed.')
            return None

        #append status
        self.append_setup_status('Removed local helga maya pipeline files')


    #remove_nuke_pipeline
    def remove_nuke_pipeline(self):
        """
        Remove nuke pipeline.
        """

        try:
            #user_setup_destination_dir
            user_setup_destination_dir = quick_setup_functionality.get_user_setup_destination_dir('nuke')
            #user_setup_file
            user_setup_file = os.path.join(user_setup_destination_dir, 'init.py')
            #menu_file
            menu_file = os.path.join(user_setup_destination_dir, 'menu.py')

            #delete
            os.remove(user_setup_file)
            os.remove(menu_file)
        
        except:
            #append status
            self.append_setup_status('Error removing Nuke init.py and menu.py files. Maybe none of these files or the .nuke directory existed.')
            return None

        #append status
        self.append_setup_status('Removed local helga nuke pipeline files')


    #remove_houdini_pipeline
    def remove_houdini_pipeline(self):
        """
        Remove houdini pipeline.
        """

        try:
            #user_setup_destination_dir
            user_setup_destination_dir = quick_setup_functionality.get_user_setup_destination_dir('houdini', '13.0')
            #user_setup_file
            user_setup_file = os.path.join(user_setup_destination_dir, 'houdini.env')

            #delete
            os.remove(user_setup_file)
        
        except:
            #append status
            self.append_setup_status('Error removing hoduini.env file. Maybe no houdini.env file or Houdini directory existed.')
            return None

        #append status
        self.append_setup_status('Removed local helga hoduini pipeline files')








    #Favorites
    #------------------------------------------------------------------

    #add_favorites
    def add_favorites(self):
        """
        Add favorites.
        """

        #clear status
        self.clear_setup_status()

        
        #iterate and set favorites
        for shortcut_name in sorted(FAVORITES_DICT.keys()):
            
            #target_path
            target_path = FAVORITES_DICT[shortcut_name]

            try:
                
                #add
                quick_setup_functionality.add_favorite(shortcut_name, target_path)

                #append status
                self.append_setup_status('Added favorite: {0} --> {1}'.format(shortcut_name, target_path))

            except:
                
                #append status
                self.append_setup_status('Error adding favorite: {0} --> {1}'.format(shortcut_name, target_path))

        
        
        #append status
        self.append_setup_status('---------------------------------')
        #append status
        self.append_setup_status('Setting favorites finished')
        #log
        self.logger.debug('Setting favorites finished')

    
    #remove_favorites
    def remove_favorites(self):
        """
        Remove favorites.
        """

        #clear status
        self.clear_setup_status()

        

        #iterate and set favorites
        for shortcut_name, target_path in FAVORITES_DICT.iteritems():
            
            try:
                
                #shortcut_path
                shortcut_path = os.path.join(quick_setup_functionality.get_links_directory(), '{0}.lnk'.format(shortcut_name))

                #if isfile delete
                if(os.path.isfile(shortcut_path)):
                    
                    #delete
                    os.remove(shortcut_path)

                #append status
                self.append_setup_status('Deleted favorite: {0}'.format(shortcut_name))

            except:

                #append status
                self.append_setup_status('Error deleting favorite: {0}'.format(shortcut_name))


        #append status
        self.append_setup_status('---------------------------------')
        #append status
        self.append_setup_status('Removing favorites finished')
        #log
        self.logger.debug('Removing favorites finished')

        



    #Getter & Setter
    #------------------------------------------------------------------

    #set_status
    def set_status(self, new_value):
        """
        Set le_status text
        """

        #clear
        self.le_status.clear()
        #set text
        self.le_status.setText(new_value)

    
    #get_status
    def get_status(self):
        """
        Return content of le_status
        """

        return str(self.le_status.text())


    #append_setup_status
    def append_setup_status(self, message):
        """
        Append to self.te_setup_status
        """

        #append
        self.te_setup_status.append(message)


    #clear_setup_status
    def clear_setup_status(self):
        """
        Clear self.te_setup_status
        """

        #clear
        self.te_setup_status.clear()


        

        