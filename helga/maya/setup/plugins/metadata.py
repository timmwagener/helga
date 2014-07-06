





#Import
#------------------------------------------------------------------
import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMaya as OpenMaya







#Metadata
#------------------------------------------------------------------
class Metadata(OpenMayaMPx.MPxNode):
	
	#registration
	kPluginNodeId = OpenMaya.MTypeId(0x00000001)
	kPluginName = 'metadata'
 	
 	#attrs
 	a_alembic_pathes = OpenMaya.MObject()
 	a_alembic_textures = OpenMaya.MObject()

 	#methods
	def __init__(self):
		OpenMayaMPx.MPxNode.__init__(self)
 
	



#Initialize
#------------------------------------------------------------------
def creator():
	return OpenMayaMPx.asMPxPtr(Metadata())
 
def initialize():
	
	#functionsets
	nAttr = OpenMaya.MFnNumericAttribute()
	tAttr = OpenMaya.MFnTypedAttribute()
 	
 	#a_alembic_pathes
	Metadata.a_alembic_pathes = tAttr.create('alembic_path', 'alembic_path', OpenMaya.MFnData.kString)
	tAttr.setWritable(True)
	tAttr.setStorable(True)
	Metadata.addAttribute(Metadata.a_alembic_pathes)

	#a_alembic_textures / divide by ";"
	Metadata.a_alembic_textures = tAttr.create('alembic_textures', 'alembic_textures', OpenMaya.MFnData.kString)
	tAttr.setWritable(True)
	tAttr.setStorable(True)
	Metadata.addAttribute(Metadata.a_alembic_textures)
 
	
#Register
#------------------------------------------------------------------
def initializePlugin(obj):
	plugin = OpenMayaMPx.MFnPlugin(obj, 'Timm Wagener', '1.0', 'Any')
	try:
		plugin.registerNode(Metadata.kPluginName, Metadata.kPluginNodeId, creator, initialize)
	except:
		raise RuntimeError, 'Failed to register node'
 
def uninitializePlugin(obj):
	plugin = OpenMayaMPx.MFnPlugin(obj)
	try:
		plugin.deregisterNode(Metadata.kPluginNodeId)
	except:
		raise RuntimeError, 'Failed to register node'