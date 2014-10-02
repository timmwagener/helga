#!usr/bin/env/python

import sys
import os
import subprocess

from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import uic

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from PIL import Image
import multiprocessing
from multiprocessing import Pool
from multiprocessing import Process
import threading

form_class, base_class = uic.loadUiType("media/rat_converter.ui")

MODE_TO_BPP = {'1':1, 'L':8, 'P':8, 'RGB':24, 'RGBA':32, 'CMYK':32, 'YCbCr':24, 'I':32, 'F':32}
INDEX_TO_BIT_DEPTH = {0:, 1:, 2:, 3:}

class ConvertThread(threading.Thread):

    def __init__(self, iconvert_path, source_paths):

        super(ConvertThread, self).__init__()

        self.iconvert_path = iconvert_path
        self.source_paths = source_paths

    def run(self):

        for path in self.source_paths:

            img_full_path = str(path.replace('\\', '/'))

            dst_full_path = str(img_full_path.rsplit('.', 1)[0] + '.rat')

            commandline = str(self.iconvert_path + ' -d ' + str(self.get_image_bit_depth(img_full_path)) + ' ' + '-g off ' + '\"' + img_full_path + '\"' + ' ' + '\"'+ dst_full_path + '\"' + '\n')

            subprocess.call(commandline, shell=True)

            print path

    def get_image_bit_depth(self, path):

        if(path.endswith('.exr')):
            return 32

        else:
            return 8

        '''
        data = Image.open(path)
        print MODE_TO_BPP[data.mode]/3

        return MODE_TO_BPP[data.mode]/3
        '''


class RatConverter(base_class, form_class):

    model_ext = QStandardItemModel()

    def __init__(self, parent=None):
        
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.button_batch_convert.clicked.connect(self.batch_convert_threaded)
        self.button_remove_source.clicked.connect(self.remove_source)
        self.button_remove_target.clicked.connect(self.remove_target)

        self.setAcceptDrops(True)

        self.thread_count.setMaximum(multiprocessing.cpu_count())
        self.thread_count.setValue(int(multiprocessing.cpu_count()/2))
        
        self.add_bit_depth.insertItem(0,'8 bit')
        self.add_bit_depth.insertItem(1,'16 bit unsigned int')
        self.add_bit_depth.insertItem(2,'16 bit floating point')
        self.add_bit_depth.insertItem(3,'32 bit')

        self.set_initial_filetypes()


    def set_initial_filetypes(self):

        self.add_ext_to_list('exr', 3)
        self.add_ext_to_list('hdr', 3)
        self.add_ext_to_list('jpg', 0)
        self.add_ext_to_list('jpeg', 0)
        self.add_ext_to_list('png', 0)
        self.add_ext_to_list('tga', 0)
        self.add_ext_to_list('tif', 0)
        self.add_ext_to_list('tiff', 0)


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

        switch(bit) {
            case 0:
                self.bit_depth.addItem('8 bit')
                break
            case 1:
                self.bit_depth.addItem('16 bit unsigned int')
                break
            case 2:
                self.bit_depth.addItem('16 bit floating point')
                break
            case 3:
                self.bit_depth.addItem('32 bit')
                break
        }
        
        
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

        threads = []
        all_paths = []

        nthreads = int(self.thread_count.value())

        # get all target paths
        for item_row in range(self.target_list.count()):
            all_paths.append(str(self.target_list.item(item_row).text()).replace('\\', '/'))


        chunk_count = int(len(all_paths)/nthreads)

        # split all paths and send them to threads
        for thread_nr in range(nthreads):
            if(thread_nr == nthreads-1):
                paths = all_paths[thread_nr*chunk_count:]
            else:
                paths = all_paths[thread_nr*chunk_count:thread_nr*chunk_count+chunk_count]

            print paths

            thread = ConvertThread(iconvert_path, paths)
            threads.append(thread)
            thread.start()
        
    def f(self, x):

        print str(x*x)

    def initializer(self, inst):
        inst.start_process()

    def batch_convert(self, id):

        iconvert_path = '\"' + self.path_iconvert.text() + '\"'

        current_img_number = 1
        for item_row in range(self.target_list.count()):

            img_full_path = str(self.target_list.item(item_row).text().replace('\\', '/'))

            dst_full_path = str(img_full_path.rsplit('.', 1)[0] + '.rat')

            commandline = ICONVERT_PATH + ' -d ' + str(self.get_image_bit_depth(img_full_path)) + ' ' + '-g off ' + '\"' + img_full_path + '\"' + ' ' + '\"'+ dst_full_path + '\"' + '\n'

            self.progressbar.setFormat('Converting ' + img_full_path.rstrip('/')[0])

            print(commandline)

            subprocess.call(commandline, shell =True)

            self.progressbar.setValue((current_img_number*100)/self.target_list.count())
            current_img_number += 1

            pass

        self.progressbar.setFormat('Done.')


    def convert_file(self, row):

        print "convert_file"

        img_full_path = str(self.target_list.item(item_row).text().replace('\\', '/'))

        dst_full_path = str(img_full_path.rsplit('.', 1)[0] + '.rat')

        commandline = ICONVERT_PATH + ' -d ' + str(self.get_image_bit_depth(img_full_path)) + ' ' + '-g off ' + '\"' + img_full_path + '\"' + ' ' + '\"'+ dst_full_path + '\"' + '\n'

        self.progressbar.setFormat('Converting ' + img_full_path.rstrip('/')[0])

        print(commandline)

        subprocess.call(commandline, shell =True)

        self.progressbar.setValue((current_img_number*100)/self.target_list.count())


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
                    print "No images in " + url_str

                for image in images:
                    self.insert_in_qlistwidget(image, self.target_list)

            else:
                print "Neither Folder Nor File"


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
            item = self.model_ext.item(row).text()

            img_formats.append(item)

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
            print folder + ' is not a directory'

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

    def get_image_bit_depth(self, path):

        if(path.endswith('.exr')):
            return 32

        else:
            return 8

        '''
        data = Image.open(path)
        print MODE_TO_BPP[data.mode]/3

        return MODE_TO_BPP[data.mode]/3
        '''

if(__name__ == '__main__'):

    app = QtGui.QApplication(sys.argv)
    app.setStyle('plastique')
    window = RatConverter(None)
    window.show()

    print "Starting App"
    app.exec_()
    print "Closing App"