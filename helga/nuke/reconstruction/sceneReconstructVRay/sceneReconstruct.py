





"""
sceneReconstruct
==========================================

Automatic reconstruction of 3d scenes in Nuke from exr metadata.
It works together with :mod:`helga.maya.rendering.setExrMetadata`
and can recreate:

	* Camera animation
	* Alembics with textures
	* Light setups

.. note::
	
	The light reconstruction will try to find the best match for lights it doesnt know.
	For example a Vray Sunlight might translate to a directional light in Nuke.
	The mapping is far from complete and far from perfect though.

Please remember that this module only works, when exr metadata is set.

-----------------------

.. Rubric:: Usage

::
	
	from helga.nuke.reconstruction.sceneReconstructVRay import sceneReconstruct
	reload(sceneReconstruct)

	#Create instance
	sceneReconstructInstance = sceneReconstruct.SceneReconstruct()
	
	#------------------------------
	#Select some Nuke Read nodes
	#------------------------------

	#Reconstruct alembics
	sceneReconstructInstance.reconstruct_alembic()

	#Reconstruct exr cam
	sceneReconstructInstance.create_exr_cam_vray()

	#Reconstruct light
	sceneReconstructInstance.reconstruct_light()

	

-----------------------
"""


#Imports
#------------------------------------------------------------------
import sys
import os
import nuke



do_reload = True

#reconstruct_alembic
import lib.reconstruct_alembic as reconstruct_alembic
if(do_reload): reload(reconstruct_alembic)
#reconstruct_camera_from_vray_exr
import lib.reconstruct_camera_from_vray_exr as reconstruct_camera_from_vray_exr
if(do_reload): reload(reconstruct_camera_from_vray_exr)
#reconstruct_light
import lib.reconstruct_light as reconstruct_light
if(do_reload): reload(reconstruct_light)







#SceneReconstruct class
#------------------------------------------------------------------

class SceneReconstruct():
	
	
	#Constructor
	def __init__(self):
		
		#Instance Vars
		#------------------------------------------------------------------
		self.verbose = True
		
	
	
	
	
	#Methods
	#------------------------------------------------------------------
	
	
	
	
	#reconstruct_alembic
	def reconstruct_alembic(self):
		"""
		Reconstruct Alembic nodes from read nodes with exr input file
		"""

		try:
		
			#get selected nodes
			nodes_list = nuke.selectedNodes()
			
			#check if node selected
			if not(len(nodes_list)):
				print('No nodes selected')
				return False
			
			#iterate selected nodes and rebuild all passes
			for node in nodes_list:
				#reconstruct
				reconstruct_alembic.reconstruct_alembic(node)
		
		except:
			#status
			print('Error reconstructing Alembic files')


	#create_exr_cam_vray
	def create_exr_cam_vray(self):
		"""
		Reconstruct a cam from a vray exr. ONLY works with vray exrs
		"""

		try:
		
			#get selected nodes
			nodes_list = nuke.selectedNodes()
			
			#check if node selected
			if not(len(nodes_list)):
				print('No nodes selected')
				return False
			
			#iterate selected nodes and rebuild all passes
			for node in nodes_list:
				#reconstruct
				reconstruct_camera_from_vray_exr.create_exr_cam_vray(node)
		
		except:
			#status
			print('Error reconstructing camera from vray exr files. This method only works with vray exrs')


	#reconstruct_light
	def reconstruct_light(self):
		"""
		Reconstruct Light nodes from read nodes with exr input file
		"""

		try:
		
			#get selected nodes
			nodes_list = nuke.selectedNodes()
			
			#check if node selected
			if not(len(nodes_list)):
				print('No nodes selected')
				return False
			
			#iterate selected nodes and rebuild all passes
			for node in nodes_list:
				#reconstruct
				reconstruct_light.reconstruct_light(node)
		
		except:
			#status
			print('Error reconstructing light details')
	
	
	
	
	
		
	
	
	
	
	#Shared Methods
	#------------------------------------------------------------------
	
	#nodetypeMatches
	def nodetypeMatches(self, node, nodetype):
		
		if(node.Class() == nodetype):
			return True
		return False
		

		


#TMP Execute in script editor
#------------------------------------------------------------------
'''
from kugeltiere.nuke.sceneReconstruct import sceneReconstruct
reload(sceneReconstruct)
sceneReconstructInstance = sceneReconstruct.SceneReconstruct()

#reconstruct alembics
sceneReconstructInstance.reconstruct_alembic()
sceneReconstructInstance.create_exr_cam_vray()
sceneReconstructInstance.reconstruct_light()
'''

		
		

		