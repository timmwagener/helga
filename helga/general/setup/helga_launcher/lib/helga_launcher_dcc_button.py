
"""
helga_launcher_dcc_button
==========================================

Subclass of QPushButton to allow for customized drag&drop behaviour
"""




#Import
#------------------------------------------------------------------
#python
import logging
import os
import sys
#PyQt4
from PyQt4 import QtGui
from PyQt4 import QtCore







#HelgaLauncherDCCButton class
#------------------------------------------------------------------
class HelgaLauncherDCCButton(QtGui.QPushButton):
    """
    Subclass of QPushButton to allow for customized drag&drop behaviour
    """

    def __init__(self, 
                logging_level = logging.DEBUG,
                button_text = None,
                icon_path = None,
                icon_path_hover = None,
                icon_path_drag = None,
                parent=None): 
        
        #super class constructor
        if(button_text):
            super(HelgaLauncherDCCButton, self).__init__(button_text, parent)
        else:
            super(HelgaLauncherDCCButton, self).__init__(parent)

        #icon_path
        self.icon_path = icon_path
        #set stylesheet
        if(self.icon_path):
            if(os.path.isfile(self.icon_path)):
                self.setStyleSheet("border-image: url({0});".format(self.icon_path))
        
        #icon_path_hover
        self.icon_path_hover = icon_path_hover

        #icon_path_drag
        self.icon_path_drag = icon_path_drag

        #accept drops
        self.setAcceptDrops(True)
        #setMouseTracking
        self.setMouseTracking(True)


    def enterEvent(self, event):
        #set stylesheet
        if(self.icon_path_hover):
            if(os.path.isfile(self.icon_path_hover)):
                self.setStyleSheet("border-image: url({0});".format(self.icon_path_hover))
        event.accept()

    def leaveEvent(self, event):
        #set stylesheet
        if(self.icon_path):
            if(os.path.isfile(self.icon_path)):
                self.setStyleSheet("border-image: url({0});".format(self.icon_path))
        event.accept()


    def dragEnterEvent(self, event):
        if (event.mimeData().hasUrls()):
            #set stylesheet
            if(self.icon_path_drag):
                if(os.path.isfile(self.icon_path_drag)):
                    self.setStyleSheet("border-image: url({0});".format(self.icon_path_drag))
            event.accept()

        else:
            event.ignore()
 
    
    def dragMoveEvent(self, event):
        if (event.mimeData().hasUrls()):
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()


    def dragLeaveEvent(self, event):
        #set stylesheet
        if(self.icon_path):
            if(os.path.isfile(self.icon_path)):
                self.setStyleSheet("border-image: url({0});".format(self.icon_path))
        event.accept()
 
    
    def dropEvent(self, event):
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
            event.ignore()

