

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
from distutils.core import setup
import py2exe











#setup
#------------------------------------------------------------------

#options_dict
options_dict = dict(
    
    ascii = False,  # Exclude encodings
    includes = ['sip'],
    excludes = ['PyQt4.uic.port_v3'],  # Exclude standard library
    dll_excludes = ['MSVCP90.dll'],  # Exclude msvcr71
    compressed = True,  # Compress library.zip
)


#data_files_list
data_files_list = [
    ('media', ['media/quick_setup.ui']),
    ('media/icons', ['media/icons/icon_quick_setup.png'])
    ]


#setup
setup(
    
    name = 'QuickSetup',
    version = '0.1',
    description = 'Put in / or remove DCC pipeline tools from deployment.',
    author = 'Timm Wagener',
    windows = ['quick_setup_loader.py'],
    data_files = data_files_list,
    zipfile = None,
    options = {'py2exe': options_dict}
)