

#shuffleFramebufferRE Module
#------------------------------------------------------------------

'''
Description:
Reconstructs the framebuffer render elements (spec, refl, refr.) of one or several read files according to our pipeline standards
'''

'''
ToDo:

'''



#Imports
#------------------------------------------------------------------
import nuke
import nukescripts


doReload = True

#reconstruct_globals
import reconstruct_globals
if(doReload): reload(reconstruct_globals)



#ShuffleFramebufferRE class
#------------------------------------------------------------------

class ShuffleFramebufferRE():
	
	#Constructor
	def __init__(self):
		
		
		#Instance Vars
		#------------------------------------------------------------------
		self.verbose = True
		self.backdropColorFramebuffer = [0.26,0.54,0.74]
	

	
	
	
	#Toplevel Methods
	#------------------------------------------------------------------
	
	#reconstructFramebufferRenderElements
	def reconstructFramebufferRenderElements(self, node):
		
		
		#check if node is read node
		if not(self.nodetypeMatches(node, 'Read')):
			print('%s is not of type Read' %(node.name()))
			return False
			
			
			
			
		#Shuffle FramebufferContributions
		#------------------------------------------------------------------
			
		outputDotList = []
			
		#rbReflection
		if(self.getLayers(node, '{0}Reflection'.format(reconstruct_globals.PREFIX))):
			outputDotList.append(self.shuffleRE(node, '{0}Reflection'.format(reconstruct_globals.PREFIX), frameBuffer = True))
			
		#rbRefraction
		if(self.getLayers(node, '{0}Refraction'.format(reconstruct_globals.PREFIX))):
			outputDotList.append(self.shuffleRE(node, '{0}Refraction'.format(reconstruct_globals.PREFIX), frameBuffer = True))
			
		#rbSpecular
		if(self.getLayers(node, '{0}Specular'.format(reconstruct_globals.PREFIX))):
			outputDotList.append(self.shuffleRE(node, '{0}Specular'.format(reconstruct_globals.PREFIX), frameBuffer = True))
		
		#rbSubsurface
		if(self.getLayers(node, '{0}Subsurface'.format(reconstruct_globals.PREFIX))):
			outputDotList.append(self.shuffleRE(node, '{0}Subsurface'.format(reconstruct_globals.PREFIX), frameBuffer = True))
			
			
			
			
			
		#Add all Shuffle FramebufferContributions
		#------------------------------------------------------------------
		
		#check if outputDotList contains more than 0
		if(len(outputDotList) > 0):
		
			#addFramebufferContributions
			addFramebufferContributions =  nuke.nodes.Merge2()
			addFramebufferContributions.knob('operation').setValue('plus')
			addFramebufferContributions.knob('Achannels').setValue('rgb')
				
			#position add node under last reconstructed element
			posX = outputDotList[-1].xpos()
			posY = outputDotList[-1].ypos()
			offsetY = 60
			posY = posY + offsetY
			addFramebufferContributions.setXYpos(posX, posY)
				
				
			#for length of outputDotList connect to merge
			for index in range(0,len(outputDotList)):
				#if index is not 0 or 1 increment index for input pipe
				if(index == 0 or index == 1):addFramebufferContributions.setInput(index, outputDotList[index])
				else:addFramebufferContributions.setInput(index+1, outputDotList[index])
				
			
			#retun final merge node
			return addFramebufferContributions
			
		#return None if no layers found
		return None
	
	
	
	
	#Methods
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
			backdrop = self.createBackdrop(nodesList, self.rgbToHexString(self.backdropColorFramebuffer))
			backdrop.knob('label').setValue(node.name() +'_' +layer +'RE')
			backdrop.knob('note_font_size').setValue(20)
			
			return outputDot
			
		
		return shuffleRE
		
		
		
	
	
	#Shared Methods
	#------------------------------------------------------------------
	
	
	
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

	
	
	
	
	
	
	
	