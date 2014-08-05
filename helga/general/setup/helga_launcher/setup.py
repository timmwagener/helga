

"""
setup
=====

Helper module for py2exe to build a distribution.

-----------------------

**Author:** `Timm Wagener <mailto:wagenertimm@gmail.com>`_
"""






#win32com py2exe shell fix
#------------------------------------------------------------------
try:
    
    #import module finder
    try:
        #from py2exe
        import py2exe.mf as modulefinder
    except ImportError:
        #else default
        import modulefinder
    

    #default imports
    import win32com
    import sys
    
    for path in win32com.__path__[1:]:
        modulefinder.AddPackagePath("win32com", path)
    
    for extra in ["win32com.shell"]: #,"win32com.mapi"
        __import__(extra)
        m = sys.modules[extra]
        for path in m.__path__[1:]:
            modulefinder.AddPackagePath(extra, path)

except ImportError:
    # no build path setup, no worries.
    pass







#Import
#------------------------------------------------------------------
#python
import sys
import os
from distutils.core import setup
from glob import glob
import shutil
#py2exe
import py2exe






#Import protection
#------------------------------------------------------------------

if (__name__ == '__main__'):

    #Only execute script if it is not imported



    #Variables
    #------------------------------------------------------------------

    #application_name
    application_name = 'HelgaLauncher'

    #application_version
    application_version = '0.1'

    #author_name
    author_name = 'Timm Wagener'



    #msvc_library_directory
    msvc_library_directory = r'C:/Program Files (x86)/Microsoft Visual Studio 9.0/VC/redist/amd64/Microsoft.VC90.CRT'

    #include_list
    include_list = ['sip']

    #exclude_list
    exclude_list = ['PyQt4.uic.port_v3']

    #dll_exclude_list
    dll_exclude_list = ['MSVCP90.dll']

    #data_files_list
    data_files_list = [
        ('media', ['media/helga_launcher.ui']),
        ('media/icons', ['media/icons/icon_helga_launcher.png',
                        'media/icons/icon_dcc_button_maya.png',
                        'media/icons/icon_dcc_button_maya_hover.png',
                        'media/icons/icon_dcc_button_maya_drag.png',
                        'media/icons/icon_dcc_button_houdini.png',
                        'media/icons/icon_dcc_button_houdini_hover.png',
                        'media/icons/icon_dcc_button_houdini_drag.png',
                        'media/icons/icon_dcc_button_nuke.png',
                        'media/icons/icon_dcc_button_nuke_hover.png',
                        'media/icons/icon_dcc_button_nuke_drag.png',
                        'media/icons/icon_dcc_button_hiero.png',
                        'media/icons/icon_dcc_button_hiero_hover.png',
                        'media/icons/icon_dcc_button_hiero_drag.png',
                        'media/icons/icon_dcc_button_doc.png',
                        'media/icons/icon_dcc_button_doc_hover.png',
                        'media/icons/icon_dcc_button_doc_drag.png'
                        ]),
        ('data', ['data/pipeline_base_data.yaml', 
                    'data/pipeline_base_data_sandbox.yaml',
                    'data/pipeline_base_data_home.yaml'])
        ]









    #MSVC Libraries
    #------------------------------------------------------------------

    #if msvc_library_directory exists copy .dlls into py2exe bundle
    if (os.path.isdir(msvc_library_directory)):
        
        #msvc_library_tuple
        msvc_library_tuple = ("Microsoft.VC90.CRT", glob(msvc_library_directory + r'/*.*'))
        #append
        data_files_list.append(msvc_library_tuple)









    #setup
    #------------------------------------------------------------------

    #options_dict
    options_dict = dict(
        
        ascii = False,  # Exclude encodings
        includes = include_list,
        excludes = exclude_list,  # Exclude standard library
        dll_excludes = dll_exclude_list,  # Exclude 'MSVCP90.dll'
        compressed = True,  # Compress library.zip
        dist_dir = application_name
    )

    
    
    #build_dict
    build_dict = dict(
        build_base = application_name + '_build'
    )


    
    #setup
    setup(
        
        name = application_name,
        version = application_version,
        description = 'Pipeline tools launcher.',
        author = author_name,
        console = ['helga_launcher_loader.py'],
        data_files = data_files_list,
        options = {
        'build': build_dict,
        'py2exe': options_dict
        }
    )







    #Remove build directory
    #------------------------------------------------------------------

    try:
        
        #setup_module_file
        setup_module_file = os.path.realpath(sys.argv[0])
        #setup_module_dir
        setup_module_dir = os.path.dirname(setup_module_file)
        #batch_dir
        build_dir = os.path.join(setup_module_dir, application_name + '_build')

        #if build_dir exists delete
        if(os.path.isdir(build_dir)):
            shutil.rmtree(build_dir)

        #log
        print('\n\nSuccessfully deleted build directory: {0}'.format(build_dir))

    except:
        
        #log
        print('Error deleting build directory')





    #Create batches
    #------------------------------------------------------------------


    def create_batch(helga_launcher_path, 
                        batch_dir, 
                        batch_name, 
                        command_line_arg_list = []):
        """
        Create helga launcher batch (No UNC/relative pathes allowed)
        """

        try:
            #batch_file_path
            batch_file_path = os.path.join(batch_dir, batch_name)

            #command
            command = helga_launcher_path

            #add command line args
            for argument in command_line_arg_list:
                command += argument

            #batch_file
            with open(batch_file_path, 'w+') as batch_file:

                #write
                batch_file.write(command)

        except:

            #log
            print('Error creating batch file')

    try:

        #batch_dir_name
        batch_dir_name = 'batch'

        #setup_module_file
        setup_module_file = os.path.realpath(sys.argv[0])
        #setup_module_dir
        setup_module_dir = os.path.dirname(setup_module_file)
        #final_dir
        final_dir = os.path.join(setup_module_dir, application_name)
        #batch_dir
        batch_dir = os.path.join(final_dir, batch_dir_name)

        #if batch dir exists, rebuild
        if (os.path.isdir(batch_dir)):
            #delete
            shutil.rmtree(batch_dir)
        
        #recreate
        os.makedirs(batch_dir)

        #helga_launcher_path
        helga_launcher_path = r'Y:/Production/scripts/deploy/helga/bin/HelgaLauncher/helga_launcher_loader.exe'

        #helga_launcher_path_home
        helga_launcher_path_home = r'C:/symlinks/filmaka/helga/Production/scripts/deploy/helga/bin/HelgaLauncher/helga_launcher_loader.exe'

        

        #helga_launcher
        #------------------------------------------------------------------

        #helga_launcher
        batch_name = 'helga_launcher.bat'
        create_batch(helga_launcher_path, batch_dir, batch_name)

        #helga_launcher_maya
        batch_name = 'helga_launcher_maya.bat'
        create_batch(helga_launcher_path, batch_dir, batch_name, [r' -rma 1'])

        #helga_launcher_nuke
        batch_name = 'helga_launcher_nuke.bat'
        create_batch(helga_launcher_path, batch_dir, batch_name, [r' -rnk 1'])

        #helga_launcher_houdini
        batch_name = 'helga_launcher_houdini.bat'
        create_batch(helga_launcher_path, batch_dir, batch_name, [r' -rho 1'])


        



        #helga_launcher_sandbox
        #------------------------------------------------------------------

        #helga_launcher_sandbox
        batch_name = 'helga_launcher_sandbox.bat'
        create_batch(helga_launcher_path, batch_dir, batch_name, [r' -sbx 1'])

        #helga_launcher_sandbox_maya
        batch_name = 'helga_launcher_sandbox_maya.bat'
        create_batch(helga_launcher_path, batch_dir, batch_name, [r' -sbx 1', r' -rma 1'])

        #helga_launcher_sandbox_nuke
        batch_name = 'helga_launcher_sandbox_nuke.bat'
        create_batch(helga_launcher_path, batch_dir, batch_name, [r' -sbx 1', r' -rnk 1'])

        #helga_launcher_sandbox_houdini
        batch_name = 'helga_launcher_sandbox_houdini.bat'
        create_batch(helga_launcher_path, batch_dir, batch_name, [r' -sbx 1', r' -rho 1'])




        #helga_launcher home
        #------------------------------------------------------------------

        #helga_launcher_home
        batch_name = 'helga_launcher_home.bat'
        create_batch(helga_launcher_path_home, batch_dir, batch_name, 
                        [r' --custom_yaml_path "C:/symlinks/filmaka/helga/Production/scripts/deploy/helga/bin/HelgaLauncher/data/pipeline_base_data_home.yaml"'])



        #log
        print('\n\nSuccessfully created batches in: {0}'.format(batch_dir))

    except:
        
        #log
        print('Error creating batches')
    