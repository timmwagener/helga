


.. _mesh_checklist:

.. 
	Mesh checklist for characters and props before rigging.



Mesh checklist
==================

.. note::
	Don't let Marco H. trick you.... here's what to look out for ;)

---------------

#. Normals facing correct ?
	Probably by default do Normals>Conform and Normals>Set to Face on all geo in Maya.

#. Is the geo frozen (Translate, Rotate, Scale) and the pivots of all objects are at (0,0,0) in worldspace?
	This ensures all Alembics will be at the right position under the world later on and its also
	cleaner when rigging. In Maya you can run this:

	.. code::
		
		import pymel.core as pm

		selected_nodes = pm.ls(sl = True, fl = True)

		for selected_node in selected_nodes:
		    
		    #freeze
		    pm.makeIdentity(selected_node, a = True)
		    #reset pivot
		    pm.xform(selected_node, piv = (0,0,0))


#. Doublesided and Opposite turned off?
	This ensures that all faces point to the desired direction for all renderers without custom correction.
	In Maya you can do this in the Attribute Spreadsheet under the **Render** tab. *(The first two tabs)*
	
	.. figure:: /media/images/mesh_checklist/double_sided_opposite.jpg
		:width: 100px
		:alt: Double Sided and Opposite attributes on the shape


#. No empty UV Sets floating around and all primary UV Sets are enabled?
	In case there are empty UV sets it makes sense to delete them. Also for some reason Maya likes to have
	its primary UV set named **map1**. While this is not always necessary, its good to follow this convention
	if possible.
	
	.. figure:: /media/images/mesh_checklist/primary_uv_set_map1.jpg
		:width: 100px
		:alt: Primary UV set called map1

#. No overlapping UVs on all the primary UV sets?
	Maybe sometimes there might be reasons to do otherwise but in general its a good idea to have UV sets not overlapping,
	so that follicles or other rigging nodes that are placed on the surface based on UVs work correct.

#. UVs have the correct winding order? (Are the UV shells blue instead of red?)
	This happens through flipping and freezing of geometry for example. Can be fixed with Edit UVs>Flip
	
	.. figure:: /media/images/mesh_checklist/uv_winding_order.jpg
		:width: 100px
		:alt: UV winding order

#. Do objects have the right scale?
	Default units in Maya are cm.

#. Only geo nodes in scene?
	No history, random materials (for example from .obj import) or other nodes should pollute the scene.
	All geo should have the default Lambert material assigned.

#. Geometry usefully grouped?
	\grp_geo
		\grp_body
			\grp_left_leg...

#. All geometry that is actively simulated (cloth etc.) needs to be all quads and tris!
	Collision geometry is fine with NGons. When in doubt ask Johannes.




























