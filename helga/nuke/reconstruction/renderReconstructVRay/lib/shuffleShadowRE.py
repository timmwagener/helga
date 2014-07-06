

"""
shuffleShadowRE
==========================================

Internal module that reconstructs shadow render elements.

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





#ShuffleShadowRE class
#------------------------------------------------------------------

class ShuffleShadowRE():
	
	#Constructor
	def __init__(self):
		
		
		#Instance Vars
		#------------------------------------------------------------------
		self.verbose = True
		self.backdropColorData = [0.0,0,0.0]
	

	
	
	
	#Toplevel Methods
	#------------------------------------------------------------------
	
	#reconstructShadowRenderElements
	def reconstructShadowRenderElements(self, node):
		
		#check if node is read node
		if not(self.nodetypeMatches(node, 'Read')):
			print('%s is not of type Read' %(node.name()))
			return False
				
			
		#Reconstruct shadow elements
		#------------------------------------------------------------------
			
		shadowShuffleNodesList = []
			
		#check if rbRawShadow channel exists and if so, shuffle it
		if(self.getLayers(node, '{0}RawShadow'.format(reconstruct_globals.PREFIX))):
			shadowShuffleNodesList.append(self.shuffleRE(node, '{0}RawShadow'.format(reconstruct_globals.PREFIX)))
		
		#check if rbShadow channel exists and if so, shuffle it
		if(self.getLayers(node, '{0}Shadow'.format(reconstruct_globals.PREFIX))):
			shadowShuffleNodesList.append(self.shuffleRE(node, '{0}Shadow'.format(reconstruct_globals.PREFIX)))
		
			
			
			
		#check if shadowShuffleNodesList has content to add backdrop
		if(len(shadowShuffleNodesList) > 0):		
			#create backdrop
			backdrop = self.createBackdrop(shadowShuffleNodesList, self.rgbToHexString(self.backdropColorData))
			backdrop.knob('label').setValue(node.name() +'_shadowPasses')
			backdrop.knob('note_font_size').setValue(20)
			
		
		
	
	
	
	#Methods
	#------------------------------------------------------------------
	
	#shuffleRE
	def shuffleRE(self, node, layer):
		
		#shuffleRE
		shuffleRE = nuke.nodes.Shuffle(label = layer +'_rbg', inputs = [node])
		shuffleRE['in'].setValue( layer )
		shuffleRE['in2'].setValue( 'rgba' )
		shuffleRE['alpha'].setValue( 'alpha2' )
		shuffleRE['postage_stamp'].setValue( True )
		shuffleRE['hide_input'].setValue(True)
		
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
	
	
	
	
	
	
	