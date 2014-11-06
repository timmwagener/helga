





"""
direct_access
==========================================

Methods to set env. variables and launch applications.

-----------------------

To execute use this with shell:

cd path/to/direct_access
python -c 'import direct_access;reload(direct_access);direct_access.run("houdini")'

-----------------------

Possible applications are:

#. maya
#. houdini
#. nuke
-----------------------
"""





#Import
#------------------------------------------------------------------
#python
import sys
import os
import functools
import logging
import subprocess










#Globals
#------------------------------------------------------------------

MODULE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
YAML_DIRECTORY = os.path.join(MODULE_DIRECTORY, 'yaml')
YAML_FILE_NAME = 'pipeline_base_data.yaml'
YAML_PATH = os.path.join(YAML_DIRECTORY, YAML_FILE_NAME)
VALID_APPLICATION_LIST = ['houdini', 'maya', 'nuke']










#Run Main Functions
#------------------------------------------------------------------

def run(application = None):
    """
    Run Houdini within the helga pipeline.
    Possible applications are:

    #. maya
    #. houdini
    #. nuke
    """

    #application empty
    if not (application):

        #log
        print('You did not pass an application. Please pass either maya, houdini or nuke as parameter to run.')
        return

    #application invalid
    if not (application in VALID_APPLICATION_LIST):

        #log
        print('{0} is not a valid application. Please pass either maya, houdini or nuke as parameter to run.'.format(application))
        return



    #set_pipeline_base_env_vars
    set_pipeline_base_env_vars()

    #set_environment_vars
    set_environment_vars()

    #run_application
    run_application(application)










#Functions
#------------------------------------------------------------------


#Pipeline Base Data
#------------------------------------------------------------------


def set_pipeline_base_env_vars():
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
    pipeline_base_data_dict = get_pipeline_base_data()

    #check
    if not (pipeline_base_data_dict):

        #log
        print('pipeline_base_data_dict empty. Not setting pipeline base env vars.')
        return


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
        os.environ['PYTHONPATH'] = os.getenv('PYTHONPATH') + os.pathsep + PIPELINE_SCRIPTS_BASE_PATH


def get_pipeline_base_data():
    """
    Return dict with pipeline base data from yaml file.
    """

    #pipeline_base_data_dict
    pipeline_base_data_dict = None

    try:

        #import
        import yaml

        #pipeline_base_data_dict
        pipeline_base_data_dict = load_yaml(YAML_PATH)

    except:

        #pipeline_base_data_dict
        pipeline_base_data_dict = parse_yaml_file_manually(YAML_PATH)
    

    return pipeline_base_data_dict


def load_yaml(yaml_path):
    """
    Load yaml from file
    """

    #custom
    import yaml

    #yaml_object
    yaml_object = None
    
    try:
        with open(yaml_path) as yaml_file:
            yaml_object = yaml.load(yaml_file)

        #log
        print('Retrieved objects from yaml file {0}.'.format(yaml_path))

    except:

        #log
        print('Error retrieving yaml file {0}. Returning None'.format(yaml_path))
        return None


    return yaml_object


def parse_yaml_file_manually(yaml_path):
    """
    Read yaml file with text parsing. Help method in case yaml cannot be imported.
    In a clean environment this is never used.
    """

    #check path
    if not (os.path.isfile(yaml_path)):

        #log
        print('YAML path {0} does not exist.'.format(yaml_path))
        return None

    #lines_list
    with open(yaml_path) as yaml_file:
        lines_list = yaml_file.readlines()

        #log
        print('Retrieved objects from yaml file {0}.'.format(yaml_path))


    #keyword_list
    keyword_list = ['PIPELINE_BASE_PATH', 'PIPELINE_FLAVOUR', 'MAYA_EXE', 'NUKE_EXE', 'HOUDINI_EXE']

    #pipeline_base_data_dict
    pipeline_base_data_dict = {}

    #iterate and fill pipeline_base_data_dict
    for line in lines_list:

        #iterate keywords
        for keyword in keyword_list:

            #check match
            if (line.startswith(keyword)):

                #value
                value = line[len(keyword):]
                value = value.replace(':', '', 1)
                value = value.replace('"', '')
                value = value.replace('\n', '')
                value = value.replace('\r', '')
                value = value.replace(' ', '', 1)

                #append to pipeline_base_data_dict
                pipeline_base_data_dict[keyword] = value
                break

    
    #check if empty
    if not (pipeline_base_data_dict):
        pipeline_base_data_dict = None

    
    #return
    return pipeline_base_data_dict







#Pipeline Env Vars
#------------------------------------------------------------------


def get_pipeline_env_var_dict():
    """
    Return a nested list with all pipeline specific env vars.
    """

    #do_reload
    do_reload = True

    #helga_launcher_maya_functionality
    from helga.general.setup.helga_launcher.lib import helga_launcher_maya_functionality
    if(do_reload):reload(helga_launcher_maya_functionality)

    #helga_launcher_nuke_functionality
    from helga.general.setup.helga_launcher.lib import helga_launcher_nuke_functionality
    if(do_reload):reload(helga_launcher_nuke_functionality)

    #helga_launcher_houdini_functionality
    from helga.general.setup.helga_launcher.lib import helga_launcher_houdini_functionality
    if(do_reload):reload(helga_launcher_houdini_functionality)

    #helga_launcher_ocio_functionality
    from helga.general.setup.helga_launcher.lib import helga_launcher_ocio_functionality
    if(do_reload):reload(helga_launcher_ocio_functionality)


    
    
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

    #return
    return env_var_dict


def get_pipeline_env_var_list():
    """
    Convert env. var. dict to nested list (because that was handy for the helga_launcher mvc).
    Unneccessary here, but needed for the set_environment_vars() method that uses this method.
    """

    #env_var_dict
    env_var_dict = get_pipeline_env_var_dict()

    #env_var_exclusive_dict
    env_var_exclusive_dict = {}

    #iterate env_var_dict
    for dcc_name, dcc_dict in env_var_dict.iteritems():

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


    #return
    return env_var_list


def set_environment_vars(unique_value_list = ['OCIO']):
    """
    Set env. vars. from env_var_list
    """

    #env_var_list
    env_var_list = get_pipeline_env_var_list()

    #iterate
    for variable_name, variable_value_list in env_var_list:

        #iterate variable values
        for variable_value in variable_value_list:

            #env var does not exist
            if not(os.getenv(variable_name, False)):
                os.environ[variable_name] = variable_value
            #env var exists (insert new value at the beginning)
            else:
                os.environ[variable_name] = variable_value + ';' + os.getenv(variable_name)

            #exception for ocio (needs to be unique)
            if(variable_name in unique_value_list):
                os.environ[variable_name] = variable_value









#Run Application
#------------------------------------------------------------------

def run_application(application = None):
    """
    Run application.
    """

    #maya
    if (application == 'maya'):
        run_application_maya()

    #nuke
    elif (application == 'nuke'):
        run_application_nuke()

    #houdini
    elif (application == 'houdini'):
        run_application_houdini()

    #unknown (this should have been caught before)
    else:
        
        #log
        print('Application {0} unknown'.format(application))


def run_application_maya():
    """
    Run application maya.
    """

    #do_reload
    do_reload = True

    #import
    from helga.general.setup.helga_launcher.lib import helga_launcher_maya_functionality
    if(do_reload): reload(helga_launcher_maya_functionality)
    
    #run
    helga_launcher_maya_functionality.run()
    

def run_application_nuke():
    """
    Run application nuke.
    """

    #do_reload
    do_reload = True

    #import
    from helga.general.setup.helga_launcher.lib import helga_launcher_nuke_functionality
    if(do_reload): reload(helga_launcher_nuke_functionality)
    
    #run
    helga_launcher_nuke_functionality.run()


def run_application_houdini():
    """
    Run application houdini.
    """

    #do_reload
    do_reload = True

    #import
    from helga.general.setup.helga_launcher.lib import helga_launcher_houdini_functionality
    if(do_reload): reload(helga_launcher_houdini_functionality)
    
    #run
    helga_launcher_houdini_functionality.run()

