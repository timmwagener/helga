###################################################################
#
#    "Helga" Character Manangment System
#            -Helga_AutoRigger_System
#            -Helga_Character_UI
#
#
#    author:  Arash Hosseini
#
#    contact: s.arashhosseini@gmail.com
#
#
#    date:
#        v 1.0 _ 2014-05-25 - start working on '"Helga".CMS'.
#
###################################################################

#importing Libaries
try:
    import maya.cmds as cmds
    import os
    import sys
    import time
    import getpass
except Exception as e:
    print "Error: importing python modules!!!\n",
    print e

HELGA_VERSION = "v 0.1"

#################################################################################
#
#
#base_UI
#
#
#################################################################################

class base:
    def __init__(self):
        pass


    def delete_window(self, name):
        if cmds.window(name, query = True, exists =True):
            cmds.deleteUI(name, window = True)

    def delete_dock_control(self, name):
        if cmds.dockControl(name, query = True, exists=True):
            cmds.deleteUI(name, control=True)



#################################################################################
#
#
#login_UI
#
#
#################################################################################

class helga_cms_login_UI(base):
    def __init__(self, windows_width = 350, windows_height = 200):
        query_username = getpass.getuser()
        self.loginUIs = {}

        self.delete_window('helga_cms_login')
        self.delete_window('helga_td_window')
        self.delete_dock_control('HelgaAutoRiggerSystem')

        self.windows_height = windows_height
        self.windows_width = windows_width
        self.loginUIs["helga_login_window"] = cmds.window('helga_cms_login', title = 'Welcome '+str(query_username),
                                                            widthHeight = (self.windows_width, self.windows_height),
                                                            sizeable = False, menuBar = False, minimizeButton = True,
                                                            maximizeButton = False)
        self.login_UI()
    def login_UI(self, *args):
        self.loginUIs["row_column_a"] = cmds.columnLayout ('main_login_layput', columnAttach = ('both', 0),
                                                            rowSpacing = 1, adjustableColumn = True , bgc = (1.0,1.0,1.0))
        self.loginUIs["separator_a"] = cmds.separator(h=10, vis=True, st='none')
        self.loginUIs["image_path"] = image_path = cmds.internalVar(upd = True) + "icons/icon_helgaCMS_login.png"
        self.loginUIs["image"] =cmds.image(w = 300, h = 100, image = image_path)
        self.loginUIs["separator_b"] = cmds.separator(h=10, vis=True, st='none')
        self.loginUIs["rowColumnLayout_a"] = cmds.rowColumnLayout( numberOfColumns=5, columnSpacing=(1,1),
                                                                    columnWidth=[(1,50), (2,100), (3,50),(4,100), (5,50)])
        self.loginUIs["color_a"] = cmds.symbolButton(h=100, vis=False)
        self.loginUIs["color_b"] = cmds.symbolButton(image="icons/icon_helgaCMS_TD.png", h=100, vis=True, command = self.run_helga_cms_td_UI)
        self.loginUIs["color_c"] = cmds.symbolButton(image="icons/icon_helgaCMS_login_design.png",h=100, vis=True)
        self.loginUIs["color_d"] = cmds.symbolButton(image="icons/icon_helgaCMS_Animation.png", h=100, vis=True, command = self.run_helga_cms_anim_UI)
        self.loginUIs["separator_c"] = cmds.separator(h=10, vis=True, st='none')
        cmds.showWindow(self.loginUIs ["helga_login_window"])


    def run_helga_cms_td_UI(self, *args):
        helga_cms_td_UI()
        self.delete_window('helga_cms_login')

    def run_helga_cms_anim_UI(self, *args):
        helga_cms_anim_UI()
        self.delete_window('helga_cms_login')

#########################################################################################
#TD_UI
#
'''color>init//'''
'''helga_cms_td_UI>init//helga_cms_td_main_UI//delete_dock_td_control//job_reload_UI'''
#
#
#
#
#########################################################################################


class Color():
    def __init__():
        print "Nnjnjnj"
    red = (Color.cl(219), Color.cl(152), Color.cl(21))
    green = (0.0, 1.0, 0.0)
    blue = (1.0, 0.0, 1.0)
    purple = (1.0, 0.0, 0.0)
    colorConstant = 255
    @staticmethod
    def cl(val):
        return val / Color.colorConstant

class helga_cms_td_UI(base, Color):
    def __init__(self):
        self.tdUIs = {}
        self.delete_window('helga_td_window')
        self.delete_dock_control('HelgaAutoRiggerSystem')
        helga_td_win_width = 305
        helga_td_win_height = 605
        self.tdUIs["helga_td_win"] = cmds.window('helga_td_window', title = 'Helga AutoRig System - v '+str(HELGA_VERSION)+' - UI',
                                                widthHeight = (helga_td_win_width,helga_td_win_height), menuBar = True, sizeable = False,
                                                minimizeButton=True, maximizeButton=False)
        cmds.menu('optionMenu', label= 'Window',tearOff = True)
        cmds.menuItem ('reloadUI_td', label='Reload UI', command=self.job_reload_UI)
        cmds.menuItem ('quitUI_td', label='Quit', command=self.delete_dock_td_control)
        cmds.setParent('..', menu=True)

        self.tdUIs["td_mainLayout"] = cmds.formLayout('td_mainLayout')
        self.helga_cms_td_main_UI()
        cmds.dockControl('HelgaAutoRiggerSystem', area = "left", content = self.tdUIs["helga_td_win"])


    def helga_cms_td_main_UI(self, child_width=295, parent_width=300):
        self.child_width = child_width
        self.parent_width = parent_width

        self.tdUIs["td_modules_layout_a"] = cmds.columnLayout('td_modules_layout_a',columnAttach = ('both',0), rowSpacing = 1,  adjustableColumn=True)
        self.tdUIs["td_modules_frame_a"] = cmds.frameLayout('td_modules_frame_a',label='Rigging',  cll = True, borderStyle ='in', w=self.parent_width)
        self.tdUIs["td_modules_layout_b"] = cmds.columnLayout('td_modules_layout_b', columnAttach = ('both', 0), rowSpacing = 1)
        self.tdUIs["color_a"] = cmds.symbolButton(h=50, vis=True, w=self.child_width )
        self.tdUIs["color_a"] = cmds.symbolButton(h=50, vis=True, w=self.child_width )
        self.tdUIs["color_a"] = cmds.symbolButton(h=50, vis=True, w=self.child_width )
        self.tdUIs["color_a"] = cmds.symbolButton(h=50, vis=True, w=self.child_width )
        self.tdUIs["color_a"] = cmds.symbolButton(h=50, vis=True, w=self.child_width )
        self.tdUIs["color_a"] = cmds.symbolButton(h=50, vis=True, w=self.child_width )
        cmds.setParent('..')
        cmds.setParent('..')
        self.tdUIs["td_modules_frame_b"] = cmds.frameLayout('td_modules_frame_b',label='Check Modules',  cll = True, borderStyle ='in', w=self.parent_width)
        self.tdUIs["td_modules_layout_c"] = cmds.columnLayout('td_modules_layout_c', columnAttach = ('both', 0), rowSpacing = 1)
        cmds.setParent('..')
        cmds.setParent('..')
        self.tdUIs["td_modules_frame_c"] = cmds.frameLayout('td_modules_frame_c',label='Options',  cll = True, borderStyle ='in', w=self.parent_width)
        self.tdUIs["td_modules_layout_d"] = cmds.columnLayout('td_modules_layout_d', columnAttach = ('both', 0), rowSpacing = 1)
        cmds.setParent('..')
        cmds.setParent('..')
        self.tdUIs["td_modules_frame_d"] = cmds.frameLayout('td_modules_frame_d',label='Rig Modules',  cll = True, borderStyle ='in', w=self.parent_width)
        self.tdUIs["td_modules_layout_e"] = cmds.columnLayout('td_modules_layout_e', columnAttach = ('both', 0), rowSpacing = 1)
        self.tdUIs["td_modules_button_a"] = cmds.button('td_modules_button_a', bgc=Color.red, label='Rig all Modules', w=self.child_width)
        self.tdUIs["td_modules_button_b"] = cmds.button('td_modules_button_b', label='Rig selected Modules', w=self.child_width)
        cmds.setParent('..')
        cmds.setParent('..')



    def delete_dock_td_control(self, name):
        if cmds.dockControl('HelgaAutoRiggerSystem', query = True, exists=True):
            cmds.deleteUI('HelgaAutoRiggerSystem', control=True)


    def job_reload_UI(self, *args):
        cmds.select(clear = True)
        helga_cms_td_UI()
        # from helga.maya.arash.helga_login import helga_login
        # reload(helga_login)
        # helga_login_ui = helga_login.helga_cms_login_UI()

#################################################################################
#
#
#ANIM_UI
#
#
#################################################################################
class helga_cms_anim_UI:
    def __init__(self):
        print "class helga_cms_anim_UI"










#################################################################################
#
#
#calling main class
#
#
#################################################################################
if(__name__ == '__main__'):
    helga_cms_login_UI()