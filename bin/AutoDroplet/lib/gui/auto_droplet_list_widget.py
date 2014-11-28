
"""
auto_droplet_list_widget
==========================================

Subclass of QListWidget to allow for customized drag&drop behaviour
"""












#Import
#------------------------------------------------------------------
#python
import sys
import os
import logging
#PyQt
from PyQt4 import QtGui
from PyQt4 import QtCore








#Globals
#------------------------------------------------------------------











#AutoDropletListWidget class
#------------------------------------------------------------------
class AutoDropletListWidget(QtGui.QListWidget):
    """
    Subclass of QListWidget to allow for Drag&Drop behaviour
    """

    #signals
    sgnl_set_all_label_counts = QtCore.pyqtSignal()



    def __new__(cls, *args, **kwargs):
        """
        AutoDropletListWidget instance factory.
        """

        #auto_droplet_list_widget_instance
        auto_droplet_list_widget_instance = super(AutoDropletListWidget, cls).__new__(cls, args, kwargs)

        return auto_droplet_list_widget_instance

    
    def __init__(self, 
                logging_level = logging.DEBUG,
                parent = None):
        """
        AutoDropletListWidget instance customization.
        """

        #base_class
        self.base_class = super(AutoDropletListWidget, self)
        self.base_class.__init__(parent)
        
            


        #instance variables
        #------------------------------------------------------------------

        #filter_list
        self.filter_list = []

        
        #logger
        #------------------------------------------------------------------
        #logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logging_level = logging_level
        self.logger.setLevel(self.logging_level)
        self.logger.handlers = []

        #stream_handler
        stream_handler = logging.StreamHandler(sys.stdout)
        #add
        self.logger.addHandler(stream_handler)


        #Init procedure
        #------------------------------------------------------------------

        #setup_ui
        self.setup_ui()

        #connect_ui
        self.connect_ui()









    #UI setup methods
    #------------------------------------------------------------------
    
    def setup_ui(self):
        """
        Setup additional UI.
        """

        #setAcceptDrops
        self.setAcceptDrops(True)
        #setDragEnabled
        self.setDragEnabled(True)
        #setDragDropMode
        self.setDragDropMode(QtGui.QAbstractItemView.InternalMove)


    def connect_ui(self):
        """
        Connect UI widgets with slots or functions.
        """
        
        self.connect(self, QtCore.SIGNAL("dropped"), self.set_list_items)



    #Methods
    #------------------------------------------------------------------

    def set_list_items(self, drop_url_list):
        """
        Drop callback. Clears and then sets the items from the drop_url_list.
        """

        #clear
        self.clear()

        #checked_drop_url_list
        checked_drop_url_list = self.check_path_list(drop_url_list)

        #drop_url_stringlist
        drop_url_stringlist = self.list_to_stringlist(checked_drop_url_list)

        #removeDuplicates
        drop_url_stringlist.removeDuplicates()

        #sort
        drop_url_stringlist.sort()

        #set
        self.addItems(drop_url_stringlist)


        #sgnl_set_all_label_counts
        self.sgnl_set_all_label_counts.emit()


    def check_path_list(self, path_list):
        """
        Check l. Does the following:

        1. Resolve directories
        2. Filters against self.filter_list
        """

        #file_list
        file_list = self.resolve_directories(path_list)

        #filtered_file_list
        filtered_file_list = self.filter_file_list(file_list)

        #modified_file_list
        modified_file_list = [self.modify_path(file_path) for file_path in filtered_file_list]

        return modified_file_list
        

    def resolve_directories(self, path_list):
        """
        Resolve all directories. Return list that has only the files
        directly below.
        """

        #file_list
        file_list = []

        #iterate
        for path in path_list:

            #directory
            if (os.path.isdir(path)):

                #iterate path
                for file in os.listdir(path):

                    #file_path
                    file_path = os.path.join(path, file).replace('\\', '/')
                    #append
                    file_list.append(file_path)

            #file
            elif (os.path.isfile(path)):

                #append
                file_list.append(path)

        
        #return
        return file_list


    def filter_file_list(self, file_list):
        """
        Filter stringlist against self.filter_list.
        """

        #filtered_file_list
        filtered_file_list = []

        #iterate
        for file in file_list:

            #file_name, file_extension
            file_name, file_extension = os.path.splitext(file)

            #check
            if (file_extension[1:] in self.filter_list):

                filtered_file_list.append(file)


        #return
        return filtered_file_list


    def modify_path(self, file_path):
        """
        Modify file_path in order to make Photoshop find it.
        """

        #modified_file_path
        modified_file_path = os.path.abspath(file_path)
        
        #return
        return modified_file_path 


    def list_to_stringlist(self, list_to_convert):
        """
        Convert list of string to a QStringList and return it
        """

        #stringlist
        stringlist = QtCore.QStringList()

        #list empty or None
        if not (list_to_convert):
            return stringlist

        
        #iterate and set
        for path in list_to_convert:

            #append
            stringlist.append(str(path))

        return stringlist


    
    #Getter & Setter
    #------------------------------------------------------------------

    def append_filter_list(self, extension):
        """
        Append extension ('exe', 'zip' etc.) to self.filter_list.
        """

        self.filter_list.append(extension)


    def set_filter_list(self, filter_list):
        """
        Set self.filter_list.
        """

        self.filter_list = filter_list


    def get_filter_list(self):
        """
        Return self.filter_list.
        """

        return self.filter_list


    def get_items(self):
        """
        Return list of items as strings.
        """

        #list_widget_item_list
        list_widget_item_list = []
        for index in xrange(self.count()):
            list_widget_item_list.append(self.item(index))
        
        #string_list
        string_list = [str(item.text()) for item in list_widget_item_list]

        #return
        return string_list


    def remove_selected_items(self):
        """
        Remove selected items from list.
        """

        #iterate and remove
        for item in self.selectedItems():

            #log
            self.logger.debug('Remove: {0}'.format(str(item.text())))
            
            #remove
            self.takeItem(self.row(item))


        #sgnl_set_all_label_counts
        self.sgnl_set_all_label_counts.emit()


    def remove_all_items(self):
        """
        Remove all items from list.
        Wraps self.clear to enable call to
        sgnl_set_all_label_counts().
        """

        #clear
        self.clear()

        #sgnl_set_all_label_counts
        self.sgnl_set_all_label_counts.emit()




    #Events
    #------------------------------------------------------------------

    def dragEnterEvent(self, event):
        """
        Accept event if it has pathes.
        """

        if(event.mimeData().hasUrls()):
            event.accept()
        else:
            #parent
            self.base_class.dragEnterEvent(event)


    def dragMoveEvent(self, event):
        """
        Accept event if it has pathes.
        """

        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            #parent
            self.base_class.dragMoveEvent(event)
 
    
    def dropEvent(self, event):
        """
        Drop event
        """

        #event has pathes
        if (event.mimeData().hasUrls()):
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            
            #url_list
            url_list = []
            for url in event.mimeData().urls():
                url_list.append(str(url.toLocalFile()))
            
            #emit dropped
            self.emit(QtCore.SIGNAL("dropped"), url_list)
        
        else:
            #parent
            self.base_class.dropEvent(event)


    
