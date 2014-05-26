

"""
reconstruct_light
==========================================

Internal module that reconstructs nuke light from metadata in exrs according to our pipeline standards.

.. important::
	
	This module is internal. Access its functionality from :mod:`helga.nuke.reconstruction.sceneReconstructVRay.sceneReconstruct`

-----------------------
"""






#Imports
#------------------------------------------------------------------
#python
import sys
import os
import cPickle as pickle
import logging
import math
#nuke
import nuke
import nukescripts


#do_reload
do_reload = True

#own
import reconstruct_globals as reconstruct_globals
if(do_reload): reload(reconstruct_globals)





#Methods
#------------------------------------------------------------------

def reconstruct_light(node = None, verbose = True):
	"""Reconstruct light from exr metada in read node"""

	try:
		#node = None
		if not(node):
			if(verbose):
				print('Node = None. Returning...')
			return

		#node != type Read
		if not(nodetypeMatches(node, 'Read')):
			if(verbose):
				print('Node {0} is not of type Read. Returning...'.format(node.name()))
			return


		#metadata_dict
		metadata_dict = node.metadata()


		#light_dict_key
		light_dict_key = reconstruct_globals.NUKE_EXR_METADATA_PREFIX + reconstruct_globals.LIGHT_DICTIONARY_KEY
		
		#metadata_dict has no key light
		if not(light_dict_key in metadata_dict):
			if(verbose):
				print('Key {0} not in metadata of node {1}. Returning...'.format(light_dict_key, node.name()))
			return


		#light_details_list [{details}, {details}, {details}]
		light_details_list = pickle.loads(metadata_dict[light_dict_key])

		for light_detail_dict in light_details_list:
			print(light_detail_dict)
			print('----------------------------------------------------------------')

		#light_details_list empty
		if not(light_details_list):
			if(verbose):
				print('Light details list for node {0} empty. Returning...'.format(node.name()))
			return


		#lights_list
		lights_list = []

		#recreate_lights
		for light_detail_dict in light_details_list:
			light_node = reconstruct_light_by_type(light_detail_dict)
			#append
			if(light_node):
				lights_list.append(light_node)



		#lights_list empty
		if not(lights_list):
			if(verbose):
				print('Lights list for node {0} empty. No lights reconstructed. Returning...'.format(node.name()))
			return

		#backdrop
		backdrop = create_backdrop(lights_list, rgb_to_hex_string(reconstruct_globals.LIGHT_NODE_BACKDROP_COLOR))
		backdrop.knob('label').setValue(node.name() +'_lights')
		backdrop.knob('note_font_size').setValue(20)


		#lights_scene_node
		lights_scene_node = nuke.nodes.Scene(inputs = lights_list)
		
		

	except:
		#status
		if(node.name()):
			print('Error reconstructing light for node {0}'.format(node.name()))
		else:
			print('Error reconstructing light detail')


def reconstruct_light_by_type(light_detail_dict):
	"""Reconstruct light by type"""

	#light_type_key
	light_type_key = 'light_type'

	#VRayLightDomeShape
	if(light_detail_dict[light_type_key] == 'VRayLightDomeShape'):
		light_node = reconstruct_VRayLightDomeShape(light_detail_dict)
		return light_node
	#VRaySunShape
	elif(light_detail_dict[light_type_key] == 'VRaySunShape'):
		light_node = reconstruct_VRaySunShape(light_detail_dict)
		return light_node
	else:
		print('Light type: {0} is not known. Light not recreated'.format(light_detail_dict[light_type_key]))
		return None


#reconstruct_VRayLightDomeShape
def reconstruct_VRayLightDomeShape(light_detail_dict):
	"""reconstruct_VRayLightDomeShape"""

	#env_light_node
	env_light_node = nuke.nodes.Environment()
	#label
	env_light_node['label'].setValue(light_detail_dict['light_transform_name'])
	#color
	env_light_node['color'].setValue(light_detail_dict['lightColor'])
	#intensity
	env_light_node['intensity'].setValue(light_detail_dict['intensityMult'])

	return env_light_node


#reconstruct_VRaySunShape
def reconstruct_VRaySunShape(light_detail_dict):
	"""reconstruct_VRaySunShape"""

	#direct_light_node
	direct_light_node = nuke.nodes.DirectLight()
	#label
	direct_light_node['label'].setValue(light_detail_dict['light_transform_name'])
	#color
	direct_light_node['color'].setValue(1,1,1)
	#intensity
	direct_light_node['intensity'].setValue(light_detail_dict['intensityMult'])
	#cast_shadows
	direct_light_node['cast_shadows'].setValue(light_detail_dict['shadows'])


	
	#list_matrix
	list_matrix = light_detail_dict['matrix']

	#nuke_matrix
	nuke_matrix = nuke.math.Matrix4()
	nuke_matrix.makeIdentity()

	#iterate and fill
	for k,v in enumerate(list_matrix):
		nuke_matrix[k] = v
	

	#translate
	translate = nuke_matrix.transform(nuke.math.Vector3(0, 0, 0))  # Get a vector that represents the camera translation   
	#rotate
	rotate = nuke_matrix.rotationsZXY() # give us xyz rotations from cam matrix (must be converted to degrees)

	#translate
	direct_light_node['translate'].setValue((float(translate.x), float(translate.y), float(translate.z)))
	#rotate
	direct_light_node['rotate'].setValue((float(math.degrees(rotate[0])), float(math.degrees(rotate[1])), float(math.degrees(rotate[2]))))


	return direct_light_node




def nodetypeMatches(node, nodetype):
	"""Check if the nodetype matches"""
	
	if(node.Class() == nodetype):
		return True
	return False


def create_backdrop(nodesList, hexColor):
	"""Create backdrop for nodesList with hexColor"""

	#deselect all
	deselect_all()

	#Select nodesList in viewport
	for node in nodesList:
		node.setSelected(True)
	
	
	#nukescripts autobackdrop
	backdrop = nukescripts.autoBackdrop()
	backdrop['tile_color'].setValue(hexColor)

	return backdrop


def deselect_all():
	"""Deselect All"""

	#Select All to invert the selection XD
	nuke.selectAll()
	nuke.invertSelection() 


def rgb_to_hex_string(colorList = [0,0,0]):
	"""Convert RGB List to hex color"""

	#getColors
	r = colorList[0]
	g = colorList[1]
	b = colorList[2]
	
	#get hexColor
	hexColor = int('%02x%02x%02x%02x' % (r*255,g*255,b*255,1),16)
	
	return hexColor






#Temp
#------------------------------------------------------------------

"""
#alembic_path
alembic_path = r'P:\23_NEUE_CLIPS\01_Erdmaennchen\150_rnd\rnd_timm\alembic_reconstruct_test\cache\cam_vertex_and_trans_matrix_animation.abc'
#alembic_read_node
#alembic_read_node = nuke.nodes.ReadGeo2()
#set path
#alembic_read_node['file'].fromUserText(alembic_path)

#alembic_read_node
alembic_read_node_temp = nuke.createNode('ReadGeo2', 'file {' +alembic_path +'}') 
sceneView = alembic_read_node_temp['scene_view']
all_items = sceneView.getAllItems()            # get a list of all nodes stored in the abc file
print(all_items)
nuke.delete(alembic_read_node_temp)

#alembic_read_node_list
alembic_read_node_list = []

#iterate and create node
for item in all_items:
    alembic_read_node = nuke.createNode('ReadGeo2', 'file {' +alembic_path +'}')
    alembic_read_node.knob('label').setValue(item)
    sceneView = alembic_read_node['scene_view']
    sceneView.setImportedItems([item])    # import all items into the ReadGeo node
    sceneView.setSelectedItems([item])      # set everything to selected (i.e. visible)
    alembic_read_node_list.append(alembic_read_node)

#align nodes
alignNodes(alembic_read_node_list, direction = 'y')
#hide control panel
for alembic_read_node in alembic_read_node_list:
    alembic_read_node.hideControlPanel()
"""