

"""
HelgaShotsMetadata
==========================================

Simple node plugin that holds metadata related to helga shots.

-----------------------
"""



#Import
#------------------------------------------------------------------
import maya.OpenMayaMPx as open_maya_mpx
import maya.OpenMaya as open_maya







#HelgaShotsMetadata
#------------------------------------------------------------------
class HelgaShotsMetadata(open_maya_mpx.MPxNode):
	
	#registration
	plugin_node_id = open_maya.MTypeId(0x00000003)
	plugin_name = 'HelgaShotsMetadata'
 	

 	#methods
	def __init__(self):
		open_maya_mpx.MPxNode.__init__(self)
 
	



#Initialize
#------------------------------------------------------------------
def create():
	return open_maya_mpx.asMPxPtr(HelgaShotsMetadata())
 
def initialize():
	
	#functionsets
	nAttr = open_maya.MFnNumericAttribute()
	tAttr = open_maya.MFnTypedAttribute()
 	
 	#a_shot_name
	HelgaShotsMetadata.a_shot_name = tAttr.create('shot_name', 'shot_name', open_maya.MFnData.kString)
	tAttr.setWritable(True)
	tAttr.setStorable(True)
	HelgaShotsMetadata.addAttribute(HelgaShotsMetadata.a_shot_name)

	#a_alembic_path
	HelgaShotsMetadata.a_alembic_path = tAttr.create('alembic_path', 'alembic_path', open_maya.MFnData.kString)
	tAttr.setWritable(True)
	tAttr.setStorable(True)
	HelgaShotsMetadata.addAttribute(HelgaShotsMetadata.a_alembic_path)

	#a_shot_cam
	HelgaShotsMetadata.a_shot_cam = tAttr.create('shot_cam', 'shot_cam', open_maya.MFnData.kString)
	tAttr.setWritable(True)
	tAttr.setStorable(True)
	HelgaShotsMetadata.addAttribute(HelgaShotsMetadata.a_shot_cam)

	#a_shot_start
	HelgaShotsMetadata.a_shot_start = nAttr.create('shot_start', 'shot_start', open_maya.MFnNumericData.kInt)
	tAttr.setWritable(True)
	tAttr.setStorable(True)
	HelgaShotsMetadata.addAttribute(HelgaShotsMetadata.a_shot_start)

	#a_shot_end
	HelgaShotsMetadata.a_shot_end = nAttr.create('shot_end', 'shot_end', open_maya.MFnNumericData.kInt)
	tAttr.setWritable(True)
	tAttr.setStorable(True)
	HelgaShotsMetadata.addAttribute(HelgaShotsMetadata.a_shot_end)


 
	
#Register
#------------------------------------------------------------------
def initializePlugin(obj):
	
	#fn_plugin
	fn_plugin = open_maya_mpx.MFnPlugin(obj, 'Timm Wagener', '0.1', 'Any')
	
	try:
		fn_plugin.registerNode(HelgaShotsMetadata.plugin_name, HelgaShotsMetadata.plugin_node_id, create, initialize)
	except:
		raise RuntimeError, 'Failed to register node'
 
def uninitializePlugin(obj):
	
	#fn_plugin
	fn_plugin = open_maya_mpx.MFnPlugin(obj)
	
	try:
		fn_plugin.deregisterNode(HelgaShotsMetadata.plugin_node_id)
	except:
		raise RuntimeError, 'Failed to register node'