

"""
helga_launcher_loader
==========================================

Helper module to enable import of helga_launcher.
This module makes sure the __file__ attribute of the helga_launcher module delivers
a path.

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
import argparse
#PyQt4
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import uic
#qdarkstyle
import qdarkstyle


#Import variable
do_reload = True

#helga_launcher
import helga_launcher
if(do_reload):reload(helga_launcher)








#load_helga_launcher
#------------------------------------------------------------------

#load_helga_launcher
def load_helga_launcher():
    """
    Start an QApp loop and load an instance of HelgaLauncher in it.
    """

    #Command line args
    #------------------------------------------------------------------

    #parser
    parser = argparse.ArgumentParser(description = 'Parse the command line for helga_launcher variables.')
    
    #custom_yaml_path
    parser.add_argument('-cyp','--custom_yaml_path', help='Path to custom yaml file. This file holds the base pipeline data.', required=False)
    #sandbox
    parser.add_argument('-sbx','--sandbox', help='Use builtin sandbox yaml file.', required=False, type=int, default=0)
    #runmaya
    parser.add_argument('-rma','--runmaya', help='Immediately start Maya.', required=False, type=int, default=0)
    #runnuke
    parser.add_argument('-rnk','--runnuke', help='Immediately start Nuke.', required=False, type=int, default=0)
    #runhoudini
    parser.add_argument('-rho','--runhoudini', help='Immediately start Houdini.', required=False, type=int, default=0)
    #rundoc
    parser.add_argument('-rdo','--rundoc', help='Immediately start documentation.', required=False, type=int, default=0)

    
    #command_line_args_dict
    command_line_args_dict = vars(parser.parse_args())
    
    #print command line args
    print('\n\nCommand Line Arguments\n------------------------------------------------')
    for argument_name, argument_value in command_line_args_dict.iteritems():
        print('{0} - {1}'.format(argument_name, argument_value))


    #Start helga launcher
    #------------------------------------------------------------------
    
    #app_helga_launcher
    app_helga_launcher = QtGui.QApplication(sys.argv)

    #load darkstyle
    app_helga_launcher.setStyleSheet(qdarkstyle.load_stylesheet(pyside=False))

    #helga_launcher_instance (instanciation sets up env. vars.)
    helga_launcher_instance = helga_launcher.HelgaLauncher(command_line_args_dict = command_line_args_dict)

    

    #directly run application / no GUI
    if(command_line_args_dict.get('runmaya') or
        command_line_args_dict.get('runnuke') or
        command_line_args_dict.get('runhoudini') or
        command_line_args_dict.get('rundoc')):

        

        #launch maya
        if (command_line_args_dict.get('runmaya')):
            #run
            run_maya()
            

        #launch nuke
        if (command_line_args_dict.get('runnuke')):
            #run
            run_nuke()

        #launch houdini
        if (command_line_args_dict.get('runhoudini')):
            #run
            run_houdini()

        #launch doc
        if (command_line_args_dict.get('rundoc')):
            helga_launcher_instance.open_doc()

        #exit helga launcher
        sys.exit(0)

    #else show ui
    else:

        #show
        helga_launcher_instance.show()

    #exit
    sys.exit(app_helga_launcher.exec_())






#Run methods
#------------------------------------------------------------------

def run_maya():
    """
    Run maya
    """
    
    #do_reload
    do_reload = True

    #helga_launcher_maya_functionality
    from lib import helga_launcher_maya_functionality
    if(do_reload):reload(helga_launcher_maya_functionality)

    #run
    helga_launcher_maya_functionality.run()


def run_nuke():
    """
    Run nuke
    """
    
    #do_reload
    do_reload = True

    #helga_launcher_maya_functionality
    from lib import helga_launcher_nuke_functionality
    if(do_reload):reload(helga_launcher_nuke_functionality)

    #run
    helga_launcher_nuke_functionality.run()


def run_houdini():
    """
    Run houdini
    """
    
    #do_reload
    do_reload = True

    #helga_launcher_maya_functionality
    from lib import helga_launcher_houdini_functionality
    if(do_reload):reload(helga_launcher_houdini_functionality)

    #run
    helga_launcher_houdini_functionality.run()




#Run if not imported
#------------------------------------------------------------------
if (__name__ == '__main__'):

    #load_helga_launcher
    load_helga_launcher()
    
    
    
    
        

        