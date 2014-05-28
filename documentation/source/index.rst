

.. _index:

.. 
	helga_pipeline_documentation documentation master file, created by
	sphinx-quickstart on Sun May 18 20:10:32 2014.
	You can adapt this file completely to your liking, but it should at least
	contain the root `toctree` directive.


.. figure:: media/images/general/pipeline_documentation_header.jpg
	:width: 200px
	:align: center
	:alt: alternate text





Helga pipeline documentation
============================

Welcome to the Helga pipeline documentation. Here you can find almost all answers to questions about how we do things within the Helga pipeline. It is the first place to look for answers if you have a questions. The second option is to ask me (Timm Wagener) or write me an `email <mailto:wagenertimm@gmail.com?Subject=[Helga]%20Pipeline%20issue>`_.

**Important:** 
It's always better to communicate! I want you to come and ask if you are unsure. (Don't be afraid that your question is dumb! Even if it's dumb, it's probably not half as dumb as the questions i managed to ask to people... ;) ). 


Manual
------

.. toctree::
	:maxdepth: 1
	
	manual/quick_guide
	manual/naming_convention
	manual/work_and_publish
	manual/pipeline
	manual/faq
	manual/i_am_a/i_am_a



API Documentation
-----------------

.. toctree::
   :maxdepth: 2

   manual/apidoc/apidoc_overview
   manual/apidoc/apidoc_coding_convention


-----------------------


.. autosummary::
	:toctree: apidoc/

	helga.houdini
	helga.maya
	helga.nuke


-----------------------


.. Debug Mode

.. ifconfig:: debug == True
	
	Debug mode: On


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`

.. * :ref:`search`

