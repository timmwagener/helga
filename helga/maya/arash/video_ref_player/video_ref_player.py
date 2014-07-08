try:
    #python
    import os
    import sys
    import time
    import getpass
    import maya.utils
    import subprocess
    import threading
    import maya.OpenMaya as openMaya
    import maya.OpenMayaUI as openMayaUi
    import maya.cmds as cmds
    import pymel.core as pm
    import maya.mel as mel
    from functools import partial
    from xml.dom.minidom import parse, Document
except Exception as e:
    print "Error: importing python modules!!!\n",
    print e




class Reference_Video_UI():

    def __init__(self, windows_ref_width = 350, windows_ref_height = 200):
        """Clear legacy  windows if existing and reraise Helga UI"""

        #super(Reference_Video_UI, self).__init__()

        self.query_username = getpass.getuser()
        self.ref_vid_ui = {}
        self.windows_ref_height = windows_ref_height
        self.windows_ref_width = windows_ref_width
        self.ref_vid_ui["ref_vid_main_window"] = cmds.window('ref_vid_main_Window', title = 'Welcome '+str(self.query_username),
                                                            widthHeight = (self.windows_ref_width, self.windows_ref_height),
                                                            sizeable = False, menuBar = False, minimizeButton = True,
                                                            maximizeButton = False)
        self.ref_vid_UI_layout()
    def ref_vid_UI_layout(self, *args):
        self.ref_vid_ui["ref_column_a"] = cmds.columnLayout ('ref_column_a', columnAttach = ('both', 20),
                                                            rowSpacing = 1, adjustableColumn = True, , columnWidth=300)
        cmds.showWindow(self.ref_vid_ui ["ref_vid_main_window"])

def run():
    """Standardized run() method. Used to call modules functionality"""

    #Helga_cms_login_UI()
    Reference_Video_UI()