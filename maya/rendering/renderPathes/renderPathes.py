
"""
renderPathes
==========================================

Automatic setup of the correct rendering pathes for images according
to Pipeline standards. It is ment to work with VRay for Maya exclusively.
This is a very simple module, it basically only determines where renderings
will go to.

-----------------------

Usage
-----

::
	
	from helga.maya.rendering.renderPathes import renderPathes
	reload(renderPathes)

	#Create instance
	renderPathesInstance = renderPathes.RenderPathes()
	#set render pathes for final lighting
	renderPathesInstance.setPathLighting()
	#set render pathes for testing
	renderPathesInstance.setPathTesting()

-----------------------
"""



#Import
#----------------------------------------------------
import os
import sys
#maya
import pymel.core as pm
import maya.cmds as cmds







#Globals
#----------------------------------------------------




#RenderPathes Class
#----------------------------------------------------

class RenderPathes():
	
	
	
	#Constructor
	def __init__(self):
		
		#Instance Vars
		#----------------------------------------------------
		
		#Debug
		self.verbose = True
		
			
	
	
	
	
	
	
	
	
	
	#Toplevel Methods
	#----------------------------------------------------
	
	
	
	#setPathLighting
	def setPathLighting(self):
		"""
		Render path for images. The output here should be copied and used by compositing.
		"""
		
		
		#Check if vray is loaded
		
		#exit if vray for maya plugin is not loaded
		if not(self.vrayLoaded()):
			if(self.verbose): print('Vray Plugin not loaded')
			return None
			
		#exit if vray rendersettings node doesnt exist
		if not(self.vrayRenderSettingsNode()): 
			if(self.verbose): print('Vray Rendersettings node not found')
			return None
			
		
		
		
		#Build Path
		#----------------------------------------------------
		
		
		#Assemble Render Path
		renderPath = r'lighting/<Scene>/<Layer>/<Scene>_<Layer>_'
				
		
		
		
		#Set Path
		#----------------------------------------------------
		
		#Get Vray rendersettings node
		vrayRenderSettingsNode = self.vrayRenderSettingsNode()
		
		pm.setAttr(vrayRenderSettingsNode.fileNamePrefix, renderPath)
	
	
		#success msg
		if(self.verbose): print('Successfully set lighting renderpath')
	
	
	
	
	
	
	
	#setPathTesting
	def setPathTesting(self):
		"""
		Render path for testing images. The output here is purely for your own testing
		and could be deleted anytime. If you want to keep it, then copy it to your rnd folder.
		"""
		
		
		#Check if vray is loaded
		
		#exit if vray for maya plugin is not loaded
		if not(self.vrayLoaded()):
			if(self.verbose): print('Vray Plugin not loaded')
			return None
			
		#exit if vray rendersettings node doesnt exist
		if not(self.vrayRenderSettingsNode()): 
			if(self.verbose): print('Vray Rendersettings node not found')
			return None
			
		
		
		
		#Build Path
		#----------------------------------------------------
		
		#get Current user
		currentUser = os.environ.get('USERNAME')
		
		#Assemble Render Path
		renderPath = r'testing/' +currentUser +r'/<Scene>/<Layer>/<Scene>_<Layer>_'
		
		
		#Set Path
		#----------------------------------------------------
		
		#Get Vray rendersettings node
		vrayRenderSettingsNode = self.vrayRenderSettingsNode()
		
		pm.setAttr(vrayRenderSettingsNode.fileNamePrefix, renderPath)
	
	
		#success msg
		if(self.verbose): print('Successfully set testing renderpath')
		
		
	
	
	
	
	
	#Methods
	#----------------------------------------------------
	
	
	
	
	
	
	
	
	
	#Shared Methods
	#----------------------------------------------------
	
	
	
	#vrayLoaded
	def vrayLoaded(self):
		"""
		Check if the VRay for Maya Plugin is loaded.
		"""

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
	
	
	
	
	
	
	
	
#Testing
#----------------------------------------------------
#----------------------------------------------------

if (__name__ is '__main__'):
	from rugbyBugs.maya.rbRenderPathes import rbRenderPathes

	#Reload if true
	doReload = True
	if(doReload): reload(rbRenderPathes)

	#Create Instance
	rbRenderPathesInstance = rbRenderPathes.RbRenderPathes()

	#set final path
	#rbRenderPathesInstance.setPathLighting()
	rbRenderPathesInstance.setPathTesting()

