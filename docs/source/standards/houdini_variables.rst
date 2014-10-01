


.. _houdini_variables:

.. 
	Here is a quick overview of all the specific variables that can be used in Houdini.







Houdini Variables
=====================


.. note::

	Here is a quick overview of all the specific variables that can be used in Houdini.
	They **should** always be used instead of a hard wired path. They will expand before an .ifd is generated
	so they should be working with the farm properly.

	All helga variables are prefixed with HELGA, if they arent, they are not specific to
	the helga project.

.. info::

	This list is subject to constant updates.


----------------------------------

How To?
-------

Here's how its used in Houdini. Its simple and comfortable.

.. figure:: /media/images/standards/houdini_variables/houdini_variables_expand_example.jpg
		:width: 400px
		:alt: Houdini env. Variables expand example.




----------------------------------

Applications
------------


+-------------------------+----------------------------+----------------------------------------------------+
| $HELGA_HOUDINI_EXE      | Path to pipeline Houdini   | C:/symlinks/houdini/13.0.260/hfs/bin/houdinifx.exe |
+-------------------------+----------------------------+----------------------------------------------------+
| $HELGA_MAYA_EXE         | Path to pipeline Maya      | C:/symlinks/maya/maya2014x64/bin/maya.exe          |
+-------------------------+----------------------------+----------------------------------------------------+
| $HELGA_NUKE_EXE         | Path to pipeline Nuke      | D:/tools/Nuke8.0v1/Nuke8.0.exe                     |
+-------------------------+----------------------------+----------------------------------------------------+


----------------------------------

Pipeline
--------


+--------------------------------+------------------------------------+----------------------------------------------------+
| $HELGA_PIPELINE_BASE_PATH      | Root path of server                | //bigfoot/grimmhelga                               |
+--------------------------------+------------------------------------+----------------------------------------------------+
| $HELGA_PIPELINE_FLAVOUR        | Currently active pipeline flavour. | deploy, sandbox etc.                               |
|                                | Could be deploy or sandbox etc.    |                                                    |
+--------------------------------+------------------------------------+----------------------------------------------------+


----------------------------------

Houdini
-------


+--------------------------------+------------------------------------+------------------------------------------------------------------------------+
| $HELGA_SCRIPTS_BASE_PATH       | Python package base path.          | //bigfoot/grimmhelga/Production/scripts/deploy/helga                         |
|                                | From here you can import helga.    |                                                                              |
+--------------------------------+------------------------------------+------------------------------------------------------------------------------+
| $HELGA_HDRI_PATH               | Path for all HDRIs                 | $HELGA_PIPELINE_BASE_PATH + /Production/2d/hdri                              |
+--------------------------------+------------------------------------+------------------------------------------------------------------------------+
| $HELGA_OTL_PATH                | Default path for helga otls        | $HELGA_PIPELINE_BASE_PATH + /Production/3d/maya/scenes/assets/otls           |
+--------------------------------+------------------------------------+------------------------------------------------------------------------------+
| $HELGA_FUR_PATH                | Path for fur caches                | $HELGA_PIPELINE_BASE_PATH + /Production/3d/maya/cache/fur                    |
+--------------------------------+------------------------------------+------------------------------------------------------------------------------+
| $HELGA_ALEMBIC_PATH            | Path for **all** abc caches        | $HELGA_PIPELINE_BASE_PATH + /Production/3d/maya/cache/alembic                |
|                                | used in lighting, fur and sim.     |                                                                              |
+--------------------------------+------------------------------------+------------------------------------------------------------------------------+
| $HELGA_TEXTURES_PATH           | Path for **all** textures          | $HELGA_PIPELINE_BASE_PATH + /Production/3d/maya/scenes/assets/textures       |
|                                | used in the helga project.         |                                                                              |
+--------------------------------+------------------------------------+------------------------------------------------------------------------------+
| $HELGA_RENDER_PATH             | Root Path where all images are     | $HELGA_PIPELINE_BASE_PATH + /Production/3d/maya/images                       |
|                                | rendered to from 3d.               |                                                                              |
+--------------------------------+------------------------------------+------------------------------------------------------------------------------+








