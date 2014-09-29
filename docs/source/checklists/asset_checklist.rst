


.. _asset_checklist:

.. 
	Asset checklist for characters and props.



Asset checklist
==================

.. note::
	In order for the smooth, customized export of assets from animation to lighting/shading, sim and
	everybody else, the assets need a little treatment before going in production.
	Here's a little list of things to take care of.
	It is advisable (although not needed) to use the **AssetManager** to automate a lot of
	these steps in Maya.

---------------

#. Asset has blank prop or char metadata node ?
	This tells the asset manager which categories you want to export.
	The node options are left blank, because they need to be filled in the scene as a local reference edit.

	.. figure:: /media/images/asset_checklist/asset_prop_metadata_node.jpg
		:width: 100px
		:alt: Prop metadata node

	(Shot metadata nodes are embedded in the shot files, and never belong into an asset).

#. Export Attributes attached (proxy, rendergeo, locator...)?
	This tells the asset manager what the content of the categories is.
	Do all the export objects have the correct attributes assigned.
	The following attributes are typical:

		#. helga_proxy
		#. helga_rendergeo
		#. helga_locator
		#. helga_highpoly_rendergeo <-- Points to the highpoly render version of the asset.

	These attributes are always assigned on the **transform** nodes of the objects in Maya.
	No attributes are put on shape nodes by default. (Although its perfectly fine by artists to do so).

	The asset manager tool provides an interface to add or remove those attributes on selected nodes:

	.. figure:: /media/images/asset_checklist/asset_manager_add_remove_attributes.jpg
		:width: 100px
		:alt: Add or remove attributes with the asset manager.

	**Only objects with export attributes will be considered for the export**

#. helga_highpoly_rendergeo attribute on locator set?
	The helga_highpoly_rendergeo attr. is filled out on the asset **before** referencing.
	It points to the highpoly render replacement geometry, usually an alembic file located
	in cache/alembic/highpoly_rendergeo.

#. Does the asset have a material?
	Make sure the textures are lightweight and published in the textures/props/prop_xy directory.

#. Does the asset have a rig, and are the joints and locator hidden?

#. Did you check the asset with the AssetManager after publishing?
	Always be the first to reference in your newly published asset and check
	if it performs with the AssetManager.
	
	.. figure:: /media/images/asset_checklist/asset_manager_check_prop_after_publish.jpg
		:width: 100px
		:alt: Check a prop after publishing to see if it performs with AssetManager.

































