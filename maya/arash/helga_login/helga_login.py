

"""
helga_login
==========================================

GUI for the auto-rigger for the Helga characters.

-----------------------

Usage
-----

::

    from helga.maya.arash.helga_login import helga_login
    reload(helga_login)

    #run
    helga_login.run()

**Author:** `Arash Hosseini <mailto:s.arashhosseini@gmail.com>`_

-----------------------
"""

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
    #python
    import os
    import sys
    import time
    import getpass
    #maya
    import maya.cmds as cmds
    import pymel.core as pm
    import maya.mel as mel
except Exception as e:
    print "Error: importing python modules!!!\n",
    print e

# Global Helpstrings
HELGA_VERSION = "0.1"
helper_td_main_module = "Hallo Welcome to Helga CMS"
helper_arm_module = "arm________________"
helper_leg_module = "leg________________"
helper_spine_module = "spine________________"
helper_head_module = "head________________"
helper_biped_module = "biped________________"

#################################################################################
#
#
#base_UI
#
#
#################################################################################

class Base(object):

    def __init__(self):

        #instance variables
        #--------------------------------
        self.color = [255, 255, 0]



    def delete_window(self, name):
        if cmds.window(name, query = True, exists =True):
            cmds.deleteUI(name, window = True)

    def delete_dock_control(self, name):
        if cmds.dockControl(name, query = True, exists=True):
            cmds.deleteUI(name, control=True)


    def quit_UI_window(self, name):
        if cmds.window(name, query = True, exists =True):
            cmds.deleteUI(name, window = True)


    #Getter & setter
    #--------------------------------
    def get_color(self):
        """Return color as tuple"""

        return self.color

    def set_color(self, new_color):
        """Set color tuple"""

        self.color = new_color



#################################################################################
#
#
#login_UI
#
#
#################################################################################

class Helga_cms_login_UI(Base):

    def __init__(self, windows_width = 350, windows_height = 200):
        """Clear legacy  windows if existing and reraise Helga UI"""

        super(Helga_cms_login_UI, self).__init__()

        self.query_username = getpass.getuser()
        self.loginUIs = {}

        self.delete_window('helga_cms_login')
        self.delete_window('helga_td_window')
        self.delete_window('helper')
        self.delete_dock_control('HelgaAutoRiggerSystem')

        self.windows_height = windows_height
        self.windows_width = windows_width
        self.loginUIs["helga_login_window"] = cmds.window('helga_cms_login', title = 'Welcome '+str(self.query_username),
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

    def login_file(self, *args):
        #query_debug_text = cmds.textField('debugTextField', text=True, query=True)
        now = time.localtime(time.time())
        current_time = time.strftime("  %y/%m/%d %H:%M", now)
        file = open("Y:/Production/rnd/ahosseini/helga_td_login_file/helga_login_file.txt", "a")
        file.write("open: "+current_time+" by "+self.query_username+"\n")
        file.close()
        #warning = cmds.warning("successful sending to Arash")


    def run_helga_cms_td_UI(self, *args):
        Helga_cms_td_UI()
        self.login_file()
        self.delete_window('helga_cms_login')

    def run_helga_cms_anim_UI(self, *args):
        Helga_cms_anim_UI()
        self.login_file()
        self.delete_window('helga_cms_login')


#########################################################################################
#TD_UI
#
'''color>init//'''
'''helga_cms_td_UI>init//helga_cms_td_main_UI//show_helper//delete_dock_td_control//job_reload_UI//check_scene_jnt'''
#
#
#
#
#########################################################################################
class Color(object):
    def __init__(self):
        pass

    colorConstant = 255.0
    red = (255 / colorConstant , 0.0, 0.0)
    blue_a = (96 / colorConstant, 185 / colorConstant, 207 / colorConstant)
    green_a = (96 / colorConstant, 207 / colorConstant, 164 / colorConstant)
    orange_a = (255 / colorConstant, 191 / colorConstant, 64 / colorConstant)
    gray_a = (138 / colorConstant, 120/ colorConstant, 128 / colorConstant)



class Helga_cms_td_UI(Base):

    def __init__(self):
        # myHelper = Helper()
        # myHelper.load_helper_UI()


        #call superclass constructor for inheritance in Python . This is neccessary
        super(Helga_cms_td_UI, self).__init__()

        self.tdUIs = {}
        self.delete_window('helga_td_window')
        self.delete_dock_control('HelgaAutoRiggerSystem')
        helga_td_win_width = 330
        helga_td_win_height = 880
        self.tdUIs["helga_td_win"] = cmds.window('helga_td_window', title = 'Helga AutoRig System - v '+str(HELGA_VERSION)+' - UI',
                                                widthHeight = (helga_td_win_width,helga_td_win_height), menuBar = True, sizeable = False,
                                                minimizeButton=True, maximizeButton=False)
        cmds.menu('optionMenu_window', label= 'Window',tearOff = True)
        cmds.menuItem ('reloadUI_td', label='Reload UI', command=self.job_reload_UI)
        cmds.menuItem ('quitUI_td', label='Quit', command=self.delete_dock_td_control)
        cmds.setParent('..', menu=True)
        cmds.menu('optionMenu_Helper', label = 'Helper', tearOff = True)
        cmds.menuItem ('HelperUI', label='Helper', command = (lambda message: self.show_helper(helper_td_main_module)))
        self.tdUIs["td_mainLayout_scroll"] = cmds.scrollLayout('td_mainLayout_scroll',w=300 , h=880)
        self.tdUIs["td_mainLayout"] = cmds.formLayout('td_mainLayout',w=305 , h=880)

        self.helga_cms_td_main_UI()
        cmds.dockControl('HelgaAutoRiggerSystem', area = "left", content = self.tdUIs["helga_td_win"])


    def helga_cms_td_main_UI(self, child_width=295, parent_width=300):

        self.child_width = child_width
        self.parent_width = parent_width

        self.tdUIs["td_modules_layout_a"] = cmds.columnLayout('td_modules_layout_a',columnAttach = ('both',0), rowSpacing = 1,  adjustableColumn=True)
        self.tdUIs["td_modules_frame_a"] = cmds.frameLayout('td_modules_frame_a',cl=True,label='Modules', bgc=Color.gray_a ,cll = True, borderStyle ='in', w=self.parent_width)
        self.tdUIs["td_modules_rowColumn_a"] = cmds.rowColumnLayout( numberOfColumns=3, columnWidth=[(1, 20), (2, 150), (3, 120)])
        self.tdUIs["td_modules_button_a"] = cmds.button(h=30, label = '?',  vis=True, command = (lambda message: self.show_helper(helper_arm_module)))
        self.tdUIs["td_modules_image_a"] = cmds.image(h=30, image = "icons/icon_helgaCMS_armModule.png")
        self.tdUIs["td_modules_button_b"] = cmds.button(h=30, label = "create arm Module",  vis=True, command =self.create_check_module_arm)
        self.tdUIs["td_modules_button_c"] = cmds.button(h=30, label = '?',  vis=True, command = (lambda message: self.show_helper(helper_leg_module)))
        self.tdUIs["td_modules_image_b"] = cmds.image(h=30, image = "icons/icon_helgaCMS_legModule.png")
        self.tdUIs["td_modules_button_d"] = cmds.button(h=30, label = "create leg Module",  vis=True, command =self.create_check_module_leg)
        self.tdUIs["td_modules_button_e"] = cmds.button(h=30, label = '?',  vis=True, command = (lambda message: self.show_helper(helper_spine_module)))
        self.tdUIs["td_modules_image_c"] = cmds.image(h=30, image = "icons/icon_helgaCMS_spineModule.png")
        self.tdUIs["td_modules_button_f"] = cmds.button(h=30, label = "create spine Module",  vis=True, command =self.create_check_module_spine)
        self.tdUIs["td_modules_button_g"] = cmds.button(h=30, label = '?',  vis=True, command = (lambda message: self.show_helper(helper_head_module)))
        self.tdUIs["td_modules_image_d"] = cmds.image(h=30, image = "icons/icon_helgaCMS_headModule.png")
        self.tdUIs["td_modules_button_h"] = cmds.button(h=30, label = "create head Module",  vis=True, command =self.create_check_module_head)
        self.tdUIs["td_modules_button_i"] = cmds.button(h=30, label = '?',  vis=True, command = (lambda message: self.show_helper(helper_biped_module)))
        self.tdUIs["td_modules_image_e"] = cmds.image(h=30, image = "icons/icon_helgaCMS_bipedModule.png")
        self.tdUIs["td_modules_button_j"] = cmds.button(h=30, label = "create biped Module",  vis=True, command =self.create_check_module_biped)
        cmds.setParent('..')
        cmds.setParent('..')
        self.tdUIs["td_modules_frame_b"] = cmds.frameLayout('td_modules_frame_b',cl=True,label='Check Modules',bgc=Color.gray_a , cll = True, borderStyle ='in', w=self.parent_width)
        self.tdUIs["td_modules_button_delete_module_a"] = cmds.button('td_modules_button_delete_module_a',label="Delete selected Module", command=self.delete_module)
        self.tdUIs["td_check_modules_rowColumn_a"] = cmds.rowColumnLayout( numberOfColumns=3, columnWidth=[(1, 180), (2,50), (3, 50)])
        cmds.setParent('..')
        cmds.setParent('..')
        self.tdUIs["td_modules_frame_c"] = cmds.frameLayout('td_modules_frame_c',cl=True,label='Options',bgc=Color.gray_a ,  cll = True, borderStyle ='in', w=self.parent_width)
        self.tdUIs["td_modules_rowColumn_b"] = cmds.rowColumnLayout( numberOfColumns=2, columnWidth=[(1, 150), (2, 150)])
        self.tdUIs["td_modules_checkBox_a"] = cmds.checkBox('td_modules_checkBox_a', label = "Show Joint after Rigging" )
        cmds.setParent('..')
        cmds.setParent('..')
        self.tdUIs["td_modules_frame_d"] = cmds.frameLayout('td_modules_frame_d',cl=True,label='Rig Modules',bgc=Color.gray_a ,  cll = True, borderStyle ='in', w=self.parent_width)
        self.tdUIs["td_modules_layout_e"] = cmds.columnLayout('td_modules_layout_e', columnAttach = ('both', 0), rowSpacing = 1)
        self.tdUIs["space_a"]=cmds.separator(h=5, vis=True, st='none',w=self.child_width)
        self.tdUIs["td_rig_modules_button_a"] = cmds.button('td_rig_modules_button_a', bgc = Color.blue_a,label='Rig all Modules', h=30, w=self.child_width)
        self.tdUIs["space_b"]=cmds.separator(h=5, vis=True, st='none',w=self.child_width)
        self.tdUIs["td_rig_modules_button_b"] = cmds.button('td_rig_modules_button_b', bgc = Color.green_a, label='Rig selected Modules', h=30, w=self.child_width)
        self.tdUIs["space_c"]=cmds.separator(h=5, vis=True, st='none',w=self.child_width)
        cmds.setParent('..')
        cmds.setParent('..')
        self.tdUIs["td_modules_frame_e"] = cmds.frameLayout('td_modules_frame_e',cl=True,label='Skinning',bgc=Color.gray_a ,  cll = True, borderStyle ='in', w=self.parent_width)
        self.tdUIs["td_modules_rowColumn_c"] = cmds.rowColumnLayout( numberOfColumns=2, columnWidth=[(1, 150), (2, 130)])
        self.tdUIs["td_modules_checkBox_b"] = cmds.checkBox('td_modules_checkBox_b', label = "Helga CMS Joints")
        self.tdUIs["td_modules_checkBox_c"] = cmds.checkBox('td_modules_checkBox_c', label = "Scene Joints")
        self.tdUIs["td_modules_pop_joint_text"] = cmds.text('td_modules_pop_joint_text', label = "Populate Joints: ")
        self.tdUIs["td_modules_pop_joints_button"] = cmds.button('td_modules_pop_joints_button', label = "Populate Joints", command=self.check_scene_jnt)
        self.tdUIs["td_modules_pop_polygone_text"] = cmds.text('td_modules_pop_polygone_text', label = "Populate Polygone: ")
        self.tdUIs["td_modules_pop_polygone_button"] = cmds.button('td_modules_pop_polygone_button', label ="Populate Polygone", command=self.check_scene_polygone)
        self.tdUIs["td_modules_layout_f"] = cmds.columnLayout('td_modules_layout_f', columnAttach = ('both', 0), rowSpacing = 1, w=self.child_width)
        self.tdUIs["td_modules_skinning_joint_text"] = cmds.text('td_modules_skinning_joint_text', label="Joints Area",w=self.child_width)
        self.tdUIs["td_modules_skinning_joint_area"] = cmds.textScrollList('td_modules_skinning_joint_area', ams =True,w = self.child_width, h = 150)
        self.tdUIs["td_modules_skinning_polygine_text"] = cmds.text('td_modules_skinning_polygone_text', label="Polygone Area",w=self.child_width)
        self.tdUIs["td_modules_skinning_polygone_area"] = cmds.textScrollList('td_modules_skinning_polygone_area', ams =True, w = self.child_width, h=150)
        self.tdUIs["space_d"]=cmds.separator(h=10, vis=True, st='none',w=self.child_width)
        self.tdUIs["td_modules_button_c"] = cmds.button('td_modules_button_c', bgc = Color.blue_a, h=30, label = 'Skinning', w=self.child_width, command=self.skinning)
        self.tdUIs["space_e"]=cmds.separator(h=10, vis=True, st='none',w=self.child_width)
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.setParent('..')
        self.tdUIs["td_modules_frame_f"] = cmds.frameLayout('td_modules_frame_f',cl=True,label='Tools',bgc=Color.gray_a ,  cll = True, borderStyle ='in', w=self.parent_width)
        self.tdUIs["td_modules_layout_g"] = cmds.columnLayout('td_modules_layout_g', columnAttach = ('both', 0), rowSpacing = 1)
        self.tdUIs["color_a"] = cmds.symbolButton(image="icons/icon_helgaCMS_jelly_tool_Module.png", h=50, vis=True, w=self.child_width , command =self.tool_jelly)
        self.tdUIs["color_a"] = cmds.symbolButton(h=50, vis=True, w=self.child_width )
        self.tdUIs["color_a"] = cmds.symbolButton(h=50, vis=True, w=self.child_width )
        self.tdUIs["color_a"] = cmds.symbolButton(h=50, vis=True, w=self.child_width )
        self.tdUIs["color_a"] = cmds.symbolButton(h=50, vis=True, w=self.child_width )
        self.tdUIs["color_a"] = cmds.symbolButton(h=50, vis=True, w=self.child_width )
        cmds.setParent('..')
        cmds.setParent('..')


        # #color_picker_temp////self.get_color()
        # self.color_picker_temp = pm.colorEditor(parent = self.tdUIs["td_modules_layout_e"])

    def show_helper(self, message):

        if cmds.window("helper", exists=True):
            cmds.deleteUI("helper")
        helper_windows = cmds.window("helper",title="Helper",mnb=True, mxb=False,w=400,h=130,sizeable=False)
        helper_form_layout = cmds.formLayout('helper_dialog_UI')
        helper_colum_layout = cmds.columnLayout(columnAttach=('both', 0), rowSpacing=5, columnWidth=250)
        cmds.separator(h=50,vis=True, st='none')
        helper_text = cmds.text('helper_text_a',label=message, align = 'center')
        cmds.showWindow()

    def delete_dock_td_control(self, name):
        if cmds.dockControl('HelgaAutoRiggerSystem', query = True, exists=True):
            cmds.deleteUI('HelgaAutoRiggerSystem', control=True)


    def job_reload_UI(self, *args):
        cmds.select(clear = True)
        Helga_cms_td_UI()
        # from helga.maya.arash.helga_login import helga_login
        # reload(helga_login)
        # helga_login_ui = helga_login.helga_cms_login_UI()

    def check_scene_jnt(self, scene_joints):
        cmds.select(clear=True)
        query_checkBox_helgaCMS_jnt = cmds.checkBox('td_modules_checkBox_b', value = True, query = True)
        query_checkBox_scene_jnt = cmds.checkBox('td_modules_checkBox_c', value =True, query = True)
        self.scene_joints = cmds.ls(type='joint')
        self.cms_joints  = cmds.ls('Helga_cms_*', type = 'joint')

        if query_checkBox_scene_jnt and query_checkBox_helgaCMS_jnt == True:
            cmds.warning('please select a type')
        else:
            if len(self.scene_joints) ==0:
                cmds.warning('No Joints in Scene')
            else:
                if query_checkBox_scene_jnt ==True:
                    print "do scene Joint func"
                    self.populate_scene_jnt()
                else:
                    if query_checkBox_helgaCMS_jnt ==True:
                        print "do CMS Joint func"
                        self.populate_cms_jnt()
                    else:
                        cmds.warning('No Joint type selected')

    def check_scene_polygone(self, scene_polygone):
        cmds.select(clear = True)
        self.scene_polygone = cmds.ls(type='mesh')
        if len(self.scene_polygone) ==0:
            cmds.warning('No meshes in Scene')
        else:
            self.populate_polygone()

    def populate_scene_jnt(self, *args):
        cmds.textScrollList('td_modules_skinning_joint_area', e =True, ra=True)
        for scene_joint in self.scene_joints:
            cmds.textScrollList('td_modules_skinning_joint_area', edit = True, append = scene_joint)

    def populate_cms_jnt(self, *args):
        cmds.textScrollList('td_modules_skinning_joint_area', e =True, ra=True)
        for scene_joint in self.cms_joints:
            cmds.textScrollList('td_modules_skinning_joint_area', edit = True, append = scene_joint)

    def populate_polygone(self, *args):
        cmds.textScrollList('td_modules_skinning_polygone_area', e =True, ra=True)
        for scene_polygone in self.scene_polygone:
            cmds.textScrollList('td_modules_skinning_polygone_area', edit = True, append = scene_polygone)

    def skinning(self, *args):
        mel.eval('SmoothBindSkinOptions')


    def create_check_module_arm(self, *args):
        if cmds.button('td_check_modules_button_a', exists =True) and cmds.button('td_check_modules_button_b', exists = True):
            cmds.warning('Module already exists')
        else:
            self.tdUIs["td_check_modules_text_a"] = cmds.text('td_check_modules_text_a',label="Arm Module", parent = self.tdUIs["td_check_modules_rowColumn_a"])
            self.tdUIs["td_check_modules_button_a"] = cmds.button('td_check_modules_button_a', label = "", parent = self.tdUIs["td_check_modules_rowColumn_a"], bgc=Color.gray_a,command=(lambda message: self.select_module("td_check_modules_button_a")))
            self.tdUIs["td_check_modules_button_b"] = cmds.button('td_check_modules_button_b',label = "Color", parent = self.tdUIs["td_check_modules_rowColumn_a"], command=(lambda message: self.color_Editor("td_check_modules_button_b")))

    def create_check_module_leg(self, *args):
        if cmds.button('td_check_modules_button_c', exists =True) and cmds.button('td_check_modules_button_d', exists = True):
            cmds.warning('Module already exists')
        else:
            self.tdUIs["td_check_modules_text_b"] = cmds.text('td_check_modules_text_b',label="Leg Module", parent = self.tdUIs["td_check_modules_rowColumn_a"])
            self.tdUIs["td_check_modules_button_c"] = cmds.button('td_check_modules_button_c',label = "", parent = self.tdUIs["td_check_modules_rowColumn_a"], bgc=Color.gray_a,command=(lambda message: self.select_module("td_check_modules_button_c")))
            self.tdUIs["td_check_modules_button_d"] = cmds.button('td_check_modules_button_d',label = "Color", parent = self.tdUIs["td_check_modules_rowColumn_a"], command=(lambda message: self.color_Editor("td_check_modules_button_d")))

    def create_check_module_spine(self, *args):
        if cmds.button('td_check_modules_button_e', exists =True) and cmds.button('td_check_modules_button_f', exists = True):
            cmds.warning('Module already exists')
        else:
            self.tdUIs["td_check_modules_text_c"] = cmds.text('td_check_modules_text_c',label="Spine Module", parent = self.tdUIs["td_check_modules_rowColumn_a"])
            self.tdUIs["td_check_modules_button_e"] = cmds.button('td_check_modules_button_e',label = "", parent = self.tdUIs["td_check_modules_rowColumn_a"], bgc=Color.gray_a,command=(lambda message: self.select_module("td_check_modules_button_e")))
            self.tdUIs["td_check_modules_button_f"] = cmds.button('td_check_modules_button_f',label = "Color", parent = self.tdUIs["td_check_modules_rowColumn_a"], command=(lambda message: self.color_Editor("td_check_modules_button_f")))

    def create_check_module_head(self, *args):
        if cmds.button('td_check_modules_button_g', exists =True) and cmds.button('td_check_modules_button_h', exists = True):
            cmds.warning('Module already exists')
        else:
            self.tdUIs["td_check_modules_text_d"] = cmds.text('td_check_modules_text_d',label="Head Module", parent = self.tdUIs["td_check_modules_rowColumn_a"])
            self.tdUIs["td_check_modules_button_g"] = cmds.button('td_check_modules_button_g',label = "", parent = self.tdUIs["td_check_modules_rowColumn_a"], bgc=Color.gray_a,command=(lambda message: self.select_module("td_check_modules_button_g")))
            self.tdUIs["td_check_modules_button_h"] = cmds.button('td_check_modules_button_h',label = "Color", parent = self.tdUIs["td_check_modules_rowColumn_a"], command=(lambda message: self.color_Editor("td_check_modules_button_h")))

    def create_check_module_biped(self, *args):
        if cmds.button('td_check_modules_button_i', exists =True) and cmds.button('td_check_modules_button_j', exists = True):
            cmds.warning('Module already exists')
        else:
            self.tdUIs["td_check_modules_text_e"] = cmds.text('td_check_modules_text_e', label="Biped Module", parent = self.tdUIs["td_check_modules_rowColumn_a"])
            self.tdUIs["td_check_modules_button_i"] = cmds.button('td_check_modules_button_i',label = "", parent = self.tdUIs["td_check_modules_rowColumn_a"], bgc=Color.gray_a,command=(lambda message: self.select_module("td_check_modules_button_i")))
            self.tdUIs["td_check_modules_button_j"] = cmds.button('td_check_modules_button_j',label = "Color", parent = self.tdUIs["td_check_modules_rowColumn_a"], command=(lambda message: self.color_Editor("td_check_modules_button_j")))


    def color_Editor(self, name):
        cmds.colorEditor()
        self.name = name
        if cmds.colorEditor(query=True, result=True):
            value = cmds.colorEditor(q = True, rgb = True)
            cmds.button(name, edit=True, bgc=value)
        else:
            cmds.warning('Editor was dismissed')


    def select_module(self, name):
        query_button = cmds.button(name, q=True, label=True)
        if query_button=="S":
            cmds.button(name, edit = True, label="")
            cmds.button(name, edit =True, bgc=Color.gray_a)
        else:
            cmds.button(name, edit=True, label="S", bgc=Color.green_a)

    def delete_module(self, *args):
        if cmds.button('td_check_modules_button_a', exists =True):
            query_select_button_a = cmds.button('td_check_modules_button_a', q=True, label=True)
            if query_select_button_a =="S":
                cmds.deleteUI('td_check_modules_text_a','td_check_modules_button_a','td_check_modules_button_b')
        else:
            pass
        if cmds.button('td_check_modules_button_c', exists =True):
            query_select_button_c = cmds.button('td_check_modules_button_c', q=True, label=True)
            if query_select_button_c =="S":
                cmds.deleteUI('td_check_modules_text_b','td_check_modules_button_c','td_check_modules_button_d')
        else:
            pass
        if cmds.button('td_check_modules_button_e', exists =True):
            query_select_button_e = cmds.button('td_check_modules_button_e', q=True, label=True)
            if query_select_button_e =="S":
                cmds.deleteUI('td_check_modules_text_c','td_check_modules_button_e','td_check_modules_button_f' )
        else:
            pass
        if cmds.button('td_check_modules_button_g', exists =True):
            query_select_button_g = cmds.button('td_check_modules_button_g', q=True, label=True)
            if query_select_button_g =="S":
                cmds.deleteUI('td_check_modules_text_d','td_check_modules_button_g','td_check_modules_button_h' )
        else:
            pass
        if cmds.button('td_check_modules_button_i', exists =True):
            query_select_button_i = cmds.button('td_check_modules_button_i', q=True, label=True)
            if query_select_button_i =="S":
                cmds.deleteUI('td_check_modules_text_e','td_check_modules_button_i','td_check_modules_button_j' )


    def tool_jelly(self, *args):
        from helga.maya.arash.dynamo import dynamo
        reload(dynamo)
        dynamo.UI()

#################################################################################
###################################Animation#####################################
#################################################################################
#################################################################################
#################################################################################
#################################################################################
#
#
#ANIM_UI_character_choice
#
#
#################################################################################
class Helga_cms_anim_UI(Base):

    def __init__(self):
        # myHelper = Helper()
        # myHelper.load_helper_UI()


        #call superclass constructor for inheritance in Python . This is neccessary
        super(Helga_cms_anim_UI, self).__init__()

        self.anim_choiceUIs = {}
        helga_anim_choice_win_width = 300
        helga_anim_choice_win_height = 200
        self.delete_window('helga_anim_choice_window')
        self.anim_choiceUIs["helga_anim_choice_win"] = cmds.window('helga_anim_choice_window', title = 'Helga Character Set',
                                                widthHeight = (helga_anim_choice_win_width,helga_anim_choice_win_height), menuBar = True, sizeable = True,
                                                minimizeButton=True, maximizeButton=False)
        self.character_choice()
    def character_choice(self, *args):
        self.anim_choiceUIs['helga_choice_column_a']=cmds.columnLayout('helga_choice_column_a', columnAttach=('both', 20), rowSpacing=3, columnWidth=300)
        self.anim_choiceUIs['helga_choice_separator_a']=cmds.separator('helga_choice_separator_a', h=20, st='none', vis=True)
        self.anim_choiceUIs['helga_choice_text_a'] = cmds.text('helga_choice_text_a', label="Choice Character", align='center')
        self.anim_choiceUIs['helga_choice_separator_b']=cmds.separator('helga_choice_separator_b', h=10, st='none', vis=True)
        self.anim_choiceUIs['helga_choice_option_a'] =cmds.optionMenu('helga_choice_option_a', w=180, label ="Character Body UI")
        self.anim_choiceUIs['helga_choice_option_b'] =cmds.optionMenu('helga_choice_option_b', w=180, label ="Character Hand UI")
        self.anim_choiceUIs['helga_choice_menuItem_a'] =cmds.menuItem('helga_choice_menuItem_a',label="1. Ulfbert",  parent =self.anim_choiceUIs['helga_choice_option_a'])
        self.anim_choiceUIs['helga_choice_menuItem_b'] =cmds.menuItem('helga_choice_menuItem_b',label="2. Helga",parent =self.anim_choiceUIs['helga_choice_option_a'])
        self.anim_choiceUIs['helga_choice_menuItem_c'] =cmds.menuItem('helga_choice_menuItem_c',label="3. Ritter", parent =self.anim_choiceUIs['helga_choice_option_a'])
        self.anim_choiceUIs['helga_choice_menuItem_d'] =cmds.menuItem('helga_choice_menuItem_d',label="1. Ulfbert",parent =self.anim_choiceUIs['helga_choice_option_b'])
        self.anim_choiceUIs['helga_choice_menuItem_e'] =cmds.menuItem('helga_choice_menuItem_e',label="2. Helga", parent =self.anim_choiceUIs['helga_choice_option_b'])
        self.anim_choiceUIs['helga_choice_menuItem_f'] =cmds.menuItem('helga_choice_menuItem_f',label="3. Ritter", parent =self.anim_choiceUIs['helga_choice_option_b'])
        self.anim_choiceUIs['helga_choice_separator_c']=cmds.separator('helga_choice_separator_c', h=5, st='none', vis=True)
        self.anim_choiceUIs['helga_choice_button_a'] = cmds.button('helga_choice_button_a',command= self.character_body_button, h = 30,  label="Create Character UI")
        self.anim_choiceUIs['helga_choice_button_b'] = cmds.button('helga_choice_button_b', command= self.character_hand_button,h=30, label="Create Hand UI")
        #self.anim_choiceUIs['helga_choice_column_b']=cmds.columnLayout('helga_choice_column_b', columnAttach=('both', 0), rowSpacing=3, columnWidth=300, parent = self.anim_choiceUIs["helga_anim_choice_win"])
        #self.anim_choiceUIs['helga_choice_separator_d']=cmds.separator('helga_choice_separator_d', h=5, st='none', vis=True)

        #self.anim_choiceUIs['helga_choice_text_b'] = cmds.text('helga_choice_text_b', bgc= (0.0,0.0,0.0),h = 20, align = 'left', label= "Hallo", parent = self.anim_choiceUIs['helga_choice_column_b'])


        cmds.showWindow(self.anim_choiceUIs ["helga_anim_choice_win"])

##################################################
#
#
#ANIM_UI_character_choice_function
#
#
##################################################


    def character_body_button(self, *args):
        query_character_button = cmds.optionMenu('helga_choice_option_a', query = True, value = True)[0]

        if query_character_button =='1':
            self.delete_ulfbert_character_UIs()
            Ulfbert_body_UI()
        else:
            pass
        if query_character_button =='2':
            self.delete_helja_character_UIs()
            Helja_body_UI()
        else:
            pass
        if query_character_button =='3':
            self.delete_ritter_character_UIs()
            Ritter_body_UI()


    def character_hand_button(self, *args):
        query_character_hand_button = cmds.optionMenu('helga_choice_option_b', query = True, value = True)[0]
        if query_character_hand_button =='1':
            print "Ulfbert_hand_UI()"
        else:
            pass
        if query_character_hand_button =='2':
            print "hand Helga"
        else:
            pass
        if query_character_hand_button =='3':
            print "hand Ritter"

    def delete_ulfbert_character_UIs(self, *args):
        if cmds.window('ulfbert_body_window', exists=True):
            self.delete_window('ulfbert_body_window')

    def delete_helja_character_UIs(self, *args):
        if cmds.window('helja_body_window', exists=True):
            self.delete_window('helja_body_window')

    def delete_ritter_character_UIs(self, *args):
        if cmds.window('ritter_body_window', exists=True):
            self.delete_window('ritter_body_window')


#################################################################################
#
#
#ANIM_UI_character_body_UI
#
#
#################################################################################

class Ulfbert_body_UI(Base):
    def __init__(self, ulfbert_parent_width = 500, ulfbert_parent_height = 730, ulfbert_child_width = 495, ulfbert_child_height = 495):

        super(Ulfbert_body_UI, self).__init__()

        self.ulfbert_body_UIs = {}
        #self.delete_window('helga_anim_choice_window')
        self.ulfbert_parent_width = ulfbert_parent_width
        self.ulfbert_parent_height = ulfbert_parent_height
        self.ulfbert_child_width = ulfbert_child_width
        self.ulfbert_child_height = ulfbert_child_height
        self.ulfbert_body_UIs["ulfbert_body_win"] = cmds.window('ulfbert_body_window', title = 'Ulfebrt Character UI',
                                                widthHeight = (self.ulfbert_parent_width,self.ulfbert_parent_height),
                                                menuBar = True, sizeable = False, topEdge= 0, leftEdge= 0, minimizeButton=True, maximizeButton=False)
        self.ulfbert_body_main_UI()

    def ulfbert_body_main_UI(self, *args):

        self.ulfbert_body_UIs['ulfbert_column_a'] = cmds.columnLayout('ulfbert_column_a', columnAttach=('both', 0), rowSpacing=3, columnWidth=self.ulfbert_child_width, parent =self.ulfbert_body_UIs["ulfbert_body_win"] )
        ########to go'''
        self.ulfbert_body_UIs['ulfbert_rowColumn_a'] = cmds.rowColumnLayout('ulfbert_rowColumn_a', w= self.ulfbert_child_width, h=self.ulfbert_child_height, numberOfColumns=11, columnSpacing=(1,1),
                                                            columnWidth=[(1,45), (2,45), (3,45),(4,45), (5,45),(6,45), (7,45), (8,45),(9,45), (10,45),(11,45)], parent= self.ulfbert_body_UIs['ulfbert_column_a'] )
        '''never, have to import as module'''
        self.ulfbert_body_UIs['ulfbert_icon_1'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_2'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_3'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_4'] = cmds.symbolButton(bgc=(1.0,1.0,1.0),image="icons/Helga_character_UI/cms_cog.png", h=45, vis=True)
        self.ulfbert_body_UIs['ulfbert_icon_5'] = cmds.symbolButton(bgc=(1.0,1.0,1.0), image="icons/Helga_character_UI/cms_cog.png", h=45, vis=True)
        self.ulfbert_body_UIs['ulfbert_icon_6'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_7'] = cmds.symbolButton(bgc=(1.0,1.0,1.0),image="icons/Helga_character_UI/cms_cog.png", h=45, vis=True)
        self.ulfbert_body_UIs['ulfbert_icon_8'] = cmds.symbolButton(bgc=(1.0,1.0,1.0),image="icons/Helga_character_UI/cms_cog.png", h=45, vis=True)
        self.ulfbert_body_UIs['ulfbert_icon_9'] = cmds.symbolButton( h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_10'] = cmds.symbolButton( h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_11'] = cmds.symbolButton( h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_12'] = cmds.symbolButton( h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_13'] = cmds.symbolButton(bgc=(1.0,1.0,1.0),image="icons/Helga_character_UI/cms_cog.png", h=45, vis=True)
        self.ulfbert_body_UIs['ulfbert_icon_14'] = cmds.symbolButton(bgc=(1.0,1.0,1.0),image="icons/Helga_character_UI/cms_cog.png", h=45, vis=True)
        self.ulfbert_body_UIs['ulfbert_icon_15'] = cmds.symbolButton(bgc=(1.0,1.0,1.0),image="icons/Helga_character_UI/cms_cog.png", h=45, vis=True)
        self.ulfbert_body_UIs['ulfbert_icon_16'] = cmds.symbolButton(bgc=(1.0,1.0,1.0),image="icons/Helga_character_UI/cms_cog.png", h=45, vis=True)
        self.ulfbert_body_UIs['ulfbert_icon_17'] = cmds.symbolButton(bgc=(1.0,1.0,1.0), image="icons/Helga_character_UI/cms_cog.png", h=45, vis=True)
        self.ulfbert_body_UIs['ulfbert_icon_18'] = cmds.symbolButton(bgc=(1.0,1.0,1.0),image="icons/Helga_character_UI/cms_cog.png", h=45, vis=True)
        self.ulfbert_body_UIs['ulfbert_icon_20'] = cmds.symbolButton(bgc=(1.0,1.0,1.0),image="icons/Helga_character_UI/cms_cog.png", h=45, vis=True)
        self.ulfbert_body_UIs['ulfbert_icon_21'] = cmds.symbolButton(bgc=(1.0,1.0,1.0),image="icons/Helga_character_UI/cms_cog.png", h=45, vis=True)
        self.ulfbert_body_UIs['ulfbert_icon_22'] = cmds.symbolButton(bgc=(1.0,1.0,1.0),image="icons/Helga_character_UI/cms_cog.png", h=45, vis=True)
        self.ulfbert_body_UIs['ulfbert_icon_23'] = cmds.symbolButton( h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_24'] = cmds.symbolButton(bgc=(1.0,1.0,1.0),image="icons/Helga_character_UI/cms_cog.png", h=45, vis=True)
        self.ulfbert_body_UIs['ulfbert_icon_25'] = cmds.symbolButton(bgc=(1.0,1.0,1.0),image="icons/Helga_character_UI/cms_cog.png", h=45, vis=True)
        self.ulfbert_body_UIs['ulfbert_icon_27'] = cmds.symbolButton(bgc=(1.0,1.0,1.0),image="icons/Helga_character_UI/cms_cog.png", h=45, vis=True)
        self.ulfbert_body_UIs['ulfbert_icon_28'] = cmds.symbolButton(bgc=(1.0,1.0,1.0),image="icons/Helga_character_UI/cms_cog.png", h=45, vis=True)
        self.ulfbert_body_UIs['ulfbert_icon_29'] = cmds.symbolButton(bgc=(1.0,1.0,1.0),image="icons/Helga_character_UI/cms_cog.png", h=45, vis=True)
        self.ulfbert_body_UIs['ulfbert_icon_30'] = cmds.symbolButton(bgc=(1.0,1.0,1.0),image="icons/Helga_character_UI/cms_cog.png", h=45, vis=True)
        self.ulfbert_body_UIs['ulfbert_icon_31'] = cmds.symbolButton(bgc=(1.0,1.0,1.0),image="icons/Helga_character_UI/cms_cog.png", h=45, vis=True)
        self.ulfbert_body_UIs['ulfbert_icon_32'] = cmds.symbolButton(bgc=(1.0,1.0,1.0),image="icons/Helga_character_UI/cms_cog.png", h=45, vis=True)
        self.ulfbert_body_UIs['ulfbert_icon_33'] = cmds.symbolButton(bgc=(1.0,1.0,1.0),image="icons/Helga_character_UI/cms_cog.png", h=45, vis=True)
        self.ulfbert_body_UIs['ulfbert_icon_34'] = cmds.symbolButton(bgc=(1.0,1.0,1.0),image="icons/Helga_character_UI/cms_cog.png", h=45, vis=True)
        self.ulfbert_body_UIs['ulfbert_icon_35'] = cmds.symbolButton(bgc=(1.0,1.0,1.0),image="icons/Helga_character_UI/cms_cog.png", h=45, vis=True)
        self.ulfbert_body_UIs['ulfbert_icon_36'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_37'] = cmds.symbolButton( h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_38'] = cmds.symbolButton(bgc=(1.0,1.0,1.0),image="icons/Helga_character_UI/cms_cog.png", h=45, vis=True)
        self.ulfbert_body_UIs['ulfbert_icon_39'] = cmds.symbolButton( h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_40'] = cmds.symbolButton( h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_41'] = cmds.symbolButton(bgc=(1.0,1.0,0.5),image="icons/Helga_character_UI/cms_cog.png", h=45, vis=True, command=self.select_ulfbert_chestA)
        self.ulfbert_body_UIs['ulfbert_icon_42'] = cmds.symbolButton( h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_43'] = cmds.symbolButton( h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_45'] = cmds.symbolButton(bgc=(1.0,1.0,1.0),image="icons/Helga_character_UI/cms_cog.png", h=45, vis=True)
        self.ulfbert_body_UIs['ulfbert_icon_46'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_47'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_48'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_49'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_50'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_51'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_52'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_53'] = cmds.symbolButton(bgc = (1.0,1.0,1.0),image="icons/Helga_character_UI/cms_cog.png", h=45, vis=True)
        self.ulfbert_body_UIs['ulfbert_icon_54'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_55'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_56'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_57'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_58'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_59'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_60'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_61'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_62'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_63'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_64'] = cmds.symbolButton(bgc = (1.0,1.0,1.0), image="icons/Helga_character_UI/cms_cog.png", h=45, vis=True)
        self.ulfbert_body_UIs['ulfbert_icon_65'] = cmds.symbolButton( h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_66'] = cmds.symbolButton( h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_67'] = cmds.symbolButton( h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_68'] = cmds.symbolButton( h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_69'] = cmds.symbolButton( h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_70'] = cmds.symbolButton( h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_71'] = cmds.symbolButton( h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_72'] = cmds.symbolButton( h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_73'] = cmds.symbolButton( h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_74'] = cmds.symbolButton( h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_75'] = cmds.symbolButton(bgc= (1.0,1.0,1.0), image="icons/Helga_character_UI/cms_cog.png", h=45, vis=True)
        self.ulfbert_body_UIs['ulfbert_icon_76'] = cmds.symbolButton( h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_77'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_78'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_79'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_80'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_6'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_7'] = cmds.symbolButton(bgc= (1.0,1.0,1.0),image="icons/Helga_character_UI/cms_cog.png",h=45, vis=True)
        self.ulfbert_body_UIs['ulfbert_icon_8'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_9'] = cmds.symbolButton(bgc= (1.0,1.0,1.0),image="icons/Helga_character_UI/cms_cog.png",h=45, vis=True)
        self.ulfbert_body_UIs['ulfbert_icon_10'] = cmds.symbolButton(bgc= (1.0,1.0,1.0),image="icons/Helga_character_UI/cms_cog.png",h=45, vis=True)
        self.ulfbert_body_UIs['ulfbert_icon_11'] = cmds.symbolButton(bgc= (1.0,0.5,1.0),image="icons/Helga_character_UI/cms_cog.png", h=45, vis=True, command=self.select_ulfbert_hipsA)
        self.ulfbert_body_UIs['ulfbert_icon_12'] = cmds.symbolButton(bgc= (1.0,1.0,1.0),image="icons/Helga_character_UI/cms_cog.png", h=45, vis=True)
        self.ulfbert_body_UIs['ulfbert_icon_13'] = cmds.symbolButton(bgc=(1.0,1.0,1.0),image="icons/Helga_character_UI/cms_cog.png",h=45, vis=True)
        self.ulfbert_body_UIs['ulfbert_icon_14'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_15'] = cmds.symbolButton(bgc=(1.0,1.0,1.0),image="icons/Helga_character_UI/cms_cog.png",h=45, vis=True)
        self.ulfbert_body_UIs['ulfbert_icon_16'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_17'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_18'] = cmds.symbolButton(bgc= (1.0,1.0,1.0),image="icons/Helga_character_UI/cms_cog.png", h=45, vis=True)
        self.ulfbert_body_UIs['ulfbert_icon_1'] = cmds.symbolButton(bgc= (1.0,1.0,1.0),image="icons/Helga_character_UI/cms_cog.png", h=45, vis=True)
        self.ulfbert_body_UIs['ulfbert_icon_2'] = cmds.symbolButton(bgc= (1.0,1.0,1.0),image="icons/Helga_character_UI/cms_cog.png", h=45, vis=True)
        self.ulfbert_body_UIs['ulfbert_icon_3'] = cmds.symbolButton(bgc= (1.0,1.0,1.0),image="icons/Helga_character_UI/cms_cog.png", h=45, vis=True)
        self.ulfbert_body_UIs['ulfbert_icon_4'] = cmds.symbolButton(bgc= (1.0,1.0,1.0),image="icons/Helga_character_UI/cms_cog.png", h=45, vis=True)
        self.ulfbert_body_UIs['ulfbert_icon_5'] = cmds.symbolButton(bgc= (1.0,1.0,1.0),image="icons/Helga_character_UI/cms_cog.png", h=45, vis=True)
        self.ulfbert_body_UIs['ulfbert_icon_6'] = cmds.symbolButton(bgc= (1.0,1.0,1.0),image="icons/Helga_character_UI/cms_cog.png", h=45, vis=True)
        self.ulfbert_body_UIs['ulfbert_icon_7'] = cmds.symbolButton(bgc= (1.0,1.0,1.0),image="icons/Helga_character_UI/cms_cog.png", h=45, vis=True)
        self.ulfbert_body_UIs['ulfbert_icon_8'] = cmds.symbolButton(bgc= (1.0,1.0,1.0),image="icons/Helga_character_UI/cms_cog.png", h=45, vis=True)
        self.ulfbert_body_UIs['ulfbert_icon_9'] = cmds.symbolButton( h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_10'] = cmds.symbolButton( h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_11'] = cmds.symbolButton( h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_12'] = cmds.symbolButton( h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_13'] = cmds.symbolButton(bgc= (1.0,1.0,1.0),image="icons/Helga_character_UI/cms_cog.png", h=45, vis=True)
        self.ulfbert_body_UIs['ulfbert_icon_14'] = cmds.symbolButton(bgc= (1.0,1.0,1.0),image="icons/Helga_character_UI/cms_cog.png", h=45, vis=True)
        self.ulfbert_body_UIs['ulfbert_icon_15'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_16'] = cmds.symbolButton(bgc= (1.0,1.0,1.0),image="icons/Helga_character_UI/cms_cog.png", h=45, vis=True)
        self.ulfbert_body_UIs['ulfbert_icon_17'] = cmds.symbolButton(bgc= (1.0,1.0,1.0),image="icons/Helga_character_UI/cms_cog.png", h=45, vis=True)
        self.ulfbert_body_UIs['ulfbert_icon_18'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_1'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_2'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_3'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_4'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_5'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_6'] = cmds.symbolButton(bgc= (1.0,1.0,1.0),image="icons/Helga_character_UI/cms_cog.png", h=45, vis=True)
        self.ulfbert_body_UIs['ulfbert_icon_7'] = cmds.symbolButton(bgc= (1.0,1.0,1.0),image="icons/Helga_character_UI/cms_cog.png", h=45, vis=True)
        self.ulfbert_body_UIs['ulfbert_icon_8'] = cmds.symbolButton(bgc= (1.0,1.0,1.0),image="icons/Helga_character_UI/cms_cog.png", h=45, vis=True)
        self.ulfbert_body_UIs['ulfbert_icon_9'] = cmds.symbolButton(bgc= (1.0,1.0,1.0),image="icons/Helga_character_UI/cms_cog.png", h=45, vis=True)
        self.ulfbert_body_UIs['ulfbert_icon_10'] = cmds.symbolButton(bgc= (1.0,1.0,1.0),image="icons/Helga_character_UI/cms_cog.png", h=45, vis=True)
        self.ulfbert_body_UIs['ulfbert_icon_11'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_12'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_13'] = cmds.symbolButton(h=45, vis=False)
        cmds.setParent('..')
        # self.ulfbert_body_UIs['ulfbert_separator_a'] = cmds.separator(h=20, st='none', vis=True)
        # self.ulfbert_body_UIs['ulfbert_rowColumn_b'] = cmds.rowColumnLayout('ulfbert_rowColumn_b', w= self.ulfbert_child_width, h=100, numberOfColumns=6, columnSpacing=(1,1),
        #                                                     columnWidth=[(1,60), (2,100), (3,60),(4,100), (5,60),(6,100)], parent = self.ulfbert_body_UIs['ulfbert_column_a'] )
        # ##---X----
        # self.ulfbert_body_UIs['ulfbert_trans_x_text'] = cmds.text('ulfbert_trans_x_text',label="Translate X")
        # self.ulfbert_body_UIs['ulfbert_trans_x_textField'] = cmds.textField('ulfbert_trans_x_textField', text="0")
        # self.ulfbert_body_UIs['ulfbert_rotate_x_text'] = cmds.text('ulfbert_rotate_x_text',label="Rotate X")
        # self.ulfbert_body_UIs['ulfbert_rotate_x_textField'] = cmds.textField('ulfbert_rotate_x_textField', text="0")
        # self.ulfbert_body_UIs['ulfbert_scale_x_text'] = cmds.text('ulfbert_scale_x_text',label="Scale X")
        # self.ulfbert_body_UIs['ulfbert_scale_x_textField'] = cmds.textField('ulfbert_scale_x_textField', text="0")
        # ##---Y----
        # self.ulfbert_body_UIs['ulfbert_trans_y_text'] = cmds.text('ulfbert_trans_y_text',label="Translate Y")
        # self.ulfbert_body_UIs['ulfbert_trans_y_textField'] = cmds.textField('ulfbert_trans_y_textField', text="0")
        # self.ulfbert_body_UIs['ulfbert_rotate_y_text'] = cmds.text('ulfbert_rotate_y_text',label="Rotate Y")
        # self.ulfbert_body_UIs['ulfbert_rotate_y_textField'] = cmds.textField('ulfbert_rotate_y_textField', text="0")
        # self.ulfbert_body_UIs['ulfbert_scale_y_text'] = cmds.text('ulfbert_scale_y_text',label="Scale Y")
        # self.ulfbert_body_UIs['ulfbert_scale_y_textField'] = cmds.textField('ulfbert_scale_y_textField', text="0")
        # ##---Z----
        # self.ulfbert_body_UIs['ulfbert_trans_z_text'] = cmds.text('ulfbert_trans_z_text',label="Translate Z")
        # self.ulfbert_body_UIs['ulfbert_trans_z_textField'] = cmds.textField('ulfbert_trans_z_textField', text="0")
        # self.ulfbert_body_UIs['ulfbert_rotate_z_text'] = cmds.text('ulfbert_rotate_z_text',label="Rotate Z")
        # self.ulfbert_body_UIs['ulfbert_rotate_z_textField'] = cmds.textField('ulfbert_rotate_z_textField', text="0")
        # self.ulfbert_body_UIs['ulfbert_scale_z_text'] = cmds.text('ulfbert_scale_z_text',label="Scale Z")
        # self.ulfbert_body_UIs['ulfbert_scale_z_textField'] = cmds.textField('ulfbert_scale_z_textField', text="0")
        # ##---button----
        # self.ulfbert_body_UIs['ulfbert_text_palceHolder_a'] = cmds.text('ulfbert_text_palceHolder_a',label="")
        # self.ulfbert_body_UIs['ulfbert_key_trans_button'] = cmds.button('ulfbert_key_trans_button', label="Key Translate")
        # self.ulfbert_body_UIs['ulfbert_text_palceHolder_b'] = cmds.text('ulfbert_text_palceHolder_b',label="")
        # self.ulfbert_body_UIs['ulfbert_key_rotate_button'] = cmds.button('ulfbert_key_rotate_button', label="Key Rotate")
        # self.ulfbert_body_UIs['ulfbert_text_palceHolder_c'] = cmds.text('ulfbert_text_palceHolder_c',label="")
        #self.ulfbert_body_UIs['ulfbert_key_scale_button'] = cmds.button('ulfbert_key_scale_button', label="Key Scale")


        self.ulfbert_body_UIs['ulfbert_column_b'] = cmds.columnLayout('ulfbert_column_b', columnAttach=('both', 20), rowSpacing=3, columnWidth=self.ulfbert_child_width, parent =self.ulfbert_body_UIs['ulfbert_column_a'] )
        self.ulfbert_body_UIs['ulfbert_key_all_button'] = cmds.button('ulfbert_key_all_button', label="Key all")
        self.ulfbert_body_UIs['ulfbert_key_save_body_button'] = cmds.button('ulfbert_key_save_body_button', label="Save Body Pose")
        self.ulfbert_body_UIs['ulfbert_key_open_libary_button'] = cmds.button('ulfbert_key_open_libary_button', label="Open Body Pose Libary")


        cmds.showWindow(self.ulfbert_body_UIs["ulfbert_body_win"])

    def select_ulfbert_hipsA(self, *args):
        ulfbert_hipsA = cmds.select('spine_hipsA_ctrl')
    #     self.get_trans_data('spine_hipsA_ctrl')
    #     self.get_rotate_data('spine_hipsA_ctrl')
    #     self.get_scale_data('spine_hipsA_ctrl')
    #     # self.connect_attr('spine_hipsA_ctrl.translateX','ulfbert_trans_x_textField.text')
    #     # self.connect_attr('spine_hipsA_ctrl.translateY','ulfbert_trans_y_textField.text')
    #     # self.connect_attr('spine_hipsA_ctrl.translateZ','ulfbert_trans_z_textField.text')

    def select_ulfbert_chestA(self, *args):
        ulfbert_chestA = cmds.select('spine_chestA_ctrl')
    #     self.get_trans_data('spine_chestA_ctrl')
    #     self.get_rotate_data('spine_chestA_ctrl')
    #     self.get_scale_data('spine_chestA_ctrl')
    #     # self.connect_attr('spine_chestA_ctrl.translateX','ulfbert_trans_x_textField.text')
    #     # self.connect_attr('spine_chestA_ctrl.translateY','ulfbert_trans_y_textField.text')
    #     # self.connect_attr('spine_chestA_ctrl.translateZ','ulfbert_trans_z_textField.text')

    # def get_trans_data(self, name):
    #     val_trans_x = cmds.getAttr(name+'.translateX')
    #     val_trans_y = cmds.getAttr(name+'.translateY')
    #     val_trans_z = cmds.getAttr(name+'.translateZ')
    #     cmds.textField('ulfbert_trans_x_textField', edit=True, text=val_trans_x)
    #     cmds.textField('ulfbert_trans_y_textField', edit=True, text=val_trans_y)
    #     cmds.textField('ulfbert_trans_z_textField', edit=True, text=val_trans_z)
    #     print val_trans_x
    #     print val_trans_y
    #     print val_trans_z
    # def get_rotate_data(self, name):
    #     val_rotate_x = cmds.getAttr(name+'.rotateX')
    #     val_rotate_y = cmds.getAttr(name+'.rotateY')
    #     val_rotate_z = cmds.getAttr(name+'.rotateZ')
    #     cmds.textField('ulfbert_rotate_x_textField', edit=True, text=val_rotate_x)
    #     cmds.textField('ulfbert_rotate_y_textField', edit=True, text=val_rotate_y)
    #     cmds.textField('ulfbert_rotate_z_textField', edit=True, text=val_rotate_z)
    #     print val_rotate_x
    #     print val_rotate_y
    #     print val_rotate_z
    # def get_scale_data(self, name):
    #     val_scale_x = cmds.getAttr(name+'.scaleX')
    #     val_scale_y = cmds.getAttr(name+'.scaleY')
    #     val_scale_z = cmds.getAttr(name+'.scaleZ')
    #     cmds.textField('ulfbert_scale_x_textField', edit=True, text=val_scale_x)
    #     cmds.textField('ulfbert_scale_y_textField', edit=True, text=val_scale_y)
    #     cmds.textField('ulfbert_scale_z_textField', edit=True, text=val_scale_z)
    #     print val_scale_x
    #     print val_scale_y
    #     print val_scale_z

    # def connect_attr(self, driver, driven):
    #     cmds.connectAttr(driver, driven)


  



    def delete_ulfbert_character_body_UI(self, *args):
        self.quit_UI_window('ulfbert_body_window')









class Helja_body_UI(Base):
    def __init__(self, helja_parent_width = 500, helja_parent_height = 500, helja_child_width = 480, helja_child_height = 480):

        super(Helja_body_UI, self).__init__()

        self.helja_body_UIs = {}
        #self.delete_window('helga_anim_choice_window')
        self.helja_parent_width = helja_parent_width
        self.helja_parent_height = helja_parent_height
        self.helja_child_width = helja_child_width
        self.helja_child_height = helja_child_height
        self.helja_body_UIs["helja_body_win"] = cmds.window('helja_body_window', title = 'Helga Character UI',
                                                widthHeight = (self.helja_parent_width,self.helja_parent_height),
                                                menuBar = True, sizeable = True, minimizeButton=True, maximizeButton=False)
        self.helja_body_main_UI()

    def helja_body_main_UI(self, *args):
        self.helja_body_UIs['helja_column_a'] = cmds.columnLayout('helja_column_a', columnAttach=('both', 20), rowSpacing=3, columnWidth=self.helja_parent_width)
        cmds.showWindow(self.helja_body_UIs["helja_body_win"])
    def delete_helja_character_body_UI(self, *args):
        self.quit_UI_window('helja_body_window')


class Ritter_body_UI(Base):
    def __init__(self, ritter_parent_width = 500, ritter_parent_height = 500, ritter_child_width = 480, ritter_child_height = 480):

        super(Ritter_body_UI, self).__init__()

        self.ritter_body_UIs = {}
        #self.delete_window('helga_anim_choice_window')
        self.ritter_parent_width = ritter_parent_width
        self.ritter_parent_height = ritter_parent_height
        self.ritter_child_width = ritter_child_width
        self.ritter_child_height = ritter_child_height
        self.ritter_body_UIs["ritter_body_win"] = cmds.window('ritter_body_window', title = 'Ritter Character UI',
                                                widthHeight = (self.ritter_parent_width,self.ritter_parent_height),
                                                menuBar = True, sizeable = True, minimizeButton=True, maximizeButton=False)
        self.ritter_body_main_UI()

    def ritter_body_main_UI(self, *args):
        self.ritter_body_UIs['ritter_column_a'] = cmds.columnLayout('ritter_column_a', columnAttach=('both', 20), rowSpacing=3, columnWidth=self.ritter_parent_width)
        cmds.showWindow(self.ritter_body_UIs["ritter_body_win"])
    def delete_ritter_character_body_UI(self, *args):
        self.quit_UI_window('ritter_body_window')

#################################################################################
#
#
#ANIM_UI_character_body_function
#
#
#################################################################################

#################################################################################
#
#
#calling main class
#
#
#################################################################################
if(__name__ == '__main__'):
    Helga_cms_login_UI()