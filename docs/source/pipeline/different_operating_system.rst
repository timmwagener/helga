


.. _different_operating_system:

.. 
	Experimental: How to run/test the helga pipeline via direct_access module on a different platform than win7.





.. figure:: /media/images/pipeline/different_operating_system_header.jpg
	:width: 800px
	:align: center
	:alt: Different operating system header


Running on a different OS
=========================


.. note::

	The helga pipeline is developed/maintained foremost on the **windows** platform. However there might be the need
	sometimes to switch to a different operating system like Linux. For these cases you can find a quick 
	guide here how to start the DCCs in the correct environment, but keep in mind, that support for operating systems 
	other than windows at the moment is **very experimental**.

.. warning::

	This guide and method are considered temporary and might become deprecated once there is time for a refactoring
	of the HelgaLauncher tool that is used under windows.


------------------------


Tested on
---------

* CentOS7
	* Houdini: Yes
	* Nuke: No
	* Maya: Untested


------------------------


Step by step guide
------------------

**Please note that this guide is geared towards TDs or people that are a little familiar with git or Python, since there is.
a little effort involved in making it run outside of how it is ment to be run. 
6 little steps to take on your own risk :D**

#. **Temporary clone the helga git repo**
	Clone the helga repo to a temporary location. Just navigate to some temp folder and execute this snippet in your git enabled shell:
	
	.. code::

		git clone https://github.com/timmwagener/helga.git helga

	This should create a folder named helga at your current path and clone the helga repository in it.

#. **Helga folder structure**
	Now in your temporary helga repo navigate to *helga/general/setup/direct_access/supplementary_material/folder_structure*.
	There you will find a zip file called **helga.zip**, that contains the helga folder structure.
	Extract this zip to where you want the helga pipeline and project to be located.
	**PS:** The helga folder structure is based on the Maya project structure which might be unfamiliar to non Maya users.

#. **The real clone - work repository**
	Now its time to do the real clone of the helga repo and fit it into the new folder structure.
	Navigate to *your_root/Production/scripts/work* and execute

	.. code::

		git clone https://github.com/timmwagener/helga.git helga

	there again. This is the repo you will keep up-to-date and maintain and always copy into sandbox or deploy
	when you want to publish changes to production.

#. **Start procedure for Houdini, Maya & Nuke**
	Now its time to adjust the startup module for your dccs (Supported are Maya 2014, Nuke 8.x and Houdini 13.0.xxx).
	Please go to *Production/scripts/sandbox/helga/helga/general/setup/direct_access/yaml* where you will find a file
	called **pipeline_base_data.yaml**. 
	Open it with a text editor, for example sublime text or notepad and adjust the following values:

	#. **PIPELINE_BASE_PATH:** "path/to/where/Production/and/Organization/folders/are/under"
	#. **PIPELINE_FLAVOUR:** "deploy" <-- Pick either **sandbox** or **deploy**. This is the folder name where the script environment you want to use is under.
	#. **MAYA_EXE:** "path/to/maya.exe"
	#. **NUKE_EXE:** "path/to/Nuke8.0.exe"
	#. **HOUDINI_EXE:** "path/to/houdinifx.exe" (or houdini.exe)

	Save and you are good.

#. **Pipeline repo production copies - sandbox and deploy**
	Those two fellas could also be named experimental and stable, beta or gold......you get the idea.
	Just go and copy the whole helga folder, in which you just did modifications, and __init__.py file from work into sandbox and deploy.

#. **Finally**
	Test if the application runs correctly. Navigate to *deploy|sandbox/helga/helga/general/setup/direct_access* and type the following
	in a python enabled shell:

	.. code::

		#Houdini:
		python -c 'import direct_access;reload(direct_access);direct_access.run("houdini")'
		#Maya:
		python -c 'import direct_access;reload(direct_access);direct_access.run("maya")'
		#Nuke:
		python -c 'import direct_access;reload(direct_access);direct_access.run("nuke")'


	If everything went well, your DCC **should** start within the helga pipeline environment (either sandbox or deploy) 


------------------------

Hopefully that was not too confusing ;) Please remember that you now have the pathes and setup in place, the structure if you will,
but you still need a lot of content like .otls for example. In your own production you would of course populate the pipeline
with your own scripts, plugins, digital assets, gizmos etc.

Good luck :D

