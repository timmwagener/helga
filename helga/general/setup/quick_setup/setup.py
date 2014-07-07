

"""
setup
==========================================

Helper module for py2exe to build a distribution.

-----------------------

-----------------------
"""





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
    application_name = 'QuickSetup'

    #application_version
    application_version = '0.2'

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
        ('media', ['media/quick_setup.ui']),
        ('media/icons', ['media/icons/icon_quick_setup.png'])
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
        description = 'Put in / or remove DCC pipeline tools from deployment.',
        author = author_name,
        windows = ['quick_setup_loader.py'],
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
        #build_dir
        build_dir = os.path.join(setup_module_dir, application_name + '_build')

        #if build_dir exists delete
        if(os.path.isdir(build_dir)):
            shutil.rmtree(build_dir)

        #log
        print('\n\nSuccessfully deleted build directory: {0}'.format(build_dir))

    except:
        
        #log
        print('Error deleting build directory')
    