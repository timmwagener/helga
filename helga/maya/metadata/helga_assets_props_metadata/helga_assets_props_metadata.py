

"""
HelgaAssetsPropsMetadata
==========================================

Simple node plugin that holds metadata related to the automatic
export of alembic caches.

-----------------------
"""



#Import
#------------------------------------------------------------------
import maya.OpenMayaMPx as open_maya_mpx
import maya.OpenMaya as open_maya







#HelgaAssetsPropsMetadata
#------------------------------------------------------------------
class HelgaAssetsPropsMetadata(open_maya_mpx.MPxNode):
	
	#registration
	plugin_node_id = open_maya.MTypeId(0x00000002)
	plugin_name = 'HelgaAssetsPropsMetadata'
 	
 	#attrs
 	a_alembic_name = open_maya.MObject()
 	

 	#methods
	def __init__(self):
		open_maya_mpx.MPxNode.__init__(self)
 
	



#Initialize
#------------------------------------------------------------------
def create():
	return open_maya_mpx.asMPxPtr(HelgaAssetsPropsMetadata())
 
def initialize():
	
	#functionsets
	nAttr = open_maya.MFnNumericAttribute()
	tAttr = open_maya.MFnTypedAttribute()
 	
 	#a_alembic_name
	HelgaAssetsPropsMetadata.a_alembic_name = tAttr.create('alembic_name', 'alembic_name', open_maya.MFnData.kString)
	tAttr.setWritable(True)
	tAttr.setStorable(True)
	HelgaAssetsPropsMetadata.addAttribute(HelgaAssetsPropsMetadata.a_alembic_name)


 
	
#Register
#------------------------------------------------------------------
def initializePlugin(obj):
	
	#fn_plugin
	fn_plugin = open_maya_mpx.MFnPlugin(obj, 'Timm Wagener', '0.1', 'Any')
	
	try:
		fn_plugin.registerNode(HelgaAssetsPropsMetadata.plugin_name, HelgaAssetsPropsMetadata.plugin_node_id, create, initialize)
	except:
		raise RuntimeError, 'Failed to register node'
 
def uninitializePlugin(obj):
	
	#fn_plugin
	fn_plugin = open_maya_mpx.MFnPlugin(obj)
	
	try:
		fn_plugin.deregisterNode(HelgaAssetsPropsMetadata.plugin_node_id)
	except:
		raise RuntimeError, 'Failed to register node'