
"""
createDataPasses
==========================================

Automatic setup of the following VRay Render Elements in Maya.
They are also the names of the channels in the multichannel exr.
You can call this function as often as you want. It will not duplicate 
existing elements, only add missing ones.

The following elements are created:
	
	* Normals
	* BumpNormals
	* VelocityFiltered
	* VelocityUnfiltered
	* ZDepth.filtered
	* ZDepth.unfiltered
	* EtAmbOcc (Ambient Occlusion from extra tex)
	* EtWorldPos (World Position from extra tex)
	* EtSTMap
	* EtFresnelLarge
	* EtFresnelSmall
	* RenderId.index

-----------------------

Usage
-----

::
	
	from helga.maya.rendering.createUpdateRenderElements import createDataPasses
	reload(createDataPasses)

	#Create instance
	createDataPassesInstance = createDataPasses.CreateDataPasses()
	#Create/Update data passes
	createDataPassesInstance.createDataPasses()

-----------------------
"""





#Imports
#------------------------------------------------------------------
import pymel.core as pm
import maya.OpenMaya as openMaya


#reload?
doReload = True

#own
import vrayGlobals as vrayGlobals
if(doReload): reload(vrayGlobals)









#CreateDataPasses class
#------------------------------------------------------------------

class CreateDataPasses():
	
	#Constructor / Main Procedure
	def __init__(self):
		
		#Instance Vars
		#------------------------------------------------------------------
		self.verbose = True
		
		
	
	#Top Level Methods
	#------------------------------------------------------------------
	
	#createDataPasses
	def createDataPasses(self):
		"""
		Function to create/update data passes.
		"""
		
		
		
		#Check if Vray Loaded, else set Status and return
		if not(self.vrayLoaded()):
			openMaya.MGlobal.displayWarning('Vray for Maya Plugin not loaded')
			return None
		
		
		try:
			#NormalsRE
			attrName = 'vray_name_normals'
			attrValue = '{0}Normals'.format(vrayGlobals.PREFIX)
			if not(self.REWithAttrAndValueExists(attrName, attrValue)): self.createNormalsRE()
			
			#BumpNormalsRE
			attrName = 'vray_name_bumpnormals'
			attrValue = '{0}BumpNormals'.format(vrayGlobals.PREFIX)
			if not(self.REWithAttrAndValueExists(attrName, attrValue)): self.createBumpNormalsRE()
			
			#VelocityREFiltered
			attrName = 'vray_filename_velocity'
			attrValue = '{0}VelocityFiltered'.format(vrayGlobals.PREFIX)
			if not(self.REWithAttrAndValueExists(attrName, attrValue)): self.createVelocityREFiltered()
			
			#VelocityREUnfiltered
			attrName = 'vray_filename_velocity'
			attrValue = '{0}VelocityUnfiltered'.format(vrayGlobals.PREFIX)
			if not(self.REWithAttrAndValueExists(attrName, attrValue)): self.createVelocityREUnfiltered()
			
			#zDepthREFiltered
			attrName = 'vray_name_zdepth'
			attrValue = '{0}ZDepth.filtered'.format(vrayGlobals.PREFIX)
			if not(self.REWithAttrAndValueExists(attrName, attrValue)): self.createZDepthREFiltered()
			
			#zDepthREUnfiltered
			attrName = 'vray_name_zdepth'
			attrValue = '{0}ZDepth.unfiltered'.format(vrayGlobals.PREFIX)
			if not(self.REWithAttrAndValueExists(attrName, attrValue)): self.createZDepthREUnfiltered()
			
			#etAmbOccRE
			attrName = 'vray_explicit_name_extratex'
			attrValue = '{0}EtAmbOcc'.format(vrayGlobals.PREFIX)
			if not(self.REWithAttrAndValueExists(attrName, attrValue)): self.createEtAmbOccRE()
			
			#etWorldPosRE
			attrName = 'vray_explicit_name_extratex'
			attrValue = '{0}EtWorldPos'.format(vrayGlobals.PREFIX)
			if not(self.REWithAttrAndValueExists(attrName, attrValue)): self.createEtWorldPosRE()
			
			#etSTMapRE
			attrName = 'vray_explicit_name_extratex'
			attrValue = '{0}EtSTMap'.format(vrayGlobals.PREFIX)
			if not(self.REWithAttrAndValueExists(attrName, attrValue)): self.createEtSTMapRE()

			#etFresnelLarge
			attrName = 'vray_explicit_name_extratex'
			attrValue = '{0}EtFresnelLarge'.format(vrayGlobals.PREFIX)
			if not(self.REWithAttrAndValueExists(attrName, attrValue)): self.createEtFresnelLargeRE()

			#etFresnelSmall
			attrName = 'vray_explicit_name_extratex'
			attrValue = '{0}EtFresnelSmall'.format(vrayGlobals.PREFIX)
			if not(self.REWithAttrAndValueExists(attrName, attrValue)): self.createEtFresnelSmallRE()
			
			#RenderIdRE
			attrName = 'vray_name_renderid'
			attrValue = '{0}RenderId.index'.format(vrayGlobals.PREFIX)
			if not(self.REWithAttrAndValueExists(attrName, attrValue)): self.createRenderIdRE()
			
			#msg
			openMaya.MGlobal.displayInfo('Data Passes created succesfully')

		except:
			#msg
			openMaya.MGlobal.displayWarning('Error creating Data Passes')
	
	
	
	
	
	
	#Methods
	#------------------------------------------------------------------
	
	
	
	#Data Pases
	#------------------------------------------------------------------
	
	#createNormalsRE
	def createNormalsRE(self):
		
		#create normals RE
		normalsRE = self.createRenderElement('normalsChannel')
		pm.rename(normalsRE, '{0}Normals'.format(vrayGlobals.PREFIX))
		
		#SetAttrs on normalsRE
		pm.setAttr(normalsRE.vray_filtering_normals, 0)
		pm.setAttr(normalsRE.vray_name_normals, '{0}Normals'.format(vrayGlobals.PREFIX))
		
		#verbose
		if(self.verbose): print('Normals RE created')
		
		
	
	#createBumpNormalsRE
	def createBumpNormalsRE(self):
		
		#create bump normals RE
		bumpNormalsRE = self.createRenderElement('bumpNormalsChannel')
		pm.rename(bumpNormalsRE, '{0}BumpNormals'.format(vrayGlobals.PREFIX))
		
		#SetAttrs on bumpNormalsRE
		pm.setAttr(bumpNormalsRE.vray_filtering_bumpnormals, 0)
		pm.setAttr(bumpNormalsRE.vray_name_bumpnormals, '{0}BumpNormals'.format(vrayGlobals.PREFIX))
		
		#verbose
		if(self.verbose): print('Bump Normals RE created')
	
		
	
	#createVelocityREFiltered
	def createVelocityREFiltered(self):
		
		#create velocity RE Filtered
		velocityREFiltered = self.createRenderElement('velocityChannel')
		pm.rename(velocityREFiltered, '{0}VelocityFiltered'.format(vrayGlobals.PREFIX))
		
		#SetAttrs on velocityREFiltered
		pm.setAttr(velocityREFiltered.vray_filtering_velocity, 1)
		pm.setAttr(velocityREFiltered.vray_filename_velocity, '{0}VelocityFiltered'.format(vrayGlobals.PREFIX))
		pm.setAttr(velocityREFiltered.vray_clamp_velocity, 0)
		pm.setAttr(velocityREFiltered.vray_ignorez_velocity, 0)
		
		#verbose
		if(self.verbose): print('Velocity RE Filtered created')
		
	
	#createVelocityREUnfiltered
	def createVelocityREUnfiltered(self):
		
		#create velocity RE Unfiltered
		velocityREUnfiltered = self.createRenderElement('velocityChannel')
		pm.rename(velocityREUnfiltered, '{0}VelocityUnfiltered'.format(vrayGlobals.PREFIX))
		
		#SetAttrs on velocityREUnfiltered
		pm.setAttr(velocityREUnfiltered.vray_filtering_velocity, 0)
		pm.setAttr(velocityREUnfiltered.vray_filename_velocity, '{0}VelocityUnfiltered'.format(vrayGlobals.PREFIX))
		pm.setAttr(velocityREUnfiltered.vray_clamp_velocity, 0)
		pm.setAttr(velocityREUnfiltered.vray_ignorez_velocity, 0)
		
		#verbose
		if(self.verbose): print('Velocity RE Unfiltered created')
		
	
	#createZDepthREFiltered
	def createZDepthREFiltered(self):
		
		#create zDepthREFiltered
		zDepthREFiltered = self.createRenderElement('zdepthChannel')
		pm.rename(zDepthREFiltered, '{0}ZDepthFiltered'.format(vrayGlobals.PREFIX))
		
		#SetAttrs on zDepthREFiltered
		pm.setAttr(zDepthREFiltered.vray_depthFromCamera_zdepth, 0)
		pm.setAttr(zDepthREFiltered.vray_name_zdepth, '{0}ZDepth.filtered'.format(vrayGlobals.PREFIX))
		pm.setAttr(zDepthREFiltered.vray_depthClamp, 0)
		pm.setAttr(zDepthREFiltered.vray_depthWhite, 1)
		pm.setAttr(zDepthREFiltered.vray_filtering_zdepth, 1)
		
		#verbose
		if(self.verbose): print('ZDepth RE Filtered created')
		
		
		
	#createZDepthREUnfiltered
	def createZDepthREUnfiltered(self):
		
		#create zDepthREUnfiltered
		zDepthREUnfiltered = self.createRenderElement('zdepthChannel')
		pm.rename(zDepthREUnfiltered, '{0}ZDepthUnfiltered'.format(vrayGlobals.PREFIX))
		
		#SetAttrs on zDepthREUnfiltered
		pm.setAttr(zDepthREUnfiltered.vray_depthFromCamera_zdepth, 0)
		pm.setAttr(zDepthREUnfiltered.vray_name_zdepth, '{0}ZDepth.unfiltered'.format(vrayGlobals.PREFIX))
		pm.setAttr(zDepthREUnfiltered.vray_depthClamp, 0)
		pm.setAttr(zDepthREUnfiltered.vray_depthWhite, 1)
		pm.setAttr(zDepthREUnfiltered.vray_filtering_zdepth, 0)
		
		#verbose
		if(self.verbose): print('ZDepth RE Unfiltered created')
		
		
		
		
	#createEtAmbOccRE
	def createEtAmbOccRE(self):
		
		#create etAmbOccRE
		etAmbOccRE = self.createRenderElement('ExtraTexElement')
		pm.rename(etAmbOccRE, '{0}EtAmbOcc'.format(vrayGlobals.PREFIX))
		
		#SetAttrs on etAmbOccRE
		pm.setAttr(etAmbOccRE.vray_name_extratex, '{0}EtAmbOcc'.format(vrayGlobals.PREFIX))
		pm.setAttr(etAmbOccRE.vray_explicit_name_extratex, '{0}EtAmbOcc'.format(vrayGlobals.PREFIX))
		pm.setAttr(etAmbOccRE.vray_affectmattes_extratex, 0)
		
		
		#Create vraydirt tex and setAttrs
		pm.select(cl = True)
		
		vrayDirtTex = pm.createNode('VRayDirt')
		pm.rename(vrayDirtTex, '{0}VRayDirt'.format(vrayGlobals.PREFIX))
		pm.setAttr(vrayDirtTex.workWithTransparency, 1)
		
		#connect vraydirt tex
		vrayDirtTex.outColor >> etAmbOccRE.vray_texture_extratex
		pm.select(cl = True)
		
		
		#verbose
		if(self.verbose): print('Extra Tex AmbOcc RE created')
		
		
	
	#createEtWorldPosRE
	def createEtWorldPosRE(self):
		
		#create etWorldPosRE
		etWorldPosRE = self.createRenderElement('ExtraTexElement')
		pm.rename(etWorldPosRE, '{0}EtWorldPos'.format(vrayGlobals.PREFIX))
		
		#SetAttrs on etWorldPosRE
		pm.setAttr(etWorldPosRE.vray_name_extratex, '{0}EtWorldPos'.format(vrayGlobals.PREFIX))
		pm.setAttr(etWorldPosRE.vray_explicit_name_extratex, '{0}EtWorldPos'.format(vrayGlobals.PREFIX))
		pm.setAttr(etWorldPosRE.vray_affectmattes_extratex, 0)
		pm.setAttr(etWorldPosRE.vray_filtering_extratex, 0)
		
		
		#Create vrayfresnel tex and setAttrs
		pm.select(cl = True)
		
		vrayFresnelTex = pm.createNode('VRayFresnel')
		pm.rename(vrayFresnelTex, '{0}VRayFresnelWorldPos'.format(vrayGlobals.PREFIX))
		pm.setAttr(vrayFresnelTex.IOR, 1)
		
		pm.select(cl = True)
		
		#Create sampler Info Node
		samplerInfoWorldPos = pm.createNode('samplerInfo')
		pm.rename(samplerInfoWorldPos, '{0}SamplerInfoWorldPos'.format(vrayGlobals.PREFIX))
		
		#connections
		samplerInfoWorldPos.pointWorld >> vrayFresnelTex.frontColor
		samplerInfoWorldPos.pointWorld >> vrayFresnelTex.sideColor
		vrayFresnelTex.outColor >> etWorldPosRE.vray_texture_extratex
		pm.select(cl = True)
		
		
		#verbose
		if(self.verbose): print('Extra Tex World Pos RE created')
		
	
	
	#createEtSTMapRE
	def createEtSTMapRE(self):
		
		#create etSTMapRE
		etSTMapRE = self.createRenderElement('ExtraTexElement')
		pm.rename(etSTMapRE, '{0}EtSTMap'.format(vrayGlobals.PREFIX))
		
		#SetAttrs on etSTMapRE
		pm.setAttr(etSTMapRE.vray_name_extratex, '{0}EtSTMap'.format(vrayGlobals.PREFIX))
		pm.setAttr(etSTMapRE.vray_explicit_name_extratex, '{0}EtSTMap'.format(vrayGlobals.PREFIX))
		pm.setAttr(etSTMapRE.vray_affectmattes_extratex, 0)
		pm.setAttr(etSTMapRE.vray_filtering_extratex, 0)
		
		
		#Create Red Ramp
		redRamp = self.createRamp(rampDirection = 0)
		pm.rename(redRamp, '{0}STMapRedRamp'.format(vrayGlobals.PREFIX))
		#remove middle colorValue
		pm.removeMultiInstance (redRamp.colorEntryList[1], b=True)
		#set upper pos color to red
		redRamp.colorEntryList[2].color.set([1,0,0])
		redRamp.colorEntryList[2].position.set(1)
		#set lower pos color to black
		redRamp.colorEntryList[0].color.set([0,0,0])
		redRamp.colorEntryList[0].position.set(0)
		
		#Create Green Ramp
		greenRamp = self.createRamp(rampDirection = 1)
		pm.rename(greenRamp, '{0}STMapGreenRamp'.format(vrayGlobals.PREFIX))
		#remove middle colorValue
		pm.removeMultiInstance (greenRamp.colorEntryList[1], b=True)
		#set upper pos color to green
		greenRamp.colorEntryList[2].color.set([0,1,0])
		greenRamp.colorEntryList[2].position.set(1)
		#set lower pos color to black
		greenRamp.colorEntryList[0].color.set([0,0,0])
		greenRamp.colorEntryList[0].position.set(0)
		
		pm.select(cl = True)
		
		#Connect ramps
		redRamp.outColor >> greenRamp.colorOffset
		
		#connect to extratex
		greenRamp.outColor >> etSTMapRE.vray_texture_extratex
		
		#verbose
		if(self.verbose): print('Extra Tex World Pos RE created')
	
	
	#createEtFresnelLargeRE
	def createEtFresnelLargeRE(self):
		
		#create etFresnelLargeRE
		etFresnelLargeRE = self.createRenderElement('ExtraTexElement')
		pm.rename(etFresnelLargeRE, '{0}EtFresnelLarge'.format(vrayGlobals.PREFIX))
		
		#SetAttrs on etFresnelLargeRE
		pm.setAttr(etFresnelLargeRE.vray_name_extratex, '{0}EtFresnelLarge'.format(vrayGlobals.PREFIX))
		pm.setAttr(etFresnelLargeRE.vray_explicit_name_extratex, '{0}EtFresnelLarge'.format(vrayGlobals.PREFIX))
		pm.setAttr(etFresnelLargeRE.vray_affectmattes_extratex, 0)
		pm.setAttr(etFresnelLargeRE.vray_filtering_extratex, 1)
		
		
		#vray_fresnel_node
		vray_fresnel_node = pm.createNode('VRayFresnel')
		vray_fresnel_node.IOR.set(2)
		pm.select(cl = True)
		
		#connect to extratex
		vray_fresnel_node.outColor >> etFresnelLargeRE.vray_texture_extratex
		
		#verbose
		if(self.verbose): print('Extra Tex Fresnel Large RE created')


	#createEtFresnelSmallRE
	def createEtFresnelSmallRE(self):
		
		#create etFresnelSmallRE
		etFresnelSmallRE = self.createRenderElement('ExtraTexElement')
		pm.rename(etFresnelSmallRE, '{0}EtFresnelSmall'.format(vrayGlobals.PREFIX))
		
		#SetAttrs on etFresnelSmallRE
		pm.setAttr(etFresnelSmallRE.vray_name_extratex, '{0}EtFresnelSmall'.format(vrayGlobals.PREFIX))
		pm.setAttr(etFresnelSmallRE.vray_explicit_name_extratex, '{0}EtFresnelSmall'.format(vrayGlobals.PREFIX))
		pm.setAttr(etFresnelSmallRE.vray_affectmattes_extratex, 0)
		pm.setAttr(etFresnelSmallRE.vray_filtering_extratex, 1)
		
		
		#vray_fresnel_node
		vray_fresnel_node = pm.createNode('VRayFresnel')
		vray_fresnel_node.IOR.set(1.1)
		pm.select(cl = True)
		
		#connect to extratex
		vray_fresnel_node.outColor >> etFresnelSmallRE.vray_texture_extratex
		
		#verbose
		if(self.verbose): print('Extra Tex Fresnel Small RE created')
	
	
	#createRenderIdRE
	def createRenderIdRE(self):
		
		#create render id RE
		renderIdRE = self.createRenderElement('renderIDChannel')
		pm.rename(renderIdRE, '{0}RenderId'.format(vrayGlobals.PREFIX))
		
		#SetAttrs on renderIdRE
		pm.setAttr(renderIdRE.vray_name_renderid, '{0}RenderId.index'.format(vrayGlobals.PREFIX))
		
		#verbose
		if(self.verbose): print('RenderID RE created')
		
	
	
	
	
	
	
	
	#Shared Methods
	#------------------------------------------------------------------
	
	
	#REWithAttrAndValueExists
	def REWithAttrAndValueExists(self, attrName, attrValue):
		
		#List all nodes of Type VRayRenderElement
		REList = pm.ls(fl = True, typ = 'VRayRenderElement')
		
		#if list < 1 return False (no RE in scene, ready to create)
		if not(REList): return False
		
		#if list larger check if REName in list of RElements
		for RE in REList:
			#check if RE has attr of attrName and if return True
			try:
				if(pm.getAttr(RE.name() +'.' +attrName) == attrValue): return True
			except:
				pass
		
		#Else False (ready to create)
		return False
	
	
	
	#createRenderElement
	def createRenderElement(self, renderElementName):
		
		#clear Selection
		pm.select(cl = True)
		
		#build MEL Cmd
		createRElementMELCmd = 'vrayAddRenderElement ' +renderElementName +';'
		
		#Execute
		pm.mel.eval(createRElementMELCmd)
		
		#return created RenderElementNode
		renderElement = pm.ls(sl = True, fl = True)[0]
		pm.select(cl = True)
		
		return renderElement
		
	
	#createRamp
	def createRamp(self, rampDirection = 1):
		
		#rampDirection 1 = u, 0 = v
		
		#clear selection
		pm.select(cl = True)
		#createRamp
		ramp = pm.createNode('ramp')
		pm.setAttr(ramp.name() +'.type' , rampDirection)
		pm.select(cl = True)
		#createUVCoords
		place2dTexture = pm.createNode('place2dTexture')
		pm.rename(place2dTexture, '{0}STMapPlace2dTextureNode'.format(vrayGlobals.PREFIX))
		pm.select(cl = True)
		#connections
		place2dTexture.outUV >> ramp.uvCoord
		place2dTexture.outUvFilterSize >> ramp.uvFilterSize
		pm.select(cl = True)
		
		return ramp
		
		
	#vrayLoaded
	def vrayLoaded(self):
		#Get list of all loaded plugIns
		plugInList = pm.pluginInfo( query=True, listPlugins=True )
		
		#Return true if loaded else setStatus and return false
		if('vrayformaya' in plugInList):
			return True
		
		return False
	
	
	
	
	