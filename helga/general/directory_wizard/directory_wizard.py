

"""
directory_wizard
==========================================

Simple but hopefully helpful module to automatically generate
folderstructures for assets, comps etc.
It uses PySide and is ment to run from Mayas, Nukes and Houdinis
Python interpreters.

-----------------------

.. rubric:: Usage

::
    
    from helga.general.directory_wizard import directory_wizard
    reload(directory_wizard)

    #run
    directory_wizard.run()

-----------------------
"""




#Add relative pathes
#------------------------------------------------------------------

#import
import sys
import os

#tool_root_path
tool_root_path = os.path.dirname(__file__)
sys.path.append(tool_root_path)

#media_path
media_path = os.path.join(os.path.dirname(__file__), 'media')
sys.path.append(media_path)

#icons_path
icons_path = os.path.join(media_path, 'icons')
sys.path.append(icons_path)




#Import
#------------------------------------------------------------------
#python
import functools
import logging
import subprocess
#PySide
from PySide import QtGui
from PySide import QtCore
from PySide import QtUiTools


#Import variable
do_reload = True

#directory_wizard_logging_handler
from lib import directory_wizard_logging_handler
if(do_reload):reload(directory_wizard_logging_handler)

#prop_directory
from lib import directory_creator
if(do_reload):reload(directory_creator)

#global_variables
from helga.general.setup.global_variables import global_variables
if(do_reload):reload(global_variables)

#global_functions
from helga.general.setup.global_functions import global_functions
if(do_reload):reload(global_functions)







#DirectoryWizard class
#------------------------------------------------------------------

class DirectoryWizard(QtGui.QWidget):
    
    #Constructor
    def __init__(self, 
                logging_level = logging.DEBUG, 
                parent = global_functions.get_main_window()):
        super(DirectoryWizard, self).__init__(parent)


        #instance variables
        #------------------------------------------------------------------
        self.title_name = self.__class__.__name__
        self.version = 0.1
        self.title = self.title_name +' ' + str(self.version)

        self.icon_path = os.path.join(icons_path, 'icon_directory_wizard.png')

        
        #logger
        #------------------------------------------------------------------
        #status_handler
        self.status_handler = directory_wizard_logging_handler.StatusStreamHandler(self)
        #logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logging_level = logging_level
        self.logger.setLevel(self.logging_level)
        self.logger.addHandler(self.status_handler)



        #ui setup variables
        #------------------------------------------------------------------
        self.ui_file_extension = 'ui'
        self.ui_file_name = __name__.split('.')[-1] +'.' +self.ui_file_extension
        #ui_file_path
        self.ui_file_path = os.path.join(media_path, self.ui_file_name)
        #ui_file_widget
        self.ui_file_widget = self.create_widget_from_ui_file(self.ui_file_path)
        

        

        
        #Init procedure
        #------------------------------------------------------------------
        
        #set_ui_instance_variables
        self.set_ui_instance_variables()
        
        #connect_ui
        self.connect_ui()
        
        #Configure Instance and show
        self.configure_instance()

        #show
        self.show()
        
        
        
        
    
    
    
    #UI setup methods
    #------------------------------------------------------------------
    #------------------------------------------------------------------
    
    #create_widget_from_ui_file
    def create_widget_from_ui_file(self, ui_file_path):
        #Create widget from ui file
        loader_instance = QtUiTools.QUiLoader()
        #file to load in as unicode obj
        ui_file = QtCore.QFile(ui_file_path)
        ui_file.open(QtCore.QFile.ReadOnly)
        #Create Widget
        ui_file_widget = loader_instance.load(ui_file, self)
        #close ui_File
        ui_file.close()

        return ui_file_widget
    
    
    
    
    #set_ui_instance_variables
    def set_ui_instance_variables(self):
        
        #wdgt_header_icon
        self.wdgt_header_icon = self.ui_file_widget.findChild(QtGui.QWidget, 'wdgt_header_icon')

        #lbl_header_text
        self.lbl_header_text = self.ui_file_widget.findChild(QtGui.QLabel, 'lbl_header_text')

        #le_root_directory
        self.le_root_directory = self.ui_file_widget.findChild(QtGui.QLineEdit, 'le_root_directory')
        #le_asset_name
        self.le_asset_name = self.ui_file_widget.findChild(QtGui.QLineEdit, 'le_asset_name')
        #le_status
        self.le_status = self.ui_file_widget.findChild(QtGui.QLineEdit, 'le_status')
        
        #btn_set_root_directory
        self.btn_set_root_directory = self.ui_file_widget.findChild(QtGui.QPushButton, 'btn_set_root_directory')
        
        #btn_create_character_directories
        self.btn_create_character_directories = self.ui_file_widget.findChild(QtGui.QPushButton, 'btn_create_character_directories')
        #btn_create_prop_directories
        self.btn_create_prop_directories = self.ui_file_widget.findChild(QtGui.QPushButton, 'btn_create_prop_directories')
        #btn_create_shot_directories
        self.btn_create_shot_directories = self.ui_file_widget.findChild(QtGui.QPushButton, 'btn_create_shot_directories')
        #btn_create_comp_directories
        self.btn_create_comp_directories = self.ui_file_widget.findChild(QtGui.QPushButton, 'btn_create_comp_directories')
        #btn_create_photoscan_directories
        self.btn_create_photoscan_directories = self.ui_file_widget.findChild(QtGui.QPushButton, 'btn_create_photoscan_directories')

        #btn_reveal_in_explorer
        self.btn_reveal_in_explorer = self.ui_file_widget.findChild(QtGui.QPushButton, 'btn_reveal_in_explorer')
        
    
    
    
    
    #connect_ui
    def connect_ui(self):
        
        #btn_set_root_directory
        self.btn_set_root_directory.clicked.connect(functools.partial(self.set_root_directory))
        
        #btn_create_character_directories
        self.btn_create_character_directories.clicked.connect(functools.partial(self.create_directories, 'character'))
        #btn_create_prop_directories
        self.btn_create_prop_directories.clicked.connect(functools.partial(self.create_directories, 'prop'))
        #btn_create_shot_directories
        self.btn_create_shot_directories.clicked.connect(functools.partial(self.create_directories, 'shot'))
        #btn_create_comp_directories
        self.btn_create_comp_directories.clicked.connect(functools.partial(self.create_directories, 'comp'))
        #btn_create_photoscan_directories
        self.btn_create_photoscan_directories.clicked.connect(functools.partial(self.create_directories, 'photoscan'))

        #btn_reveal_in_explorer
        self.btn_reveal_in_explorer.clicked.connect(functools.partial(self.reveal_in_explorer))
        
        
    
    
    
    
    #configure_instance
    def configure_instance(self):
        
        #Embed created ui file in Layout
        lyt = QtGui.QVBoxLayout()
        lyt.addWidget(self.ui_file_widget)
        self.setLayout(lyt)
        
        #Configure instance size Policies
        self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding))

        #set self size
        self.resize(self.ui_file_widget.width(), self.ui_file_widget.height())

        #make sure its floating intead of embedded
        self.setWindowFlags(QtCore.Qt.Window)

        #set title
        self.setWindowTitle(self.title)

        #set icon
        #window_icon = QtGui.QIcon(self.icon_path)
        #self.setWindowIcon(window_icon)

        #set header icon
        self.wdgt_header_icon.setStyleSheet("border-image: url({0});".format(self.icon_path.replace('\\', '/')))

        #set header label
        self.lbl_header_text.setText(self.title)



        #Button tooltips
        #------------------------------------------------------------------
        
        #btn_create_character_directories
        self.btn_create_character_directories.setToolTip(directory_creator.CharacterDirectoryCreator('character', '').get_directories_string())
        #btn_create_prop_directories
        self.btn_create_prop_directories.setToolTip(directory_creator.PropDirectoryCreator('prop', '').get_directories_string())
        #btn_create_shot_directories
        self.btn_create_shot_directories.setToolTip(directory_creator.ShotDirectoryCreator('shot', '').get_directories_string())
        #btn_create_comp_directories
        self.btn_create_comp_directories.setToolTip(directory_creator.CompDirectoryCreator('comp', '').get_directories_string())
        #btn_create_photoscan_directories
        self.btn_create_photoscan_directories.setToolTip(directory_creator.PhotoscanDirectoryCreator('photoscan', '').get_directories_string())
        

        
        
        



    #Methods
    #------------------------------------------------------------------
    #------------------------------------------------------------------

    #create_directories
    def create_directories(self, directory_type = None):
        """
            Create Prop directories.
        """

        #directory_type is None
        if (directory_type is None):
            
            #log
            self.logger.debug('directory_type is None. Not creating directories, returning None')
            return None


        #asset_name
        asset_name = self.get_asset_name()

        #root_directory
        root_directory = self.get_root_directory()

        
        #check directory and asset
        if(self.check_directory_and_asset_names(asset_name, root_directory)):
            
            
            #creator_instance
            #------------------------------------------------------------------

            #creator_instance
            creator_instance = None

            #character
            if(directory_type == 'character'):
                #creator_instance
                creator_instance = directory_creator.CharacterDirectoryCreator(asset_name, root_directory)

            #prop
            elif(directory_type == 'prop'):
                #creator_instance
                creator_instance = directory_creator.PropDirectoryCreator(asset_name, root_directory)

            #shot
            elif(directory_type == 'shot'):
                #creator_instance
                creator_instance = directory_creator.ShotDirectoryCreator(asset_name, root_directory)

            #comp
            elif(directory_type == 'comp'):
                #creator_instance
                creator_instance = directory_creator.CompDirectoryCreator(asset_name, root_directory)

            #photoscan
            elif(directory_type == 'photoscan'):
                #creator_instance
                creator_instance = directory_creator.PhotoscanDirectoryCreator(asset_name, root_directory)


           




            #create directories
            #------------------------------------------------------------------
            
            #creator_instance is None
            if (creator_instance is None):

                #log
                self.logger.debug('creator_instance is None. Not creating directories, returning None')
                return None


            #asset_directory
            asset_directory = os.path.join(root_directory, asset_name)

            #create_directories
            try:

                #create_directories
                creator_instance.create_directories()

                #log
                self.logger.debug('Successfully created {0} directories in {1}'.format(creator_instance.get_directory_type(), 
                                                                                        asset_directory))

            except:

                #log
                self.logger.debug('Error creating directories for: {0}'.format())
            


    #reveal_in_explorer
    def reveal_in_explorer(self):
        """
            Reveal current root_directory asset_name combination in explorer if
            the directory exists.
        """

        #asset_name
        asset_name = self.get_asset_name()

        #root_directory
        root_directory = self.get_root_directory()

        
        #check directory and asset
        if(self.check_directory_and_asset_names(asset_name, root_directory, False)):

            #open folder
            subprocess.Popen(r'explorer /select,"{0}"'.format(os.path.join(root_directory, asset_name)))
            




    #Check Methods
    #------------------------------------------------------------------
    #------------------------------------------------------------------

    #check_directory_and_asset_names
    def check_directory_and_asset_names(self, asset_name, root_directory, asset_directory_exists_is_false = True):
        """
            Test suite for asset_name and root_directory
        """

        #asset_directory
        asset_directory = os.path.join(root_directory, asset_name)

        #asset_name empty
        if not(asset_name):
            #log
            self.logger.debug('Asset name empty. Not creating directories, returning False')
            return False

        #root_directory empty
        if not(root_directory):
            #log
            self.logger.debug('Root directory empty. Not creating directories, returning False')
            return False

        #root_directory doesnt exist
        if not(os.path.isdir(root_directory)):
            #log
            self.logger.debug('Root directory {0} does not exist. Not creating directories, returning False'.format(root_directory))
            return False

        
        #asset_directory_exists_is_false
        if(asset_directory_exists_is_false):
            #asset_directory exists
            if (os.path.isdir(asset_directory)):
                #log
                self.logger.debug('Asset directory {0} already exists. Not creating directories, returning False'.format(asset_directory))
                return False

        #asset_directory_exists_is_false = False
        if not (asset_directory_exists_is_false):
            #asset_directory exists
            if not (os.path.isdir(asset_directory)):
                #log
                self.logger.debug('Asset directory {0} does not exist. Returning False'.format(asset_directory))
                return False


        #checks successful
        return True



    
    
    
    #Getter & Setter
    #------------------------------------------------------------------
    #------------------------------------------------------------------
        
    #get_root_directory
    def get_root_directory(self):
        """
            Return content of le_root_directory
        """

        return str(self.le_root_directory.text())


    #set_root_directory
    def set_root_directory(self):
        """
            Set content of le_root_directory
        """

        #new_directory
        new_directory = QtGui.QFileDialog.getExistingDirectory()
        
        #if new_directory set it
        if(new_directory):
            #set text
            self.le_root_directory.setText(new_directory)

            #log
            self.logger.debug('Set root dir. to: {0}'.format(new_directory))

        #else
        else:
            #set text
            self.le_root_directory.setText('')
            #log
            self.logger.debug('Selected directory empty. New directory not set.')


    #get_asset_name
    def get_asset_name(self):
        """
            Return content of le_asset_name
        """

        return str(self.le_asset_name.text())


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



#Run
#------------------------------------------------------------------

def run():
    """
        Standardized run() method
    """

    #directory_wizard_instance
    directory_wizard_instance = DirectoryWizard()






#Test
#------------------------------------------------------------------

if (__name__ == '__main__'):

    #run
    run()
        
        
        
        
        

        