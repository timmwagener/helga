

"""
reconstruct_globals
==========================================

Globals module to hosts constants for the :mod:`helga.nuke.reconstruction.renderReconstructVRay` package.

-----------------------

Usage
-----

::
	
	from helga.nuke.reconstruction.renderReconstructVRay import reconstruct_globals
	reload(reconstruct_globals)

	#my_fancy_prefix
	my_fancy_prefix = reconstruct_globals.PREFIX

-----------------------
"""



#Globals
#------------------------------------------------------------------

PREFIX = 'gh'
"""
Prefix for the channels in multichannel exrs. 
For example: ghDiffuse, ghReflection
"""