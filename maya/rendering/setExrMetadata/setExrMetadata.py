
"""
setExrMetadata
==========================================

Module that will parse the scene and add exr metadata to the rendersettings node.
The module is designed to work with VRay for Maya exclusively.
You can import and run it as a Pre-Frame script while batch rendering (on the farm).

-----------------------

Usage
-----

::
	
	from helga.maya.rendering.setExrMetadata import setExrMetadata
	reload(setExrMetadata)

	#run
	setExrMetadata.run()

.. warning::
	
	Module is known to cause crashes when rendering.
	Use with caution

-----------------------
"""




#Imports
#------------------------------------------------------------------
#python
import sys
import os
from functools import wraps
import cPickle as pickle
import platform
import datetime
import multiprocessing
#maya
import maya.OpenMaya as open_maya
import maya.api.OpenMaya as open_maya_2
import maya.cmds as cmds
import pymel.core as pm




#Globals
#------------------------------------------------------------------
VRAY_LIGHT_PARAMETERS_LIST = ['intensityMult', 'subdivs', 'lightColor', 'shadows', 'invisible', 'rayDistanceOn', 
								'domeSpherical', 'affectDiffuse', 'affectSpecular', 'affectReflections']
MAYA_LIGHT_PARAMETERS_LIST = ['color', 'intensity', 'emitDiffuse', 'emitDiffuse', 'shadowColor', 'useRayTraceShadows', 
								'lightAngle', 'shadowRays', 'rayDepthLimit']

VRAY_CAMERA_PARAMETERS_LIST = []
MAYA_CAMERA_PARAMETERS_LIST = ['focalLength', 'nearClipPlane', 'farClipPlane', 'horizontalFilmAperture', 'verticalFilmAperture'
								'depthOfField', 'focusDistance', 'fStop', 'focusRegionScale', 'backgroundColor', 'shutterAngle'
								'panZoomEnabled', 'horizontalPan', 'verticalPan', 'zoom', 'renderPanZoom', 'orthographic'
								'orthographicWidth']




#General Methods
#------------------------------------------------------------------

#vrayRenderSettingsNode
def vrayRenderSettingsNode():
	"""Get Vray rendersettings node"""
	
	#deselct all
	pm.select(cl = True)
	#select all nodes of type vraysettingsNode
	selList = pm.ls(fl = True, typ = 'VRaySettingsNode')
	
	#If selList < 1 return false and set status
	if not(selList):
		return None
	
	return selList[0]


#vray_settings_test
def vray_settings_test(func):
	"""Decorate adding of metadata with vray settings node existence test"""

	@wraps(func)
	def new_func():
		
		#log_progress
		log_progress = True

		try:
			#vray_settings_node
			vray_settings_node = vrayRenderSettingsNode()
			if not(vray_settings_node):
				print("Could not aquire vray settings node. Not added metadata for function: \n{0}".format(func.__doc__))
				return None

			#execute func
			attr, value = func(vray_settings_node)

			#cut value if larger than 20
			#if(len(str(value)) > 20):
			#	value = str(value)[:20] + '...'

			#log
			if(log_progress):
				print("Successfully added metadata: {0}={1}".format(attr, value))


		except:
			#if(log_progress):
			print("Error executing:\n{0}".format(func.__doc__))

	return new_func


#clear_metadata
def clear_metadata():
	"""Set metadata empty"""

	#log_progress
	log_progress = False

	try:
		#vray_settings_node
		vray_settings_node = vrayRenderSettingsNode()
		if not(vray_settings_node):
			print("Could not aquire vray settings node. Not cleared metadata")
			return None

		#clear
		vray_settings_node.imgOpt_exr_attributes.set("")

		#log
		if(log_progress):
			print("Successfully cleared metadata")


	except:
		#log
		if(log_progress):
			print("Error clearing metadata")


#get_inclusive_matrix
def get_inclusive_matrix(node_name):
	"""Get fn dag path from node name"""

	sel_list = open_maya.MSelectionList()
	try:
		sel_list.add(node_name)
	except:
		return None
	dag_path = open_maya.MDagPath()
	sel_list.getDagPath( 0, dag_path )
	return dag_path.inclusiveMatrix()


#mmatrix_to_list
def mmatrix_to_list(mmatrix):
	"""Convert Maya API 1 Matrix to flat python list"""

	if not(mmatrix):
		return []

	#list_matrix
	list_matrix = []

	#iterate and fill
	for row in range(4):
		for column in range(4):
			list_matrix.append(mmatrix(row, column))

	return list_matrix


#get_alembic_details_list
def get_alembic_details_list(include_search_from_alembic_node_type = False):
	"""Parse the scene for alembic nodes and return list with information"""

	#log_progress
	log_progress = False
	
	

	#alembic_details_list
	alembic_details_list = []



	#if include_search_from_alembic_node_type
	if(include_search_from_alembic_node_type):
		
		#iterate and gather from AlembicNodes
		#------------------------------------------------------------------

		#alembic_nodes_list
		alembic_nodes_list = cmds.ls(type = 'AlembicNode')

		#iterate
		for alembic_node_name in alembic_nodes_list:

			#alembic_details_dict
			alembic_details_dict = {}

			#add maya_node_name
			alembic_details_dict['maya_node_name'] = alembic_node_name

			#add maya_node_type
			alembic_details_dict['maya_node_type'] = cmds.nodeType(alembic_node_name)

			#alembic_path
			alembic_details_dict['alembic_path'] = cmds.getAttr(alembic_node_name +'.abc_File')

			#alembic_textures
			alembic_details_dict['alembic_textures'] = ''
			
			#append dict to list
			alembic_details_list.append(alembic_details_dict)


	


	#iterate and gather from metadata nodes
	#------------------------------------------------------------------
	
	#metadata_nodes_list
	metadata_nodes_list = pm.ls(type = 'metadata')

	for metadata_node in metadata_nodes_list:

		#alembic_details_dict
		alembic_details_dict = {}

		#add maya_node_name
		alembic_details_dict['maya_node_name'] = metadata_node.name()

		#add maya_node_type
		alembic_details_dict['maya_node_type'] = pm.nodeType(metadata_node)

		#alembic_path
		alembic_details_dict['alembic_path'] = cmds.getAttr(metadata_node.name() +'.alembic_path')

		#alembic_textures
		alembic_details_dict['alembic_textures'] = cmds.getAttr(metadata_node.name() +'.alembic_textures')
		
		#append dict to list
		alembic_details_list.append(alembic_details_dict)

	




	return alembic_details_list


#get_all_scene_lights
def get_all_scene_lights():
	"""get_all_scene_lights"""
	
	#clear selection
	pm.select(cl = True)
	
	#get standard maya lightslist
	mayaLightsList = pm.ls(fl = True, type = 'light')
	
	#get VRay Sphere Lights List
	vraySphereLightsList = pm.ls(fl = True, type = 'VRayLightSphereShape')
	
	#get VRay Dome Lights List
	vrayDomeLightsList = pm.ls(fl = True, type = 'VRayLightDomeShape')
	
	#get VRay Rect Lights List
	vrayRectLightsList = pm.ls(fl = True, type = 'VRayLightRectShape')
	
	#get VRay IES Lights List
	vrayIESLightsList = pm.ls(fl = True, type = 'VRayLightIESShape')

	#get VRay sun light List
	vraySunLightsList = pm.ls(fl = True, type = 'VRaySunShape')
	
	
	#return combined Lists
	return mayaLightsList + vraySphereLightsList + vrayDomeLightsList + vrayRectLightsList + vrayIESLightsList + vraySunLightsList


#get_light_details_list
def get_light_details_list():
	"""Parse the scene for light nodes and return list with information"""

	#log_progress
	log_progress = False

	#scene_lights_list
	scene_lights_list = get_all_scene_lights()
	#empty
	if not(scene_lights_list):
		print('No light nodes in the scene.')
		return []

	#scene_light_details_list
	scene_light_details_list = []

	#iterate and add details
	for light_node in scene_lights_list:

		#light_details_dict
		light_details_dict = {}

		#light_shape_name
		light_details_dict['light_shape_name'] = light_node.name()
		#light_transform_name
		light_details_dict['light_transform_name'] = light_node.getParent().name()
		#light_type
		light_details_dict['light_type'] = pm.nodeType(light_node)

		
		#inclusive_matrix
		inclusive_matrix = get_inclusive_matrix(light_node.name())
		#list_matrix
		list_matrix = mmatrix_to_list(inclusive_matrix)
		#add to dict
		light_details_dict['matrix'] = list_matrix




		#iterate LIGHT_PARAMETERS_LIST and add values if existing
		LIGHT_PARAMETERS_LIST = VRAY_LIGHT_PARAMETERS_LIST + MAYA_LIGHT_PARAMETERS_LIST
		for attr in LIGHT_PARAMETERS_LIST:
			if(light_node.hasAttr(attr)):
				#attr_value
				attr_value = pm.getAttr(light_node.name() +'.' +attr)
				#append to dict
				light_details_dict[attr] = attr_value

		

		#append dict to list
		scene_light_details_list.append(light_details_dict)


	return scene_light_details_list


#get_camera_details_list
def get_camera_details_list():
	"""Parse the scene for camera nodes and return list with information"""

	#log_progress
	log_progress = False

	#scene_cameras_list
	scene_cameras_list = pm.ls(ca = True)
	#empty
	if not(scene_cameras_list):
		print('No camera nodes in the scene.')
		return []

	#camera_details_list
	camera_details_list = []

	#iterate and add details
	for camera_node in scene_cameras_list:

		#camera_details_dict
		camera_details_dict = {}

		#camera_shape_name
		camera_details_dict['camera_shape_name'] = camera_node.name()
		#camera_transform_name
		camera_details_dict['camera_transform_name'] = camera_node.getParent().name()
		#camera_type
		camera_details_dict['camera_type'] = pm.nodeType(camera_node)

		
		#inclusive_matrix
		inclusive_matrix = get_inclusive_matrix(camera_node.name())
		#list_matrix
		list_matrix = mmatrix_to_list(inclusive_matrix)
		#add to dict
		camera_details_dict['matrix'] = list_matrix




		#iterate LIGHT_PARAMETERS_LIST and add values if existing
		CAMERA_PARAMETERS_LIST = VRAY_CAMERA_PARAMETERS_LIST + MAYA_CAMERA_PARAMETERS_LIST
		for attr in CAMERA_PARAMETERS_LIST:
			if(camera_node.hasAttr(attr)):
				#attr_value
				attr_value = pm.getAttr(camera_node.name() +'.' +attr)
				#append to dict
				camera_details_dict[attr] = attr_value

		

		#append dict to list
		camera_details_list.append(camera_details_dict)


	return camera_details_list


#get_rendersettings_dict
def get_rendersettings_dict():
	"""Parse the vray rendersettings node and return dict with information"""

	#log_progress
	log_progress = False

	#vray_settings_node
	vray_settings_node = vrayRenderSettingsNode()
	#empty
	if not(vray_settings_node):
		print('No vray rendersettings node in the scene.')
		return {}

	#rendersettings_details_dict
	rendersettings_details_dict = {}

	#iterate attrs
	for attr in vray_settings_node.listAttr():
		try:
			if(vray_settings_node.fileNamePrefix.name() != attr.name()):
				rendersettings_details_dict[pm.attributeName(attr)] = attr.get()
		except:
			#log
			if(log_process):
				print("Error getting value from attr. {0} from vray settings node {1}".format(pm.attributeName(attr), vray_settings_node.name()))


	return rendersettings_details_dict




#Add Data Methods
#------------------------------------------------------------------

@vray_settings_test
def add_render_settings_attr(vray_settings_node = None):
	"""render_settings"""

	#render_settings_dict
	render_settings_dict = get_rendersettings_dict()

	#attr
	attr = 'render_settings'
	#value
	value = pickle.dumps(render_settings_dict)
	#add
	vray_settings_node.imgOpt_exr_attributes.set("{0}{1}={2};".format(vray_settings_node.imgOpt_exr_attributes.get(), attr, value))

	return [attr, value]


@vray_settings_test
def add_test_attr(vray_settings_node = None):
	"""myTestAttr"""

	#attr
	attr = 'test_attr'
	#value
	value = 'test_value'
	#add
	vray_settings_node.imgOpt_exr_attributes.set("{0}{1}={2};".format(vray_settings_node.imgOpt_exr_attributes.get(), attr, value))

	return [attr, value]


@vray_settings_test
def add_pickle_list_attr(vray_settings_node = None):
	"""pickle_list"""

	#attr
	attr = 'pickle_list'
	#value
	value = 'render_settings, alembic_details, light_details, camera_details, scene_geometry_objects, scene_light_objects, scene_material_objects, scene_reference_pathes, scene_objects'
	#add
	vray_settings_node.imgOpt_exr_attributes.set("{0}{1}={2};".format(vray_settings_node.imgOpt_exr_attributes.get(), attr, value))

	return [attr, value]


@vray_settings_test
def add_username_attr(vray_settings_node = None):
	"""username"""

	#attr
	attr = 'username'
	#value
	value = os.environ.get('USERNAME')
	#add
	vray_settings_node.imgOpt_exr_attributes.set("{0}{1}={2};".format(vray_settings_node.imgOpt_exr_attributes.get(), attr, value))

	return [attr, value]


@vray_settings_test
def add_machine_name_attr(vray_settings_node = None):
	"""machine_name"""

	#attr
	attr = 'machine_name'
	#value
	value = platform.node()
	#add
	vray_settings_node.imgOpt_exr_attributes.set("{0}{1}={2};".format(vray_settings_node.imgOpt_exr_attributes.get(), attr, value))

	return [attr, value]


@vray_settings_test
def add_render_start_time_attr(vray_settings_node = None):
	"""render_start_time"""

	#attr
	attr = 'render_start_time'
	#value
	value = repr(datetime.datetime.now())
	#add
	vray_settings_node.imgOpt_exr_attributes.set("{0}{1}={2};".format(vray_settings_node.imgOpt_exr_attributes.get(), attr, value))

	return [attr, value]


@vray_settings_test
def add_render_cores_attr(vray_settings_node = None):
	"""render_cores"""

	#attr
	attr = 'render_cores'
	#value
	value = multiprocessing.cpu_count()
	#add
	vray_settings_node.imgOpt_exr_attributes.set("{0}{1}={2};".format(vray_settings_node.imgOpt_exr_attributes.get(), attr, value))

	return [attr, value]


@vray_settings_test
def add_alembic_details_attr(vray_settings_node = None):
	"""alembic_details"""

	#alembic_details_list
	alembic_details_list = get_alembic_details_list()
	

	#attr
	attr = 'alembic_details'
	#value
	value = pickle.dumps(alembic_details_list)
	#add
	vray_settings_node.imgOpt_exr_attributes.set("{0}{1}={2};".format(vray_settings_node.imgOpt_exr_attributes.get(), attr, value))

	return [attr, value]


@vray_settings_test
def add_light_details_attr(vray_settings_node = None):
	"""light_details"""

	#light_details_list
	light_details_list = get_light_details_list()
	

	#attr
	attr = 'light_details'
	#value
	value = pickle.dumps(light_details_list)
	#add
	vray_settings_node.imgOpt_exr_attributes.set("{0}{1}={2};".format(vray_settings_node.imgOpt_exr_attributes.get(), attr, value))

	return [attr, value]


@vray_settings_test
def add_camera_details_attr(vray_settings_node = None):
	"""camera_details"""

	#camera_details_list
	camera_details_list = get_camera_details_list()
	

	#attr
	attr = 'camera_details'
	#value
	value = pickle.dumps(camera_details_list)
	#add
	vray_settings_node.imgOpt_exr_attributes.set("{0}{1}={2};".format(vray_settings_node.imgOpt_exr_attributes.get(), attr, value))

	return [attr, value]


@vray_settings_test
def add_scene_geometry_objects_attr(vray_settings_node = None):
	"""scene_geometry_objects"""

	#scene_objects_list
	scene_objects_list = pm.ls(g = True)
	#scene_objects_name_list
	scene_objects_name_list = [node.name() for node in scene_objects_list]

	print("{0}-{1}".format('Scene objects list', scene_objects_list))
	print("{0}-{1}".format('Scene objects name list', scene_objects_name_list))

	#attr
	attr = 'scene_geometry_objects'
	#value
	value = pickle.dumps(scene_objects_name_list)

	#temp
	print('Add pickled list to vray options')

	#add
	vray_settings_node.imgOpt_exr_attributes.set("{0}{1}={2};".format(vray_settings_node.imgOpt_exr_attributes.get(), attr, value))

	return [attr, value]


@vray_settings_test
def add_scene_light_objects_attr(vray_settings_node = None):
	"""scene_light_objects"""

	#scene_objects_list
	scene_objects_list = pm.ls(lt = True)
	#scene_objects_name_list
	scene_objects_name_list = [node.name() for node in scene_objects_list]

	print("{0}-{1}".format('Scene lights list', scene_objects_list))
	print("{0}-{1}".format('Scene lights name list', scene_objects_name_list))

	#attr
	attr = 'scene_light_objects'
	#value
	value = pickle.dumps(scene_objects_name_list)

	#temp
	print('Add pickled list to vray options')

	#add
	vray_settings_node.imgOpt_exr_attributes.set("{0}{1}={2};".format(vray_settings_node.imgOpt_exr_attributes.get(), attr, value))

	return [attr, value]


@vray_settings_test
def add_scene_material_objects_attr(vray_settings_node = None):
	"""scene_material_objects"""

	#scene_objects_list
	scene_objects_list = pm.ls(mat = True)
	#scene_objects_name_list
	scene_objects_name_list = [node.name() for node in scene_objects_list]

	#attr
	attr = 'scene_material_objects'
	#value
	value = pickle.dumps(scene_objects_name_list)

	#temp
	print('Add pickled list to vray options')

	#add
	vray_settings_node.imgOpt_exr_attributes.set("{0}{1}={2};".format(vray_settings_node.imgOpt_exr_attributes.get(), attr, value))

	return [attr, value]


@vray_settings_test
def add_scene_reference_pathes_attr(vray_settings_node = None):
	"""scene_reference_pathes"""

	#scene_objects_list
	scene_objects_list = pm.ls(rf = True)
	#scene_objects_name_list
	scene_objects_name_list = [node.referenceFile() for node in scene_objects_list]

	#attr
	attr = 'scene_reference_pathes'
	#value
	value = pickle.dumps(scene_objects_name_list)

	#temp
	print('Add pickled list to vray options')

	#add
	vray_settings_node.imgOpt_exr_attributes.set("{0}{1}={2};".format(vray_settings_node.imgOpt_exr_attributes.get(), attr, value))

	return [attr, value]


@vray_settings_test
def add_scene_objects_attr(vray_settings_node = None):
	"""scene_objects"""

	#scene_objects_list
	scene_objects_list = pm.ls()
	#scene_objects_name_type_list
	scene_objects_name_type_list = [[node.name(), node.type()] for node in scene_objects_list]

	#attr
	attr = 'scene_objects'
	#value
	value = pickle.dumps(scene_objects_name_type_list)

	#temp
	print('Add pickled list to vray options')
	
	#add
	vray_settings_node.imgOpt_exr_attributes.set("{0}{1}={2};".format(vray_settings_node.imgOpt_exr_attributes.get(), attr, value))

	return [attr, value]



#Run
#------------------------------------------------------------------
def run():
	"""General and only method to invoke to start adding metadata"""

	#clear metadata
	clear_metadata()
	
	#add_render_settings_attr
	add_render_settings_attr()
	#test_attr
	add_test_attr()
	#add_pickle_list_attr
	add_pickle_list_attr()
	#add_username_attr
	add_username_attr()
	#add_machine_name_attr
	add_machine_name_attr()
	#add_render_start_time_attr
	add_render_start_time_attr()
	#add_render_cores_attr
	add_render_cores_attr()
	#add_alembic_details_attr
	add_alembic_details_attr()
	#add_light_details_attr
	add_light_details_attr()
	#add_camera_details_attr
	add_camera_details_attr()
	#add_scene_geometry_objects_attr
	add_scene_geometry_objects_attr()
	#add_scene_light_objects_attr
	add_scene_light_objects_attr()
	#add_scene_material_objects_attr
	add_scene_material_objects_attr()
	#add_scene_reference_pathes_attr
	add_scene_reference_pathes_attr()
	#add_scene_objects_attr
	add_scene_objects_attr()
	
	
	

#Execute
#------------------------------------------------------------------
if(__name__ == '__main__'):
	
	#run
	run()
	


