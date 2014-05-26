

"""
renderReconstruct
==========================================

Automatic reconstruction of multichannel exrs that have been created according
to our pipeline standards. This has happened most probably with a module from 
:mod:`helga.maya.rendering.createUpdateRenderElements`.


The following elements can be reconstructed separately:
	
	* Light
	* Data
	* Framebuffer
	* Multi Mattes
	* Shadow

Of course it is also possible to recreate them alltogether.

.. note::
	
	The final result of the reconstruction might differ a little from the
	original rendering, since Ambient Occlusion is rendered as an Extra Tex
	pass and multiplied with the GI on reconstruction.

-----------------------

.. Rubric:: Usage

::
	
	from helga.nuke.reconstruction.renderReconstructVRay import renderReconstruct
	reload(renderReconstruct)

	#Create instance
	renderReconstructInstance = renderReconstruct.RenderReconstruct()
	
	#------------------------------
	#Select some Nuke Read nodes
	#------------------------------

	#Reconstruct all elements
	renderReconstructInstance.reconstructAll()

	#Reconstruct light only
	renderReconstructInstance.reconstructLightREs()

	#Reconstruct data only
	renderReconstructInstance.reconstructDataREs()

	#Reconstruct framebuffer only
	renderReconstructInstance.reconstructFramebufferREs()

	#Reconstruct multi mattes only
	renderReconstructInstance.reconstructMultiMatteREs()

	#Reconstruct shadow only
	renderReconstructInstance.reconstructShadowREs()

-----------------------
"""


#Imports
#------------------------------------------------------------------
import sys
import os
import nuke



doReload = True

#shuffleLightRE
import lib.shuffleLightRE as shuffleLightRE
if(doReload): reload(shuffleLightRE)

#shuffleDataRE
import lib.shuffleDataRE as shuffleDataRE
if(doReload): reload(shuffleDataRE)

#shuffleFramebufferRE
import lib.shuffleFramebufferRE as shuffleFramebufferRE
if(doReload): reload(shuffleFramebufferRE)

#shuffleMmRE
import lib.shuffleMmRE as shuffleMmRE
if(doReload): reload(shuffleMmRE)

#shuffleShadowRE
import lib.shuffleShadowRE as shuffleShadowRE
if(doReload): reload(shuffleShadowRE)




#RenderReconstruct class
#------------------------------------------------------------------

class RenderReconstruct():
	
	
	#Constructor
	def __init__(self):
		
		#Instance Vars
		#------------------------------------------------------------------
		self.verbose = True
		
	
	
	
	
	#Methods
	#------------------------------------------------------------------
	
	
	
	
	#reconstructLightREs
	def reconstructLightREs(self):
		"""
		Reconstruct light render elements (AOVs) for the selected Read nodes.
		"""
		
		try:
		
			#get selected nodes
			nodesList = nuke.selectedNodes()
			
			#check if node selected
			if not(len(nodesList)):
				print('No nodes selected')
				return False
			
			#iterate selected nodes and rebuild all passes
			for node in nodesList:
				#reconstruct
				shuffleLightRE.ShuffleLightRE().reconstructLightRenderElements(node)
				
			#status
			print('Light Elements successfully rebuilt')
		
		except:
			#status
			print('Error rebuilding Light Elements')
		
	
	
	
	
	#reconstructDataREs
	def reconstructDataREs(self):
		"""
		Reconstruct data render elements (AOVs) for the selected Read nodes.
		"""
		
		try:
			#get selected nodes
			nodesList = nuke.selectedNodes()
			
			#check if node selected
			if not(len(nodesList)):
				print('No nodes selected')
				return False
			
			#iterate selected nodes and rebuild all passes
			for node in nodesList:
				#reconstruct
				shuffleDataRE.ShuffleDataRE().reconstructDataRenderElements(node)
				
			#status
			print('Data Elements successfully rebuilt')
		
		except:
			#status
			print('Error rebuilding Data Elements')
	
	
	
	#reconstructFramebufferREs
	def reconstructFramebufferREs(self):
		"""
		Reconstruct framebuffer render elements (AOVs) for the selected Read nodes.
		"""
		
		try:
			#get selected nodes
			nodesList = nuke.selectedNodes()
			
			#check if node selected
			if not(len(nodesList)):
				print('No nodes selected')
				return False
			
			#iterate selected nodes and rebuild all passes
			for node in nodesList:
				#reconstruct
				shuffleFramebufferRE.ShuffleFramebufferRE().reconstructFramebufferRenderElements(node)
			
			#status
			print('Framebuffer Elements successfully rebuilt')
		
		except:
			#status
			print('Error rebuilding Framebuffer Elements')
	
	
	
	
	#reconstructMultiMatteREs
	def reconstructMultiMatteREs(self):
		"""
		Reconstruct multi matte render elements (AOVs) for the selected Read nodes.
		"""
		
		try:
			#get selected nodes
			nodesList = nuke.selectedNodes()
			
			#check if node selected
			if not(len(nodesList)):
				print('No nodes selected')
				return False
			
			#iterate selected nodes and rebuild all passes
			for node in nodesList:
				#reconstruct
				shuffleMmRE.ShuffleMmRE().reconstructMultiMatteRenderElements(node)
				
			#status
			print('Multi Mattes successfully rebuilt')
		
		except:
			#status
			print('Error rebuilding Multi Matte Elements')
			
			
			
	
	#reconstructShadowREs
	def reconstructShadowREs(self):
		"""
		Reconstruct shadow render elements (AOVs) for the selected Read nodes.
		"""
		
		try:
			#get selected nodes
			nodesList = nuke.selectedNodes()
			
			#check if node selected
			if not(len(nodesList)):
				print('No nodes selected')
				return False
			
			#iterate selected nodes and rebuild all passes
			for node in nodesList:
				#reconstruct
				shuffleShadowRE.ShuffleShadowRE().reconstructShadowRenderElements(node)
				
			#status
			print('Shadow Elements successfully rebuilt')
		
		except:
			#status
			print('Error rebuilding Shadow Elements')
		
	
	
	
	
	#reconstructAll
	def reconstructAll(self):
		"""
		Reconstruct all render elements (AOVs) for the selected Read nodes.
		The elements are added together to reconstruct the final render.
		The rendering might differ a little from the original since Ambient
		Occlusion is multiplied with the GI.
		"""
		
		#get selected nodes
		nodesList = nuke.selectedNodes()
		
		#check if node selected
		if not(len(nodesList)):
			print('No nodes selected')
			return False
		
		
		#outputDotList
		outputDotList = []
		
		#iterate selected nodes and rebuild all passes
		for node in nodesList:
		
			
			#check if node is read node
			if not(self.nodetypeMatches(node, 'Read')):
				print('%s is not of type Read' %(node.name()))
				continue
			
			
			#mergeList
			mergeNodeList = []
			
			
			#recreateLightREs
			mergeNodeList.append(shuffleLightRE.ShuffleLightRE().reconstructLightRenderElements(node))
			
			#recreateFramebufferREs
			mergeNodeList.append(shuffleFramebufferRE.ShuffleFramebufferRE().reconstructFramebufferRenderElements(node))
			
			#recreateDataREs
			shuffleDataRE.ShuffleDataRE().reconstructDataRenderElements(node)
			
			#recreateMultiMattes
			shuffleMmRE.ShuffleMmRE().reconstructMultiMatteRenderElements(node)
			
			#recreateShadowREs
			shuffleShadowRE.ShuffleShadowRE().reconstructShadowRenderElements(node)
			
			
			#trim mergeNodeList from None entries
			mergeNodeListTemp = []
			for item in mergeNodeList:
				if(item):mergeNodeListTemp.append(item)
				
			mergeNodeList = mergeNodeListTemp
			
		
			#Add all Passes of single layer (except data)
			#------------------------------------------------------------------
			
			#check if node contains different contributions to merge (light or framebuffer)
			if(len(mergeNodeList) > 0):
			
				#addFramebufferContributions
				addFramebufferContributionsSingleLayer =  nuke.nodes.Merge2()
				addFramebufferContributionsSingleLayer.knob('operation').setValue('plus')
				addFramebufferContributionsSingleLayer.knob('Achannels').setValue('rgb')
				
				#position add node under last reconstructed element merge node
				posX = mergeNodeList[-1].xpos()
				posY = mergeNodeList[-1].ypos()
				offsetY = 60
				posY = posY + offsetY
				addFramebufferContributionsSingleLayer.setXYpos(posX, posY)
				
				#iterate through mergeList and connect to addFramebufferContributionsSingleLayer
				for index in range(0,len(mergeNodeList)):
					#if index is not 0 or 1 increment index for input pipe
					if(index == 0 or index == 1):addFramebufferContributionsSingleLayer.setInput(index, mergeNodeList[index])
					else:addFramebufferContributionsSingleLayer.setInput(index+1, mergeNodeList[index])
				
				
				#premultCompleteLayer
				premultCompleteLayer = nuke.nodes.Premult()
				premultCompleteLayer.setInput(0,addFramebufferContributionsSingleLayer)
				
				
				
				#outputDot
				outputDot = nuke.nodes.Dot(label = node.name() +'_rgb_OUT')
				outputDot.setInput(0, premultCompleteLayer)
				outputDotList.append(outputDot)
			
			
		
		
		#Add all Layers if more than on read was selected
		#------------------------------------------------------------------
		
		#check if outputDotList contains more than 1
		if(len(outputDotList) > 1):
			
			#addFramebufferContributionsAllLayer
			addFramebufferContributionsAllLayer =  nuke.nodes.Merge2()
			addFramebufferContributionsAllLayer.knob('operation').setValue('plus')
			addFramebufferContributionsAllLayer.knob('Achannels').setValue('rgb')
			
			#position add node under last reconstructed element merge node
			posX = outputDotList[-1].xpos()
			posY = outputDotList[-1].ypos()
			offsetY = 60
			posY = posY + offsetY
			addFramebufferContributionsAllLayer.setXYpos(posX, posY)
			
			#iterate through mergeList and connect to addFramebufferContributionsSingleLayer
			for index in range(0,len(outputDotList)):
				#if index is not 0 or 1 increment index for input pipe
				if(index == 0 or index == 1):addFramebufferContributionsAllLayer.setInput(index, outputDotList[index])
				else:addFramebufferContributionsAllLayer.setInput(index+1, outputDotList[index])
			
			
			#status
			print('Successfully Reconstructed RenderElements')
			
				
			return addFramebufferContributionsAllLayer
		
		#status
		print('Successfully Reconstructed RenderElements')
		
		return outputDotList
		
	
	
	
	
	#Shared Methods
	#------------------------------------------------------------------
	
	#nodetypeMatches
	def nodetypeMatches(self, node, nodetype):
		
		if(node.Class() == nodetype): return True
		return False
		

		


#Test execute
#------------------------------------------------------------------
#------------------------------------------------------------------

if(__name__ == '__main__'):

	from rugbyBugs.nuke.rbRenderReconstruct import rbRenderReconstruct
	reload(rbRenderReconstruct)
	rbRenderReconstructInstance = rbRenderReconstruct.RbRenderReconstruct()

	#shuffle light passes for selected Nodes

	#rbRenderReconstructInstance.reconstructLightREs()
	#rbRenderReconstructInstance.reconstructFramebufferREs()
	#rbRenderReconstructInstance.reconstructDataREs()


	rbRenderReconstructInstance.reconstructAll()


		
		

		