

"""
shuffleLightRE
==========================================

Internal module that reconstructs light render elements.

.. important::
	
	This module is internal. Access its functionality from :mod:`helga.nuke.reconstruction.renderReconstructVRay.renderReconstruct`

-----------------------
"""



#Imports
#------------------------------------------------------------------
import nuke
import nukescripts


doReload = True

#reconstruct_globals
import reconstruct_globals
if(doReload): reload(reconstruct_globals)





#ShuffleLightRE class
#------------------------------------------------------------------

class ShuffleLightRE():
	
	#Constructor
	def __init__(self):
		
		
		#Instance Vars
		#------------------------------------------------------------------
		self.verbose = True
		self.backdropColorDirectLight = [1,0.86,0.14]
		self.backdropColorGi = [1,0.91,0.44]
		self.backdropColorSelfIllum = [1,0.93,0.61]
	

	
	
	
	#Methods
	#------------------------------------------------------------------
	
	#reconstructLightRenderElements (return final light merge node)
	def reconstructLightRenderElements(self, node):
		
		#check if node is read node
		if not(self.nodetypeMatches(node, 'Read')):
			print('%s is not of type Read' %(node.name()))
			return None
				
		#check if rbDiffuse channel exists
		if not(self.getLayers(node, '{0}Diffuse'.format(reconstruct_globals.PREFIX))):
			print('No diffuse channel in %s nodes file' %(node.name()))
			return None
			
			
			
		#get layerList for rbLs
		layerListLs = self.getLayers(node, '{0}Ls'.format(reconstruct_globals.PREFIX))
			
		#get rbGi
		layerListGi = self.getLayers(node, '{0}Gi'.format(reconstruct_globals.PREFIX))
			
		#Merge GI and LightSelects
		layerListLight = layerListLs + layerListGi
			
			
		#check if lightLayers exist
		if(len(layerListLight) > 0):
		
			#iterate lightLayers and reconstruct each
			outputDotList = []
			for layer in layerListLight:
				#if layer == rbGi reconstruct with gi flag = True
				if(layer == '{0}Gi'.format(reconstruct_globals.PREFIX)):
					outputDotList.append(self.reconstructLightRE(node, layer, gi = True))
				#else start normal (gi flag = False)
				else: outputDotList.append(self.reconstructLightRE(node, layer))
					
					
				
				
			#Check if rbSelfIllum RE exists and if so create nodes
			if(self.getLayers(node, '{0}SelfIllum'.format(reconstruct_globals.PREFIX))):
				outputDotList.append(self.shuffleRE(node, '{0}SelfIllum'.format(reconstruct_globals.PREFIX), frameBuffer = True))
				
				
				
			#addLightContributions
			addLightContributions =  nuke.nodes.Merge2()
			addLightContributions.knob('operation').setValue('plus')
			addLightContributions.knob('Achannels').setValue('rgb')
				
			#position add node under last reconstructed element
			posX = outputDotList[-1].xpos()
			posY = outputDotList[-1].ypos()
			offsetY = 60
			posY = posY + offsetY
			addLightContributions.setXYpos(posX, posY)
				
				
			#for length of outputDotList connect to merge
			for index in range(0,len(outputDotList)):
				#if index is not 0 or 1 increment index for input pipe
				if(index == 0 or index == 1):addLightContributions.setInput(index, outputDotList[index])
				else:addLightContributions.setInput(index+1, outputDotList[index])
				
				
			
			return addLightContributions
			
		#return None if no layer found
		return None
	
	
	
	#reconstructLightRE (return outputDot node)
	def reconstructLightRE(self, node, layer, gi = False):
		
		#Create, set and connect nodes
		
		#create nodesList for backdrop bbox computation
		nodesList = []
		
		#shuffleLight
		shuffleLight = nuke.nodes.Shuffle(label = layer +'_rbg', inputs = [node])
		shuffleLight['in'].setValue( layer )
		shuffleLight['in2'].setValue( 'rgba' )
		shuffleLight['alpha'].setValue( 'alpha2' )
		shuffleLight['postage_stamp'].setValue( True )
		shuffleLight['hide_input'].setValue(True)
		nodesList.append(shuffleLight)
		
		#unpremultShuffleLight
		unpremultShuffleLight = nuke.nodes.Unpremult()
		unpremultShuffleLight.setInput(0,shuffleLight)
		nodesList.append(unpremultShuffleLight)
		
		
		#shuffleDiffuse
		shuffleDiffuse = nuke.nodes.Shuffle(label = '{0}Diffuse_rgb'.format(reconstruct_globals.PREFIX), inputs = [node])
		shuffleDiffuse['in'].setValue( '{0}Diffuse'.format(reconstruct_globals.PREFIX) )
		shuffleDiffuse['in2'].setValue( 'rgba' )
		shuffleDiffuse['alpha'].setValue( 'alpha2' )
		shuffleDiffuse['postage_stamp'].setValue( True )
		shuffleDiffuse['hide_input'].setValue(True)
		nodesList.append(shuffleDiffuse)
		
		#unpremultShuffleDiffuse
		unpremultShuffleDiffuse = nuke.nodes.Unpremult()
		unpremultShuffleDiffuse.setInput(0,shuffleDiffuse)
		nodesList.append(unpremultShuffleDiffuse)
		
		
		
		#divideLightByDiffuse
		divideLightByDiffuse = nuke.nodes.Merge2()
		divideLightByDiffuse.knob('operation').setValue('divide')
		divideLightByDiffuse.setInput(0, unpremultShuffleDiffuse)
		divideLightByDiffuse.setInput(1, unpremultShuffleLight)
		nodesList.append(divideLightByDiffuse)
		
		
		
		#gradeRawLight
		gradeRawLight = nuke.nodes.Grade()
		gradeRawLight.setInput(0,divideLightByDiffuse)
		nodesList.append(gradeRawLight)
		
		
		#colorcorrectRawLight
		colorcorrectRawLight = nuke.nodes.ColorCorrect()
		colorcorrectRawLight.setInput(0,gradeRawLight)
		nodesList.append(colorcorrectRawLight)
		
		
		#multiplyRawLightWithDiffuse
		multiplyRawLightWithDiffuse = nuke.nodes.Merge2()
		multiplyRawLightWithDiffuse.knob('operation').setValue('multiply')
		multiplyRawLightWithDiffuse.setInput(0, colorcorrectRawLight)
		multiplyRawLightWithDiffuse.setInput(1, unpremultShuffleDiffuse)
		nodesList.append(multiplyRawLightWithDiffuse)
		
		
		
		
		
		#ambOcc (if gi flag is True)
		#------------------------------------------------------------------
		
		#set bool for outputDot connection test = False
		connectAmbOcc = False
		
		if(gi == True):
			
			#get rbEtAmbOcc
			layerListAmbOcc = self.getLayers(node, '{0}EtAmbOcc'.format(reconstruct_globals.PREFIX))
			
			#only execute if amb occ layer exists
			if(layerListAmbOcc):
				
				#get ambocc layer
				layerAmbOcc = layerListAmbOcc[0]
				
				
				#shuffleAmbOcc
				shuffleAmbOcc = nuke.nodes.Shuffle(label = layerAmbOcc +'_rbg', inputs = [node])
				shuffleAmbOcc['in'].setValue( layerAmbOcc )
				shuffleAmbOcc['in2'].setValue( 'rgba' )
				shuffleAmbOcc['alpha'].setValue( 'alpha2' )
				shuffleAmbOcc['postage_stamp'].setValue( True )
				shuffleAmbOcc['hide_input'].setValue(True)
				nodesList.append(shuffleAmbOcc)
				
				
				#unpremultShuffleAmbOcc
				unpremultShuffleAmbOcc = nuke.nodes.Unpremult()
				unpremultShuffleAmbOcc.setInput(0,shuffleAmbOcc)
				nodesList.append(unpremultShuffleAmbOcc)
				
				
				#gradeAmbOcc
				gradeAmbOcc = nuke.nodes.Grade()
				gradeAmbOcc.setInput(0,unpremultShuffleAmbOcc)
				nodesList.append(gradeAmbOcc)
				
				
				#colorcorrectAmbOcc
				colorcorrectAmbOcc = nuke.nodes.ColorCorrect()
				colorcorrectAmbOcc.setInput(0,gradeAmbOcc)
				nodesList.append(colorcorrectAmbOcc)
				
				
				#clampAmbOcc
				clampAmbOcc = nuke.nodes.Clamp()
				clampAmbOcc.setInput(0,colorcorrectAmbOcc)
				nodesList.append(clampAmbOcc)
				
				
				#multiplyGiWithAmbOcc
				multiplyGiWithAmbOcc = nuke.nodes.Merge2()
				multiplyGiWithAmbOcc.knob('operation').setValue('multiply')
				multiplyGiWithAmbOcc.setInput(0, multiplyRawLightWithDiffuse)
				multiplyGiWithAmbOcc.setInput(1, clampAmbOcc)
				nodesList.append(multiplyGiWithAmbOcc)
				
				#set bool for outputDot connection test = True
				connectAmbOcc = True
			
			#else, no ambOcc layer exists
			else: print('No {0}EtAmbOcc layer exists'.format(reconstruct_globals.PREFIX))
				
		
		
		
		
		#outputDot
		outputDot = nuke.nodes.Dot(label = layer +'_rgb_OUT')
		#check if multiplyGiWithAmbOcc exists and based on that connect outputDot
		if(connectAmbOcc):
			outputDot.setInput(0, multiplyGiWithAmbOcc)
		else:
			outputDot.setInput(0, multiplyRawLightWithDiffuse)
		nodesList.append(outputDot)
		
		
		#create backdrop
		backdrop = self.createBackdrop(nodesList, self.rgbToHexString(self.backdropColorDirectLight))
		#recolor if ambOcc = True
		if(connectAmbOcc):backdrop.knob('tile_color').setValue(self.rgbToHexString(self.backdropColorGi))
		backdrop.knob('label').setValue(node.name() +'_' +layer +'RE')
		backdrop.knob('note_font_size').setValue(20)
		
		
		return outputDot
		
		
		
	
	
	#Shared Methods
	#------------------------------------------------------------------
	
	
	#shuffleRE
	def shuffleRE(self, node, layer, frameBuffer = False):
		
		nodesList = []
		
		#shuffleRE
		shuffleRE = nuke.nodes.Shuffle(label = layer +'_rbg', inputs = [node])
		shuffleRE['in'].setValue( layer )
		shuffleRE['in2'].setValue( 'rgba' )
		shuffleRE['alpha'].setValue( 'alpha2' )
		shuffleRE['postage_stamp'].setValue( True )
		shuffleRE['hide_input'].setValue(True)
		nodesList.append(shuffleRE)
		
		#If layer is framebuffer contribution, append unpremult, grade, colorcorrect and 
		if(frameBuffer):
			
			#unpremultShuffleRE
			unpremultShuffleRE = nuke.nodes.Unpremult()
			unpremultShuffleRE.setInput(0,shuffleRE)
			nodesList.append(unpremultShuffleRE)
			
			
			#gradeRE
			gradeRE = nuke.nodes.Grade()
			gradeRE.setInput(0,unpremultShuffleRE)
			nodesList.append(gradeRE)
		
		
			#colorcorrectRE
			colorcorrectRE = nuke.nodes.ColorCorrect()
			colorcorrectRE.setInput(0,gradeRE)
			nodesList.append(colorcorrectRE)
			
			#outputDot
			outputDot = nuke.nodes.Dot(label = layer +'_rgb_OUT')
			outputDot.setInput(0, colorcorrectRE)
			nodesList.append(colorcorrectRE)
			
			
			#create backdrop
			backdrop = self.createBackdrop(nodesList, self.rgbToHexString(self.backdropColorSelfIllum))
			backdrop.knob('label').setValue(node.name() +'_' +layer +'RE')
			backdrop.knob('note_font_size').setValue(20)
			
			return outputDot
			
		
		return shuffleRE
		
	
	
	
	#nodetypeMatches
	def nodetypeMatches(self, node, nodetype):
		
		if(node.Class() == nodetype): return True
		return False
		
	
	
	#getLayers
	def getLayers(self, node, prefix = False):
		
		#Get channelsList
		channelsList = node.channels()
		
		#iterate over channelslist, split name and append layer
		layerList = []
		for channel in channelsList:
			layer = channel.split('.')[0]
			layerList.append(layer)
			
		#remove duplicates
		layerList = list(set(layerList))
		
		
		#If prefix is set, iterate again to return all layers starting with prefix
		if(prefix):
			layerListPrefix = []
			prefixLength = len(prefix)
			for layer in layerList:
				if(layer[0:prefixLength] == prefix): layerListPrefix.append(layer)
				
			return layerListPrefix
		
		return layerList
		
	
	
	#createBackdrop
	def createBackdrop(self, nodesList, hexColor):
		
		#deselect all
		self.deselectAll()
		
		#Select nodesList in viewport
		for node in nodesList:
			node.setSelected(True)
		
		
		#nukescripts autobackdrop
		backdrop = nukescripts.autoBackdrop()
		backdrop['tile_color'].setValue(hexColor)
		
		return backdrop
		
		
	
	#deselectAll
	def deselectAll(self):
		#Select All to invert the selection XD
		nuke.selectAll()
		nuke.invertSelection()

	
	
	#rgbToHexString
	def rgbToHexString(self, colorList = [0,0,0]):
		
		#getColors
		r = colorList[0]
		g = colorList[1]
		b = colorList[2]
		
		#get hexColor
		hexColor = int('%02x%02x%02x%02x' % (r*255,g*255,b*255,1),16)
		
		return hexColor	
		

	
	
	
	
	
	
	
	