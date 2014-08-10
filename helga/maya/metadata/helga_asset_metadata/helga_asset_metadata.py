

"""
HelgaAssetMetadata
==========================================

Helga asset metadata nodes.
The following nodes are defined here:

- HelgaAssetMetadata
- HelgaPropMetadata
- HelgaCharacterMetadata

The fake_inheritance_initialize method checks if the classobject equals a given classobject
and if so, executes the fitting initialize static methods.

This is smartfuck and i hate myself for that.
Hopefully at one point it will poop on my head!!!

-----------------------
"""



#Import
#------------------------------------------------------------------
#python
import functools
#Maya
import maya.OpenMayaMPx as open_maya_mpx
import maya.OpenMaya as open_maya







#HelgaAssetMetadata
#------------------------------------------------------------------
class HelgaAssetMetadata(open_maya_mpx.MPxNode):
    
    #registration
    plugin_node_id = open_maya.MTypeId(0x00000010)
    plugin_name = 'HelgaAssetMetadata'
    
    #methods
    def __init__(self):
        open_maya_mpx.MPxNode.__init__(self)

    #create
    @staticmethod
    def create():
        return open_maya_mpx.asMPxPtr(HelgaAssetMetadata())

    #initialize
    @staticmethod
    def initialize(class_to_manipulate):

        #functionsets
        tAttr = open_maya.MFnTypedAttribute()
        
        #a_assetname
        class_to_manipulate.a_assetname = tAttr.create('asset_name', 'asset_name', open_maya.MFnData.kString)
        tAttr.setWritable(True)
        tAttr.setStorable(True)
        class_to_manipulate.addAttribute(class_to_manipulate.a_assetname)






#HelgaPropMetadata
#------------------------------------------------------------------
class HelgaPropMetadata(open_maya_mpx.MPxNode):
    
    #registration
    plugin_node_id = open_maya.MTypeId(0x00000011)
    plugin_name = 'HelgaPropMetadata'
    
    #methods
    def __init__(self):
        open_maya_mpx.MPxNode.__init__(self)

    #create
    @staticmethod
    def create():
        return open_maya_mpx.asMPxPtr(HelgaPropMetadata())

    #initialize
    @staticmethod
    def initialize(class_to_manipulate):

        #functionsets
        tAttr = open_maya.MFnTypedAttribute()
        nAttr = open_maya.MFnNumericAttribute()
        
        #a_proxy_visible
        class_to_manipulate.a_proxy_visible = nAttr.create('proxy_visible', 'proxy_visible', open_maya.MFnNumericData.kBoolean, False)
        nAttr.setWritable(True)
        nAttr.setStorable(True)
        class_to_manipulate.addAttribute(class_to_manipulate.a_proxy_visible)

        #a_rendergeo_visible
        class_to_manipulate.a_rendergeo_visible = nAttr.create('rendergeo_visible', 'rendergeo_visible', open_maya.MFnNumericData.kBoolean, False)
        nAttr.setWritable(True)
        nAttr.setStorable(True)
        class_to_manipulate.addAttribute(class_to_manipulate.a_rendergeo_visible)

        #a_locator_visible
        class_to_manipulate.a_locator_visible = nAttr.create('locator_visible', 'locator_visible', open_maya.MFnNumericData.kBoolean, False)
        nAttr.setWritable(True)
        nAttr.setStorable(True)
        class_to_manipulate.addAttribute(class_to_manipulate.a_locator_visible)

        #a_proxy_export
        class_to_manipulate.a_proxy_export = nAttr.create('proxy_export', 'proxy_export', open_maya.MFnNumericData.kBoolean, False)
        nAttr.setWritable(True)
        nAttr.setStorable(True)
        class_to_manipulate.addAttribute(class_to_manipulate.a_proxy_export)

        #a_rendergeo_export
        class_to_manipulate.a_rendergeo_export = nAttr.create('rendergeo_export', 'rendergeo_export', open_maya.MFnNumericData.kBoolean, False)
        nAttr.setWritable(True)
        nAttr.setStorable(True)
        class_to_manipulate.addAttribute(class_to_manipulate.a_rendergeo_export)

        #a_locator_export
        class_to_manipulate.a_locator_export = nAttr.create('locator_export', 'locator_export', open_maya.MFnNumericData.kBoolean, False)
        nAttr.setWritable(True)
        nAttr.setStorable(True)
        class_to_manipulate.addAttribute(class_to_manipulate.a_locator_export)






#HelgaCharacterMetadata
#------------------------------------------------------------------
class HelgaCharacterMetadata(open_maya_mpx.MPxNode):
    
    #registration
    plugin_node_id = open_maya.MTypeId(0x00000012)
    plugin_name = 'HelgaCharacterMetadata'
    
    #methods
    def __init__(self):
        open_maya_mpx.MPxNode.__init__(self)

    #create
    @staticmethod
    def create():
        return open_maya_mpx.asMPxPtr(HelgaCharacterMetadata())

    #initialize
    @staticmethod
    def initialize(class_to_manipulate):

        #functionsets
        tAttr = open_maya.MFnTypedAttribute()
        nAttr = open_maya.MFnNumericAttribute()

        #a_rendergeo_export
        class_to_manipulate.a_rendergeo_export = nAttr.create('rendergeo_export', 'rendergeo_export', open_maya.MFnNumericData.kBoolean, False)
        nAttr.setWritable(True)
        nAttr.setStorable(True)
        class_to_manipulate.addAttribute(class_to_manipulate.a_rendergeo_export)





#fake_inheritance_initialize
#------------------------------------------------------------------

#fake_inheritance_initialize
def fake_inheritance_initialize(cls):
    """
        Fake inheritance initialization function that creates node
        attributes based on the cls parameter it was passed.
    """

    #HelgaAssetMetadata
    if(cls == HelgaAssetMetadata):
        #Own
        HelgaAssetMetadata.initialize(HelgaAssetMetadata)

    #HelgaPropMetadata
    elif(cls == HelgaPropMetadata):
        #Base
        HelgaAssetMetadata.initialize(HelgaPropMetadata)
        #Own
        HelgaPropMetadata.initialize(HelgaPropMetadata)

    #HelgaCharacterMetadata
    elif(cls == HelgaCharacterMetadata):
        #Base
        HelgaAssetMetadata.initialize(HelgaCharacterMetadata)
        #Own
        HelgaCharacterMetadata.initialize(HelgaCharacterMetadata)


 
    


#Register
#------------------------------------------------------------------
def initializePlugin(obj):
    
    #fn_plugin
    fn_plugin = open_maya_mpx.MFnPlugin(obj, 'Timm Wagener', '0.1', 'Any')
    
    try:
        #HelgaAssetMetadata
        fn_plugin.registerNode(HelgaAssetMetadata.plugin_name, 
                                HelgaAssetMetadata.plugin_node_id, 
                                HelgaAssetMetadata.create, 
                                functools.partial(fake_inheritance_initialize, HelgaAssetMetadata))

        #HelgaPropMetadata
        fn_plugin.registerNode(HelgaPropMetadata.plugin_name, 
                                HelgaPropMetadata.plugin_node_id, 
                                HelgaPropMetadata.create, 
                                functools.partial(fake_inheritance_initialize, HelgaPropMetadata))

        #HelgaCharacterMetadata
        fn_plugin.registerNode(HelgaCharacterMetadata.plugin_name, 
                                HelgaCharacterMetadata.plugin_node_id, 
                                HelgaCharacterMetadata.create, 
                                functools.partial(fake_inheritance_initialize, HelgaCharacterMetadata))
    except:
        raise RuntimeError, 'Failed to register node'
 
def uninitializePlugin(obj):
    
    #fn_plugin
    fn_plugin = open_maya_mpx.MFnPlugin(obj)
    
    try:
        fn_plugin.deregisterNode(HelgaAssetMetadata.plugin_node_id)
        fn_plugin.deregisterNode(HelgaPropMetadata.plugin_node_id)
        fn_plugin.deregisterNode(HelgaCharacterMetadata.plugin_node_id)
    except:
        raise RuntimeError, 'Failed to register node'