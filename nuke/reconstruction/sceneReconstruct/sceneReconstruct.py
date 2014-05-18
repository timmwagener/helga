





#sceneReconstruct Module
#------------------------------------------------------------------


'''
Reconstructs scene elements from nuke metadata according to our pipeline standards
'''

'''
ToDo:

'''


#Imports
#------------------------------------------------------------------
import sys
import os
import nuke



do_reload = True

#reconstruct_alembic
import reconstruct_alembic
if(do_reload): reload(reconstruct_alembic)
#reconstruct_camera_from_vray_exr
import reconstruct_camera_from_vray_exr
if(do_reload): reload(reconstruct_camera_from_vray_exr)
#reconstruct_light
import reconstruct_light
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
		"""Reconstruct Alembic nodes from read nodes with exr input file"""

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
		"""Reconstruct a cam from a vray exr. ONLY works with vray exrs"""

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
		"""Reconstruct Light nodes from read nodes with exr input file"""

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

		
		

		