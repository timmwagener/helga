


"""
reconstruct_alembic
==========================================

Internal module that reconstructs nuke 3d scenes from metadata in exrs according to our pipeline standards

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

def reconstruct_alembic(node = None, verbose = True):
	"""Reconstruct alembic from exr metada in read node"""

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


		#alembic_dict_key
		alembic_dict_key = reconstruct_globals.NUKE_EXR_METADATA_PREFIX + reconstruct_globals.ALEMBIC_DICTIONARY_KEY
		
		#metadata_dict has no key alembic
		if not(alembic_dict_key in metadata_dict):
			if(verbose):
				print('Key {0} not in metadata of node {1}. Returning...'.format(alembic_dict_key, node.name()))
			return


		#alembic_details_list [{details}, {details}, {details}]
		alembic_details_list = pickle.loads(metadata_dict[alembic_dict_key])

		for item in alembic_details_list:
			print(item)
			print('----------------------------------------------------------------')

		#alembic_details_list empty
		if not(alembic_details_list):
			if(verbose):
				print('Alembic details list for node {0} empty. Returning...'.format(node.name()))
			return


		
		#read_node_list
		read_node_list = create_alembic_read_nodes(alembic_details_list = alembic_details_list, verbose = verbose)

		#read_node_list empty
		if not(read_node_list):
			if(verbose):
				print('Read node list for node {0} empty. No alembics reconstructed. Returning...'.format(node.name()))
			return


		#backdrop
		for alembic_parts_list in read_node_list:
			backdrop = create_backdrop(alembic_parts_list, rgb_to_hex_string(reconstruct_globals.ALEMBIC_READ_NODE_BACKDROP_COLOR))
			backdrop.knob('label').setValue(node.name() +'_alembic')
			backdrop.knob('note_font_size').setValue(20)


		#complete_read_nodes_list
		complete_read_nodes_list = []
		for alembic_parts_list in read_node_list:
			complete_read_nodes_list += alembic_parts_list
		#scene_node
		scene_node = nuke.nodes.Scene(inputs = complete_read_nodes_list)
		

	except:
		#status
		if(node.name()):
			print('Error reconstructing Alembic files for node {0}'.format(node.name()))
		else:
			print('Error reconstructing Alembic files')


def create_alembic_read_nodes(alembic_details_list = [], verbose = True):
	"""Create Geo read nodes for alembic pathes in node and return list of them"""

	#alembic_pathes_list
	alembic_pathes_list = [alembic_dict.get('alembic_path', '') for 
							alembic_dict in 
							alembic_details_list if
							alembic_dict.get('alembic_path', '')]

	#alembic_textures_list
	alembic_textures_list = [alembic_dict.get('alembic_textures', '') for 
							alembic_dict in 
							alembic_details_list if
							alembic_dict.get('alembic_path', '')]

	

	#alembic_pathes_list empty
	if not(alembic_pathes_list):
		if(verbose):
			print('Alembic pathes list empty. Returning empty list...')
		return []

	

	#alembic_parts_list / [[readGeo, readGeo], [readGeo, readGeo,readGeo]]
	alembic_parts_list = []

	#iterate and create
	for index, alembic_path in enumerate(alembic_pathes_list):
		#append
		alembic_parts_list.append(create_alembic_parts(alembic_path, 
														alembic_textures_list[index],
														recreate_textures = True))


	return alembic_parts_list


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


def create_alembic_parts(alembic_path, texture_path, recreate_textures = False):
	"""Create alembic node with given path"""

	#alembic_read_node
	alembic_read_node_temp = nuke.createNode('ReadGeo2', 'file {' +alembic_path +'}') 
	#scene_view
	scene_view = alembic_read_node_temp['scene_view']
	#all_items
	all_items = scene_view.getAllItems() # get a list of all nodes stored in the abc file
	#delete temp node
	nuke.delete(alembic_read_node_temp)

	#alembic_read_node_list
	alembic_read_node_list = []

	#iterate and create node
	for item in all_items:
		#alembic_read_node
		alembic_read_node = nuke.createNode('ReadGeo2', 'file {' +alembic_path +'}')
		alembic_read_node.knob('label').setValue(item)
		#scene_view
		scene_view = alembic_read_node['scene_view']
		scene_view.setImportedItems([item]) #import all items into the ReadGeo node
		scene_view.setSelectedItems([item]) #set everything to selected (i.e. visible)

		#append to list
		alembic_read_node_list.append(alembic_read_node)

	#align nodes
	reconstruct_globals.align_nodes(alembic_read_node_list, direction = 'y')

	#hide control panel
	for alembic_read_node in alembic_read_node_list:
		alembic_read_node.hideControlPanel()



	#if recreate_textures
	if(recreate_textures):
		
		#if texture path
		if(texture_path):

			#material_node
			material_node = nuke.nodes.BasicMaterial()

			#set position
			offset = -30
			pos_x = alembic_read_node_list[0]['xpos'].value()
			pos_y = alembic_read_node_list[0]['ypos'].value() + offset
			material_node['xpos'].setValue(pos_x)
			material_node['ypos'].setValue(pos_y)
			material_node['specular'].setValue(0.1)
			

			#texture_node
			texture_node = nuke.nodes.Read()
			texture_node['file'].fromUserText(texture_path)

			#set position
			offset = -150
			pos_x = alembic_read_node_list[0]['xpos'].value()
			pos_y = alembic_read_node_list[0]['ypos'].value() + offset
			texture_node['xpos'].setValue(pos_x)
			texture_node['ypos'].setValue(pos_y)

			#connect to material
			material_node.setInput(1, texture_node)




			#connect alembic parts
			for alembic_read_node in alembic_read_node_list:
				alembic_read_node.setInput(0, material_node)

			#append texture node
			alembic_read_node_list.append(texture_node)





	return alembic_read_node_list



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