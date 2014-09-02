

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
import logging

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










#MayapyExportProcess class
#------------------------------------------------------------------
class MayapyExportProcess(object):
    """
    Helper class to run the whole alembic export process in Mayapy in headless mode.
    """

    def __new__(cls, *args, **kwargs):
        """
        MayapyExportProcess instance factory.
        """

        #mayapy_export_process_instance
        mayapy_export_process_instance = super(MayapyExportProcess, cls).__new__(cls, args, kwargs)

        return mayapy_export_process_instance

    
    def __init__(self, logging_level = logging.DEBUG):
        """
        Customize MayapyExportProcess instance.
        """

        #logger
        #------------------------------------------------------------------
        
        #logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logging_level = logging_level
        self.logger.setLevel(self.logging_level)




        #instance variables
        #------------------------------------------------------------------

        #export_dict
        self.export_dict = self.get_export_dict()






    #Run
    #------------------------------------------------------------------

    def run(self):
        """
        Method to start export process.
        """

        #print_export_dict
        self.print_export_dict()

        #open_file_and_export
        self.open_file_and_export()



    #Methods
    #------------------------------------------------------------------

    def get_export_dict(self):
        """
        Get dict of the env. vars. that start with HELGA_ABC
        """

        #env_dict
        env_dict = os.environ.copy()

        #export_dict
        export_dict = {}
        #iterate
        for key, value in env_dict.iteritems():

            #start with HELGA_ABC
            if (key.startswith('HELGA_ABC')):

                #set
                export_dict.setdefault(key, value)

        #return
        return export_dict


    def print_export_dict(self):
        """
        Get dict of the env. vars. that start with HELGA_ABC
        """

        #get_export_dict
        export_dict = self.get_export_dict()

        #iterate
        for key, value in export_dict.iteritems():

            self.logger.debug('{0} - {1}'.format(key, value))


    def open_file_and_export(self):
        """
        Get the env. vars., open the file and export.
        """

        #abc_command
        abc_command = self.export_dict.get('HELGA_ABC_COMMAND', None)
        #check
        if not (abc_command):
            #log
            self.logger.debug('HELGA_ABC_COMMAND is None. Not exporting.')
            return

        #maya_file
        maya_file = self.export_dict.get('HELGA_ABC_MAYA_FILE', None)
        #check
        if not (maya_file):
            #log
            self.logger.debug('HELGA_ABC_MAYA_FILE is None. Not exporting.')
            return



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















#Run
#------------------------------------------------------------------

def run():
    """
    Execute the export.
    """

    #mayapy_export_process_instance
    mayapy_export_process_instance = MayapyExportProcess()
    #run
    mayapy_export_process_instance.run()










