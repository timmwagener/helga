##omtMenu_menuname=PAIE - Animation Transfer GUI
##omtMenu_annotation=Python animation import/export
##omtMenu_optionWindow=none
##omtMenu_execString=GUI()

'''
Header 
	Toolname:	Python Attribute Import/Export (PAIE)
	Developer:	Jakob Welner, Radar Film
	Homepage:	http://www.jakob.welner.dk
	Homepage:	http://opensource.discoworms.com
	
______________________________________________
Description:
	PAIE is a python based Autodesk Maya tool for handling attribute
	transfer in version 8.5 and later. 

	Activate interface by typing "paie.GUI()" on a python commandLine
		
	Features:
	 	General functionality:
		- supports selection sets
		- exports animation from current timeline
		- imports onto current frame
		
		GUI
		- delete files through fileList using the delete key
		- when importing animation onto existing keyframes, paie promts user for permission to overwrite
		- nonAnimated attributes gets imported by setting the attribute value (no keys). 
			Only sets attribute when source and target is different (to avoid unnessesary reference attribute overwrites)
		- "pose only" exports the current attribute values of selection instead of possible animation
		- can export unlimited namespaces and objects to one file
		- choose what namespace in file to import from
		- import matching on obj names or selection order
		
		Command line
		- all functionality through maya-python cmdLine
		- accepts timerange, filepath, namespace, selection list, anim/pose, fileComments and selection order
		- execute with importData and exportData. Use is explained in their definitions

______________________________________________
License:
	PAIE is free software: you can redistribute it and/or modify
	it under the terms of the GNU Lesser General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	PAIE is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU Lesser General Public License for more details.

	You should have received a copy of the GNU Lesser General Public License
	along with PAIE.  If not, see <http://www.gnu.org/licenses/>.
	
______________________________________________
Update Log:
  21-01-2012: v1.3.2 by Jakob Welner
      - Fixed some OSX bugs
      - Streamlined OS dependent operations

  01-04-2011: v1.3.1 by Jakob Welner
      - changed PAIE title to correct version
      - fixed a slight issue with selection after deleting files
	
  30-03-2011: v1.3.0 by Jakob Welner
      - fixed browse-button for both windows and linux
      - new Export All Animation and Import to original position
      - fixed error on deleting files in export mode
      - fixed some GUI issues
      - fixed infinity again?
      - added OMT header for menu support with OMToolbox (first 4 lines)
      - supporting boolean attrs - didn't know that this wasn't working
      - returns instance on initiating GUI, in case anyone wanna use it?
      - including stack trace in error msgs
      - sorting file lists alphabetically
      - on Import prompting whether to change rotation order according to source
		Prints out affected controls to the script editor
	
  11-09-2008: v1.2.0 by Jakob Welner
      - import now only matches to obj name - not path - and only accepts unique naming
      - undo when importing has been fixed - was a bitch so you'd better be glad
      - errors are now more obvious on a popup window instead of the response line
      - updated file structure - NOT BACKWARD COMPATIBLE!!
      - listed framerate now actually works and is reliable
      - pose imports now only checks current frame for existing keys that will be overwritten
      - importing onto locked and hidden attributes no longer fails
      - the normal minor updates here and there
      - more stable GUI on linux
	
  04-04-2008: v1.1.2 by Jakob Welner
      - minor refinements
      - fixed some linux issues: ProgressHandler missing 'next()' method
      - fixed infinity transfer on namespaced objects
      - minor change in UI - replaced export 'pose only' with radioButtons (animation/pose)
	
  02-04-2008: v1.1.1 by Jakob Welner
      - fixed some stuff when handling paths with restricted permissions
	
  02-04-2008: v1.1.0 by Jakob Welner
      - enabled deleting files from list using the delete key
      - autoselect namespace if there is only one
      - fixed tangentType transfer
      - fixed some warning messages
      - fixed inifinity transfer
	
  27-03-2008: v1.0.0 by Jakob Welner
      - Initial release
		
______________________________________________
Todo:
	- when current path is invalid, open browser in default home dir (change everything from def app to def home)
	- handle spaces in filenames
	- handling namespace selections
	- search/replace name method on dataContainer
	- check if nothing matches selection, search for L_ or R_ and swap, try again. - to automatically use poses between left and right
	- export from selected timeline (superceding everything else)
	- Fix comments width
	- finish debugger implementation
	- apply to selected attrs only

        
Todo, next version:
	- maybe reduce undo memory usage by turning undo off, apply anim data, cut animCurve, turn undo back on, paste animCurves
	- direct anim/pose transfer
	- optional static selection pr. tab. Enables importing onto a predefined list of objects without having to select them each time
      - current selection / fixed selection / character set
	- rigthclick on files to list obj selection order
	- search/replace name feature on import objNames
	- get shapeNodes from transform - save as separate obj
	- add support for breakdown keys
	- option: import using original namespaces
	- support for cmdLine (import maya.standalone, maya.standalone.initialize() (mayapy.exe?))
	- support for saving/writing compound attributes
	- support for saving/writing connections
	- auto import oldVersionHandler for handling older files/structures/classes
'''




'''
File Structure Example

'header':
	'filetype':        		'anim'/'pose',
	'framerate':    		'##',
	'filename':     		'filename',
	'exportedBy':   		[user],
	'dataOfExport': 		'09:40-26/03/07',
	'structVersion':		'1.00',
	'clipLength':   		[####],
	'startframe':			[####],
	'paieVersion':			<type: string>
	'comment':			[can contain multiple lines of text],
'data':
	[SourceNamespace]
		<type: int> (selection order)
			'objData':
				'fullPath':		'|full|path|to|object',
				'rotateOrder':  <type: int>,
			'objAttrs':
				[attribute1]:
					'values':
						'pose':
							'type':		[attrType],
							'value':	<type [attrType]>,
						'anim':
							'animData':
								'preInfinity':			<type: int>,
								'postInfinity':			<type: int>,
								'weightedTangents':		<type: bool>,
							'animKeys':
								0:
									'lock':         		1,
									'inWeight':     		1.0,
									'outWeight':    		1.0,
									'outTangentType':		u'clamped',
									'inTangentType':		u'clamped',
									'weightLock':   		1,
									'value':        		-3.8118083050471538,
									'inAngle':      		55.549106946982356,
									'time':         		0.0,
									'outAngle':     		55.549106946982356,
									'breakdown':			'not in use yet'
								1:
									'lock':         		1,
									'inWeight':     		1.0,
									'outWeight':    		1.0,
									'outTangentType':		u'clamped',
									'inTangentType':		u'clamped',
									'weightLock':   		1,
									'value':        		2.0189274219867128,
									'inAngle':      		34.446127611844133,
									'time':         		4.0,
									'outAngle':     		34.446127611844133,
									'breakdown':			'not in use yet',
				[attribute2]: 
					...
					...

'''


# 0 = no debug messages
# 1 = text output
# 2 = time markers
debugger = 0

# Contains reference to current GUI class 
global gGuiRef

import time
import maya.cmds as mc
import maya.mel as mm
import os
import sys
import traceback

try:
	import cPickle as pickle
except ImportError:
	print '# Module Top >> Could not import cPickle. Using pickle. This is slower'
	import pickle 

# Structure Version
structVersion = 1.0
paieVersion = '1.3.2'


platformCase = None
if sys.platform == "win32" or sys.platform == "win64":
	platformCase = "ms"
elif sys.platform == "linux2":
	platformCase = "gnu"
elif sys.platform == "darwin":
	platformCase = "apple"
else:
	raise ValueError, "No support for OS: " + sys.platform 
		
	
	
class DataWrapper:
	
	def __init__(self):
		self.dataObj = None
		
	def clear(self):
		self.__dict__.clear()
	
		
	def load(self, filepath):

		self.loadedVersion = None
		try:
			file = open(filepath, 'rb')
			
		except IOError:
			raise StandardError,'# DataWrapper.load >> Could not open file. Permissions most probably denied. Fix it and try again'
		else:
			try:
				pickled = pickle.load(file)
				self.loadedVersion = pickled.structVersion
				
				if pickled.structVersion != structVersion:
					raise StandardError 
				else:
					self.dataObj = pickled
				
			except (StandardError, AttributeError):
				file.close()
				print ""
				print "# DataWrapper.load >> Imported pickle dosn't match current class version. This feature is not supported yet",
				return 0
	
		file.close()	
		return self.hasContent()
		
		
		
		
	def save(self, filepath):
		
		if self.dataObj == None:
			print ""
			print "# DataWrapper.save >> No content to save",
			
		else:
			### Trying to open file
			try:
				file = open(filepath, 'w')
		
			### Input/Output error handler
			except IOError:
				print ""
				print '# DataWrapper.save >> Could not open file. Most likely permissions or wrong dir. Fix it and try again',
		
			else:
				try:
					pickle.dump(self.dataObj, file, -1)
					self.dataObj.clear()
						
				except:
					raise StandardError, '# DataWrapper.save >> Could not write to file'
				else:
					print ""
					print '# DataWrapper.save >> File was successfully written at: ' + filepath,
				
				file.close()
				
				
				
				
	def hasContent(self):
		returnVal = 0
		try:
			if self.dataObj != None:
				if self.dataObj.hasContent():
					returnVal = 1
		except:
			pass
					
		return returnVal
				
				
				
				
	def getFramerate(self):
		# Get the current time base as a string
		unit = mc.currentUnit(q=True, time=True)
	
		# If it matches any of the predefined labels, set $fps accordingly
		if unit == "game":
			return 15
		elif unit == "film":
			return 24
		elif unit == "pal":
			return 25
		elif unit == "ntsc":
			return 30
		elif unit == "show":
			return 48
		elif unit == "palf":
			return 50
		elif unit == "ntscf":
			return 60
		elif unit == "millisec":
			return 1000
		elif unit == "sec":
			return 1
		elif unit == "min":
			return 0.01666
		elif unit == "hour":
			return 0
		else:
			return 0

				
	def getUser(self):
		
		if platformCase == 'gnu' or platformCase == "apple":
			return os.getenv('USER')
		elif platformCase == 'ms':
			return os.getenv('USERNAME')
		else:
			return '[Username]'
			
		
		
				
	def getData(self, selList, startFrame, endFrame, dataType, attrsType, comments):
		'''
		selList:    			List of selected objects
		startFrame: 			guess
		endFrame:   			guess
		dataType:   			'pose'/'anim'
		attrsType:  			'all'/'keyable' (save all attributes or only keyables)
		comments:   			string
		'''
		
		dataDict = {'header': {}, 'data': {} }
		
		# writing header:
		filetype = dataType
		framerate = self.getFramerate()
		exportedBy = self.getUser()
		dateOfExport = mc.date( format = "hh:mm-DD/MM/YY")
		if dataType == 'pose':
			clipLength = 1
		else:
			clipLength = (endFrame-startFrame)+1
		originalStartframe = startFrame
		
		dataDict['header'] = {'paieVersion': paieVersion, 'filetype': filetype, 'framerate': framerate, 'exportedBy': exportedBy, 'dateOfExport': dateOfExport,
		'structVersion': structVersion, 'clipLength': clipLength, 'startframe': originalStartframe,
		'comments': comments}
		
		
		namespaceDict = {}
		
		#Initializing progressBar
		progress = ProgressHandler(len(selList), "Exporting Data")
		progress.printStatus()
		
		
		# Handle selection list: (get shapenodes for each transform.. f.x.)
		
		
		# Handle namespaces
		iter = range(0, len(selList) )
		for i in iter:
			
			# Update progress
			progress.printStatus()
			
			objWithNamespace = selList[i].split("|")[-1]		# gets last obj in path
			split = objWithNamespace.split(":")
			
			if len(split) == 1:		# No namespace
				if "none" not in namespaceDict:
					namespaceDict["none"] = {}
	
				namespaceDict["none"][ i ] = self.getObjDict(selList[i], startFrame, endFrame, dataType, attrsType)
					
				
				
			else:	# Namespaces
				# get whole namespace
				objName = objWithNamespace.split(":")[-1]			# strips obj from namespace
				namespace = objWithNamespace[ : len(objName) * -1]	# gets full namespace
				
				if namespace not in namespaceDict:
					namespaceDict[namespace] = {}
	
				namespaceDict[namespace][ i ] = self.getObjDict(selList[i], startFrame, endFrame, dataType, attrsType)
		
		dataDict['data'] = namespaceDict
	
		# Finishing progressBar
		progress.finish()
		
		self.dataObj = DataContainer(dataDict)
		self.dataObj.structVersion = structVersion
		return self.dataObj.hasContent()
		
		
		
		
			
	def getObjDict(self, objFullPath, startFrame, endFrame, dataType, attrsType):
		
		objDict = {'objData': {}, 'objAttrs': {}, }
		
		# set object name
		# strip from namespaces
		
		fullStrippedPath = ""
		for lvl in objFullPath.split("|")[1:]:
			strippedObj = lvl.split(":")[-1]
			fullStrippedPath += "|" + strippedObj
			
			
		objDict['objData']['fullPath'] = fullStrippedPath
	
		
		# Set rotation order
		''' Rotate order meaning:
		0: "xyz"
		1: "yzx"
		2: "zxy"
		3: "xzy"
		4: "yxz"
		5: "zyx"
		'''
		
		if mc.objExists( objFullPath + '.rotateOrder'):
			objDict['objData']['rotateOrder'] = mc.getAttr( objFullPath +'.rotateOrder' )
		else: objDict['objData']['rotateOrder'] = 0
		
		
		# add object attributes
		if attrsType == 'all':
			attrList = mc.listAttr(objFullPath, unlocked=True, scalar=True, multi=True)
		else: #defaults to 'keyable' if none set
			attrList = mc.listAttr(objFullPath, unlocked=True, keyable=True, visible=True, scalar=True, multi=True)
			
		if type(attrList) != type([]):
			attrList = []
			
		for attrName in attrList:
			objDict['objAttrs'][attrName] = self.getAttrDict( objFullPath, attrName, startFrame, endFrame, dataType )
			
		return objDict
		
		
		
		
		
		
		
	
	def getAttrDict(self, objFullPath, attrName, startFrame, endFrame, dataType):
		
		# setting attribute data
		objName = objFullPath
	
		attrDict = {'values': {} } 
		keyframeCount = mc.keyframe(objName + '.' + attrName, time=( startFrame, endFrame ), q=True, keyframeCount=True)
		
		if keyframeCount != 0 and dataType == 'anim':
			# setting attribute anim data
			attrDict['values']['anim'] = {'animData': {}, 'animKeys': {} }
			attrDict['values']['anim']['animData']['weightedTangents'] = mc.keyTangent(objName + '.' + attrName, time=( startFrame , endFrame ), q=True, wt=True)[0]
			
			'''
			###	infinity state meaning:
			0: "constant"
			1: "linear"
			2: "constant"
			3: "cycle"
			4: "cycleRelative"
			5: "oscillate"
			'''
			
			try:
				preInfinity, postInfinity = mc.setInfinity(objName, attribute = attrName, query=True, pri=True, poi=True)
			except:
				print "# paie.getAttrDict >> Getting infinity values failed. Defaulting to 'constant'"
				traceback.print_exc()
				preInfinity, postInfinity = ("constant", "constant")
			
			attrDict['values']['anim']['animData']['preInfinity'] = preInfinity
			attrDict['values']['anim']['animData']['postInfinity'] = postInfinity
	
			# adding attribute keyframes
			attrDict['values']['anim']['animKeys'] = self.getKeyframeDict(objFullPath, attrName, keyframeCount, startFrame, endFrame)
			
		else:
			# setting attribute pose data
			attrValue = mc.getAttr(objFullPath + '.' + attrName)
				
			# Isn't used for anything yet
			if type(attrValue) == type(1.0):
				attrType = 'float'
			elif type(attrValue) == type(1):
				attrType = 'int'
				
			# These are Bools but works as integers
                        elif attrValue == True:
                                attrType = 'int'
                                attrValue = 1
                        elif attrValue == False:
                                attrType = 'int'
                                attrValue = 0
			else:
				raise StandardError, "# DataContainer.getAttrDict >> Attribute type isn't supported yet. Value in question: " + objFullPath + '.' + attrName + " = " + str(attrValue)
				
			attrDict['values']['pose'] = {}
			attrDict['values']['pose']['type'] = attrType
			attrDict['values']['pose']['value'] = attrValue
	
			
		return attrDict
		
		
		
	def getKeyframeDict(self, objFullPath, attrName, keyframeCount, startFrame, endFrame):
		
		attributes = mc.keyTangent(objFullPath + '.' + attrName, time=( startFrame , endFrame ), q=True, inAngle=True, outAngle=True, inWeight=True, outWeight=True, inTangentType=True, outTangentType=True, lock=True, weightLock=True)
		frameValues = mc.keyframe(objFullPath + '.' + attrName, time=( startFrame , endFrame ), query=True, absolute=True, timeChange=True, valueChange=True)
		
		#breakdown = mc.keyframe(objFullPath + '.' + attrName, time=( startFrame , endFrame ), query=True, breakdown=True)
		
		breakdownState = 0
		#if breakdown != None:
		#	breakdownState = 1
		
		keyDict = {}
		iter = range(0, keyframeCount )
		for i in iter:		
			keyDict[i] = { 
				'time' : frameValues[ ((i+1)*2) - 2 ] - (startFrame),	###	Place first key at frame 1 
				'value' : frameValues[ ((i+1)*2) - 1 ],
				'inAngle' : attributes[ i*8],
				'outAngle' : attributes[ i*8 + 1],
				'inWeight' : attributes[ i*8 + 2],
				'outWeight' : attributes[ i*8 + 3],
				'inTangentType' : attributes[ i*8 + 4],
				'outTangentType' : attributes[ i*8 + 5],
				'lock' : attributes[ i*8 + 6],
				'weightLock' : attributes[ i*8 + 7],
				'breakedown' : breakdownState,
			}	
		
		return keyDict
			
		

	def convertSelToDict(self, selList):
		selDict = {}
		
		iter = range(0, len(selList) )
		for i in iter:
			selDict[i] = selList[i]
			
		return selDict
		
		
		
		
	def mapImportToSelection(self, selection):
		
		objIdDict = self.dataObj.getObjIdDict()
		outputDict = {}
		for j in selection:
			sel = j.split("|")[-1]
			sel = sel.split(":")[-1]
			iMatch = None
			for i in objIdDict:
				
				importName = objIdDict[i].split("|")[-1]
				
				if importName == sel:
					outputDict[i] = j
					iMatch = i
					
			if iMatch != None:
				objIdDict.pop(iMatch)
		
		if len(outputDict.keys() ) == 0:
			raise StandardError, "# mapImportToSelection >> No import objects matched selection"
			
		return outputDict
		
		
		
		
			
	def writeToScene(self, selection, selectOrder, namespace, animOffset):
		
		if debugger == 2:
			print "# writeToScene start: ".ljust(30), time.clock()
			
		self.dataObj.setDefaultNamespace(namespace)
		
		if selectOrder == 1:
			# for convenience, convert selection to a dictionary when selectOrder is set
			# so that it matches the return value of compareSelection()
			mutualObjs = self.convertSelToDict(selection)
		else:
			if debugger == 2:
				print "# CompareSelection start: ".ljust(30), time.clock()
				
			mutualObjs = self.mapImportToSelection(selection)
	
			if debugger == 2:
				print "# CompareSelection End: ".ljust(30), time.clock()
				
		
		curFps = self.getFramerate()
		srcFps = self.dataObj.getHeaderAttr("framerate")
		
		if curFps != 0 and srcFps != 0:
			if srcFps != curFps:
				userInput = mc.confirmDialog( title="Framerate doesn't match", message = ("Animation was exported with a different framerate than \nyour current settings. Continue anyway? \n\nSource: " + `srcFps` + " fps\nCurrent: " + `curFps` + " fps"), ma="left", button = ["Yes", "No"], defaultButton = "No", cancelButton = "No", dismissString = "No")
					
				if userInput == "No":
					raise KeyboardInterrupt, "# writeToScene >> Program terminated by user"
	
		
					
			
		
		###	Clear keys in frameRange	
		nonExistingObjs = []
		proceed = 0
		isKey = 0
		
		objList = []
		existObjIdIter = []
	
		if debugger == 2:
			print "# Check for existin keys: ".ljust(30), time.clock()
			
		startTime = animOffset 
		stopTime = animOffset + self.dataObj.getHeaderAttr('clipLength') - 1
		
		# make 'em look nice
		if int(startTime) == startTime:
			startTime = int(startTime)
		if int(stopTime) == stopTime:
			stopTime = int(stopTime)
		
		###	Checks for existing keys and nonexisting objects
		for i in mutualObjs:
			
			try:
				if (mc.keyframe(mutualObjs[i], time=( startTime , stopTime ), q=True, keyframeCount=True)):
					isKey = 1
					
			except TypeError:
				nonExistingObjs.append(mutualObjs[i])		# Saved for future reference
				
			else:
				objList.append(mutualObjs[i])			# Containing all existing objects as a list
				existObjIdIter.append(i)				# Containing ID's on existing objects
				
		if self.dataObj.getHeaderAttr('filetype') == 'anim':		
			if isKey:
				proceed = mc.confirmDialog( title="Keys exist", message = ("Keys already exist in framerange: " + str(startTime) + '-' + str(stopTime) + '\nOverrwrite?'), button = ["Yes", "No"], defaultButton = "Yes", cancelButton = "No", dismissString = "No")
		
				
				if proceed == 'No':
					raise KeyboardInterrupt, "# writeToScene >> Procedure cancelled by user"
					
				
				# remove existing animation on objs with importAnim data		
				mc.cutKey( objList , time=(startTime , stopTime), clear=True)
			
		# Starting to write data
		skippedAttrs = []
		
		if debugger == 2:
			print "# write keys start: ".ljust(30), time.clock()
			
	
		# Checks for dismatching rotation order and whatever else on objects before writing	
		rooMismatchDict = {}	
		for objID in existObjIdIter:
			obj = mutualObjs[objID]	
			
			# check rotate order
			if mc.objExists( obj + '.rotateOrder'):
				currRoo = mc.getAttr(obj + '.rotateOrder')
				importRoo = self.dataObj.getObjDataVal(objID, 'rotateOrder')
	
				if currRoo != importRoo:
					rooMismatchDict[obj] = {"currentRoo" : currRoo, "sourceRoo": importRoo}
					
			else:
				# out commented to enable transfer from shape-nodes
				pass
				#raise StandardError, "# writeToScene >> objs without rotateOrder attribute?: " + obj
					
		if len(rooMismatchDict.values()):
			proceed = "Yes"
			
			print "\n### Target objects with mismatching rotation order:"
			for key in rooMismatchDict:
				print key.split("|")[-1] + ": source roo: " + str(rooMismatchDict[key]["sourceRoo"]) + ", target roo: " + str(rooMismatchDict[key]["currentRoo"])
				
			proceed = mc.confirmDialog( title="Keys exist", 
					message = ("One or more objects rotation order dismatches import values. \nMatch target rotationOrder to source?"), 
					button = ["Yes", "No"], 
					defaultButton = "Yes", 
					cancelButton = "No", 
					dismissString = "No")
					
			if proceed == "Yes":
				print "\n### Setting rotation order for target objects:"
				for key in rooMismatchDict:
					print "### " + key.split("|")[-1] + '.rotateOrder -> ' + str(rooMismatchDict[key]["sourceRoo"])
					try:
						mc.setAttr(key + '.rotateOrder', rooMismatchDict[key]["sourceRoo"])
					except:
						print "### Failed to set Rotation Order on object...It's probably locked"
			
			elif proceed == "No":
				print "### Not touching rotation order..."
				#raise KeyboardInterrupt, "# writeToScene >> Procedure cancelled by user"
			
			
				
		# Initializing progress handler
		progress = ProgressHandler( len(existObjIdIter), "Importing Data" )
		progress.printStatus()
		
		
		# Starting to write to scene
		for objID in existObjIdIter:
			obj = mutualObjs[objID]
			
			# Progress printing
			progress.printStatus()
			
			for attr in self.dataObj.listObjAttrs(objID):
			
				if mc.objExists( obj + '.' + attr ):
					
					if self.dataObj.hasAnim(objID, attr):
						
						
						# Set Keys
						for key in self.dataObj.getAttrKeyID(objID , attr):
	
							### line 773: This is hacked. Change back soon!
							######################################################################################################
							
							frameNr = float(self.dataObj.getKeyAnimData(objID, attr, key, 'time')) + animOffset
							### maya 2010 bugfix - can't set rotation values with setKeyframe when on animLayers
							#if attr in ("rotateX", "rotateY", "rotateZ"):
								#mc.currentTime( frameNr )
								#try:
									#mc.setAttr(obj + "." + attr, float(self.dataObj.getKeyAnimData(objID, attr, key, 'value')))
									#mc.setKeyframe(obj , time =  frameNr  , attribute = str(attr), breakdown=False, hierarchy='none', controlPoints=False, shape=False )
								#except:
									#pass
									
							#else:
								#mc.setKeyframe(obj , time =  frameNr  , attribute = str(attr)  , value =  float(self.dataObj.getKeyAnimData(objID, attr, key, 'value')), breakdown=False, hierarchy='none', controlPoints=False, shape=False )
								
							mc.setKeyframe(obj , time =  frameNr  , attribute = str(attr)  , value =  float(self.dataObj.getKeyAnimData(objID, attr, key, 'value')), breakdown=False, hierarchy='none', controlPoints=False, shape=False )
	
							
							
						# Set Tangents
						mc.keyTangent(obj + '.' + attr, edit=True, wt = int(self.dataObj.getAttrData(objID, attr, 'weightedTangents')))
	
						
						for keyID in self.dataObj.getAttrKeyID(objID , attr):
		
							try:
								frameNr = (float(self.dataObj.getKeyAnimData(objID, attr, keyID, 'time')) + animOffset)
								
								inAngleVal = float(self.dataObj.getKeyAnimData(objID, attr, keyID, 'inAngle'))
								outAngleVal = float(self.dataObj.getKeyAnimData(objID, attr, keyID, 'outAngle'))
								inWeightVal = float(self.dataObj.getKeyAnimData(objID, attr, keyID, 'inWeight'))
								outWeightVal = float(self.dataObj.getKeyAnimData(objID, attr, keyID, 'outWeight'))
								inTangentTypeVal = str(self.dataObj.getKeyAnimData(objID, attr, keyID, 'inTangentType')) 
								outTangentTypeVal = str(self.dataObj.getKeyAnimData(objID, attr, keyID, 'outTangentType'))
								lockVal = int(self.dataObj.getKeyAnimData(objID, attr, keyID, 'lock'))
								
								mc.keyTangent(obj + '.' + attr, time=( frameNr ,frameNr ), edit=True, inAngle = inAngleVal, outAngle = outAngleVal, inWeight = inWeightVal, outWeight = outWeightVal)
								mc.keyTangent(obj + '.' + attr, time=( frameNr ,frameNr ), edit=True, inTangentType = inTangentTypeVal, outTangentType = outTangentTypeVal)
								mc.keyTangent(obj + '.' + attr, time=( frameNr ,frameNr ), edit=True, lock = lockVal)
								if int(self.dataObj.getAttrData(objID, attr, 'weightedTangents')):
									
									weightLockVal = int(self.dataObj.getKeyAnimData(objID, attr, keyID, 'weightLock'))
									mc.keyTangent(obj + '.' + attr, time=( frameNr ,frameNr ), edit=True, weightLock = weightLockVal)
							except:
								print "# paie.writeToScene caught this kind of error while applying keyframes:"
								raise
								
			
						###	Setting infinity
						preInfinity = self.dataObj.getAttrData(objID, attr, "preInfinity")
						postInfinity = self.dataObj.getAttrData(objID, attr, "postInfinity")
						
						if preInfinity != "constant":
							mc.setInfinity(obj, attribute = attr, pri = preInfinity )
							
						if postInfinity != "constant":
							mc.setInfinity(obj, attribute = attr, poi = postInfinity )
					else:
						# set attribute value with setAttr if it is different than current value
						currentVal = mc.getAttr(obj + '.' + attr)
						importValue = self.dataObj.getAttrData(objID, attr, 'value')
						
						if currentVal != importValue:
							try:
								mc.setAttr(obj + '.' + attr, importValue)
							except:
								print ""
								print "# writeToScene >> " + obj + '.' + attr + " cannot be modified. Skipping...",
								
				
		# Progress printing done
		progress.finish()
		
		
		
		
		
		
		
		
		
	
	
class DataContainer:
	'''Container class for attribute data'''
	
	def __init__(self, dictionary = {} ):
		self.content = dictionary
		self.returnString = ''
		self.defaultNamespace = 'none'
		self.structVersion = None
		
		
	def clear(self):
		self.__dict__.clear()
	
		
		
	def hasContent(self):
		returnVal = 0
		
		for key in self.content:
			if self.content[key] != {}:
				returnVal = 1

		return returnVal
		
	
	
	def listNamespaces(self):
		return self.content['data'].keys()
		
		
	def listHeader(self):
		
		returnList = []
		for key in self.content['header']:
			if key != "comments":
				returnList.append(key.ljust(14) + str(self.content['header'][key]) )
				
		returnList.append("")
		returnList.append("comments:")
		returnList.append(str(self.content['header']["comments"]) )
			
		return returnList
			
		
		
		
	def listObjs(self, namespace=None):
		
		objList = []
		
		if namespace == None:
			namespace = self.defaultNamespace
		
		try:
			for i in self.content['data'][namespace]:
				objList.append(self.content['data'][namespace][i]['objData']['fullPath'] )
		except KeyError:
			raise StandardError, "# DataContainer.listObjs >> No objects matches criteria"
		
		return objList
		
		
		
		
			
	def getObjIdDict(self, namespace=None):
		
		if namespace == None:
			namespace = self.defaultNamespace
			
		objIdDict = {}
			
		for id in self.content['data'][namespace]:
			objIdDict[id] = self.content['data'][namespace][id]['objData']['fullPath']
			
		return objIdDict
		
		
		
		
	def hasAnim(self, objID, attr, namespace=None):
		if namespace == None:
			namespace = self.defaultNamespace
		
		try:
			valueKey = self.content['data'][namespace][objID]['objAttrs'][attr]['values'].keys()
			if len( valueKey ) == 1:
				if valueKey[0] == 'anim':
					return 1
				elif valueKey[0] == 'pose':
					return 0
				else:
					raise StandardError, "# DataContainer.hasAnim >> Wtf. nor pose nor anim in values, but still an elemet: " + valueKey
			else:
				raise StandardError, "# DataContainer.hasAnim >> " + len( valueKey ) + " keys in [" + namespace + "][" + objID + "]['objAttrs'][" + attr + "]['values']. Should be 1"
		except KeyError:
			print "# namespace: ", namespace
			print "# objID: ", objID
			print "# attr: ", attr
			raise KeyError
			

			
			
			
	def getAttrKeyID(self, objID, attr):
		try:
			returnVal = self.content['data'][self.defaultNamespace][objID]['objAttrs'][attr]['values']['anim']['animKeys'].keys()
		except KeyError:
			print "# defaultNamespace: ", self.defaultNamespace
			print "# ObjID: ", objID
			print "# Attr: ", attr
			raise KeyError
		
		return returnVal
		
		
		
		
		
	def getKeyAnimData(self, objID, attr, keyID, keyword):
		try:
			returnVal = self.content['data'][self.defaultNamespace][objID]['objAttrs'][attr]['values']['anim']['animKeys'][keyID][keyword]
		except KeyError:
			print "# defaultNamespace: ", self.defaultNamespace
			print "# objID: ", objID
			print "# Attr: ", attr
			print "# KeyID: ", keyID
			print "# Keyword: ", keyword
			raise KeyError
			
		return returnVal
		
		
		
		
		
		
	def getAttrData(self, objID, attr, keyword):
		try:
			if self.hasAnim(objID, attr):
				return self.content['data'][self.defaultNamespace][objID]['objAttrs'][attr]['values']['anim']['animData'][keyword]
			else:
				return self.content['data'][self.defaultNamespace][objID]['objAttrs'][attr]['values']['pose'][keyword]
		except KeyError:
			print "# HasAnim state: ", self.hasAnim(objID, attr)
			print "# DefaultNamespace: ", self.defaultNamespace
			print "# ObjID: ", objID
			print "# Attr: ", attr
			print "# Keyword: ", keyword
			raise KeyError
		
		
		
			
			
	def listObjAttrs(self, objID, namespace = None):
		attrList = []
		
		if namespace == None:
			namespace = self.defaultNamespace
		
		try:
			for attr in self.content['data'][namespace][objID]['objAttrs']:
				attrList.append(attr)
		except KeyError:
			print "# objID: ", objID
			print "# namespace: ", namespace
			raise KeyError
			
		return attrList
		
		
		
	def getObjDataVal(self, objID, attr, namespace=None):
		if namespace == None:
			namespace = self.defaultNamespace
		try:
			returnVal = self.content['data'][namespace][objID]['objData'][attr]
		except KeyError:
			print "# objID: ", objID
			print "# attr: ", attr
			print "# namespace: ", namespace
			raise KeyError
			
		return returnVal


			
	def setDefaultNamespace(self, namespace):
		self.defaultNamespace = namespace
		
		
		
	def getHeaderAttr(self, attr):
		return self.content['header'][attr]
		
		
		
	def digInPrint(self, data, indent):
		for key in data:
			try:
				if data[key].keys():
					self.returnString += ('  '*indent) + repr(key) + ':\n'
					self.returnString += ('  '*indent) + '{\n'
					self.digInPrint(data[key], (indent + 1))
					self.returnString += ('  '*indent) + '}\n'
			except AttributeError:
				self.returnString += ('  '*indent) + (repr(key) + ':').ljust(16) + '  ' + str(repr(data[key])) + ',\n'
	
		
		
		
		
	def display(self, startingPoint = None):
		self.returnString = ""		
		printString = '\n'
		
		###	Prints the hierachy to screen
		if self.hasContent():
			if startingPoint == None:
				
				###	Prints whole hierachy
				self.digInPrint(self.content, 0)
				printString = self.returnString
			else:
				###	Prints only specified hierachy
					
				digString = ''
				for index in startingPoint:
					digString += '[' + repr(index) + ']'
				
				try:
					tempDict = eval('self.content' + digString)
					self.digInPrint(tempDict, 0)
					printString = self.returnString
				except KeyError:
					print '# DataContainer.display >> no index matches input'
				except TypeError:
					printString = tempDict
					
		else:
			print '# DataContainer.display >> class contains no dictionary data'

			
		if printString != "":
			print printString
		else:
			return 0
				
	
			
class ProgressHandler:
	'''
	Class for handling progress notifiers
	'''
	
	def __init__(self, steps, jobType ):
		if type(steps) != type(1):
			raise StandardError, "# ProgressHandler.__init__() >> Input Error"
			
		self.stepSize = 100.0 / float(steps)
		self.curStatus = 0
		
		if platformCase == "ms":
			self.os = "windows"
			mc.progressWindow(title = jobType, progress = 0, status = "Initializing progress bar", isInterruptable = False)
			
		else:
			self.os = sys.platform
			print "# Initializing progressBar",
			
			
		
	def printStatus(self):
		if self.os == "windows":
			self.__windowsPrint()
			
		else:
			self.__linuxPrint()
			
			
	def finish(self):
		if self.os == "windows":
			mc.progressWindow(endProgress=True)
			
		
		
	def __next(self):
		self.curStatus += self.stepSize
	
		
		
	def __windowsPrint(self):
		mc.progressWindow(edit = True, progress = int(self.curStatus), status = "Progress is "+ str(int(self.curStatus)).zfill(2) + "% done" )
		self.__next()
	
	
	
	def __linuxPrint(self):
		print "# Progress is " + str(int(self.curStatus)).zfill(2) + "% done",
		self.__next()
		
		
		
		
class Callback(object):
	
	_callData = None
	
	@staticmethod
	def _doCall():
		(func, args, kwargs) = Callback._callData
		Callback._callData = func(*args, **kwargs)

	def __init__(self, func, *args, **kwargs):
		self.func = func
		self.args = args
		self.kwargs = kwargs
		
	def __call__(self, *args):
		Callback._callData = (self.func, self.args, self.kwargs)
		# Evaluating through MEL because going directly through python seems to be invoking an undo bug where all
		# maya calls from then on gets logged as seperate undoes
		#mm.eval('python("import sys; sys.modules["%s"].Callback._doCall()")' % __name__)
		#'''
		if __name__ != '__main__':
			mm.eval('python("' + __name__ + '.Callback._doCall()")')
		else:
			mm.eval('python("Callback._doCall()")')
		#'''
		return Callback._callData

		
		
		

class Timer:
	# Not implemented yet
	def __init__(self):
		self.startTime = time.clock()
		self.logList = []
		self.paused = 0.0
		self.pauseState = False
		
		self.pauseStart = 0.0
		self.pauseStop = 0.0
		
		
	def logTime(self, note):
		self.logList.append( str( time.clock() - self.startTime - self.paused ) + ": " + note )
		
	def printLog(self):
		for i in self.logList:
			print i
			
	def pauseToggle(self):
		if self.pauseState == True:
			self.pauseStart = time.clock()
			self.logTime( "Paused..." )
			self.pauseState = False
			
		elif self.pauseState == False:
			self.pauseStop = time.clock()
			self.logTime( "Continuing" )
			self.paused = self.pauseStop - self.pauseStart
			self.pauseState = True
			
		
		
		

class PaieGUI:
	def __init__(self):
		
		# optionVariables
		self.optVar_path = "paieOptVar_path" # this is an array
		
		
		# checking for empty optVar:
		defaultDir = mc.internalVar(userAppDir=True)

		if mc.optionVar( arraySize = self.optVar_path ) == 0:
			mc.optionVar( stringValueAppend=(self.optVar_path, defaultDir) )
			
		
		# other kind of variables
		self.mode = 1	#default is import
		self.currentTab = 0
		self.fileExt = ".xad"
		# Can't scale vertically, so this sort of compensates
		self.listHeight = 250
		
		
		# Initialize listVariables
		# Checkboxes
		self.selectOrder = []
		self.origNamespaces = []
		self.exportTimeline = []
		self.applyAtOrigin = []
		self.exportType = []
		
		# uiPaths
		self.uiPath_selectOrder = []
		self.uiPath_applyAtOrigin = []
		self.uiPath_exportTimeline = []
		self.uiPath_origNamespaces = []
		self.uiPath_filename = []
		self.uiPath_fileList = []
		self.uiPath_namespaceList = []
		self.uiPath_fileInfo = []
		self.uiPath_exportType = []
		self.uiPath_comments = []
		self.uiPath_pathField = []
		self.uiPath_exportButton = []
		
		self.refreshGUI()
		
		
		
		
	def addListElement(self):
		
		self.uiPath_selectOrder.append("")
		self.uiPath_exportTimeline.append("")
		self.uiPath_applyAtOrigin.append("")
		self.uiPath_origNamespaces.append("")
		self.uiPath_fileList.append("")
		self.uiPath_namespaceList.append("")
		self.uiPath_fileInfo.append("")
		self.uiPath_exportType.append("")
		self.uiPath_comments.append("")
		self.uiPath_pathField.append("")
		self.uiPath_filename.append("")
		self.uiPath_exportButton.append("")
		
		self.origNamespaces.append(False)
		self.selectOrder.append(False)
		self.exportTimeline.append(True)
		self.applyAtOrigin.append(False)
		self.exportType.append(1)


	def removeListElement(self):
		
		self.uiPath_selectOrder.pop( self.currentTab )
		self.uiPath_exportTimeline.pop( self.currentTab )
		self.uiPath_applyAtOrigin.pop( self.currentTab )
		self.uiPath_origNamespaces.pop( self.currentTab )
		self.uiPath_fileList.pop( self.currentTab )
		self.uiPath_namespaceList.pop( self.currentTab )
		self.uiPath_fileInfo.pop( self.currentTab )
		self.uiPath_exportType.pop( self.currentTab )
		self.uiPath_comments.pop( self.currentTab )
		self.uiPath_pathField.pop( self.currentTab )
		self.uiPath_filename.pop( self.currentTab )
		
		self.origNamespaces.pop( self.currentTab )
		self.selectOrder.pop( self.currentTab )
		self.exportTimeline.pop( self.currentTab )
		self.applyAtOrigin.pop( self.currentTab )
		self.exportType.pop( self.currentTab )


	def resetUiPaths(self):
                
		self.uiPath_selectOrder = []
		self.uiPath_applyAtOrigin = []
		self.uiPath_exportTimeline = []
		self.uiPath_origNamespaces = []
		self.uiPath_filename = []
		self.uiPath_fileList = []
		self.uiPath_namespaceList = []
		self.uiPath_fileInfo = []
		self.uiPath_exportType = []
		self.uiPath_comments = []
		self.uiPath_pathField = []
		self.uiPath_exportButton = []
		


		
		
	def makeGUI(self):
		guiName = "PaieGUI"
		
		if mc.window(guiName, exists=True):
			mc.deleteUI(guiName)
			self.resetUiPaths()
		
		mc.window(guiName, t="PAIE - Python Attribute Import/Export, v" + paieVersion)
		self.uiPath_mainForm = mc.formLayout(numberOfDivisions=100)
		
		self.uiPath_topBar = mc.rowLayout(parent = self.uiPath_mainForm, nc=4, adjustableColumn=1, columnAttach4=("both", "both", "both", "both"), columnAlign4=("left", "center", "center", "center") )
		
		mc.radioButtonGrp(columnWidth3=(60, 80, 80), numberOfRadioButtons=2, label="Mode:", labelArray2=("Import", "Export"), select = self.mode, on1 = lambda *args: self.setMode(1), on2 = lambda *args: self.setMode(2))
		mc.button( label="Refresh Files", width=100, command = lambda *args: self.updateFilelist() )
		mc.button( label="Add Tab", width=100, command = lambda *args: self.addNewTab() )
		mc.button( label="Remove Tab", width=100, command = lambda *args: self.removeTab() )
		
		self.uiPath_tabs = mc.tabLayout(parent = self.uiPath_mainForm, changeCommand= lambda *args: self.tabChanged())
		
		
		mc.formLayout( self.uiPath_mainForm, edit=True,
			attachForm=[
				(self.uiPath_topBar, "top", 5),
				(self.uiPath_topBar, "left", 5),
				(self.uiPath_topBar, "right", 5),
				(self.uiPath_tabs, "left", 0),
				(self.uiPath_tabs, "right", 0),
				(self.uiPath_tabs, "bottom", 0)
				],
			attachControl=[
				(self.uiPath_tabs, "top", 5, self.uiPath_topBar)
				]
		)
		
		lastActiveTab = self.currentTab
		
		tabCount = self.getPathCount()
		for i in range(0, tabCount):
			self.addListElement()
			self.makeTab(i)
			
		self.currentTab = lastActiveTab # Setting default tab
		mc.tabLayout(self.uiPath_tabs, edit=True, childResizable=True, selectTabIndex = self.currentTab+1)  # +1 when editing tabLayout. Stupid 1-indexing!
		self.updateFilelist() 
		
		if not mc.windowPref(guiName, exists=True):
			if platformCase == "gnu":
				mc.window(guiName, edit=True, height = self.listHeight + 150, width=500)
			else:
				mc.window(guiName, edit=True, height = self.listHeight + 200, width=500)
		
		mc.showWindow(guiName)
		
		width = mc.window(guiName, query=True, width=True)
		mc.window(guiName, edit=True, width=width + 2);mc.window(guiName, edit=True, width=width)
		
			
			
		
	def makeTab(self, index ):
		
		self.currentTab = index # Setting a temporary value on creation
		
		tabCol = mc.columnLayout(adj=1, rowSpacing=5, parent = self.uiPath_tabs)
		
		pathRow = mc.rowLayout(nc=3, adjustableColumn=2, columnAlign=(3, "center"), columnAttach=(1, "left", 5), columnWidth=((1, 80), (3, 60)) )
		
		mc.text(label ="Directory:", width=75)
		self.uiPath_pathField[ index ] = mc.textField( text = self.getCurrentPath(), changeCommand = lambda *args: self.setNewPath( *args ) )
		mc.button(label="Browse", width=55, command = lambda *args: self.browseFolders())
		

		if self.mode == 1: #Import
			checkRow = mc.rowLayout( parent=tabCol, nc=4, columnWidth4=(80,130, 170, 150) )
			
			mc.text( label="", width=80, height=28)
			self.uiPath_selectOrder[index] = mc.checkBox(label="Select Order", value = self.selectOrder[index], changeCommand = lambda *args: self.setSelectOrder(*args))
			self.uiPath_origNamespaces[index] = mc.checkBox(label="Use Original Namespaces", value = self.origNamespaces[index], enable = False, changeCommand = lambda *args: self.setOrigNamespace(*args))
			self.uiPath_applyAtOrigin[index] = mc.checkBox(label="Apply At Origin", value = self.applyAtOrigin[index], ann = "Imports animation onto original frame numers", enable = True, changeCommand = lambda *args: self.setApplyAtOrigin(*args))
			
			listForm = mc.formLayout(parent= tabCol, numberOfDivisions=100)
			
			group1 = mc.columnLayout( parent = listForm, adj = 1)
			
			mc.text(label="Files", font="boldLabelFont")
			self.uiPath_fileList[index] = mc.textScrollList(height = self.listHeight, deleteKeyCommand = lambda *args: self.deleteSelectedFile(), selectCommand = lambda *args: self.fileSelected() )
			
			group2 = mc.columnLayout( parent = listForm, adj = 1)
			
			mc.text(label="Namespaces", font="boldLabelFont")
			self.uiPath_namespaceList[index] = mc.textScrollList(height = self.listHeight )
			
			group3 = mc.columnLayout( parent = listForm, adj = 1)
			
			mc.text(label="File Info", font="boldLabelFont")
			self.uiPath_fileInfo[index] = mc.scrollField( height = self.listHeight - 28, editable=False, ww=1, font="smallFixedWidthFont")
			mc.button(label = "Import", align = "center", command = Callback(self.importButton) )
			#mc.button(label="Import", align="center", command = __name__ + '.importButton("' + str(self.uiPath_fileList[ index ]) + '", "' + str(self.uiPath_namespaceList[ index ]) + '", "' + str(self.optVar_path) + '", "' + str(self.uiPath_selectOrder[index]) + '", ' + str(index) + ', "' + str(self.fileExt) + '")' )
		
			mc.formLayout(listForm, edit=True, 
				attachForm=[
					(group1, "top", 5),
					(group1, "left", 5),
					(group1, "bottom", 5),
					
					(group2, "top", 5),
					(group2, "bottom", 5),
					
					(group3, "top", 5),
					(group3, "bottom", 5),
					(group3, "right", 5),
					
				],
				attachControl=[
					(group2, "left", 5, group1),
					(group2, "right", 5, group3)
				],
				attachPosition=[
					(group1, "right", 5, 33),
					
					(group3, "left", 5, 66),
				]
			)

		else: #Export
			checkRow = mc.rowLayout( parent=tabCol, nc=3, columnAttach=(1, 'left', 5), columnWidth3=(250, 320, 50) )
			
			self.uiPath_filename[ index ] = mc.textFieldGrp( label="Filename", columnAlign=(1, 'left'), columnWidth2=(75,130) )
			self.uiPath_exportType[ index ] = mc.radioButtonGrp( select = self.exportType[ index ], columnWidth=(1, 100), columnAlign=(1, "left"), on1 = lambda *args: self.setExportType(1), on2 = lambda *args: self.setExportType(2), label = "Export Type", labelArray2 = ["Animation", "Pose"], numberOfRadioButtons = 2)
			self.uiPath_exportTimeline[index] = mc.checkBox(label="Timeline Only", value = self.exportTimeline[index], ann = "Exports animation on timeline only (instead of all animation on object)", enable = True, changeCommand = lambda *args: self.setExportTimeline(*args))
			
			listForm = mc.formLayout(parent= tabCol, numberOfDivisions=100)
			
			group1 = mc.columnLayout( parent = listForm, adj = 1)
			
			mc.text(label="Existing Files", font="boldLabelFont")

			self.uiPath_fileList[index] = mc.textScrollList(height = self.listHeight, deleteKeyCommand = lambda *args: self.deleteSelectedFile(), selectCommand = lambda *args: self.fileSelected() )
			
			group3 = mc.columnLayout( parent = listForm, adj = 1)
			
			mc.text(label="Comments", font="boldLabelFont")
			self.uiPath_comments[index] = mc.scrollField( height = self.listHeight - 28, ww=1, font="smallFixedWidthFont")
			self.uiPath_exportButton[ index ] = mc.button(label="Export", align="center", command= lambda *args: self.exportButton() )
		
			mc.formLayout(listForm, edit=True, 
				attachForm=[
					(group1, "top", 5),
					(group1, "left", 5),
					(group1, "bottom", 5),
				
					(group3, "top", 5),
					(group3, "bottom", 5),
					(group3, "right", 5),
					
				],
				attachPosition=[
					(group1, "right", 5, 33),
					
					(group3, "left", 5, 33),
				]
			)
			
			self.setExportEnable()
			
			
		self.setTabLabel()
		
		
		
		

	### SET DEFINITIONS 
	############################################################################
		
	def setOrigNamespace(self, value):
		if value == "true":
			value = True
		elif value == "false":
			value = False
		self.origNamespaces[ self.currentTab ] = value
		
		
		
	def setSelectOrder(self, value):
		if value == "true":
			value = True
		elif value == "false":
			value = False
		self.selectOrder[ self.currentTab ] = value
		
		
		
	def setExportTimeline(self, value):
		if value == "true":
			value = True
		elif value == "false":
			value = False
		self.exportTimeline[ self.currentTab ] = value


        def setApplyAtOrigin(self, value):
                if value == "true":
			value = True
		elif value == "false":
			value = False
		self.applyAtOrigin[ self.currentTab ] = value
			
			
			
	def setExportEnable(self):
		# setting enabled status:
		permissions = int(os.access( self.getCurrentPath() , os.W_OK))
		if permissions == 0:
			print "# PaieGUI.setExportEnable >> You do not have write permissions to this directory",
		else:
			print "",	# Clearing the command response line

		if self.mode == 2:
			mc.textFieldGrp( self.uiPath_filename[ self.currentTab ], edit=True, editable= permissions)
			mc.radioButtonGrp( self.uiPath_exportType[ self.currentTab ], edit=True, editable= permissions)
			mc.textScrollList( self.uiPath_fileList[ self.currentTab ], edit=True, enable= permissions)
			mc.scrollField( self.uiPath_comments[ self.currentTab ], edit=True, editable= permissions)
			mc.button( self.uiPath_exportButton[ self.currentTab ], edit=True, enable= permissions)
		
		return permissions
			
			
			
	def setNewPath(self, inputPath ):
		
		if inputPath != None and inputPath != "":
			
			inputPath = inputPath.decode("ascii")
			#normPath = self.normalizePath( inputPath )
			inputPath = os.path.dirname(inputPath + "/" ) + "/"
			
			print "Dirname path: ", inputPath
			#print "Normalized Path: ", normPath
			
			if not os.path.isdir( inputPath ):
				print "# PaieGUI.setNewPath >> This is not a real path. Please try again",
				inputPath = self.getCurrentPath()

                                if not os.path.isdir( inputPath ):
                                    inputPath = mc.internalVar(userAppDir=True)
			
			
			if mc.optionVar( arraySize = self.optVar_path ) < 2:
				pathArray = [inputPath]
	
			else:
				pathArray = mc.optionVar(q=self.optVar_path)
				
			if self.currentTab < len(pathArray):
				# updating tab optionVar
				pathArray[ self.currentTab ] = inputPath
				mc.optionVar( clearArray = self.optVar_path)
				for path in pathArray:
					mc.optionVar(stringValueAppend=( self.optVar_path, path) )
					
				self.setExportEnable()
				self.updateFilelist()
					
				self.setTabLabel()
				mc.textField(self.uiPath_pathField[ self.currentTab ], edit=True, text = inputPath) 
					
			else:
				self.setTabLabel()
				raise IndexError, "# PaieGUI.setNewPath >> Current tab dosn't match anything. Tab: " + str(self.currentTab)
			
			
			
	def setTabLabel(self ):
		path = self.getCurrentPath()
		split = path.split("/")
		if len(split) > 1:
			label = split[-2]
		else:
			label = "None"
		mc.tabLayout(self.uiPath_tabs, edit=True, tabLabelIndex = [self.currentTab +1, label] )
		
		
		
	def setMode(self, mode):
		self.mode = mode
		self.refreshGUI()
		
		
		
	def setExportType(self, val):
		self.exportType[ self.currentTab ] = val
		

			
			
	### GET DEFINITIONS 
	############################################################################
		
	def getCurrentPath(self):
		'''Returns current tab path'''
		size = mc.optionVar(arraySize = self.optVar_path)
		pathList = mc.optionVar(query = self.optVar_path)
		
		if size != 0 and size != 1:
			return pathList[ self.currentTab ]
		elif self.currentTab == 0 and size == 1:
			if type( pathList ) == type([]):
				return pathList[0]
			else:
				return pathList
		else:
			raise IndexError, "# PaieGUI.getCurrentPath >> Wrong number of tabs / paths"
		
		
		
		
	def getPathCount(self):
		pathCount = mc.optionVar( arraySize = self.optVar_path)
		return pathCount
		
		
		
		
		
		
	### DATA MANIPULATION 
	############################################################################

	'''
        # No longer in use
	def normalizePath(self, path):
		drive, splitPath = os.path.splitdrive(path)
		path = splitPath.replace("\\", "/")
		fixedPath = drive + "/"
		for split in path.split("/"):
			if split != "":
				fixedPath += split + "/"
				
		if fixedPath != "":
			return fixedPath
		else:
			raise TypeError, "# PaieGUI.normalizePath >> output string is empty. Input type: " + path
        '''
		
			
	def deleteSelectedFile(self):
		dirPath = self.getCurrentPath()
		filename = mc.textScrollList( self.uiPath_fileList[ self.currentTab ], query=True, selectItem=True )[0]
		filepath = dirPath + "/" + filename + self.fileExt
		
		proceed = os.path.isfile( filepath )

		if proceed == 1:
			permissions = os.access( filepath , os.W_OK)
			if permissions == 0:
				print "# deleteSelectedFile >> You do not have permissions to delete this file",
			else:
				answer = mc.confirmDialog( title="Delete File", message = "Are you sure you want to delete this file?", button = ["Yes", "No"], defaultButton = "Yes", cancelButton = "No", dismissString = "No")
				if answer == "Yes":
					os.remove(filepath)
					curSel = mc.textScrollList( self.uiPath_fileList[ self.currentTab ], query=True, selectIndexedItem=True)[0]
					mc.textScrollList( self.uiPath_fileList[ self.currentTab ], edit = True, removeItem = filename)
					
					if curSel > 1:
						curSel -= 1
					
					curSel = mc.textScrollList( self.uiPath_fileList[ self.currentTab ], edit=True, selectIndexedItem = curSel)
                                        self.fileSelected()
                                        #if self.mode == 0:
                                        #    mc.textScrollList( self.uiPath_namespaceList[ self.currentTab ], edit = True, removeAll = True)
					print "# deleteSelectedFile >> File was successfully deleted: " + filepath,
		else:
			print "# deleteSelectedFile >> file doesn't exist: " + filepath,

			
		
		
	def listPaieFiles(self):
		'''Returns a list of all files in current tab path names *[self.fileExt]'''
		path = self.getCurrentPath()
		
		if os.path.isdir(path):
			dirFiles = os.listdir(path)
			paieFiles = []
			for entry in dirFiles:
				extSplit = os.path.splitext(entry)
				if extSplit[1] == self.fileExt:
					paieFiles.append(extSplit[0])
					
			paieFiles.sort()
			return paieFiles
		else:
			print "# PaieGUI.listPaieFiles >> No directory matching path", 
			return []
		
		
		
	def applyBrowsePath(self, *args): # catch def for windows file browser. Can maybe be omitted in python though
		self.setNewPath( args[0] )
		
	
		
		
		
	### GUI COMMANDS 
	############################################################################
		
	def addNewTab(self):
		defaultPath = mc.internalVar(userAppDir=True)
		mc.optionVar(stringValueAppend = (self.optVar_path, defaultPath))
		self.addListElement()
		pathCount = self.getPathCount()
		self.makeTab( pathCount - 1 )
		mc.tabLayout(self.uiPath_tabs, edit=True, selectTabIndex = self.currentTab+1)
		
		
		
	def removeTab(self):
		pathArraySize = self.getPathCount()
		if pathArraySize == 0 or pathArraySize == 1:
			print "# PaieGUI.removeTab >> You can't delete last tab. Sorry",
		else:
			mc.optionVar(removeFromArray = (self.optVar_path, self.currentTab) )
			self.removeListElement()
			if self.currentTab > 0:
				self.currentTab -= 1
			self.refreshGUI()
		
		
		
	def refreshGUI(self):
		# This is crucial for not to crash Maya when switching import/export mode
		mc.evalDeferred( lambda *args: self.makeGUI() )
		mc.evalDeferred( lambda *args: self.__updateWidth() )
		
		
	def __updateWidth(self):
		if platformCase == "gnu": 	# Forcing update on Linux
			oldWidth = mc.window("PaieGUI", query=True, width=True)
			mc.evalDeferred('mc.window("PaieGUI", edit=True, width= ' + str(oldWidth + 1) + ' )')
			mc.evalDeferred('mc.window("PaieGUI", edit=True, width= ' + str(oldWidth) + ' )')
		
		
	def browseFolders(self):

		if platformCase == "ms":
			version = mc.about(version=True)
			
			print "# PaieGUI.browseFolders >> Maya version: ", version
			mayaWorkspace = mc.workspace(q=True, dir=True)
			mc.workspace(dir= self.getCurrentPath() )
			mc.fileBrowserDialog(m = 4, fc = lambda *args: self.applyBrowsePath(*args), ft="directory", an="Set Work Dir", om="Import")
			mc.workspace(dir= mayaWorkspace)
				
		else:
			mayaWorkspace = mc.workspace(q=True, dir=True)
			mc.workspace(dir = self.getCurrentPath() )
			self.fileBrowserMelWrap()
			mc.workspace(dir= mayaWorkspace)
		
		
	def fileBrowserMelWrap(self):
		
		pyCodeList = []
		
		pyCodeList.append("paie = __import__('" + __name__ + "')")
		pyCodeList.append("pGui = " + __name__ + ".gGuiRef")
		pyCodeList.append("pGui.setNewPath('\" + $path + \"')")
		pyCodeList.append("pGui = 'detaching'")
			
		pyCode = '\\n'.join(pyCodeList)
		
		makeCallbackProc_evalString = '''
		global proc myCallback(string $path, string $type) {
			//print ("path = " + $path + "\\n");
			//print ("type = " + $type + "\\n");
			string $pyCmd = "''' + pyCode + '''";
			python($pyCmd);
		}
		'''
		
		mm.eval( makeCallbackProc_evalString )
		mm.eval('fileBrowser "myCallback" "Select Directory" "" 4;')
		
	
		
				
	def fileSelected(self, *args):
		selFile = mc.textScrollList( self.uiPath_fileList[ self.currentTab ], query=True, selectItem=True )

		if selFile != None:
			selFile = selFile[0]
			
			if self.mode == 1: # Import
				path = self.getCurrentPath()
				
				wrapperObj = DataWrapper()
				loadVal = wrapperObj.load( path + "/" + selFile + self.fileExt )
				if loadVal:
					namespaces = wrapperObj.dataObj.listNamespaces()
					fileInfo = wrapperObj.dataObj.listHeader()
					
					mc.textScrollList(self.uiPath_namespaceList[ self.currentTab ], edit=True, removeAll=True)
					if len(namespaces) == 1:
						mc.textScrollList( self.uiPath_namespaceList[ self.currentTab ], edit = True, append = namespaces[0])
						mc.textScrollList( self.uiPath_namespaceList[ self.currentTab ], edit = True, selectItem = namespaces[0])
					else:
						for ns in namespaces:
							mc.textScrollList( self.uiPath_namespaceList[ self.currentTab ], edit=True, append= ns)
						
					mc.scrollField( self.uiPath_fileInfo[ self.currentTab ], edit=True, clear=True)
					for infoLine in fileInfo:
						mc.scrollField( self.uiPath_fileInfo[ self.currentTab ], edit=True, insertText = infoLine + "\n" )
		
				else: # For unsupported struct versions
					mc.textScrollList(self.uiPath_namespaceList[ self.currentTab ], edit=True, removeAll=True)
					mc.scrollField( self.uiPath_fileInfo[ self.currentTab ], edit=True, clear=True)
					mc.scrollField( self.uiPath_fileInfo[ self.currentTab ], edit=True, insertText = "Unsupported Version \nThis file cannot be used\nFile Version:\t" + str(wrapperObj.loadedVersion) )
					
					
			else: # Export
				mc.textFieldGrp( self.uiPath_filename[ self.currentTab ], edit=True, text = selFile )
		else:
			print "# paieGUI.fileSelected >> FileSelected run without selection."
	
			
			
			
			
	def updateFilelist(self):
		paieFiles = self.listPaieFiles()
		if paieFiles != 0:
			mc.textScrollList(self.uiPath_fileList[ self.currentTab ], edit=True, removeAll=True)
			for f in paieFiles:
				mc.textScrollList(self.uiPath_fileList[ self.currentTab ], edit = True, append = f)
		
	
		
		
	def tabChanged(self):
		selectedTab = mc.tabLayout(self.uiPath_tabs, q=True, selectTabIndex=True)
		self.currentTab = selectedTab -1
		self.updateFilelist()
		
		
		
	def importButton(self):
		
		path = self.getCurrentPath()
		selFileList = mc.textScrollList( self.uiPath_fileList[ self.currentTab ], query=True, selectItem=True )
		selNamespaceList = mc.textScrollList( self.uiPath_namespaceList[ self.currentTab ], query=True, selectItem=True )
		
		if type(selNamespaceList) == type([]) and type(selFileList) == type([]):
			selFile = selFileList[0]
			selNamespace = selNamespaceList[0]

			importData( path + "/" + selFile + self.fileExt, self.selectOrder[ self.currentTab ], namespace = selNamespace, applyAtOrigin = self.applyAtOrigin[ self.currentTab ] )
		else:
			print ""
			print "# PaieGUI.doImport >> You need to select both a file and a namespace to import from",

			
			
			
	

	def exportButton(self):
		comments = mc.scrollField(self.uiPath_comments[ self.currentTab ], query=True, tx=True)
		filename = mc.textFieldGrp(self.uiPath_filename[ self.currentTab ], query=True, tx=True)
		try:
			comments.decode("ascii")
			filename.decode("ascii")
		
			
			path = self.getCurrentPath()
			filepath = path + "/" + filename + self.fileExt
			
			fileSplit = filename.split(".")
			if len(fileSplit) > 1:
				if fileSplit[-1] == self.fileExt[1:]:
					filepath = path + "/" + filename
	
			if self.exportType[ self.currentTab ] == 2:
				filetype = 'pose'
			else:
				filetype = 'anim'
				
			exportTimelineVal = self.exportTimeline[ self.currentTab ]
				
			if filename != "":
				exportData( filepath, filetype, exportTimeline = exportTimelineVal, userInput = comments)
				self.updateFilelist()
			else:
				raise StandardError, "# PaieGUI.exportButton >> You need to write a filename"
				
		except UnicodeEncodeError:
			print "# PaieGUI.exportButton >> Please don't use any non-unicode characters",
			
		except StandardError, arg:
			print arg
			
			
			

	
		
		
		

def __fixPath(filePath):

        try:
		filePath.decode("ascii")
	except UnicodeError:
		raise StandardError, "# fixPath >> Path can't contain non-unicode characters"
	
	### Fix file extension
	if filePath == '':
		print '# fixPath >> No path was given. Defaulting to local maya dir',
		return (mc.internalVar(userAppDir=True) + 'paieDefault.' + "xad")
			
	else:
		if platformCase == "ms":
			splitList = filePath.split('\\')
		else:
			splitList = filePath.split('/')
		
		splitList = splitList[len(splitList)-1].split('.')
	
		if len(splitList) == 1:
			return (filePath + '.xad')
	
		elif splitList[-1] != "xad":
			return filePath + ".xad"
		
		else:
			return filePath
		
		
		
def __checkFile(filePath):

	filename = filePath.split("/")[-1]
	path = filePath[ : len(filename) * -1 ]
	
	if not os.access(path, os.W_OK):
		raise StandardError, "# CheckFile >> You do not have write permissions for this directory"
		
	proceed = os.path.isfile( filePath )

	if proceed == 1:
		proceed = mc.confirmDialog( title="File exist", message = "File already exist. Overwrite it?", button = ["Yes", "No"], defaultButton = "Yes", cancelButton = "No", dismissString = "No")

	if proceed == "Yes" or proceed == 0:
		return 'Yes'
	else:
		return 'No'
	
		
		
		
def __getSelection():
	curSelection = mc.ls(sl=True, long=True)
	
	if type(curSelection) != type([]):
		return 0
		
	elif len(curSelection) != 0:
		try:
			mc.undoInfo(stateWithoutFlush=False)
			
			# Expand through sets
			mc.select(curSelection, r=True)
			selWithSets = mc.ls(sl=True, long=True)
			
			# Revert to original selection
			mc.select(curSelection, noExpand=True)
			
			return selWithSets
		finally:
			mc.undoInfo(stateWithoutFlush=True)
	else:
		return 0
	
	
	
	

	
	
def __checkForClashingNames(selList):
	
	if type(selList) != type([]):
		raise StandardError, "# checkForClashingNames >> Input isn't a list"
	
	nameList = []
	for j in selList:
		nameList.append(j.split("|")[-1])

	nameListSet = list(set(nameList))
	if len( nameList ) != len( nameListSet ):
		
		clashedNames = ''
		d = []
		for i in nameList:
			if i in d:
				clashedNames += i + "\n"
			else:
				d.append(i)
		raise StandardError, "# checkForClashingNames >> Selection contains non-unique naming. This isn't tollerated\n" + clashedNames
	
	return 1
	
	
	
	
	
def __checkNamespaceCount(selList):
	# checking namespace count in selection
	namespaceList = []
	iter = range(0, len(selList) )
	for i in iter:
		
		objWithNamespace = selList[i].split("|")[-1]		# gets last obj in path
		split = objWithNamespace.split(":")
		
		if len(split) != 1:
			# get whole namespace
			objName = objWithNamespace.split(":")[-1]		# strips obj from namespace
			nSpace = objWithNamespace[ : len(objName) * -1]		# gets full namespace
			
			if nSpace not in namespaceList:
				namespaceList.append(nSpace)
		else:
			if 'none' not in namespaceList:
				namespaceList.append("none")
				

	if len(namespaceList) > 1:
		print "# paie.__checkNamespaceCount >> List of namespaces: ", namespaceList,
		raise StandardError, "# importData >> Importing onto multiple namespaces is not supported. Check your selection"

	
	
	
	
	


def exportData(filePath, dataType, attrsType='keyable', exportTimeline=1, startFrame=None, endFrame=None, objs=None, userInput=None):
	'''
	filepath: full path and filename to export to
	dataType: 'anim' = include animation data, 'pose' forces only attribute values to be stored
	selectOrder: when importing, 1 = mathing on selection order, 0 = mathing on names
	startFrame: first frame to export
	endFrame: last frame to export
	userInput: possible user comments on the exported file
	'''
	try:	

		# Checking userInput for non-unicode characters
		if userInput != None:
			try:
				userInput.decode("ascii")
			except UnicodeDecodeError:
				raise UnicodeDecodeError, "# exportData >> input: userInput contains non-unicode characters. Please don't"
		else:
			userInput = ''
			
		dataType = dataType.lower()
		if dataType != "anim" and dataType != "pose":
			raise StandardError, "# exportData >> input: 'dataType' is wrong. Should be either 'anim' or 'pose'"
		
		attrsType = attrsType.lower()
		if attrsType != 'keyable' and attrsType != 'all':
			raise StandardError, "# exportData >> input: 'attrsType' is wrong. Should be either 'keyable' or 'all'"
			
		if filePath == None:
			raise StandardError, "# exportData >> input: 'filePath' empty"
			
		if objs == None:
			objs = __getSelection()
			if objs == 0:
				raise StandardError("# exportData >> You need to make a selection")
				
		__checkForClashingNames(objs)
		
		if exportTimeline == 1:
			if startFrame == None:
				startFrame = mc.playbackOptions( q=True, minTime=True )
			if endFrame == None:
				endFrame = mc.playbackOptions( q=True, maxTime=True )
		else:
			if startFrame == None:
				startFrame = mc.findKeyframe(objs, which='first')
			if endFrame == None:
				endFrame = mc.findKeyframe(objs, which='last')
			
				
		fixedPath = __fixPath(filePath)
		
		if __checkFile(fixedPath) == 'Yes':

			wrapperObj = DataWrapper()
			
			if wrapperObj.getData(objs, startFrame, endFrame, dataType, attrsType, userInput):
				wrapperObj.save(fixedPath)
				wrapperObj.clear()
			else:
				raise StandardError, "# exportData >> Could not get any data from selected objects"
			
		else:
			print "# exportData >> Export was cancelled",
				
	except StandardError, arg:
		mc.confirmDialog( title='Error', message=arg.__str__(), button='OK' )
		print "# PAIE.Error >> Here's the deal:"
		#print arg,
		traceback.print_exc()
		return 0
		
	except UnicodeDecodeError, UnicodeError:
		mc.confirmDialog( title='Error', message="# exportData >> Non-unicode characters aren't supported. Stop using them!", button='OK' )
		return 0
		
		
		
		
		
def importData(filepath, selectOrder, startFrame=None, namespace = "none", applyAtOrigin = None, selList = None):
	'''
	Filepath:     	full path to .xad file
	selectOrder:  	bool argument setting selection Order mode on/off
	Startframe:   	frame number on which to import the file data (Defaults to current frame)
	namespace:    	namespace in file to import from (Defaults to 'none')
	selList:      	selection list input for commandline usage (defaults to current selection)
	'''
	
	
	
	if debugger == 2:
		print ""
		print "# import start: ".ljust(30), time.clock()
	
		
	try:
		fixedPath = __fixPath(filepath)
		wrapperObj = DataWrapper()
		
		if not wrapperObj.load(fixedPath):
			print ""
			print "# importData >> File was empty. Wtf?!",
			
		else:

                        if startFrame == None:
                            if applyAtOrigin:
                                startFrame = wrapperObj.dataObj.getHeaderAttr('startframe')
                                print "# importData >> Applying data at original startframe: ", startFrame
                            else:
                                startFrame = mc.currentTime(query=True)
			
			if selList == None:
				selList = __getSelection()
			
			if selList == 0:
				raise StandardError, "# importData >> Selection list is empty. Select some objects to import on, please"
				
				
			__checkForClashingNames(selList)
			
			__checkNamespaceCount(selList)
				
			# Disable autoKeyframe (waste of time if enabled)
			if wrapperObj.dataObj.getHeaderAttr('filetype') == 'anim':
				try:
					mc.undoInfo(stateWithoutFlush=False)
			
					autoKeyState = mc.autoKeyframe(q=True, state=True)
					mc.autoKeyframe(state=0)
				
				finally:
					mc.undoInfo(stateWithoutFlush=True)
				
			
			### Writing to scene!
			try:
				wrapperObj.writeToScene(selList, selectOrder, namespace, startFrame)
			finally:
				# Enable autoKeyframe if it was previously enabled
				if wrapperObj.dataObj.getHeaderAttr('filetype') == 'anim':
					if autoKeyState == 1:
						try:
							mc.undoInfo(stateWithoutFlush=False)
							mc.autoKeyframe(state=1)
						
						finally:
							mc.undoInfo(stateWithoutFlush=True)
				wrapperObj.dataObj.clear()
				wrapperObj.clear()
				
			if debugger == 2:
				print "# import end: ".ljust(30), time.clock()
			
				
	except (StandardError, KeyboardInterrupt), arg:
		mc.confirmDialog( title='Error', message = arg.__str__() , button='OK' )
		print arg,
		return 0
		
	else:
		print "# Import was successfull",
		return 1
		
		
		
		
def GUI():
	global gGuiRef
	
	try:
		gGuiRef = PaieGUI()
		return gGuiRef
	except:
		print ""
		traceback.print_exc()
		print "# paie.GUI >> Caught by GUI()"
	
		
