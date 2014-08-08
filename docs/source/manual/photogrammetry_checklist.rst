


.. _photogrammetry_checklist:

.. 
	Things to look out for when solving with photoscan



Photogrammetry checklist
========================

.. note::
	
	Here i note the settings which seem to provide a good quality/time ratio. (For final solves).
	They are based on the first days of testing and finding out what works/doesnt work.

	If you have questions ask `Johannes <mailto:johannes.franz@filmakademie.de?Subject=[Helga]%20Photogrammetry%20issue>`_ or `Timm <mailto:wagenertimm@gmail.com?Subject=[Helga]%20Photogrammetry%20issue>`_.

---------------



Solve settings (final)
----------------------

Set the settings in the **batch process dialog** to the following.
Before the aligning of chunks (**second step**) it makes sense to check
the solved chunks and disable those that dont work before aligning and merging chunks.

.. note::

	#. Import as multiple chunks
	#. **Align Photos**: High
	#. **Align Chunks**:
		- chunks count < 10: *High*
		- chunks count > 10: *Medium*
	#. **Build dense cloud**: 
		- chunks count < 10: *High*
		- chunks count > 10: *Medium*
	#. **Mesh**: 
		- Face count: Custom (30000000 polies).
	#. **Texture**:
		- Size: 8192²
		- Format: .png



---------------


Folders to chunks
-----------------

How folders in the **prop_x/photoscan/photos** dir. map to chunks in photoscan.

.. figure:: /media/images/photogrammetry/photogrammetry_asset_folders.png
	:width: 800px
	:align: center
	:alt: Photogrammetry assets folders and import



---------------


Machine list
------------

The following machines have a Photoscan license and we
are allowed to use them:

- **Pegasus** (Manuel)
- **Gnocchi** (Timm)
- **Macheroni** (Timm)
- **Adonis** (Johannes)
- **Fusilli** (Silke)
- **Gemelli** (Nicole)

