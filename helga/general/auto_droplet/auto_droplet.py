

"""
auto_droplet
==========================================

Simple but hopefully helpful module to automatically process several droplets in a certain order.

-----------------------

**Author:** `Timm Wagener <mailto:wagenertimm@gmail.com>`_
"""





#Add relative pathes
#------------------------------------------------------------------

#import
import sys
import os

#tool_root_path
tool_root_path = os.path.dirname(__file__)
sys.path.append(tool_root_path)
#temp
print('Tool Root Path: {0}'.format(tool_root_path))

#lib_path
lib_path = os.path.join(tool_root_path, 'lib')
#py2exe
if not (os.path.isdir(lib_path)):
    lib_path = os.path.join(os.path.dirname(tool_root_path), 'lib')
sys.path.append(lib_path)
#temp
print('Lib Path: {0}'.format(lib_path))


#media_path
media_path = os.path.join(tool_root_path, 'media')
#py2exe
if not (os.path.isdir(media_path)):
    media_path = os.path.join(os.path.dirname(tool_root_path), 'media')

#icons_path
icons_path = os.path.join(media_path, 'icons')

#ui_file_name
ui_file_name = 'auto_droplet.ui'

#ui_path
ui_path = os.path.join(media_path, ui_file_name)










#Globals
#------------------------------------------------------------------

DROPLETS_FILTER_LIST = ['exe']
FILES_FILTER_LIST = ['png', 'jpg', 'exr', 'tga', 'psd', 'tif']






#Import
#------------------------------------------------------------------
#python
import functools
import logging
import subprocess
#PyQt
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import uic


#do_reload
do_reload = True

#convert_functionality
import convert_functionality
if (do_reload): reload(convert_functionality)

#auto_droplet_list_widget
from gui import auto_droplet_list_widget
if (do_reload): reload(auto_droplet_list_widget)









#form and base class
form_class, base_class = uic.loadUiType(ui_path)



#AutoDroplet class
#------------------------------------------------------------------
class AutoDroplet(base_class, form_class):
    
    
    def __init__(self, 
                logging_level = logging.DEBUG,
                parent = None):
        """
        AutoDroplet GUI
        """
        
        #base_class
        self.base_class = super(AutoDroplet, self)
        self.base_class.__init__(parent)


        #instance variables
        #------------------------------------------------------------------
        self.title_name = self.__class__.__name__
        self.version = 0.1
        self.title = self.title_name +' ' + str(self.version)

        #convert_functionality
        self.convert_functionality = convert_functionality.ConvertFunctionality()

        
        #logger
        #------------------------------------------------------------------
        #logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logging_level = logging_level
        self.logger.setLevel(self.logging_level)

        #stream_handler
        stream_handler = logging.StreamHandler(sys.stdout)
        #add
        self.logger.addHandler(stream_handler)
        

        

        
        #Init procedure
        #------------------------------------------------------------------
        
        #setupUI
        self.setupUi(self)

        #setup_ui
        self.setup_ui()
        
        #connect_ui
        self.connect_ui()

        #deferred_setup_ui
        self.deferred_setup_ui()

    




    #Startup Methods
    #------------------------------------------------------------------
    
    def setup_ui(self):
        """
        Setup additional UI
        """

        #setup_list_widgets
        self.setup_list_widgets()

        #setup_labels_count
        self.setup_labels_count()

        #setup_progressbar
        self.setup_progressbar()

        #setWindowTitle
        self.setWindowTitle(self.title)


    def connect_ui(self):
        """
        Connect UI
        """

        #btn_convert
        self.btn_convert.clicked.connect(self.convert)

        #btn_stop
        self.btn_stop.clicked.connect(self.convert_functionality.stop)

        #listwdgt_droplets
        self.listwdgt_droplets.customContextMenuRequested.connect(self.listwdgt_droplets_menu)
        self.listwdgt_droplets.sgnl_set_all_label_counts.connect(self.set_all_label_counts)

        #listwdgt_files
        self.listwdgt_files.customContextMenuRequested.connect(self.listwdgt_files_menu)
        self.listwdgt_files.sgnl_set_all_label_counts.connect(self.set_all_label_counts)


        #convert_functionality
        self.convert_functionality.sgnl_increment_progressbar_range.connect(self.increment_progressbar_range)
        self.convert_functionality.sgnl_reset_progressbar_range.connect(self.reset_progressbar_range)

        #threads
        for thread in self.convert_functionality.threads_functionality.get_thread_list():
            #connect
            thread.sgnl_task_done.connect(self.increment_progressbar)


    def deferred_setup_ui(self):
        """
        Deferred setup additional UI. This can be called
        when you need to emit signals after connecting etc.
        """

        #label counts
        self.listwdgt_droplets.sgnl_set_all_label_counts.emit()
        self.listwdgt_files.sgnl_set_all_label_counts.emit()



    def setup_labels_count(self):
        """
        Setup labels for item count.
        """

        #lbl_droplet_count
        self.lbl_droplet_count = QtGui.QLabel()
        self.lyt_droplets.addWidget(self.lbl_droplet_count)

        #lbl_file_count
        self.lbl_file_count = QtGui.QLabel()
        self.lyt_files.addWidget(self.lbl_file_count)


    def setup_list_widgets(self):
        """
        Setup auto droplet list widgets.
        """

        #listwdgt_droplets
        self.listwdgt_droplets = auto_droplet_list_widget.AutoDropletListWidget()
        self.listwdgt_droplets.set_filter_list(DROPLETS_FILTER_LIST)
        self.lyt_droplets.addWidget(self.listwdgt_droplets)
        #settings
        self.listwdgt_droplets.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.listwdgt_droplets.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

        #listwdgt_files
        self.listwdgt_files = auto_droplet_list_widget.AutoDropletListWidget()
        self.listwdgt_files.set_filter_list(FILES_FILTER_LIST)
        self.lyt_files.addWidget(self.listwdgt_files)
        #settings
        self.listwdgt_files.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.listwdgt_files.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)


    def setup_progressbar(self):
        """
        Setup self.progressbar.
        """

        #set min, max and reset
        self.progressbar.setRange(0, 1)
        self.progressbar.setValue(0)

        #log
        self.logger.debug('Progressbar range: {0} - {1}'.format(self.progressbar.minimum(), 
                                                                self.progressbar.maximum()))



    #Right Click Menus
    #------------------------------------------------------------------

    def listwdgt_droplets_menu(self, pos):
        """
        Create right click menu for listwdgt_droplets.
        """

        #context_menu
        context_menu = QtGui.QMenu(parent = self)


        #acn_remove_selected_items
        acn_remove_selected_items = QtGui.QAction('Remove selected items', self)
        acn_remove_selected_items.setObjectName('acn_remove_selected_items')
        acn_remove_selected_items.triggered.connect(self.listwdgt_droplets.remove_selected_items)
        context_menu.addAction(acn_remove_selected_items)


        #separator
        context_menu.addSeparator()
        
        #acn_clear
        acn_clear = QtGui.QAction('Clear', self)
        acn_clear.setObjectName('acn_clear')
        acn_clear.triggered.connect(self.listwdgt_droplets.remove_all_items)
        context_menu.addAction(acn_clear)


        #display
        context_menu.popup(self.listwdgt_droplets.mapToGlobal(pos))


    def listwdgt_files_menu(self, pos):
        """
        Create right click menu for listwdgt_files.
        """

        #context_menu
        context_menu = QtGui.QMenu(parent = self)


        #acn_remove_selected_items
        acn_remove_selected_items = QtGui.QAction('Remove selected items', self)
        acn_remove_selected_items.setObjectName('acn_remove_selected_items')
        acn_remove_selected_items.triggered.connect(self.listwdgt_files.remove_selected_items)
        context_menu.addAction(acn_remove_selected_items)

        
        #separator
        context_menu.addSeparator()


        #acn_clear
        acn_clear = QtGui.QAction('Clear', self)
        acn_clear.setObjectName('acn_clear')
        acn_clear.triggered.connect(self.listwdgt_files.remove_all_items)
        context_menu.addAction(acn_clear)


        #display
        context_menu.popup(self.listwdgt_files.mapToGlobal(pos))
    
    
    
    #Methods
    #------------------------------------------------------------------

    def convert(self):
        """
        Convert
        """

        #droplets_list
        droplets_list = self.listwdgt_droplets.get_items()

        #files_list
        files_list = self.listwdgt_files.get_items()

        #convert
        self.convert_functionality.convert(droplets_list, files_list)



    #Getter & Setter Methods
    #------------------------------------------------------------------

    @QtCore.pyqtSlot()
    def set_all_label_counts(self):
        """
        Set all lbl_counts.
        """

        #set_lbl_droplet_count
        self.set_lbl_droplet_count()

        #set_lbl_file_count
        self.set_lbl_file_count()


    def set_lbl_droplet_count(self):
        """
        Set lbl_droplet_count.
        """

        #item_count
        item_count = self.listwdgt_droplets.count()

        #text
        text = 'Count: {0}'.format(item_count)

        #setTExt
        self.lbl_droplet_count.setText(text)


    def set_lbl_file_count(self):
        """
        Set lbl_file_count.
        """

        #item_count
        item_count = self.listwdgt_files.count()

        #text
        text = 'Count: {0}'.format(item_count)

        #setTExt
        self.lbl_file_count.setText(text)



    #Progressbar Methods
    #------------------------------------------------------------------

    @QtCore.pyqtSlot()
    def increment_progressbar(self, step_size = 1):
        """
        Increment self.progressbar by step_size.
        """

        #current_value
        current_value = self.progressbar.value()
        #if zero set to 1 for more readable maximum checking
        if not (current_value):
            current_value = 1

        #incremented_value
        incremented_value = current_value + step_size

        
        #progressbar full (This should be true on the last job_done signal)
        if (incremented_value == self.progressbar.maximum()):

            #set range
            self.progressbar.setRange(0, 1)
            #reset
            self.progressbar.setValue(0)

            #log
            self.logger.debug('Progressbar reset.')

            #return
            return


        #set
        self.progressbar.setValue(incremented_value)

        #log
        self.logger.debug('Progressbar value: {0}'.format(self.progressbar.value()))


    @QtCore.pyqtSlot()
    def increment_progressbar_range(self, step_size = 1):
        """
        Increment progressbar maximum by one.
        Keep minimum unaffected.
        """

        #current_maximum
        current_maximum = self.progressbar.maximum()

        #incremented_maximum
        incremented_maximum = current_maximum + step_size

        #set range
        self.progressbar.setRange(0, incremented_maximum)

        #log
        self.logger.debug('Progressbar range: {0} - {1}'.format(self.progressbar.minimum(), 
                                                                self.progressbar.maximum()))


    @QtCore.pyqtSlot()
    def reset_progressbar_range(self):
        """
        Reset progressbar range.
        """

        #set min, max and reset
        self.progressbar.setRange(0, 1)
        self.progressbar.setValue(0)

        #log
        self.logger.debug('Progressbar range: {0} - {1}'.format(self.progressbar.minimum(), 
                                                                self.progressbar.maximum()))


    #Test Method
    #------------------------------------------------------------------
    
    def test_method(self):
        """
        Test method
        """

        #log
        self.logger.debug('test_method')




















    