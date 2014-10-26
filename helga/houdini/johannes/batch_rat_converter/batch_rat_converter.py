#!usr/bin/env/python

import os
import subprocess
import signal
import sys

from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import uic

from PyQt4.QtGui import *
from PyQt4.QtCore import *

import Tkinter
import tkFileDialog

from PIL import Image
import multiprocessing
import threading

form_class, base_class = uic.loadUiType("media/rat_converter.ui")

MODE_TO_BPP = {'1':1, 'L':8, 'P':8, 'RGB':24, 'RGBA':32, 'CMYK':32, 'YCbCr':24, 'I':32, 'F':32}
INDEX_TO_NAME = {0:'8 bit', 1:'16 bit unsigned int', 2:'16 bit floating point', 3:'32 bit'}
NAME_TO_COMMAND = {'8 bit':'8', '16 bit unsigned int':'16', '16 bit floating point':'half', '32 bit':'float'}

# Worker Thread For Conversion
class ConvertThread(QThread):

    def __init__(self, iconvert_path, source_paths, dest_path, ext_to_bit):
        super(ConvertThread, self).__init__()

        self.iconvert_path = iconvert_path
        self.source_paths = source_paths
        self.ext_to_bit = ext_to_bit
        self.dest_path = dest_path


    def run(self):
        for path in self.source_paths:

            img_full_path = str(path.replace('\\', '/'))

            dst_full_path = ''
            if(len(self.dest_path)==0):
                dst_full_path = str(img_full_path.rsplit('.', 1)[0] + '.rat')
            else:
                dst_full_path = str(self.dest_path) + '/' + str(img_full_path.rsplit('/')[-1].rsplit('.', 1)[0] + '.rat')
            
            bit_depth = str(self.get_image_bit_depth(img_full_path))

            color_correction = 'auto' if((bit_depth=='8' or bit_depth=='16') and not img_full_path.endswith('.tga')) else 'off'
            #if(bit_depth=='8' or bit_depth=='16'):
            #    color_correction = 'on' 
            #else:
            #    color_correction = 'off'

            commandline = str(self.iconvert_path + ' -d ' + bit_depth + ' ' + '-g ' + color_correction + ' ' + '\"' + img_full_path + '\"' + ' ' + '\"'+ dst_full_path + '\"' + '\n')
            print(img_full_path.rsplit('/')[-1] + ' --> ' + dst_full_path.rsplit('/')[-1] + ' (Bit Depth: ' + bit_depth + ', Color Correction: ' + color_correction + ')')

            subprocess.call(commandline, shell=True)

            self.emit(SIGNAL('progressbar_plus'))


    def get_image_bit_depth(self, path):
        splitted_path = path.rsplit('.')
        extension = splitted_path[len(splitted_path)-1]

        return self.ext_to_bit[extension]


# Main Class
class RatConverter(base_class, form_class):

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)

        self.setupUi(self)
        self.setup_ui()


    def setup_ui(self):
        self.button_iconvert_path.clicked.connect(self.set_iconvert_path)
        self.button_destination_path.clicked.connect(self.set_destination_path)
        self.button_batch_convert.clicked.connect(self.batch_convert_threaded)
        self.button_remove_source.clicked.connect(self.remove_source)
        self.button_remove_target.clicked.connect(self.remove_target)

        self.setAcceptDrops(True)

        self.model_ext = QStandardItemModel()

        self.thread_count.setMaximum(multiprocessing.cpu_count())
        self.thread_count.setValue(int(multiprocessing.cpu_count()/2))
        
        self.add_bit_depth.insertItem(0,'8 bit')
        self.add_bit_depth.insertItem(1,'16 bit unsigned int')
        self.add_bit_depth.insertItem(2,'16 bit floating point')
        self.add_bit_depth.insertItem(3,'32 bit')

        self.add_ext_to_list('exr', 3)
        self.add_ext_to_list('hdr', 3)
        self.add_ext_to_list('jpg', 0)
        self.add_ext_to_list('jpeg', 0)
        self.add_ext_to_list('png', 0)
        self.add_ext_to_list('tga', 0)
        self.add_ext_to_list('tif', 0)
        self.add_ext_to_list('tiff', 0)


    def update_progressbar(self):
        self.progressbar.setValue(self.progressbar.value()+1)


    def set_iconvert_path(self):
        filetypes = [('All files', '*'), ('iconvert', 'iconvert.exe')]

        Tkinter.Tk().withdraw()
        in_path = tkFileDialog.askopenfilename(filetypes=filetypes, initialfile='iconvert.exe', title='Set iconvert path')
        
        self.path_iconvert.setText(in_path)


    def set_destination_path(self):
        Tkinter.Tk().withdraw()
        in_path = tkFileDialog.askdirectory(mustexist=True, title='Set destination path')
        
        self.destination_path.setText(in_path)


    def keyPressEvent(self, event):
        if(event.key()==Qt.Key_Return):
            self.add_ext()
            #self.add_extension()
        event.accept()


    def add_ext(self):
        file_ext = str(self.add_extension.text())
        self.add_ext_to_list(file_ext, self.add_bit_depth.currentIndex())
        self.add_extension.setText('')


    def add_ext_to_list(self, file_ext, bit):     
        if(len(file_ext)==0):
            return

        # check if item already in the listview
        for row in range(self.model_ext.rowCount()):
            item = self.model_ext.item(row).text()
            if(item == file_ext):
                return

        self.bit_depth.addItem(INDEX_TO_NAME[bit])
        
        while(file_ext.startswith('.')):
            file_ext = ext[1:]

        item = QStandardItem(file_ext)
        item.setColumnCount(2)
        item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)

        check = Qt.Checked
        item.setData(QVariant(check), Qt.CheckStateRole)

        self.model_ext.appendRow(item)
        self.list_extensions.setModel(self.model_ext)


    def batch_convert_threaded(self):
        iconvert_path = '\"' + self.path_iconvert.text() + '\"'

        self.threads = []
        all_paths = []

        nthreads = int(self.thread_count.value())

        # get all target paths
        for item_row in range(self.target_list.count()):
            all_paths.append(str(self.target_list.item(item_row).text()).replace('\\', '/'))

        chunk_count = int(len(all_paths)/nthreads)
        self.progressbar.setValue(0)
        self.progressbar.setMaximum(len(all_paths))

        # split all paths and send them to threads
        for thread_nr in range(nthreads):
            if(thread_nr == nthreads-1):
                paths = all_paths[thread_nr*chunk_count:]
            else:
                paths = all_paths[thread_nr*chunk_count:thread_nr*chunk_count+chunk_count]

            thread = ConvertThread(iconvert_path, paths, self.destination_path.text(), self.build_ext_to_bit())

            QObject.connect(thread, SIGNAL('progressbar_plus'), self.update_progressbar, Qt.QueuedConnection)

            self.threads.append(thread)
            thread.start()


    def build_ext_to_bit(self):
        ext_to_bit={}

        for row in range(self.model_ext.rowCount()):
            ext = str(self.model_ext.item(row).text())
            bit = str(self.bit_depth.item(row).text())
            ext_to_bit[ext] = NAME_TO_COMMAND[bit]

        return ext_to_bit


    def remove_source(self):
        selection = self.source_list.selectedItems()

        for item in selection:
            row = self.source_list.row(item)
            self.source_list.takeItem(row)


    def remove_target(self):
        selection = self.target_list.selectedItems()

        for item in selection:
            row = self.target_list.row(item)
            self.target_list.takeItem(row)


    # Drop Event Handler
    def dropEvent(self, event):
        for url in event.mimeData().urls():
            url_str = str(url.toLocalFile())

            if(os.path.isfile(url_str)):
                if(self.checkFileIsImg(url_str)):
                    self.insert_in_qlistwidget(url_str, self.source_list)
                    self.insert_in_qlistwidget(url_str, self.target_list)

            elif(os.path.isdir(url_str)):
                self.insert_in_qlistwidget(url_str, self.source_list)
                images = self.get_images_from_folder(url_str)

                if(len(images) == 0):
                    print('No images in ' + url_str)

                for image in images:
                    self.insert_in_qlistwidget(image, self.target_list)

            else:
                print('Neither Folder Nor File')


    # Drag Event Handler
    def dragEnterEvent(self, event):
        if(event.mimeData().hasUrls()):
            event.accept()
        else:
            event.ignore()


    def checkFileIsImg(self, item):
        splitted_filename = item.split('.')
        extension = splitted_filename[len(splitted_filename)-1]

        img_formats = []

        for row in range(self.model_ext.rowCount()):
            item = self.model_ext.item(row)
            
            if(item.checkState()==2):
                img_formats.append(item.text())

        if(extension in img_formats):
            return True


    def insert_in_qlistwidget(self, item, widget):
        # check if item already in the qlistwidget
        for row in range(widget.count()):
            widget_item = widget.item(row)

            if(item == widget_item.text()):
                return

        widget.addItem(item)


    def get_images_from_folder(self, folder):
        if(os.path.isdir(folder) == False):
            print(folder + ' is not a directory')

        # Get images from folder
        folder_content = os.listdir(folder)

        images = []
        for item in folder_content:

            item_full_path = folder + '/' + item

            if(os.path.isdir(item_full_path)):
                images = self.get_images_from_folder(item_full_path) + images

            if(self.checkFileIsImg(item)):
                images.append(item_full_path)

        return images


if(__name__ == '__main__'):
    app = QtGui.QApplication(sys.argv)
    app.setStyle('plastique')
    window = RatConverter(None)
    window.show()

    print('Starting RatConverter')
    app.exec_()
    print('Closing RatConverter')