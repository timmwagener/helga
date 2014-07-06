
"""
createUpdateLightRenderElements
==========================================

Automatic setup of the following VRay Render Elements in Maya.
They are also the names of the channels in the multichannel exr.
You can call this function as often as you want. It will not duplicate 
existing elements, only add missing ones.
The light is split into light select elements and GI. To use these passes in
Nuke with the :mod:`helga.nuke.reconstruction.renderReconstruct` module you
need a diffuse pass from :mod:`helga.maya.rendering.createUpdateRenderElements.createFrameBufferContributions`.

The following elements are created:
	
	* Gi
	* Lighting
	* SelfIllum
	* Light Selects for each light where possible

-----------------------

Usage
-----

::
	
	from helga.maya.rendering.createUpdateRenderElements import createUpdateLightRenderElements
	reload(createUpdateLightRenderElements)

	#Create instance
	createUpdateLightRenderElementsInstance = createUpdateLightRenderElements.CreateUpdateLightRenderElements()
	#Create/Update shadow passes
	createUpdateLightRenderElementsInstance.createUpdateLightRenderElements()

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





#CreateUpdateLightRenderElements class
#------------------------------------------------------------------

class CreateUpdateLightRenderElements():
	
	#Constructor / Main Procedure
	def __init__(self):
		
		#Instance Vars
		#------------------------------------------------------------------
		self.verbose = True
		
		
	
	#Top Level Methods
	#------------------------------------------------------------------
	
	
	#createUpdateLightRenderElements
	def createUpdateLightRenderElements(self):
		"""
		Function to create/update light render elements (see above for AOV types).
		"""
		
		
		
		#Check if Vray Loaded, else set Status and return
		if not(self.vrayLoaded()):
			openMaya.MGlobal.displayWarning('Vray for Maya Plugin not loaded')
			return None
		
		
		
		try:
			#GiRE
			attrName = 'vray_name_gi'
			attrValue = '{0}Gi'.format(vrayGlobals.PREFIX)
			if not(self.REWithAttrAndValueExists(attrName, attrValue)): self.createGiRE()
			
			
			#lightingRE
			attrName = 'vray_name_lighting'
			attrValue = '{0}Lighting'.format(vrayGlobals.PREFIX)
			if not(self.REWithAttrAndValueExists(attrName, attrValue)): self.createLightingRE()
			
			
			#selfIllumRE
			attrName = 'vray_name_selfIllum'
			attrValue = '{0}SelfIllum'.format(vrayGlobals.PREFIX)
			if not(self.REWithAttrAndValueExists(attrName, attrValue)): self.createSelfIllumRE()
			
			
			
			#createUpdateLSREs
			self.createUpdateLSREs()
			
			
			#msg
			openMaya.MGlobal.displayInfo('Light Passes created succesfully')

		except:
			#msg
			openMaya.MGlobal.displayWarning('Error creating light passes')
	
	
	
	
	
	
	
	#Methods
	#------------------------------------------------------------------
	
	
	#createGiRE
	def createGiRE(self):
		
		#create gi RE
		giRE = self.createRenderElement('giChannel')
		pm.rename(giRE, '{0}Gi'.format(vrayGlobals.PREFIX))
		
		#SetAttrs on giRE
		pm.setAttr(giRE.vray_name_gi, '{0}Gi'.format(vrayGlobals.PREFIX))
		
		#verbose
		if(self.verbose): print('Gi RE created')
		
		
		
	#createLightingRE
	def createLightingRE(self):
		
		#create lightingRE
		lightingRE = self.createRenderElement('lightingChannel')
		pm.rename(lightingRE, '{0}Lighting'.format(vrayGlobals.PREFIX))
		
		#SetAttrs on lightingRE
		pm.setAttr(lightingRE.vray_name_lighting, '{0}Lighting'.format(vrayGlobals.PREFIX))
		
		#verbose
		if(self.verbose): print('Lighting RE created')
		
		
		
	#createSelfIllumRE
	def createSelfIllumRE(self):
		
		#create selfIllumRE
		selfIllumRE = self.createRenderElement('selfIllumChannel')
		pm.rename(selfIllumRE, '{0}SelfIllum'.format(vrayGlobals.PREFIX))
		
		#SetAttrs on selfIllumRE
		pm.setAttr(selfIllumRE.vray_name_selfIllum, '{0}SelfIllum'.format(vrayGlobals.PREFIX))
		
		#verbose
		if(self.verbose): print('SelfIllum RE created')
		
	
	
	
	#createUpdateLSREs
	def createUpdateLSREs(self):
		
		#delete all existing LS RElements whose name begins with 'rbLs'
		self.deleteAllLsRElementSets()
		if(self.verbose): print('Scene LightSelect RE Sets deleted')
		
		#get list of all lights in the scene
		lightsList = self.getAllSceneLights()
		if(self.verbose): print('Scene Lights List aquired')
		
		#create a Light Select RE for each light
		self.createLSREForEachLight(lightsList)
		if(self.verbose): print('Successfully created Light Select RE for each light')
		
	
	
	
	#deleteAllLsRElements
	def deleteAllLsRElementSets(self):
		
		#Get all LS RE from Scene
		lsReSetsList = self.getRenderElementSetsByPrefix('{0}Ls'.format(vrayGlobals.PREFIX))
		#Delete all LS REs
		if(lsReSetsList): pm.delete(lsReSetsList)
		
	
	
	#getAllSceneLights
	def getAllSceneLights(self):
		
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
		
	
	
	
	#createLSREForEachLight
	def createLSREForEachLight(self, lightsList):
		
		#create lsRESet for each light in lightList and set + connect it
		for lightShape in lightsList:
			
			#get Light Transform
			lightTrans = lightShape.getParent()
			#Create lsRESet
			lsRESet = self.createRenderElement('LightSelectElement')
			#rename lsRESet
			pm.rename(lsRESet, '{0}Ls'.format(vrayGlobals.PREFIX) +lightTrans.name())
			#setChannelName
			pm.setAttr(lsRESet.vray_name_lightselect, '{0}Ls'.format(vrayGlobals.PREFIX) +lightTrans.name())
			#set light type to diffuse
			pm.setAttr(lsRESet.vray_type_lightselect, 2)
			
			
			#connect light with lsRESet
			pm.connectAttr(lightTrans.instObjGroups[0], lsRESet.dagSetMembers[0], f = True)
	
	
	
	
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
		
	
	#getRenderElementsByPrefix
	def getRenderElementSetsByPrefix(self, prefix):
		
		#clear selection
		pm.select(cl = True)
		
		#get list of all REs
		renderElementSetsList = pm.ls(fl = True, typ = 'VRayRenderElementSet')
		
		#if renderElementList < 1 return renderElementList
		if not(renderElementSetsList): return renderElementSetsList
		
		#iterate through renderElementList and append to lsList when name beginning matches prefix
		lsReSetsList = []
		prefixLength = len(prefix)
		for RESet in renderElementSetsList:
			if(RESet.name()[0:prefixLength] == prefix): lsReSetsList.append(RESet)
			
		return lsReSetsList
	
	
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
	
	
	
	
	