#!/usr/bin/env python2


#Author
#------------------------------------------------
"""
Timm Wagener
www.timmwagener.com
wagenertimm@gmail.com

Usage:
Copy this script into Nukes script editor and execute it.
"""


#Import
#------------------------------------------------
#python
import sys
import time
import os
import logging
#PySyide
from PySide.QtGui import *
from PySide.QtCore import *
#nuke
import nuke






#MaskThread
#------------------------------------------------

class MaskThread(QThread):
	"""
		Thread that recognizes files in a source directory (photo_dir) which do not exist in
		a target dir (masks_dir). If it found such files, it will grab the specified read & 
		write nodes in the comp the script was run from, replace their file names and run the comp.

		The comp is expected to generate the key.

		It is always possible during runtime to delete files in the target folder to recompute them,
		or change the comp script on the fly.
	"""

	def __init__(self,
				starter_widget,
				parent = None):
		"""
			MaskThread
		"""


		QThread.__init__(self, parent)


		#starter_widget
		self.starter_widget = starter_widget

		#photo_dir
		self.photo_dir = self.get_photo_dir()
		#masks_dir
		self.masks_dir = self.get_masks_dir()

		#read_node_name
		self.read_node_name = self.get_read_node_name()
		#write_node_name
		self.write_node_name = self.get_write_node_name()


		#photos_images_list
		self.photos_images_list = []
		#photos_images_path_list
		self.photos_images_path_list = []

		#masks_images_list
		self.masks_images_list = []
		#masks_images_path_list
		self.masks_images_path_list = []


	def get_images_list(self, root_dir):
		"""
			Crawl root directory and return lists of pathes and file names.
		"""

		file_name_list = []
		file_path_list = []
		for root_path, sub_folders, temp_file_list in os.walk(root_dir):
			for file_name in temp_file_list:
				if(file_name.split('.')[-1] == 'jpg' or file_name.split('.')[-1] == 'JPG'):
					file_name_list.append(file_name)
					file_path_list.append(os.path.join(root_path, file_name).replace('\\', '/'))

		return [file_name_list, file_path_list]


	def update_data(self):
		"""
			Set instance variables from widget that was passed on init.
		"""

		#read_node_name
		self.read_node_name = self.get_read_node_name()
		#write_node_name
		self.write_node_name = self.get_write_node_name()

		#photo_dir
		self.photo_dir = self.get_photo_dir()
		#masks_dir
		self.masks_dir = self.get_masks_dir()


	def run_checks(self):
		"""
			Set of checks to determine wether a creation of masks is possible or not.
		"""

		#read_node_name
		if not(nuke.executeInMainThreadWithResult(nuke.exists, (self.read_node_name))):
			print('Read node with name: {0} does not exist. Returning...'.format(self.read_node_name))
			return False

		#write_node_name
		if not(nuke.executeInMainThreadWithResult(nuke.exists, (self.write_node_name))):
			print('Write node with name: {0} does not exist. Returning...'.format(self.write_node_name))
			return False

		#photo_dir
		if not(os.path.isdir(self.photo_dir)):
			print('Photo dir with name: {0} does not exist. Returning...'.format(self.photo_dir))
			return False

		#masks_dir
		if not(os.path.isdir(self.masks_dir)):
			print('Masks dir with name: {0} does not exist. Returning...'.format(self.masks_dir))
			return False

		return True


	def get_read_node_name(self):

		return str(self.starter_widget.le_read_node_name.text())


	def get_write_node_name(self):

		return str(self.starter_widget.le_write_node_name.text())


	def get_photo_dir(self):

		return str(self.starter_widget.le_photo_dir.text())


	def get_masks_dir(self):

		return str(self.starter_widget.le_masks_dir.text())


	def update_masks(self):
		"""
			Update masks
		"""

		#lists unequal == check entries
		for photo in self.photos_images_list:

			print('photo: {0}'.format(photo))

			#suppress_thread checked?
			if(self.starter_widget.chkbx_suppress_thread.isChecked()):
				break

			#update_data
			self.update_data()

			#run_checks
			if not(self.run_checks()):
				break

			#photo in masks lists
			if(photo in self.masks_images_list):
				continue

			#render
			self.render_mask(photo)


	def render_mask(self, image_name):
		"""
			Render mask
		"""


		#read_node
		read_node = nuke.executeInMainThreadWithResult(nuke.toNode, (self.read_node_name))

		#write_node
		write_node = nuke.executeInMainThreadWithResult(nuke.toNode, (self.write_node_name))

		#photo_list_index
		photo_list_index = self.photos_images_list.index(image_name)

		#photo_path
		photo_path = self.photos_images_path_list[photo_list_index]

		#set in read_node
		nuke.executeInMainThreadWithResult(read_node.knob('file').setValue, (photo_path))

		#write_node_file_path
		write_node_file_path = os.path.join(self.masks_dir, image_name).replace('\\', '/')

		#set in write_node
		nuke.executeInMainThreadWithResult(write_node.knob('file').setValue, (write_node_file_path))


		#render
		nuke.executeInMainThreadWithResult(nuke.render, (self.write_node_name, 1, 1, 1))

		#while file not yet created print a queue dot
		while not (os.path.isfile(write_node_file_path)):
			QApplication.processEvents()
			print('.'),
			self.msleep(150)


		#log
		print('Rendered mask: {0}'.format(write_node_file_path))




	def run(self):

		#finish
		print('Hello from run')

		QApplication.processEvents()

		#update_data
		self.update_data()


		#run_checks
		if(self.run_checks()):

			print('photo_dir: {0}'.format(self.photo_dir))

			#get photo and mask lists
			self.photos_images_list, self.photos_images_path_list = self.get_images_list(self.photo_dir)
			self.masks_images_list, self.masks_images_path_list = self.get_images_list(self.masks_dir)

			print(self.photos_images_list)

			#update masks
			self.update_masks()

			#sleep
			#self.msleep(1000)










#ThreadWidget
#------------------------------------------------

class ThreadWidget(QWidget):
	"""
		Main UI to be started in Nuke instance.
	"""

	def __init__(self, parent = None):

		QWidget.__init__(self, parent)


		#Create GUI
		#---------------------------------------------

		#WINDOW_NAME
		self.WINDOW_TITLE = 'Auto Key'
		#AUTO_KEY_VERSION
		self.AUTO_KEY_VERSION = 0.1
		#WINDOW_TITLE
		self.WINDOW_TITLE = self.WINDOW_TITLE +' ' + str(self.AUTO_KEY_VERSION)

		#setTitle
		self.setWindowTitle(self.WINDOW_TITLE)

		

		#btn_set_read_node_name
		self.btn_set_read_node_name = QPushButton('Get Read Node',self)
		#le_read_node_name
		self.le_read_node_name = QLineEdit(self)
		self.le_read_node_name.setPlaceholderText('Read node name')

		#btn_set_write_node_name
		self.btn_set_write_node_name = QPushButton('Get Write Node',self)
		#le_write_node_name
		self.le_write_node_name = QLineEdit(self)
		self.le_write_node_name.setPlaceholderText('Write node name')

		#btn_photo_dir
		self.btn_photo_dir = QPushButton('Get photo directory', self)
		#le_photo_dir
		self.le_photo_dir = QLineEdit(self)
		self.le_photo_dir.setPlaceholderText('Photo Directory')

		#btn_masks_dir
		self.btn_masks_dir = QPushButton('Get masks directory', self)
		#le_masks_dir
		self.le_masks_dir = QLineEdit(self)
		self.le_masks_dir.setPlaceholderText('Masks Directory')

		#chkbx_suppress_thread
		self.chkbx_suppress_thread = QCheckBox('Suppress Thread')
		self.chkbx_suppress_thread.setCheckable(True)
		self.chkbx_suppress_thread.setChecked(False)



		#lyt_widget
		self.lyt_widget = QVBoxLayout()
		#add widgets
		self.lyt_widget.addWidget(self.btn_set_read_node_name)
		self.lyt_widget.addWidget(self.le_read_node_name)
		self.lyt_widget.addWidget(self.btn_set_write_node_name)
		self.lyt_widget.addWidget(self.le_write_node_name)

		self.lyt_widget.addWidget(self.btn_photo_dir)
		self.lyt_widget.addWidget(self.le_photo_dir)
		self.lyt_widget.addWidget(self.btn_masks_dir)
		self.lyt_widget.addWidget(self.le_masks_dir)
		self.lyt_widget.addWidget(self.chkbx_suppress_thread)


		self.setLayout(self.lyt_widget)



		#Thread
		#---------------------------------------------

		#running
		self.running = False

		#thread
		self.thread = MaskThread(self)
		self.thread.started.connect(self.set_running_true)
		self.thread.finished.connect(self.set_running_false)

		#timer
		self.timer = QTimer()
		self.timer.timeout.connect(self.start_thread)
		self.timer.start(2000)


		#Connect GUI
		#---------------------------------------------

		self.btn_set_read_node_name.clicked.connect(self.set_read_node_from_selection)
		self.btn_set_write_node_name.clicked.connect(self.set_write_node_from_selection)
		self.btn_photo_dir.clicked.connect(self.set_photo_dir)
		self.btn_masks_dir.clicked.connect(self.set_masks_dir)





	def set_read_node_from_selection(self):

		try:
			selected_node = nuke.selectedNode()
		except:
			return ''

		selected_node_name = selected_node.name()

		self.le_read_node_name.setText(selected_node_name)


	def set_write_node_from_selection(self):

		try:
			selected_node = nuke.selectedNode()
		except:
			return ''

		selected_node_name = selected_node.name()

		self.le_write_node_name.setText(selected_node_name)


	def set_photo_dir(self):

		self.le_photo_dir.setText(str(QFileDialog.getExistingDirectory()))


	def set_masks_dir(self):

		self.le_masks_dir.setText(str(QFileDialog.getExistingDirectory()))


	def start_thread(self):

		if not(self.running):
			if not(self.chkbx_suppress_thread.isChecked()):
				self.thread.start()

				print('start thread on')
			else:
				#print('thread supressed, only inexpensive timer active')
				pass

		else:
			print('start thread off')

	def set_running_true(self):

		self.running = True
		print('set running True')


	def set_running_false(self):

		self.running = False
		print('set running false')


	def closeEvent(self, event):

		#kill thread
		self.thread.terminate()
		self.thread.wait()
		self.thread.exit()
		print('Thread killed')

		self.timer.stop()
		print('Timer stopped')
		

		#event accept
		event.accept()




#Execute
#------------------------------------------------

if (__name__=='__main__'):
	
	window = ThreadWidget()
	window.show()