


.. _fur_hda_setup:

.. 
	Guide to how we want to try to organize the fur workflow and HDAs.







Fur workflow
=============




Caching
-----------------

#. Load Alembic from animation or simulation (both are identical) and use the character_fur HDA to create, simulate and tweak the fur.

#. Cache the complete fur to a seperate file. This is the distilled and only output for fur. (All of the creative part of the fur process happens in a separate fur hip file, analog to the cloth or other effects files).




Rendering
-----------------


#. Load the character_fur_render HDA and point it to the cache. (Or to the cache directory if several caches are needed for several hair systems). If not all needed caches exist, the fur rendering will fail. In render files will be NO tweaking on the fur or artistry on simulation/animation, only shaders will be tweakied there.

#. Load character_fur_shading HDA and plug it in material slot of character_fur_render HDA.






----------------------------------






Required Digital Assets
----------------------------------


1. **character_fur HDA**

Provides all the functionality to create/simulate/tweak and cache the fur. This is the motor.


.. note::

	**Needed functionality:**
		
		#. Read standardized Alembic from Animation/Simulation and create fur on it.
		#. Ability to art direct the fur based on directors oppinion
		#. Simulate fur in order to account for intersection with cloth
		#. Cache the fur.

All of this happens in a seperate fur file for each shot done by the fur artist.


2. **character_fur_shading HDA**

Analog to usual shading assets. An HDA that just contains one or more materials to be plugged in the material slot(s) of the character_fur_render HDA.


3. **character_fur_render HDA**

HDA that wraps the character_fur HDA, hides all the complexity of the fur itself and exposes all the attributes needed for rendering.

.. note::

	**Needed functionality:**
		
		#. Material slots which allow to pick the materials from the character_fur_shading HDA or any other hair materials
		#. Pick the cache done by the fur artist
		#. Enable visibility for rendering and viewport

The character_fur_render HDA wraps the character_fur HDA for DRY reasons and to provide a stripped interface that hides the complexity for shading artists.
If there is no cache, the fur cannot be rendered.







