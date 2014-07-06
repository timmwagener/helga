
"""
vrayGlobals
==========================================

Globals module to hosts constants for the :mod:`helga.maya.rendering.createUpdateRenderElements` package.

-----------------------

Usage
-----

::
	
	from helga.maya.rendering.createUpdateRenderElements import vrayGlobals
	reload(vrayGlobals)

	#my_fancy_prefix
	my_fancy_prefix = vrayGlobals.PREFIX

-----------------------
"""






#Globals
#------------------------------------------------------------------
PREFIX = 'gh'
"""
Prefix for the channels in multichannel exrs. 
For example: ghDiffuse, ghReflection
"""
