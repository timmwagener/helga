


.. _apidoc_overview:

.. 
	API and APIDOC overview



API Overview
============

------------------------

Foreword
--------

First let me say that **API** is probably a little misleading since the :mod:`helga` package is mostly a collection of custom tools written in Python, which are independent of each other (like :mod:`helga.nuke.reconstruction.renderReconstructVRay`). But there might be modules in the future that are ment to
be exclusively building blocks for programmers.

------------------------

Organization
------------

Our pipeline is split up into several kinds of packages that import from a logical hierarchy.
We can add packages at any depth in the hierarchy at any time.

DCC packages
############

	* :mod:`helga.houdini`
	* :mod:`helga.maya`
	* :mod:`helga.nuke`

Category packages
#################

	* :mod:`helga.maya.rendering`
	* :mod:`helga.maya.arash`
	* :mod:`helga.maya.hanna`
	* :mod:`helga.nuke.reconstruction`
	* ...

	Please note the packages named after contributors. Packages without a name are assumed
	to be completely written by `me (Timm Wagener) <mailto:wagenertimm@gmail.com?Subject=[Helga]%20Pipeline%20issue>`_. If you want to contribute just ask and you will get your own
	category package.

	.. warning::

		Please never contribute outside of your own category package!

Tool packages
#############

	* :mod:`helga.maya.rendering.createUpdateRenderElements`
	* :mod:`helga.maya.arash.clean_save`
	* :mod:`helga.nuke.reconstruction.renderReconstructVRay`
	* ...


------------------------

Work and Deploy
---------------

There are two Helga packages located under:

	* **production/scripts/work:**

		Here is where we work and edit our scripts. **You are expected to always work here and copy your stuff over to deploy when ready.** If you work and edit in deploy to save the copy
		step, you will sooner or later loose work, since i will often delete and recopy the
		whole helga package.

	* **production/scripts/deploy:**

		Here is where the DCCs use our scripts and their compilers do the byte compilation
		(create .pyc files)


This is basically source control for the poor man, but since the helga package was initially ment to be exclusively my own sandbox we have to deal with that inconvenience.





