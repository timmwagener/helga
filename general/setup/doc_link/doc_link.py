
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




#Globals
#----------------------------------------------------

URL = r'http://www.kiiia.com/helga/documentation/build/html/index.html'
"""Default URL constant. Points to pipeline documentation"""



#run
#----------------------------------------------------

def run(url = URL):
	"""
	Open web browser with pipeline documentation
	"""

	webbrowser.open(url, new=2)
	
	
	
	
	
#Testing
#----------------------------------------------------
#----------------------------------------------------

if (__name__ == '__main__'):
	
	#run
	run()

