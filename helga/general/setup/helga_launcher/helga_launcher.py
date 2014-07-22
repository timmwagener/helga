

"""
helga_launcher
==========================================

GUI to start our pipeline DCCs.

-----------------------

The tool is available as precompiled binary under $PIPELINE_SCRIPTS_BASE_PATH/bin

-----------------------

**Author:** `Timm Wagener <mailto:wagenertimm@gmail.com>`_
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
media_path = os.path.join(tool_root_path, 'media')
#check for py2exe
if not(os.path.isdir(media_path)):
    media_path = os.path.abspath(os.path.join(tool_root_path, '..', 'media'))
#append
sys.path.append(media_path)


#icons_path
icons_path = os.path.join(media_path, 'icons')
sys.path.append(icons_path)


#data_path
data_path = os.path.join(tool_root_path, 'data')
#check for py2exe
if not(os.path.isdir(data_path)):
    data_path = os.path.abspath(os.path.join(tool_root_path, '..', 'data'))
#append
sys.path.append(data_path)







#Import
#------------------------------------------------------------------
#python
import functools
import logging
import subprocess
import time
import yaml
import shutil
import webbrowser
#PyQt4
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import uic


#Import variable
do_reload = True

#helga_launcher_logging_handler
from lib import helga_launcher_logging_handler
if(do_reload):reload(helga_launcher_logging_handler)

#environment_variables_model
from lib import environment_variables_model
if(do_reload):reload(environment_variables_model)

#environment_variables_view
from lib import environment_variables_view
if(do_reload):reload(environment_variables_view)

#environment_variables_item_delegate
from lib import environment_variables_item_delegate
if(do_reload):reload(environment_variables_item_delegate)

#helga_launcher_dcc_button
from lib import helga_launcher_dcc_button
if(do_reload):reload(helga_launcher_dcc_button)

#helga_launcher_favorites_functionality
from lib import helga_launcher_favorites_functionality
if(do_reload):reload(helga_launcher_favorites_functionality)



#launcher modules

#helga_launcher_maya_functionality
from lib import helga_launcher_maya_functionality
if(do_reload):reload(helga_launcher_maya_functionality)

#helga_launcher_nuke_functionality
from lib import helga_launcher_nuke_functionality
if(do_reload):reload(helga_launcher_nuke_functionality)

#helga_launcher_houdini_functionality
from lib import helga_launcher_houdini_functionality
if(do_reload):reload(helga_launcher_houdini_functionality)

#helga_launcher_ocio_functionality
from lib import helga_launcher_ocio_functionality
if(do_reload):reload(helga_launcher_ocio_functionality)







#UI classes
#------------------------------------------------------------------

#ui_file_path
ui_file_path = os.path.join(media_path, 'helga_launcher.ui')
classes_list = uic.loadUiType(ui_file_path)











#HelgaLauncher class
#------------------------------------------------------------------

class HelgaLauncher(classes_list[0], classes_list[1]):
    
    #Constructor
    def __init__(self, 
                logging_level = logging.DEBUG,
                command_line_args_dict = {},
                parent = None):
        
        #super class init
        super(HelgaLauncher, self).__init__(parent)


        #instance variables
        #------------------------------------------------------------------
        self.title_name = self.__class__.__name__
        self.version = 0.4
        self.title = self.title_name +' ' + str(self.version)

        #command_line_args_dict
        self.command_line_args_dict = command_line_args_dict

        #env_var_dict
        self.env_var_dict = {}
        #env_var_list
        self.env_var_list = []

        

        #logger
        #------------------------------------------------------------------
        #status_handler
        self.status_handler = helga_launcher_logging_handler.StatusStreamHandler(self)
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

        #set_pipeline_base_env_vars
        self.set_pipeline_base_env_vars()

        #update_env_var_model
        self.update_env_var_model()

        #unique_value_list (variables names of vars that should only have one value, like OCIO)
        unique_value_list = ['OCIO']
        #set_environment_vars
        self.set_environment_vars(unique_value_list = unique_value_list)



        
        



    #UI Methods
    #------------------------------------------------------------------
    
    #setup_additional_ui
    def setup_additional_ui(self):
        """
        Setup additional ui elements.
        """

        #set header icon
        header_icon_path = ''
        header_icon_name = 'icon_helga_launcher.png'
        header_icon_path = os.path.join(icons_path, header_icon_name)
        
        #set stylesheet header
        self.wdgt_header_icon.setStyleSheet("border-image: url({0});".format(header_icon_path.replace('\\', '/')))
        
        
        #set title
        self.setWindowTitle(self.title)
        #set header label
        self.lbl_header_text.setText(self.title)

        #setup dcc buttons
        self.setup_dcc_buttons()

        #setup_mvc
        self.setup_mvc()

    
    def setup_dcc_buttons(self):
        """
        Setup the buttons used to launch the pipeline DCCs
        """

        
        #btn_launch_maya
        dcc_name = 'maya'
        button_icon_path = os.path.join(icons_path, 'icon_dcc_button_{0}.png'.format(dcc_name)).replace('\\', '/')
        button_icon_path_hover = os.path.join(icons_path, 'icon_dcc_button_{0}_hover.png'.format(dcc_name)).replace('\\', '/')
        button_icon_path_drag = os.path.join(icons_path, 'icon_dcc_button_{0}_drag.png'.format(dcc_name)).replace('\\', '/')
        self.btn_launch_maya = helga_launcher_dcc_button.HelgaLauncherDCCButton(button_text = 'Launch {0}'.format(dcc_name), 
                                                                                icon_path = button_icon_path,
                                                                                icon_path_hover = button_icon_path_hover,
                                                                                icon_path_drag = button_icon_path_drag)
        self.btn_launch_maya.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        #add to lyt
        self.lyt_dcc_buttons.addWidget(self.btn_launch_maya, 0, 0)

        #btn_launch_houdini
        dcc_name = 'houdini'
        button_icon_path = os.path.join(icons_path, 'icon_dcc_button_{0}.png'.format(dcc_name)).replace('\\', '/')
        button_icon_path_hover = os.path.join(icons_path, 'icon_dcc_button_{0}_hover.png'.format(dcc_name)).replace('\\', '/')
        button_icon_path_drag = os.path.join(icons_path, 'icon_dcc_button_{0}_drag.png'.format(dcc_name)).replace('\\', '/')
        self.btn_launch_houdini = helga_launcher_dcc_button.HelgaLauncherDCCButton(button_text = 'Launch {0}'.format(dcc_name), 
                                                                                icon_path = button_icon_path,
                                                                                icon_path_hover = button_icon_path_hover,
                                                                                icon_path_drag = button_icon_path_drag)
        self.btn_launch_houdini.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        #add to lyt
        self.lyt_dcc_buttons.addWidget(self.btn_launch_houdini, 0, 1)

        #btn_launch_nuke
        dcc_name = 'nuke'
        button_icon_path = os.path.join(icons_path, 'icon_dcc_button_{0}.png'.format(dcc_name)).replace('\\', '/')
        button_icon_path_hover = os.path.join(icons_path, 'icon_dcc_button_{0}_hover.png'.format(dcc_name)).replace('\\', '/')
        button_icon_path_drag = os.path.join(icons_path, 'icon_dcc_button_{0}_drag.png'.format(dcc_name)).replace('\\', '/')
        self.btn_launch_nuke = helga_launcher_dcc_button.HelgaLauncherDCCButton(button_text = 'Launch {0}'.format(dcc_name), 
                                                                                icon_path = button_icon_path,
                                                                                icon_path_hover = button_icon_path_hover,
                                                                                icon_path_drag = button_icon_path_drag)
        self.btn_launch_nuke.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        #add to lyt
        self.lyt_dcc_buttons.addWidget(self.btn_launch_nuke, 1, 0)

        #btn_launch_hiero
        dcc_name = 'hiero'
        button_icon_path = os.path.join(icons_path, 'icon_dcc_button_{0}.png'.format(dcc_name)).replace('\\', '/')
        button_icon_path_hover = os.path.join(icons_path, 'icon_dcc_button_{0}_hover.png'.format(dcc_name)).replace('\\', '/')
        button_icon_path_drag = os.path.join(icons_path, 'icon_dcc_button_{0}_drag.png'.format(dcc_name)).replace('\\', '/')
        self.btn_launch_hiero = helga_launcher_dcc_button.HelgaLauncherDCCButton(button_text = 'Launch {0}'.format(dcc_name), 
                                                                                icon_path = button_icon_path,
                                                                                icon_path_hover = button_icon_path_hover,
                                                                                icon_path_drag = button_icon_path_drag)
        self.btn_launch_hiero.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        #add to lyt
        self.lyt_dcc_buttons.addWidget(self.btn_launch_hiero, 1, 1)


        #btn_launch_doc
        dcc_name = 'doc'
        button_icon_path = os.path.join(icons_path, 'icon_dcc_button_{0}.png'.format(dcc_name)).replace('\\', '/')
        button_icon_path_hover = os.path.join(icons_path, 'icon_dcc_button_{0}_hover.png'.format(dcc_name)).replace('\\', '/')
        button_icon_path_drag = os.path.join(icons_path, 'icon_dcc_button_{0}_drag.png'.format(dcc_name)).replace('\\', '/')
        self.btn_launch_doc = helga_launcher_dcc_button.HelgaLauncherDCCButton(button_text = 'Launch {0}'.format(dcc_name), 
                                                                                icon_path = button_icon_path,
                                                                                icon_path_hover = button_icon_path_hover,
                                                                                icon_path_drag = button_icon_path_drag)
        self.btn_launch_doc.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        #add to lyt
        self.lyt_dcc_buttons.addWidget(self.btn_launch_doc, 2, 0)


        


    def setup_mvc(self):
        """
        Setup model-view controller
        """

        #env_var_table_view
        self.env_var_table_view = environment_variables_view.EnvironmentVariablesView()
        self.env_var_table_view.setWordWrap(True)
        #set resize mode for horizontal header
        self.env_var_table_view.horizontalHeader().setResizeMode(3)
        self.env_var_table_view.horizontalHeader().setStretchLastSection(True)
        self.env_var_table_view.verticalHeader().setResizeMode(3)
        self.env_var_table_view.setAlternatingRowColors(True)
        #add to ui
        self.lyt_env_var_table_view.addWidget(self.env_var_table_view)

        #env_var_table_view_item_delegate
        self.env_var_table_view_item_delegate = environment_variables_item_delegate.EnvironmentVariablesItemDelegate()
        #set in view
        self.env_var_table_view.setItemDelegate(self.env_var_table_view_item_delegate)

        
        #env_var_table_model
        self.env_var_table_model = environment_variables_model.EnvironmentVariablesModel()
        #set model in view
        self.env_var_table_view.setModel(self.env_var_table_model)

    
    #connect_ui
    def connect_ui(self):
        """
        Connect ui elements.
        """

        #btn_create_favorites
        self.btn_create_favorites.clicked.connect(functools.partial(helga_launcher_favorites_functionality.add_favorites))
        #btn_remove_favorites
        self.btn_remove_favorites.clicked.connect(functools.partial(helga_launcher_favorites_functionality.remove_favorites))

        #btn_create_desktop_shortcuts
        self.btn_create_desktop_shortcuts.clicked.connect(functools.partial(helga_launcher_favorites_functionality.create_desktop_shortcuts))
        #btn_remove_desktop_shortcuts
        self.btn_remove_desktop_shortcuts.clicked.connect(functools.partial(helga_launcher_favorites_functionality.remove_desktop_shortcuts))
        


        #btn_launch_maya
        self.btn_launch_maya.clicked.connect(functools.partial(helga_launcher_maya_functionality.run))
        self.connect(self.btn_launch_maya, QtCore.SIGNAL("dropped"), self.drop_on_maya_button)
        
        #btn_launch_houdini
        self.btn_launch_houdini.clicked.connect(functools.partial(helga_launcher_houdini_functionality.run))
        self.connect(self.btn_launch_houdini, QtCore.SIGNAL("dropped"), self.drop_on_houdini_button)

        #btn_launch_nuke
        self.btn_launch_nuke.clicked.connect(functools.partial(helga_launcher_nuke_functionality.run))
        self.connect(self.btn_launch_nuke, QtCore.SIGNAL("dropped"), self.drop_on_nuke_button)

        #btn_launch_doc
        self.btn_launch_doc.clicked.connect(functools.partial(self.open_doc))
        
        
        

        



    #Table model
    #------------------------------------------------------------------

    def update_env_var_model(self):
        """
        Update self.env_var_model
        """

        #set_pipeline_env_var_dict
        self.set_pipeline_env_var_dict()

        #set_pipeline_env_var_list
        self.set_pipeline_env_var_list()

        #update model
        self.env_var_table_model.update(self.env_var_list)

    
    def set_pipeline_env_var_dict(self):
        """
        Return a nested list with all pipeline specific env vars.
        """

        #env_var_dict_maya
        env_var_dict_maya = helga_launcher_maya_functionality.get_env_vars()
        app_name_maya = helga_launcher_maya_functionality.get_app_name()

        #env_var_dict_nuke
        env_var_dict_nuke = helga_launcher_nuke_functionality.get_env_vars()
        app_name_nuke = helga_launcher_nuke_functionality.get_app_name()

        #env_var_dict_houdini
        env_var_dict_houdini = helga_launcher_houdini_functionality.get_env_vars()
        app_name_houdini = helga_launcher_houdini_functionality.get_app_name()

        #env_var_dict_ocio
        env_var_dict_ocio = helga_launcher_ocio_functionality.get_env_vars()
        app_name_ocio = helga_launcher_ocio_functionality.get_app_name()


        #env_var_dict
        env_var_dict = {app_name_maya:env_var_dict_maya, 
                        app_name_nuke:env_var_dict_nuke, 
                        app_name_houdini:env_var_dict_houdini,
                        app_name_ocio:env_var_dict_ocio}

        #env_var_dict
        self.env_var_dict = env_var_dict


    def set_pipeline_env_var_list(self):
        """
        Convert env. var. dict to nested list to be set in model
        """

        #env_var_exclusive_dict
        env_var_exclusive_dict = {}

        #iterate env_var_dict
        for dcc_name, dcc_dict in self.env_var_dict.iteritems():

            #iterate dcc_dict
            for env_var_name, env_var_value_list in dcc_dict.iteritems():

                #convert to list if not of type list
                if not(type(env_var_value_list) is list):
                    env_var_value_list = [env_var_value_list]

                #append
                #env var not in dict
                if not(env_var_name in env_var_exclusive_dict.keys()):
                    env_var_exclusive_dict[env_var_name] = env_var_value_list
                #key already in there
                else:
                    current_env_var_value_list = env_var_exclusive_dict[env_var_name]
                    env_var_exclusive_dict[env_var_name] = list(set(current_env_var_value_list + env_var_value_list))

        #env_var_list
        env_var_list = []

        #iterate and append
        for env_var_name, env_var_value_list in env_var_exclusive_dict.iteritems():

            #append
            env_var_list.append([env_var_name, env_var_value_list])


        #env_var_list
        self.env_var_list = env_var_list 



    


    


    

    #Set environment vars.
    #------------------------------------------------------------------

    def set_environment_vars(self, unique_value_list = []):
        """
        Set env. vars. from self.env_var_list
        """

        #iterate
        for variable_name, variable_value_list in self.env_var_list:

            #iterate variable values
            for variable_value in variable_value_list:

                #env var does not exist
                if not(os.getenv(variable_name, False)):
                    os.environ[variable_name] = variable_value
                #env var exists
                else:
                    os.environ[variable_name] = os.getenv(variable_name) + ';' + variable_value

                #exception for ocio (needs to be unique)
                if(variable_name in unique_value_list):
                    os.environ[variable_name] = variable_value

    





    #Pipeline base variables (pre-pipeline, before global_variables module)
    #------------------------------------------------------------------
    
    def set_pipeline_base_env_vars(self):
        """
        Set base env. vars. used by global_variables module to build complete structure.

        HELGA_PIPELINE_BASE_PATH
        HELGA_PIPELINE_FLAVOUR
        HELGA_MAYA_EXE
        HELGA_NUKE_EXE
        HELGA_HOUDINI_EXE
        """

        #Env. Vars. from Yaml
        #------------------------------------------------------------------

        #log
        print('\n\nPipeline Base Environment Variables (from yaml)\n------------------------------------------------')

        #pipeline_base_data_dict
        pipeline_base_data_dict = self.get_pipeline_base_data()

        #iterate and set
        for key, value in pipeline_base_data_dict.iteritems():
            #set env var
            os.environ['HELGA_{0}'.format(key)] = value
            #log
            print('{0} - {1}'.format('HELGA_{0}'.format(key), value))



        
        #Build and append PIPELINE_SCRIPTS_BASE_PATH to import helga
        #------------------------------------------------------------------

        #PIPELINE_BASE_PATH
        PIPELINE_BASE_PATH = os.getenv('HELGA_PIPELINE_BASE_PATH', False)

        #PIPELINE_SCRIPTS_BASE_PATH
        PIPELINE_SCRIPTS_BASE_PATH = PIPELINE_BASE_PATH + r'/Production/scripts/' + os.getenv('HELGA_PIPELINE_FLAVOUR', False) + r'/helga'

        #You need to set with sys.path.append and os.environ['PYTHONPATH'] to transfer to child processes !?
        #append with sys.path
        sys.path.append(PIPELINE_SCRIPTS_BASE_PATH)

        #env var does not exist
        if not(os.getenv('PYTHONPATH', False)):
            os.environ['PYTHONPATH'] = PIPELINE_SCRIPTS_BASE_PATH
        #env var exists
        else:
            os.environ['PYTHONPATH'] = os.getenv('PYTHONPATH') +';' + PIPELINE_SCRIPTS_BASE_PATH
    


    def get_pipeline_base_data(self):
        """
        Return dict with pipeline base data, either from yaml file distributed along
        or from command line option --custom_yaml_path.
        """

        #yaml_path
        yaml_path = os.path.join(data_path, 'pipeline_base_data.yaml')
        
        #sandbox
        if(self.command_line_args_dict.get('sandbox', None)):
            #yaml_path
            yaml_path = os.path.join(data_path, 'pipeline_base_data_sandbox.yaml')
        
        #command line option (-cyp, --custom_yaml_path)
        if(self.command_line_args_dict.get('custom_yaml_path', None)):
            #check if path exists
            if(os.path.isfile(self.command_line_args_dict.get('custom_yaml_path', None))):
                #yaml_path
                yaml_path = self.command_line_args_dict.get('custom_yaml_path', None)

        
        
        
        #pipeline_base_data_dict
        pipeline_base_data_dict = self.load_yaml(yaml_path)

        
        return pipeline_base_data_dict


    def load_yaml(self, yaml_path):
        """
        Load yaml from file
        """

        #yaml_object
        yaml_object = None
        
        try:
            with open(yaml_path) as yaml_file:
                yaml_object = yaml.load(yaml_file)

            #log
            self.logger.debug('Retrieved objects from yaml file {0}.'.format(yaml_path))

        except:

            #log
            self.logger.debug('Error retrieving yaml file {0}. Returning None'.format(yaml_path))
            return None

        return yaml_object







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
    

    





    #Drag & Drop
    #------------------------------------------------------------------

    def check_file_type(self, file_path, file_type):
        """
        Check file_path for file_type
        """

        #file_extension
        file_extension = os.path.splitext(file_path)[-1][1:]

        if(file_extension == file_type):
            return True

        return False


    def drop_on_maya_button(self, drop_url_list):
        """
        Drop callback for self.btn_launch_maya
        """

        #drop_url
        try:
            drop_url = drop_url_list[0]
        except:
            #log
            self.logger.debug('Error aquiring drop url')
            return

        #file exists
        if not(os.path.isfile(drop_url)):
            
            #log
            self.logger.debug('File {0} does not exist'.format(drop_url))
            return

        #is maya file
        if not (self.check_file_type(drop_url, 'ma') or 
                self.check_file_type(drop_url, 'mb')):
            
            #file_extension
            file_extension = os.path.splitext(drop_url)[-1][1:]

            #log
            self.logger.debug('Wrong file type {0} for maya'.format(file_extension))
            return

        #run
        helga_launcher_maya_functionality.run(file_path = drop_url)


    def drop_on_nuke_button(self, drop_url_list):
        """
        Drop callback for self.btn_launch_nuke
        """

        #drop_url
        try:
            drop_url = drop_url_list[0]
        except:
            #log
            self.logger.debug('Error aquiring drop url')
            return

        #file exists
        if not(os.path.isfile(drop_url)):
            
            #log
            self.logger.debug('File {0} does not exist'.format(drop_url))
            return

        #is maya file
        if not (self.check_file_type(drop_url, 'nk')):
            
            #file_extension
            file_extension = os.path.splitext(drop_url)[-1][1:]

            #log
            self.logger.debug('Wrong file type {0} for nuke'.format(file_extension))
            return

        #run
        helga_launcher_nuke_functionality.run(file_path = drop_url)


    def drop_on_houdini_button(self, drop_url_list):
        """
        Drop callback for self.btn_launch_houdini
        """

        #drop_url
        try:
            drop_url = drop_url_list[0]
        except:
            #log
            self.logger.debug('Error aquiring drop url')
            return

        #file exists
        if not(os.path.isfile(drop_url)):
            
            #log
            self.logger.debug('File {0} does not exist'.format(drop_url))
            return

        #is maya file
        if not (self.check_file_type(drop_url, 'hip') or 
                self.check_file_type(drop_url, 'hipnc')):
            
            #file_extension
            file_extension = os.path.splitext(drop_url)[-1][1:]

            #log
            self.logger.debug('Wrong file type {0} for houdini'.format(file_extension))
            return

        #run
        helga_launcher_houdini_functionality.run(file_path = drop_url)

    
    def print_drop_urls(self, drop_url_list):
        """
        Print url drop list
        """

        for index, drop_url in enumerate(drop_url_list):
            print(drop_url)






    #Docs
    #------------------------------------------------------------------

    def open_doc(self):
        """
        Open pipeline docs
        """

        try:
            
            #Reload boolean
            do_reload = True

            #Import
            from helga.general.setup.doc_link import doc_link
            if(do_reload): reload(doc_link)

            #Execute
            doc_link.run()

            #log
            self.logger.debug('Successfully opened helga docs')
            return

        except:

            #log
            self.logger.debug('Error opening helga docs')
            return






    #Events
    #------------------------------------------------------------------

    def closeEvent(self, event):
        """
        Customized closeEvent
        """
        print('run parent closeEvent')
        super(HelgaLauncher, self).closeEvent(event)


    





    #Temp
    #------------------------------------------------------------------

    def dummy_method(self, msg = 'dummy'):
        """
        Dummy method
        """

        #log
        self.logger.debug('{0}'.format(msg))
        #print
        print('{0}'.format(msg))

        