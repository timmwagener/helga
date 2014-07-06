
"""
createFrameBufferContributions
==========================================

Automatic setup of the following VRay Render Elements in Maya.
They are also the names of the channels in the multichannel exr.
You can call this function as often as you want. It will not duplicate 
existing elements, only add missing ones.

The following elements are created:
	
	* Diffuse
	* Reflection
	* Refraction
	* Specular
	* Subsurface

-----------------------

Usage
-----

::
	
	from helga.maya.rendering.createUpdateRenderElements import createFrameBufferContributions
	reload(createFrameBufferContributions)

	#Create instance
	createFrameBufferContributionsInstance = createFrameBufferContributions.CreateFrameBufferContributions()
	#Create/Update framebuffer passes
	createFrameBufferContributionsInstance.createFrameBufferContributions()

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








#CreateFrameBufferContributions class
#------------------------------------------------------------------

class CreateFrameBufferContributions():
	
	#Constructor / Main Procedure
	def __init__(self):
		
		#Instance Vars
		#------------------------------------------------------------------
		self.verbose = True
		
		
	
	#Top Level Methods
	#------------------------------------------------------------------
	
	#createFrameBufferContributions
	def createFrameBufferContributions(self):
		"""
		Function to create/update framebuffer passes (see above for AOV types).
		"""
		
		
		#Check if Vray Loaded, else set Status and return
		if not(self.vrayLoaded()):
			openMaya.MGlobal.displayWarning('Vray for Maya Plugin not loaded')
			return None
		
		
		
		try:
			#diffuseRE
			attrName = 'vray_name_rawdiffuse'
			attrValue = '{0}Diffuse'.format(vrayGlobals.PREFIX)
			if not(self.REWithAttrAndValueExists(attrName, attrValue)): self.createDiffuseRE()
			
			
			#reflectionRE
			attrName = 'vray_name_reflect'
			attrValue = '{0}Reflection'.format(vrayGlobals.PREFIX)
			if not(self.REWithAttrAndValueExists(attrName, attrValue)): self.createReflectionRE()
			
			
			#refractionRE
			attrName = 'vray_name_refract'
			attrValue = '{0}Refraction'.format(vrayGlobals.PREFIX)
			if not(self.REWithAttrAndValueExists(attrName, attrValue)): self.createRefractionRE()
			
			
			#specularRE
			attrName = 'vray_name_specular'
			attrValue = '{0}Specular'.format(vrayGlobals.PREFIX)
			if not(self.REWithAttrAndValueExists(attrName, attrValue)): self.createSpecularRE()
			
			
			#SubsurfaceRE
			attrName = 'vray_name_sss'
			attrValue = '{0}Subsurface'.format(vrayGlobals.PREFIX)
			if not(self.REWithAttrAndValueExists(attrName, attrValue)): self.createSubsurfaceRE()
			
			
			
			#msg
			openMaya.MGlobal.displayInfo('Frame Buffer Passes created succesfully')

		except:
			#msg
			openMaya.MGlobal.displayWarning('Error creating Frame Buffer passes')
	
	
	
	
	
	
	
	#Methods
	#------------------------------------------------------------------
	
	
	
	#Frame Buffer Contribution REs
	#------------------------------------------------------------------
	
	#createDiffuseRE
	def createDiffuseRE(self):
		
		#create diffuse RE
		diffuseRE = self.createRenderElement('diffuseChannel')
		pm.rename(diffuseRE, '{0}Diffuse'.format(vrayGlobals.PREFIX))
		
		#SetAttrs on diffuseRE
		pm.setAttr(diffuseRE.vray_name_rawdiffuse, '{0}Diffuse'.format(vrayGlobals.PREFIX))
		
		#verbose
		if(self.verbose): print('Diffuse RE created')
		
		
	
	#createReflectionRE
	def createReflectionRE(self):
		
		#create reflection RE
		reflectionRE = self.createRenderElement('reflectChannel')
		pm.rename(reflectionRE, '{0}Reflection'.format(vrayGlobals.PREFIX))
		
		#SetAttrs on reflectionRE
		pm.setAttr(reflectionRE.vray_name_reflect, '{0}Reflection'.format(vrayGlobals.PREFIX))
		
		#verbose
		if(self.verbose): print('Reflection RE created')
		
		
	
	#createRefractionRE
	def createRefractionRE(self):
		
		#create refractionRE
		refractionRE = self.createRenderElement('refractChannel')
		pm.rename(refractionRE, '{0}Refraction'.format(vrayGlobals.PREFIX))
		
		#SetAttrs on refractionRE
		pm.setAttr(refractionRE.vray_name_refract, '{0}Refraction'.format(vrayGlobals.PREFIX))
		
		#verbose
		if(self.verbose): print('Refraction RE created')
		
		
	
	#createSpecularRE
	def createSpecularRE(self):
		
		#create specularRE
		specularRE = self.createRenderElement('specularChannel')
		pm.rename(specularRE, '{0}Specular'.format(vrayGlobals.PREFIX))
		
		#SetAttrs on specularRE
		pm.setAttr(specularRE.vray_name_specular, '{0}Specular'.format(vrayGlobals.PREFIX))
		
		#verbose
		if(self.verbose): print('Specular RE created')
		
		
	
	#createSubsurfaceRE
	def createSubsurfaceRE(self):
		
		#create subsurfaceRE
		subsurfaceRE = self.createRenderElement('FastSSS2Channel')
		pm.rename(subsurfaceRE, '{0}Subsurface'.format(vrayGlobals.PREFIX))
		
		#SetAttrs on subsurfaceRE
		pm.setAttr(subsurfaceRE.vray_name_sss, '{0}Subsurface'.format(vrayGlobals.PREFIX))
		
		#verbose
		if(self.verbose): print('SSS RE created')
		
		
		
	
	
	
	
	
	
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
		
	
	
	#vrayLoaded
	def vrayLoaded(self):
		#Get list of all loaded plugIns
		plugInList = pm.pluginInfo( query=True, listPlugins=True )
		
		#Return true if loaded else setStatus and return false
		if('vrayformaya' in plugInList):
			return True
		
		return False
	
	
	
	
	