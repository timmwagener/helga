


.. _naming_convention:

.. 
	Naming convention rules and descriptions.



Naming Convention
==================

Here you can find a quick reference for the naming convention we use.

.. note::
	
	This naming convention holds true for most of our pipeline. 
	Please try to match it as close as possible. Small errors count!
	Think of it as right **not** if a human can understand your versioning
	but if an algorythm could successfully parse your
	files and do something meaningfull without errors.

---------------

For work files it usually goes like :

::
	
	ulfbert_model_a_0001_mh.mb
	ulfbert_sculpt_d_0012_mh.ztl
	helga_rig_base_c_0023_tw.mb
	snorri_concept_f_0012_ms.psd

Quick explanation
-----------------

* **ulfbert_model:**
	Name that explains what file we are dealing with. Could also be *snorri_base_model* or *king_larry_the_third_model_from_hell*, just make sure people know the item that is versioned here.
* **a:**
	Wide iteration letter that is for **large** changes and is a landmark for you.
	You usually know (at least when you open a file) why you upversioned the
	letter
* **0001:**
	Version number. Always has four digits.
* **mh:**
	Modifier initials of the person that saved this file.

Chain them all together and you have a beautifully explanatory naming convention that helps everybody understand what he is dealing with.

---------------

Published files
---------------

Published files are a little bit different in that they just omit the versioning suffixes.
This makes sense when you think about them as the current state of your work you made available to everybody.

Here is an example for the ulfbert rig :

Work folder
###########

Here is the file how the rigger names and versiones it up
	
::
	
	ulfbert_rig_body_c_0023_ah.mb
	ulfbert_rig_body_c_0024_ah.mb
	ulfbert_rig_body_d_0025_ah.mb
	ulfbert_rig_body_e_0026_ah.mb

Publish folder
##############

Here is the published file. This file is used by all animators
as a reference to do the animation so by overriding it, the rigger
automatically updates the whole production.
	
::
	
	ulfbert.mb

Read more about our work and publish system :ref:`here <work_and_publish>`
























