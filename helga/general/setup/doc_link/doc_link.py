
"""
doc_link
==========================================

Simple but hopefully helpful module to open up a browser to our
pipeline documentation.

-----------------------

Usage
-----

::
	
	from helga.general.setup.doc_link import doc_link
	reload(doc_link)

	#run
	doc_link.run()

-----------------------
"""



#Import
#----------------------------------------------------
#python
import os
import sys
import webbrowser



#Import variable
do_reload = True

#helga
from helga.general.setup.global_variables import global_variables
if(do_reload):reload(global_variables)





#run
#----------------------------------------------------

def run(url = None):
	"""
	Open web browser with pipeline documentation
	"""

	#if url is None and global variables url is available
	if not (url):
		
		#variable might not be available if base path 
		#env. var. is not available
		try:
			
			#set url to pipeline base
			url = global_variables.PIPELINE_DOCUMENTATION_URL
		
		except:

			#set url to google
			url = 'google.com'

	#open
	webbrowser.open(url, new=2)
	
	
	
	
	
#Testing
#----------------------------------------------------
#----------------------------------------------------

if (__name__ == '__main__'):
	
	#run
	run()

