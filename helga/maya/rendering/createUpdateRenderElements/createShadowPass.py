
"""
createShadowPass
==========================================

Automatic setup of the following VRay Render Elements in Maya.
They are also the names of the channels in the multichannel exr.
You can call this function as often as you want. It will not duplicate 
existing elements, only add missing ones.

The following elements are created:
	
	* RawShadow
	* Shadow

-----------------------

Usage
-----

::
	
	from helga.maya.rendering.createUpdateRenderElements import createShadowPass
	reload(createShadowPass)

	#Create instance
	createShadowPassInstance = createShadowPass.CreateShadowPass()
	#Create/Update shadow passes
	createShadowPassInstance.createShadowPass()

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





#CreateShadowPass class
#------------------------------------------------------------------

class CreateShadowPass():
	
	#Constructor / Main Procedure
	def __init__(self):
		
		#Instance Vars
		#------------------------------------------------------------------
		self.verbose = True
		
		
	
	#Top Level Methods
	#------------------------------------------------------------------
	
	#createShadowPass
	def createShadowPass(self):
		"""
		Function to create/update shadow passes (see above for AOV types).
		"""
		
		
		#Check if Vray Loaded, else set Status and return
		if not(self.vrayLoaded()):
			openMaya.MGlobal.displayWarning('Vray for Maya Plugin not loaded')
			return None
		
		
		try:
			
			#rawShadowRE
			attrName = 'vray_name_rawshadow'
			attrValue = '{0}RawShadow'.format(vrayGlobals.PREFIX)
			if not(self.REWithAttrAndValueExists(attrName, attrValue)): self.createRawShadowRE()
			
			#shadowRE
			attrName = 'vray_name_shadow'
			attrValue = '{0}Shadow'.format(vrayGlobals.PREFIX)
			if not(self.REWithAttrAndValueExists(attrName, attrValue)): self.createShadowRE()
			
			
			#msg
			openMaya.MGlobal.displayInfo('Shadow Passes created succesfully')

		except:
			#msg
			openMaya.MGlobal.displayWarning('Error creating shadow passes')
	
	
	
	
	
	
	
	#Methods
	#------------------------------------------------------------------
	
	
	#createRawShadowRE
	def createRawShadowRE(self):
		
		#create raw shadow RE
		rawShadowRE = self.createRenderElement('rawShadowChannel')
		pm.rename(rawShadowRE, '{0}RawShadow'.format(vrayGlobals.PREFIX))
		
		#SetAttrs on rawShadowRE
		pm.setAttr(rawShadowRE.vray_name_rawshadow, '{0}RawShadow'.format(vrayGlobals.PREFIX))
		
		#verbose
		if(self.verbose): print('Raw Shadow RE created')
		
		
		
	#createShadowRE
	def createShadowRE(self):
		
		#create shadow RE
		shadowRE = self.createRenderElement('shadowChannel')
		pm.rename(shadowRE, '{0}Shadow'.format(vrayGlobals.PREFIX))
		
		#SetAttrs on shadowRE
		pm.setAttr(shadowRE.vray_name_shadow, '{0}Shadow'.format(vrayGlobals.PREFIX))
		
		#verbose
		if(self.verbose): print('Shadow RE created')
		
		
	
	
	
	
	
	
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
	
	
	
	
	