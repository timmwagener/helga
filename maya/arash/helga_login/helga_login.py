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
HELGA_VERSION = "v 0.1"
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

        query_username = getpass.getuser()
        self.loginUIs = {}

        self.delete_window('helga_cms_login')
        self.delete_window('helga_td_window')
        self.delete_window('helper')
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
        Helga_cms_td_UI()
        self.delete_window('helga_cms_login')

    def run_helga_cms_anim_UI(self, *args):
        Helga_cms_anim_UI()
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
        self.tdUIs["td_modules_frame_a"] = cmds.frameLayout('td_modules_frame_a',label='Modules', bgc=Color.gray_a ,cll = True, borderStyle ='in', w=self.parent_width)
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
        self.tdUIs["td_modules_frame_b"] = cmds.frameLayout('td_modules_frame_b',label='Check Modules',bgc=Color.gray_a , cll = True, borderStyle ='in', w=self.parent_width)
        self.tdUIs["td_modules_button_delete_module_a"] = cmds.button('td_modules_button_delete_module_a',label="Delete selected Module", command=self.delete_module)
        self.tdUIs["td_check_modules_rowColumn_a"] = cmds.rowColumnLayout( numberOfColumns=3, columnWidth=[(1, 180), (2,50), (3, 50)])
        cmds.setParent('..')
        cmds.setParent('..')
        self.tdUIs["td_modules_frame_c"] = cmds.frameLayout('td_modules_frame_c',label='Options',bgc=Color.gray_a ,  cll = True, borderStyle ='in', w=self.parent_width)
        self.tdUIs["td_modules_rowColumn_b"] = cmds.rowColumnLayout( numberOfColumns=2, columnWidth=[(1, 150), (2, 150)])
        self.tdUIs["td_modules_checkBox_a"] = cmds.checkBox('td_modules_checkBox_a', label = "Show Joint after Rigging" )
        cmds.setParent('..')
        cmds.setParent('..')
        self.tdUIs["td_modules_frame_d"] = cmds.frameLayout('td_modules_frame_d',label='Rig Modules',bgc=Color.gray_a ,  cll = True, borderStyle ='in', w=self.parent_width)
        self.tdUIs["td_modules_layout_e"] = cmds.columnLayout('td_modules_layout_e', columnAttach = ('both', 0), rowSpacing = 1)
        self.tdUIs["space_a"]=cmds.separator(h=5, vis=True, st='none',w=self.child_width)
        self.tdUIs["td_rig_modules_button_a"] = cmds.button('td_rig_modules_button_a', bgc = Color.blue_a,label='Rig all Modules', h=30, w=self.child_width)
        self.tdUIs["space_b"]=cmds.separator(h=5, vis=True, st='none',w=self.child_width)
        self.tdUIs["td_rig_modules_button_b"] = cmds.button('td_rig_modules_button_b', bgc = Color.green_a, label='Rig selected Modules', h=30, w=self.child_width)
        self.tdUIs["space_c"]=cmds.separator(h=5, vis=True, st='none',w=self.child_width)
        cmds.setParent('..')
        cmds.setParent('..')
        self.tdUIs["td_modules_frame_e"] = cmds.frameLayout('td_modules_frame_e',label='Skinning',bgc=Color.gray_a ,  cll = True, borderStyle ='in', w=self.parent_width)
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
        self.tdUIs["td_modules_frame_f"] = cmds.frameLayout('td_modules_frame_f',label='Tools',bgc=Color.gray_a ,  cll = True, borderStyle ='in', w=self.parent_width)
        self.tdUIs["td_modules_layout_g"] = cmds.columnLayout('td_modules_layout_g', columnAttach = ('both', 0), rowSpacing = 1)
        self.tdUIs["color_a"] = cmds.symbolButton(h=50, vis=True, w=self.child_width )
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
        query_select_button_a = cmds.button('td_check_modules_button_a', q=True, label=True)
        query_select_button_c = cmds.button('td_check_modules_button_c', q=True, label=True)
        query_select_button_e = cmds.button('td_check_modules_button_e', q=True, label=True)
        query_select_button_g = cmds.button('td_check_modules_button_g', q=True, label=True)
        query_select_button_i = cmds.button('td_check_modules_button_i', q=True, label=True)
        if query_select_button_a =="S":
            cmds.deleteUI('td_check_modules_text_a','td_check_modules_button_a','td_check_modules_button_b')
        else:
            pass
        if query_select_button_c =="S":
            cmds.deleteUI('td_check_modules_text_b','td_check_modules_button_c','td_check_modules_button_d')
        else:
            pass
        if query_select_button_e =="S":
            cmds.deleteUI('td_check_modules_text_c','td_check_modules_button_e','td_check_modules_button_f' )
        else:
            pass
        if query_select_button_g =="S":
            cmds.deleteUI('td_check_modules_text_d','td_check_modules_button_g','td_check_modules_button_h' )
        else:
            pass
        if query_select_button_i =="S":
            cmds.deleteUI('td_check_modules_text_e','td_check_modules_button_i','td_check_modules_button_j' )
        else:
            cmds.warning("no Module selected")








            # cmds.button(name, edit=True, bgc=value)
    # def change_color_arm(self, name):
    #     self.name = name
    #     cmds.button(name, edit=True, bgc=self.value)


        # print scene_joints


        # print query_checkBox_helgaCMS_jnt

#################################################################################
#
#
#ANIM_UI
#
#
#################################################################################
class Helga_cms_anim_UI:

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
    Helga_cms_login_UI()