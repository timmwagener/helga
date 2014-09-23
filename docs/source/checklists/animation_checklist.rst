


.. _animation_checklist:

.. 
	Things to look out for animators, so that their Alembics move smoothly through the pipe



Animation checklist
===================

.. note::
	
	Here are some important things for the animators amongst us.
	Since your output is used in simulation, lighting, shading etc. please
	pay attention to these points, to ensure everything is running smoothly 
	through the pipe.

	If you have questions just ask `Johannes <mailto:johannes.franz@filmakademie.de?Subject=[Helga]%20Pipeline%20issue>`_, `Manuel <mailto:manuel.seifert@filmakademie.de?Subject=[Helga]%20Pipeline%20issue>`_ or `Timm <mailto:wagenertimm@gmail.com?Subject=[Helga]%20Pipeline%20issue>`_.

---------------


Simulation Preroll
------------------

In order for the extensive cloth sim, that we want to put on top of the helga characters,
there is some pre-roll time necessary. Trust me, it's not rocket science, here's how we wanna do it.

There are 2 steps that come before the character animation that are needed for the sim dudes.

#. **Frame: 901 - 951**
	Character is in T-Pose. The cloth settles on the T-Pose character.

#. **Frame: 951 - 1001**
	On frame **951** there is a keyframe of the T-Pose. From here the character morphs linearly into the start pose. Here the cloth gets ready for the real action.

#. **Frame: 1001**
	This is the **first** keyframe of the character animation.


We choose frame **1001** as the first keyframe of animation because it's a round **1000** frames offset from the usual frame 1.


	

























