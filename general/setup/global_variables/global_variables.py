
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

PIPELINE_BASE_PATH = r'//bigfoot/grimmhelga'
"""Helga pipeline base path"""

MAYA_PROJECT_PATH = r'//bigfoot/grimmhelga/Production/3d/maya'
"""Helga pipeline Maya project path"""

PIPELINE_DOCUMENTATION_URL = r'http://www.kiiia.com/helga/documentation/build/html/index.html'
"""Default URL constant. Points to pipeline documentation"""

