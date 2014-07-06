

"""
setVrayRenderGlobals
==========================================

Set the VRay Render Globals according to pipeline standards.

-----------------------

Usage
-----

::
	
	from helga.maya.rendering.setVrayRenderGlobals import setVrayRenderGlobals
	reload(setVrayRenderGlobals)

	#Create instance
	setVrayRenderGlobalsInstance = setVrayRenderGlobals.SetVrayRenderGlobals()
	
	#set render globals completely
	setVrayRenderGlobalsInstance.setVrayRenderSettings()
	#set render globals linear light settings only
	setVrayRenderGlobalsInstance.setVrayRenderSettingsLinear()

-----------------------
"""




#Imports
#------------------------------------------------------------------
import maya.OpenMaya as openMaya
import pymel.core as pm






#Globals
#------------------------------------------------------------------

PRE_RENDER_MEL_SCRIPT = "python \"import sys; sys.path.append(\'\/\/whiterider\/kugeltiere\/23_NEUE_CLIPS\/01_Erdmaennchen\/140_scripts\/deploy\');from kugeltiere.maya.setExrMetadata import setExrMetadata;reload(setExrMetadata);setExrMetadata.run()\""





#SetVrayRenderGlobals class
#------------------------------------------------------------------

class SetVrayRenderGlobals():
	
	#Constructor
	def __init__(self):
		
		#Instance Vars
		#------------------------------------------------------------------
		
		pass
		
		
	
	#Methods
	#------------------------------------------------------------------
	
	#setVrayRenderSettings
	def setVrayRenderSettings(self, set_pre_render_mel_script = False):
		"""
		Set Vray Rendersettings

		:param set_pre_render_mel_script: Set the pre render MEL script. Default is False.
		:type set_pre_render_mel_script: bool
		"""
		
		
		#exit if vray for maya plugin is not loaded
		if not(self.vrayLoaded()):
			openMaya.MGlobal.displayWarning('Vray for Maya Plugin not loaded')
			return None
			
		#exit if vray rendersettings node doesnt exist
		vray_rendersettings_node = self.vrayRenderSettingsNode()
		if not(vray_rendersettings_node):
			openMaya.MGlobal.displayWarning('Vray Rendersettings node not found')
			return None
			
			
		#setVrayRenderSettings
		self.setVrayRenderSettingsParameter(linearOnly = False, set_pre_render_mel_script = set_pre_render_mel_script)
			
			
		#printStatus
		openMaya.MGlobal.displayInfo('Successfully set Vray Rendersettings')
		
	
	
	#setVrayRenderSettingsLinear
	def setVrayRenderSettingsLinear(self):
		"""Set Vray Rendersettings, linear light settings only"""

		#exit if vray for maya plugin is not loaded
		if not(self.vrayLoaded()):
			openMaya.MGlobal.displayWarning('Vray for Maya Plugin not loaded')
			return None
			
		#exit if vray rendersettings node doesnt exist
		vray_rendersettings_node = self.vrayRenderSettingsNode()
		if not(vray_rendersettings_node):
			openMaya.MGlobal.displayWarning('Vray Rendersettings node not found')
			return None
		
		
		#setVrayRenderSettings
		self.setVrayRenderSettingsParameter(linearOnly = True)
		
		#printStatus
		openMaya.MGlobal.displayInfo('Successfully set Vray Rendersettings. Linear Light parameters only')
	
	
	
	
	#Shared Methods
	#------------------------------------------------------------------
	
	
	#setVrayRenderSettings
	def setVrayRenderSettingsParameter(self, linearOnly = False, set_pre_render_mel_script = False):
		"""Set Vray Rendersettings. Never use this method directly."""
		
		#methodVars
		verbose = True
		vraySettingsNode = self.vrayRenderSettingsNode()
		
		
		#set Vray Rendersettings
		#------------------------------------------------------------------
		#------------------------------------------------------------------
		
		#Vray Common
		#------------------------------------------------------------------
		if not (linearOnly):
			
			#Image File Output
			pm.setAttr(vraySettingsNode.imageFormatStr, 'exr (multichannel)')
			pm.setAttr(vraySettingsNode.imgOpt_exr_compression, 3)
			pm.setAttr(vraySettingsNode.imgOpt_exr_autoDataWindow, 1)
			pm.setAttr(vraySettingsNode.imgOpt_exr_bitsPerChannel, 16)
			
			#Resolution
			pm.setAttr(vraySettingsNode.width, 1280)
			pm.setAttr(vraySettingsNode.height, 720)
			pm.setAttr(vraySettingsNode.aspectRatio, 1.777)
			pm.setAttr(vraySettingsNode.pixelAspect, 1)
			pm.setAttr(vraySettingsNode.sRGBOn, 1)
			pm.setAttr(vraySettingsNode.vfbOn, 1)
			if(set_pre_render_mel_script):
				pm.setAttr("defaultRenderGlobals.preRenderMel", PRE_RENDER_MEL_SCRIPT)
			
			if(verbose): print('Vray Common Parms set')
			
		
		#Vray
		#------------------------------------------------------------------
		if not (linearOnly):
			
			#Global options
			pm.setAttr(vraySettingsNode.globopt_render_viewport_subdivision, 1)
			pm.setAttr(vraySettingsNode.globopt_geom_displacement, 1)
			pm.setAttr(vraySettingsNode.globopt_light_doDefaultLights, 0)
			
			#Image Sampler
			pm.setAttr(vraySettingsNode.samplerType, 1)
			pm.setAttr(vraySettingsNode.aaFilterOn, 1)
			pm.setAttr(vraySettingsNode.aaFilterType, 1)
			pm.setAttr(vraySettingsNode.aaFilterSize, 1.5)
			pm.setAttr(vraySettingsNode.dmcMinSubdivs, 1)
			pm.setAttr(vraySettingsNode.dmcMaxSubdivs, 4)
			pm.setAttr(vraySettingsNode.dmcThreshold, 0.01)
			
			#Environment
			pm.setAttr(vraySettingsNode.cam_overrideEnvtex, 0)
			pm.setAttr(vraySettingsNode.cam_envtexGi, (0,0,0), type = 'double3')
			
		#Color mapping
		pm.setAttr(vraySettingsNode.cmap_type, 0)
		pm.setAttr(vraySettingsNode.cmap_gamma, 2.2)
		pm.setAttr(vraySettingsNode.cmap_affectBackground, 1)
		pm.setAttr(vraySettingsNode.cmap_subpixelMapping, 1)
		pm.setAttr(vraySettingsNode.cmap_adaptationOnly, 1)
		pm.setAttr(vraySettingsNode.cmap_linearworkflow, 1)
		pm.setAttr(vraySettingsNode.cmap_clampOutput, 1)
		pm.setAttr(vraySettingsNode.cmap_clampLevel, 5)
		pm.setAttr(vraySettingsNode.cmap_affectSwatches, 1)
		if(verbose): print('Vray Linear Light Parms set')
		
		if not (linearOnly):
			
			#Misc
			pm.setAttr(vraySettingsNode.bumpMultiplier, 1)
			pm.setAttr(vraySettingsNode.texFilterScaleMultiplier, 1)
			pm.setAttr(vraySettingsNode.photometricScale, 20)
			pm.setAttr(vraySettingsNode.allowNegativeShaderColors, 1)
			
			#Vray UI
			pm.setAttr(vraySettingsNode.ui_render_swatches, 1)
			
			if(verbose): print('Vray Parms set')
		
		
		#Indirect Illumination
		#------------------------------------------------------------------
		if not (linearOnly):
			
			#GI
			pm.setAttr(vraySettingsNode.giOn, 1)
			pm.setAttr(vraySettingsNode.saturation, 1)
			pm.setAttr(vraySettingsNode.contrast, 1)
			pm.setAttr(vraySettingsNode.contrastBase, 0.5)
			
			pm.setAttr(vraySettingsNode.primaryEngine, 2)
			pm.setAttr(vraySettingsNode.primaryMultiplier, 1)
			pm.setAttr(vraySettingsNode.giRayDistOn, 1)
			pm.setAttr(vraySettingsNode.dmc_subdivs, 32)
			pm.setAttr(vraySettingsNode.dmc_depth, 2)

			pm.setAttr(vraySettingsNode.secondaryEngine, 0)
			pm.setAttr(vraySettingsNode.secondaryMultiplier, 1)
			pm.setAttr(vraySettingsNode.aoOn, 0)
			
			#(Engine Specific Options) Irradiance Map
			pm.setAttr(vraySettingsNode.imap_currentPreset, 5)
			
			
			if(verbose): print('Global Illumination Parms set')
			
		
		#Settings
		#------------------------------------------------------------------
		if not (linearOnly):
			
			#DMC Sampler
			pm.setAttr(vraySettingsNode.dmcs_timeDependent, 0)
			pm.setAttr(vraySettingsNode.dmcs_adaptiveAmount, 0.85)
			pm.setAttr(vraySettingsNode.dmcs_adaptiveThreshold, 0.01)
			pm.setAttr(vraySettingsNode.dmcs_adaptiveMinSamples, 8)
			pm.setAttr(vraySettingsNode.dmcs_subdivsMult, 1)
			
			#Default Displacement and Subdivision
			pm.setAttr(vraySettingsNode.ddisplac_edgeLength, 2)
			pm.setAttr(vraySettingsNode.ddisplac_viewDependent, 1)
			pm.setAttr(vraySettingsNode.ddisplac_maxSubdivs, 6)
			pm.setAttr(vraySettingsNode.ddisplac_tightBounds, 1)
			pm.setAttr(vraySettingsNode.ddisplac_amount, 1)
			
			#System
			pm.setAttr(vraySettingsNode.sys_rayc_dynMemLimit, 40000)
			pm.setAttr(vraySettingsNode.sys_regsgen_xylocked, 1)
			pm.setAttr(vraySettingsNode.sys_regsgen_xc, 32)
			pm.setAttr(vraySettingsNode.sys_progress_increment, 1)
			pm.setAttr(vraySettingsNode.stamp_on, 1)
			
			if(verbose): print('Settings Parms set')
	
	
	
	#vrayLoaded
	def vrayLoaded(self):
		'''Return true or false wether or not Vray is loaded'''

		#Get list of all loaded plugIns
		plugInList = pm.pluginInfo( query=True, listPlugins=True )
		
		#Return true if loaded else setStatus and return false
		if('vrayformaya' in plugInList): 
			return True
		
		return False
		
	
	
	
	#vrayRenderSettingsNode
	def vrayRenderSettingsNode(self):
		'''Get Vray rendersettings node'''
		
		#deselct all
		pm.select(cl = True)
		#select all nodes of type vraysettingsNode
		selList = pm.ls(fl = True, typ = 'VRaySettingsNode')
		
		#If selList < 1 return false and set status
		if not(selList):
			return None
		
		return selList[0]
		
		
		
		
		
		