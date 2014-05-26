
"""
bakeAnimation
==========================================

Module with methods to bake the movement/channels of one object
to another. Transform baking can be either in local or world space.
This can be usefull to bake camera movement resulting from hierarchies
into camera movement without hierarchies etc.

-----------------------

Usage
-----

::
	
	from helga.maya.animation.bakeAnimation import bakeAnimation
	reload(bakeAnimation)

	#Create instance
	bakeAnimationInstance = bakeAnimation.BakeAnimation()
	#Select object_a and object_b and execute bakeAnimationTransformOnly
	#to bake the animation from object_a to object_b for the frames 1 - 100
	bakeAnimationInstance.bakeAnimationTransformOnly(1, 100)

-----------------------
"""




#Imports
#------------------------------------------------------------------
import pymel.core as pm







#BakeAnimation class
#------------------------------------------------------------------

class BakeAnimation():
	
	#Constructor
	def __init__(self):
		
		#Instance Vars
		#------------------------------------------------------------------
		self.verbose = True
		
		


	
	
	#TopLevel Methods
	#------------------------------------------------------------------
	
	
	#bakeAnimationTransformOnly
	def bakeAnimationTransformOnly(self, animationStartTime = 0, animationEndTime = 0, localSpace = False):
		"""
		Bake animation of two objects but only bake channels that contribute
		to the transformation matrix (translate, rotate, scale). Shear is omitted
		since it has never been used in the history of animation. The selection order
		is the same as with constraints:
		
		1. Master: Source of Movement
		2. Slave: Gets baked to movement of master

		:param animationStartTime: Beginning of sequence to bake
		:type animationStartTime: int
		:param animationEndTime: End of sequence to bake
		:type animationEndTime: int
		:param localSpace: If True, only the immediate values of the object are baked. If False bake complete transformation hierarchy (WorldSpace).
		:type localSpace: bool
		"""

		#getSelection
		selectedObjectsList = self.getSelection()
		pm.select(cl = True)
		
		
		#Check if len(selection) == 2, if false print msg and return
		if not(len(selectedObjectsList) == 2):
			if(self.verbose): print('Please select two objects to bake')
			return None
		
		#else continue execution
		else:
			
			try:
				
				#getMasterObject
				masterObject = selectedObjectsList[0]
				
				#getTargetObject
				targetObject = selectedObjectsList[1]
				
				
				#check if both objects are of type transform
				if not(pm.nodeType(masterObject) == 'transform'):
					if(self.verbose): print('Master object is not of type transform')
					return None
					
					
				if not(pm.nodeType(targetObject) == 'transform'):
					if(self.verbose): print('Target object is not of type transform')
					return None
					
				#check if start and end time are equal
				if(animationStartTime == animationEndTime):
					if(self.verbose): print('Start time should not be end time. Please enter a valid range')
					return None
				
				
				
				
				
				#getCurrentAnimationRange
				currentAnimationTime = pm.currentTime(q = True)
				
				currentAnimationStart = pm.playbackOptions(ast = True, q = True)
				currentAnimationEnd = pm.playbackOptions(aet = True, q = True)
				
				currentAnimationRangeStart = pm.playbackOptions(minTime = True, q = True)
				currentAnimationRangeEnd = pm.playbackOptions(maxTime = True, q = True)
				
				
				
				
				#setTempNewAnimationRange
				self.setAnimationRange(animationStartTime, animationEndTime, animationStartTime, animationEndTime)
				
				
				
				
				#Bake animation for given range
				for index in range(animationStartTime, animationEndTime + 1):
					
					#set current time
					pm.currentTime(index)
					
					#get transform matrix of master in local or worldSpace
					if(localSpace): masterTransformMatrix = pm.xform(masterObject, matrix = True, q = True, ws = False)
					else: masterTransformMatrix = pm.xform(masterObject, matrix = True, q = True, ws = True)
					
					#setMasterTransformMatrixOnTarget
					pm.xform(targetObject, matrix = masterTransformMatrix)
					
					#Set keyframe
					pm.setKeyframe(targetObject)
				
				
				
				#setAnimationRange back to old
				self.setAnimationRange(currentAnimationStart, currentAnimationEnd, currentAnimationRangeStart, currentAnimationRangeEnd)
				
				#set Current time back to old
				pm.currentTime(currentAnimationTime)
				
			
			
			except:
				if(self.verbose): print('Error baking animation')
				return None
			
			
		
		#Print Success Msg
		if(self.verbose): print('Successfully baked animation')
		return None
		
		
		
	
	
	
	
	
	#bakeAnimation
	def bakeAnimation(self, animationStartTime = 0, animationEndTime = 0):
		"""
		Bake animation of two objects (or master - slave pairs). Bakes animation of all
		channels that are *keyable* and *not locked*. Also the channels need to be presents
		in both objects. The selection order is the same as with constraints:
		
		1. Master: Source of Movement
		2. Slave: Gets baked to movement of master

		:param animationStartTime: Beginning of sequence to bake
		:type animationStartTime: int
		:param animationEndTime: End of sequence to bake
		:type animationEndTime: int
		"""
		
		#check if start and end time are equal
		if(animationStartTime == animationEndTime):
			if(self.verbose): print('Start time should not be end time. Please enter a valid range')
			return None
		
		
		#getSelection
		selectedObjectsList = self.getSelection()
		pm.select(cl = True)
		
		
		#Check if there is any selection
		if not(len(selectedObjectsList) > 1):
			if(self.verbose): print('You have no or not enough objects selected')
			return None
			
		#Uneven number of objects selected
		if not(len(selectedObjectsList) % 2 == 0):
			if(self.verbose): print('You have an uneven number of objects selected, please select pairs of objects to bake (Order: 1.master 2.slave)')
			return None
			
			
		
		#get Masterlist
		masterList = []
		for master in selectedObjectsList[::2]:
			masterList.append(master)
			
		#get Slavelist
		slaveList = []
		for slave in selectedObjectsList[1::2]:
			slaveList.append(slave)
			
		pm.select(cl = True)
		
		
		#get masterAttributeLists
		masterAttributeLists = []
		
		#iterate all masters and get a list of all attributes that are keyable and unlocked
		#append this list to masterAttributeLists
		for master in masterList:
			masterAttributeLists.append(pm.listAttr(master, keyable = True, unlocked = True))
			
		
		#get bakeAttributeLists
		bakeAttributeLists = []
		
		#iterate slaveList and get attributeList for each 
		for index in range(len(slaveList)):
			
			#get slaveAttributeList
			slaveAttributeList = pm.listAttr(slaveList[index], keyable = True, unlocked = True)
			
			#bakeAttributeList
			bakeAttributeList = []
			
			#iterate masterAttributeList at index
			for masterAttribute in masterAttributeLists[index]:
				
				#if attribute in slaveAttributeList append to bakeAttributeList
				if(masterAttribute in slaveAttributeList): bakeAttributeList.append(masterAttribute)
			
			
			#append bakeAttributeList to bakeAttributeLists
			bakeAttributeLists.append(bakeAttributeList)
			
			
			
		
		
		#getCurrentAnimationRange
		currentAnimationTime = pm.currentTime(q = True)
				
		currentAnimationStart = pm.playbackOptions(ast = True, q = True)
		currentAnimationEnd = pm.playbackOptions(aet = True, q = True)
				
		currentAnimationRangeStart = pm.playbackOptions(minTime = True, q = True)
		currentAnimationRangeEnd = pm.playbackOptions(maxTime = True, q = True)
				
				
				
				
		#setTempNewAnimationRange
		self.setAnimationRange(animationStartTime, animationEndTime, animationStartTime, animationEndTime)	
		
		
		
		#Bake animation for given range
		for index in range(animationStartTime, animationEndTime + 1):
					
			#set current time
			pm.currentTime(index)
			
			#iterate bakeAttributeLists
			for indexBakeAttributeList in range(len(bakeAttributeLists)):
				
				#iterate bakeAttributeList
				for bakeAttribute in bakeAttributeLists[indexBakeAttributeList]:
					
					#set attr
					pm.setAttr(slaveList[indexBakeAttributeList] +'.' +bakeAttribute, pm.getAttr(masterList[indexBakeAttributeList] +'.' +bakeAttribute))
					
				
				
				#keyframe
				pm.setKeyframe(slaveList[indexBakeAttributeList])
		
	
		
		#setAnimationRange back to old
		self.setAnimationRange(currentAnimationStart, currentAnimationEnd, currentAnimationRangeStart, currentAnimationRangeEnd)
				
		#set Current time back to old
		pm.currentTime(currentAnimationTime)
		
		
		#Print Success Msg
		if(self.verbose): print('Successfully baked animation')
		return None
		
		
		
	
	
	
	#Methods
	#------------------------------------------------------------------
	
	
	
	
	
	#Shared Methods
	#------------------------------------------------------------------
	
	
	#getSelection
	def getSelection(self):
		
		return pm.ls(sl = True, fl = True)
		
		
	
	#setAnimationRange
	def setAnimationRange(self, startTime, endTime, startRange, endRange):
		
		#setStartTime
		pm.playbackOptions(ast = startTime, e = True)
		pm.playbackOptions(minTime = startRange, e = True)
		
		#setEndTime
		pm.playbackOptions(aet = endTime, e = True)
		pm.playbackOptions(maxTime = endRange, e = True)
		
		
		
		

		
		
		
#Test Execution
#------------------------------------------------------------------
'''
from kugeltiere.maya.bakeAnimation import bakeAnimation

doReload = True
if(doReload): reload(bakeAnimation)

#Create Instance
bakeAnimationInstance = bakeAnimation.BakeAnimation()

#Execute
bakeAnimationInstance.bakeAnimation(animationStartTime = 0, animationEndTime = 40)

'''






	
	
