

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

# Global Helpstrings
HELGA_VERSION = "0.1"
helper_td_main_module = "Hallo Welcome to Helga CMS"
helper_arm_module = "arm________________"
helper_leg_module = "leg________________"
helper_spine_module = "spine________________"
helper_head_module = "head________________"
helper_biped_module = "biped________________"
about="Author: Arash Hosseini"+"\n"+     "Contact: s.arashhosseini@gmail.com     Tel.: 0178 6100 674 "


#Changed image_path to be relative to your tool. If you dont want that,
#uncomment your original below. / Timm
relative_image_path = 'media/images'
image_path = os.path.join(os.path.dirname(__file__), relative_image_path)
#image_path="Y:/Production/scripts/deploy/helga/maya/arash/helga_login/media/images"


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

    # helper
    def setValue(self, nodeName, attrName, node):
        try:
            cmds.setAttr((nodeName + '.' + attrName), float(node.getAttribute(attrName)))
        except Exception, e:
            print nodeName + "." + attrName + " was locked"


    def saveValue(self, nodeName, attrName, object_node):
        attrValue = cmds.getAttr(nodeName + "." + attrName)
        object_node.setAttribute(attrName, str(attrValue))


    def delete_window(self, name):
        if cmds.window(name, query = True, exists =True):
            cmds.deleteUI(name, window = True)

    def delete_dock_control(self, name):
        if cmds.dockControl(name, query = True, exists=True):
            cmds.deleteUI(name, control=True)


    def quit_UI_window(self, name):
        if cmds.window(name, query = True, exists =True):
            cmds.deleteUI(name, window = True)

    def select_ulfbert_character_controller(self, name, *args):
        ulfbert_select_namespace_list = pm.system.listNamespaces()
        if len(ulfbert_select_namespace_list)==0:
            cmds.warning('No Character in Scene')
        else:
            query_ulfbert_selected_namespace_controller=cmds.optionMenu('ulfbert_namespace_optionmenu_a', q=True, v=True)
            cmds.select(str(query_ulfbert_selected_namespace_controller)+":"+str(name))


    def select_ulfbert_hand_controller(self, name, *args):
        ulfbert_hand_namespace_list = pm.system.listNamespaces()
        if len(ulfbert_hand_namespace_list)==0:
            cmds.warning('No Character in Scene')
        else:
            #cmds.select(clear=True)
            query_ulfbert_hand_namespace_controller=cmds.optionMenu('ulfbert_namespace_optionmenu_a', q=True, v=True)
            cmds.select(str(query_ulfbert_hand_namespace_controller)+":"+str(name))


    def fk2ik_ulfbert_character(self, name, *args):
        ulfbert_fk2ik_change_list = pm.system.listNamespaces()
        if len(ulfbert_fk2ik_change_list)==0:
            cmds.warning('No Character in Scene')
        else:
            ulfbert_fk2ik_change_query=cmds.optionMenu('ulfbert_namespace_optionmenu_a', q=True, v=True)
            ulfbert_fk2ik_change_current_name=(str(ulfbert_fk2ik_change_query)+":"+("master_ctrl"))
            cmds.setAttr(ulfbert_fk2ik_change_current_name+name, 0)

    def ik2fk_ulfbert_character(self, name, *args):
        ulfbert_ik2fk_change_list = pm.system.listNamespaces()
        if len(ulfbert_ik2fk_change_list)==0:
            cmds.warning('No Character in Scene')
        else:
            ulfbert_ik2fk_change_query=cmds.optionMenu('ulfbert_namespace_optionmenu_a', q=True, v=True)
            ulfbert_ik2fk_change_current_name=(str(ulfbert_ik2fk_change_query)+":"+("master_ctrl"))
            cmds.setAttr(ulfbert_ik2fk_change_current_name+name, 1)

    def set_name_save_pose(self, *args):
        query_main_body_UI_set_name=cmds.text('ulfbert_namespace_select_a',q=True, label=True)
        split_query_main_body_UI_set_name=query_main_body_UI_set_name.replace(":", "")
        cmds.textField('character_save_pose_scroll_c', e=True, text=split_query_main_body_UI_set_name)
    # def ik2fk_ulfbert_character(self, name, *args):


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
        self.loginUIs["image_path"] = cmds.internalVar(upd = True)
        self.loginUIs["image"] =cmds.image(w = 300, h = 100, image = image_path + "/icon_helgaCMS_login.png")
        self.loginUIs["separator_b"] = cmds.separator(h=10, vis=True, st='none')
        self.loginUIs["rowColumnLayout_a"] = cmds.rowColumnLayout( numberOfColumns=5, columnSpacing=(1,1),
                                                                    columnWidth=[(1,50), (2,100), (3,50),(4,100), (5,50)])
        self.loginUIs["color_a"] = cmds.symbolButton(h=100, vis=False)
        self.loginUIs["color_b"] = cmds.symbolButton(image=image_path + "/icon_helgaCMS_TD.png", h=100, vis=True, command = self.run_helga_cms_td_UI)
        self.loginUIs["color_c"] = cmds.symbolButton(image=image_path + "/icon_helgaCMS_login_design.png",h=100, vis=True)
        self.loginUIs["color_d"] = cmds.symbolButton(image=image_path + "/icon_helgaCMS_Animation.png", h=100, vis=True, command = self.run_helga_cms_anim_UI)
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
        self.tdUIs["td_modules_image_a"] = cmds.image(h=30, image = image_path+"/icon_helgaCMS_armModule.png")
        self.tdUIs["td_modules_button_b"] = cmds.button(h=30, label = "create arm Module",  vis=True, command =self.create_check_module_arm)
        self.tdUIs["td_modules_button_c"] = cmds.button(h=30, label = '?',  vis=True, command = (lambda message: self.show_helper(helper_leg_module)))
        self.tdUIs["td_modules_image_b"] = cmds.image(h=30, image = image_path+"/icon_helgaCMS_legModule.png")
        self.tdUIs["td_modules_button_d"] = cmds.button(h=30, label = "create leg Module",  vis=True, command =self.create_check_module_leg)
        self.tdUIs["td_modules_button_e"] = cmds.button(h=30, label = '?',  vis=True, command = (lambda message: self.show_helper(helper_spine_module)))
        self.tdUIs["td_modules_image_c"] = cmds.image(h=30, image = image_path+"/icon_helgaCMS_spineModule.png")
        self.tdUIs["td_modules_button_f"] = cmds.button(h=30, label = "create spine Module",  vis=True, command =self.create_check_module_spine)
        self.tdUIs["td_modules_button_g"] = cmds.button(h=30, label = '?',  vis=True, command = (lambda message: self.show_helper(helper_head_module)))
        self.tdUIs["td_modules_image_d"] = cmds.image(h=30, image = image_path+"/icon_helgaCMS_headModule.png")
        self.tdUIs["td_modules_button_h"] = cmds.button(h=30, label = "create head Module",  vis=True, command =self.create_check_module_head)
        self.tdUIs["td_modules_button_i"] = cmds.button(h=30, label = '?',  vis=True, command = (lambda message: self.show_helper(helper_biped_module)))
        self.tdUIs["td_modules_image_e"] = cmds.image(h=30, image = image_path+"/icon_helgaCMS_bipedModule.png")
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
        self.tdUIs["color_a"] = cmds.symbolButton(image=image_path+"/icon_helgaCMS_jelly_tool_Module.png", h=50, vis=True, w=self.child_width , command =self.tool_jelly)
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
        helga_anim_choice_win_height = 250
        self.delete_window('helga_anim_choice_window')
        self.anim_choiceUIs["helga_anim_choice_win"] = cmds.window('helga_anim_choice_window', title = 'Helga Character Set',
                                                widthHeight = (helga_anim_choice_win_width,helga_anim_choice_win_height), menuBar = True, sizeable = False,
                                                minimizeButton=True, maximizeButton=False)
        self.character_choice()
    def character_choice(self, *args):
        self.anim_choiceUIs['helga_choice_column_a']=cmds.columnLayout('helga_choice_column_a', columnAttach=('both', 0), rowSpacing=0, columnWidth=300)
        self.anim_choiceUIs['helga_choise_image_a']=cmds.image('helga_choise_image_a', image=image_path+"/cms_create_character_UI.png")
        self.anim_choiceUIs['helga_choice_column_a']=cmds.columnLayout('helga_choice_column_b', columnAttach=('both', 20), rowSpacing=3, columnWidth=300)
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
            self.delete_ulfbert_hand_UI()
            Ulfbert_hand_UI()
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

    def delete_ulfbert_hand_UI(self, *args):
        if cmds.window('ulfbert_hand_body_window', exists = True):
            self.delete_window('ulfbert_hand_body_window')


#################################################################################
#
#
#ANIM_UI_character_body_UI
#
#
#################################################################################

class Ulfbert_body_UI(Base):
    def __init__(self, ulfbert_parent_width = 500, ulfbert_parent_height = 620, ulfbert_child_width = 495, ulfbert_child_height = 495):

        super(Ulfbert_body_UI, self).__init__()

        self.ulfbert_body_UIs = {}
        #self.delete_window('helga_anim_choice_window')
        self.ulfbert_parent_width = ulfbert_parent_width
        self.ulfbert_parent_height = ulfbert_parent_height
        self.ulfbert_child_width = ulfbert_child_width
        self.ulfbert_child_height = ulfbert_child_height
        self.ulfbert_body_UIs["ulfbert_body_win"] = cmds.window('ulfbert_body_window', title = 'Ulfbert Character UI',
                                                widthHeight = (self.ulfbert_parent_width,self.ulfbert_parent_height),
                                                menuBar = True, sizeable = False, topEdge= 0, leftEdge= 0, minimizeButton=True, maximizeButton=False)
        cmds.menu('ulfbert_reference_window', label='Reference', tearOff=True)
        cmds.menuItem('ulfbert_reference_a', label='create Reference', command=self.ulfbert_create_reference)
        cmds.menuItem('ulfbert_reference_b', label='Reference Editor', command=self.ulfbert_reference_editor)
        cmds.setParent('..', menu=True)
        cmds.menu('ulfbert_optionMenu_window_a', label= 'Pose',tearOff = True)
        cmds.menuItem ('ulfbert_mirror_pose', label='Mirror', command=self.ulfbert_mirror_pose)
        cmds.menuItem ('ulfbert_reset_pose', label='Reset', command=self.ulfbert_reset_pose)
        cmds.setParent('..', menu=True)
        cmds.menu('ulfbert_optionMenu_window_b', label= 'Display',tearOff = True)
        cmds.menuItem ('ulfbert_show_controls', label='Controls')
        cmds.setParent('..', menu=True)
        cmds.menu('ulfbert_optionMenu_window_c', label="Help", tearOff=True)
        cmds.menuItem('ulfbert_send_debug', label="Send Debug", command=self.ulfbert_debug)
        cmds.menuItem('ulfbert_about', label="About", command= self.ulfbert_about)
        self.ulfbert_body_main_UI()

    def ulfbert_body_main_UI(self, *args):
        self.ulfbert_body_UIs['ulfbert_column_a_x'] = cmds.columnLayout('ulfbert_column_a_x', columnAttach=('both', 100), rowSpacing=3,h=50, columnWidth=self.ulfbert_child_width, parent =self.ulfbert_body_UIs["ulfbert_body_win"] )
        cmds.separator(h=5, st='none')
        self.ulfbert_body_UIs['ulfbert_namespace_button_a']=cmds.button('ulfbert_namespace_button_a', label="Refresh", h=40, command=self.ulfbert_namespace)
        self.ulfbert_body_UIs['ulfbert_namespace_optionmenu_a']=cmds.optionMenu('ulfbert_namespace_optionmenu_a', w=150, label ="Set NameSpace", cc=self.ulfbert_change_namespace_text_color_green)
        self.ulfbert_body_UIs['ulfbert_namespace_select_a']=cmds.text('ulfbert_namespace_select_a', label="No Namespace selected!", h=20, bgc=Color.red)


        self.ulfbert_body_UIs['ulfbert_column_a'] = cmds.columnLayout('ulfbert_column_a', columnAttach=('both', 0), rowSpacing=3, columnWidth=self.ulfbert_child_width, parent =self.ulfbert_body_UIs["ulfbert_body_win"] )
        ########to go'''
        self.ulfbert_body_UIs['ulfbert_rowColumn_a'] = cmds.rowColumnLayout('ulfbert_rowColumn_a', w= self.ulfbert_child_width, h=self.ulfbert_child_height, numberOfColumns=11,
                                                            columnWidth=[(1,45), (2,45), (3,45),(4,45), (5,45),(6,45), (7,45), (8,45),(9,45), (10,45),(11,45)], parent= self.ulfbert_body_UIs['ulfbert_column_a'] )
        #never, have to import as module
        self.ulfbert_body_UIs['ulfbert_icon_1'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_2'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_3'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_4'] = cmds.symbolButton(image=image_path+"/cms_fk2ik_R_Clavicle.png", h=45, vis=True, command=partial (self.fk2ik_ulfbert_character,'.R_clavicle3_IkFkBlend'))
        self.ulfbert_body_UIs['ulfbert_icon_5'] = cmds.symbolButton(image=image_path+"/cms_ik2fk_R_Clavicle.png", h=45, vis=True, command=partial (self.ik2fk_ulfbert_character,'.R_clavicle3_IkFkBlend'))
        self.ulfbert_body_UIs['ulfbert_icon_6'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_7'] = cmds.symbolButton(image=image_path+"/cms_fk2ik_L_Clavicle.png", h=45, vis=True, command=partial (self.fk2ik_ulfbert_character,'.L_clavicle3_IkFkBlend'))
        self.ulfbert_body_UIs['ulfbert_icon_8'] = cmds.symbolButton(image=image_path+"/cms_ik2fk_L_Clavicle.png", h=45, vis=True, command=partial (self.ik2fk_ulfbert_character,'.L_clavicle3_IkFkBlend'))
        self.ulfbert_body_UIs['ulfbert_icon_9'] = cmds.symbolButton( h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_10'] = cmds.symbolButton( h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_11'] = cmds.symbolButton( h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_12'] = cmds.symbolButton( h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_13'] = cmds.symbolButton(image=image_path+"/cms_R_down_arm_off_ctrl.png", h=45, vis=True, command=partial (self.select_ulfbert_character_controller,"R_down_arm_off_ctrl"))
        self.ulfbert_body_UIs['ulfbert_icon_14'] = cmds.symbolButton(image=image_path+"/cms_R_arm_off_ctrl.png", h=45, vis=True, command=partial (self.select_ulfbert_character_controller,"R_arm_off_ctrl"))
        self.ulfbert_body_UIs['ulfbert_icon_15'] = cmds.symbolButton(image=image_path+"/cms_R_up_arm_off_ctrl.png", h=45, vis=True, command=partial (self.select_ulfbert_character_controller,"R_up_arm_off_ctrl"))
        self.ulfbert_body_UIs['ulfbert_icon_16'] = cmds.symbolButton(image=image_path+"/cms_R_arm_clavicle_ik_ctrl.png", h=45, vis=True, command=partial (self.select_ulfbert_character_controller,"R_arm_clavicle_ik_ctrl"))
        self.ulfbert_body_UIs['ulfbert_icon_17'] = cmds.symbolButton(image=image_path+"/cms_head_head_ctrl.png", h=45, vis=True, command=partial (self.select_ulfbert_character_controller,"head_head_ctrl"))
        self.ulfbert_body_UIs['ulfbert_icon_18'] = cmds.symbolButton(image=image_path+"/cms_L_arm_clavicle_ik_ctrl.png", h=45, vis=True, command=partial (self.select_ulfbert_character_controller,"L_arm_clavicle_ik_ctrl"))
        self.ulfbert_body_UIs['ulfbert_icon_20'] = cmds.symbolButton(image=image_path+"/cms_L_up_arm_off_ctrl.png", h=45, vis=True, command=partial (self.select_ulfbert_character_controller,"L_up_arm_off_ctrl"))
        self.ulfbert_body_UIs['ulfbert_icon_21'] = cmds.symbolButton(image=image_path+"/cms_L_arm_off_ctrl.png", h=45, vis=True, command=partial (self.select_ulfbert_character_controller,"L_arm_off_ctrl"))
        self.ulfbert_body_UIs['ulfbert_icon_22'] = cmds.symbolButton(image=image_path+"/cms_L_down_arm_off_ctrl.png", h=45, vis=True, command=partial (self.select_ulfbert_character_controller,"L_down_arm_off_ctrl"))
        self.ulfbert_body_UIs['ulfbert_icon_23'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_24'] = cmds.symbolButton(image=image_path+"/cms_fk2ik_R_Arm.png", h=45, vis=True, command=partial (self.fk2ik_ulfbert_character,'.R_arm3_IkFkBlend'))
        self.ulfbert_body_UIs['ulfbert_icon_25'] = cmds.symbolButton(image=image_path+"/cms_R_arm_wrist_fk_ctrl.png", h=45, vis=True, command=self.ulfbert_R_arm_fkik)
        self.ulfbert_body_UIs['ulfbert_icon_27'] = cmds.symbolButton(image=image_path+"/cms_R_arm_elbow_fk_ctrl.png", h=45, vis=True,command=partial (self.select_ulfbert_character_controller,"R_arm_elbow_fk_ctrl"))
        self.ulfbert_body_UIs['ulfbert_icon_28'] = cmds.symbolButton(image=image_path+"/cms_R_arm_shoulder_fk_ctrl.png", h=45, vis=True,command=partial (self.select_ulfbert_character_controller,"R_arm_shoulder_fk_ctrl"))
        self.ulfbert_body_UIs['ulfbert_icon_29'] = cmds.symbolButton(image=image_path+"/cms_R_arm_clavicle_fk_ctrl.png", h=45, vis=True,command=partial (self.select_ulfbert_character_controller,"R_arm_clavicle_fk_ctrl"))
        self.ulfbert_body_UIs['ulfbert_icon_30'] = cmds.symbolButton(image=image_path+"/cms_head_neck_ctrl.png", h=45, vis=True,command=partial (self.select_ulfbert_character_controller,"head_neck_ctrl"))
        self.ulfbert_body_UIs['ulfbert_icon_31'] = cmds.symbolButton(image=image_path+"/cms_L_arm_clavicle_fk_ctrl.png", h=45, vis=True,command=partial (self.select_ulfbert_character_controller,"L_arm_clavicle_fk_ctrl"))
        self.ulfbert_body_UIs['ulfbert_icon_32'] = cmds.symbolButton(image=image_path+"/cms_L_arm_shoulder_fk_ctrl.png", h=45, vis=True,command=partial (self.select_ulfbert_character_controller,"L_arm_shoulder_fk_ctrl"))
        self.ulfbert_body_UIs['ulfbert_icon_33'] = cmds.symbolButton(image=image_path+"/cms_L_arm_elbow_fk_ctrl.png", h=45, vis=True,command=partial (self.select_ulfbert_character_controller,"L_arm_elbow_fk_ctrl"))
        self.ulfbert_body_UIs['ulfbert_icon_34'] = cmds.symbolButton(image=image_path+"/cms_L_arm_wrist_fk_ctrl.png", h=45, vis=True,command=self.ulfbert_L_arm_fkik)
        self.ulfbert_body_UIs['ulfbert_icon_35'] = cmds.symbolButton(image=image_path+"/cms_fk2ik_L_Arm.png", h=45, vis=True, command=partial (self.fk2ik_ulfbert_character,'.L_arm3_IkFkBlend'))
        self.ulfbert_body_UIs['ulfbert_icon_36'] = cmds.symbolButton(image=image_path+"/cms_ik2fk_R_Arm.png",h=45, vis=True, command=partial (self.ik2fk_ulfbert_character,'.R_arm3_IkFkBlend'))
        self.ulfbert_body_UIs['ulfbert_icon_37'] = cmds.symbolButton( h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_38'] = cmds.symbolButton(image=image_path+"/cms_R_arm_elbow_ik_ctrl.png", h=45, vis=True,command=partial (self.select_ulfbert_character_controller,"R_arm_elbow_ik_ctrl"))
        self.ulfbert_body_UIs['ulfbert_icon_39'] = cmds.symbolButton( h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_40'] = cmds.symbolButton( h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_41'] = cmds.symbolButton(image=image_path+"/cms_spine_chestA_ctrl.png", h=45, vis=True, command=partial (self.select_ulfbert_character_controller,"spine_chestA_ctrl"))
        self.ulfbert_body_UIs['ulfbert_icon_42'] = cmds.symbolButton( h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_43'] = cmds.symbolButton( h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_45'] = cmds.symbolButton(image=image_path+"/cms_L_arm_elbow_ik_ctrl.png", h=45, vis=True, command=partial (self.select_ulfbert_character_controller,"L_arm_elbow_ik_ctrl"))
        self.ulfbert_body_UIs['ulfbert_icon_46'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_47'] = cmds.symbolButton(image=image_path+"/cms_ik2fk_L_Arm.png",h=45, vis=True, command=partial (self.ik2fk_ulfbert_character,'.L_arm3_IkFkBlend'))
        self.ulfbert_body_UIs['ulfbert_icon_48'] = cmds.symbolButton(h=45, vis=True)
        self.ulfbert_body_UIs['ulfbert_icon_49'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_50'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_51'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_52'] = cmds.symbolButton(image=image_path+"/cms_select_spine_main.png",h=45, vis=True, command=self.ulfbert_select_spine)
        self.ulfbert_body_UIs['ulfbert_icon_53'] = cmds.symbolButton(image=image_path+"/cms_spine_chestB_ctrl.png", h=45, vis=True, command=partial (self.select_ulfbert_character_controller,"spine_chestB_ctrl"))
        self.ulfbert_body_UIs['ulfbert_icon_54'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_55'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_56'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_57'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_58'] = cmds.symbolButton(image=image_path+"/cms_save_pose_main.png",h=45, vis=True, command=self.call_save_pose)
        self.ulfbert_body_UIs['ulfbert_icon_59'] = cmds.symbolButton(image=image_path+"/cms_select_all_main.png",h=45, vis=True)
        self.ulfbert_body_UIs['ulfbert_icon_61'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_62'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_63'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_65'] = cmds.symbolButton( h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_64'] = cmds.symbolButton(image=image_path+"/cms_spine_middle1_ctrl.png", h=45, vis=True, command=partial (self.select_ulfbert_character_controller,"spine_middle1_ctrl"))
        self.ulfbert_body_UIs['ulfbert_icon_66'] = cmds.symbolButton( h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_67'] = cmds.symbolButton( h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_68'] = cmds.symbolButton( h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_69'] = cmds.symbolButton( h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_70'] = cmds.symbolButton(image=image_path+"/cms_pose_libary_main.png",h=45, vis=True, command=self.call_load_pose)
        self.ulfbert_body_UIs['ulfbert_icon_60'] = cmds.symbolButton(image=image_path+"/cms_reset_main.png",h=45, vis=True, command=self.ulfbert_reset_body_controller)
        self.ulfbert_body_UIs['ulfbert_icon_71'] = cmds.symbolButton( h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_72'] = cmds.symbolButton( h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_73'] = cmds.symbolButton( image=image_path+"/cms_fk2ik_R_Hip.png",h=45, vis=True, command=partial (self.fk2ik_ulfbert_character,'.R_hip1_IkFkBlend'))
        self.ulfbert_body_UIs['ulfbert_icon_74'] = cmds.symbolButton( image=image_path+"/cms_ik2fk_R_Hip.png",h=45, vis=True, command=partial (self.ik2fk_ulfbert_character,'.R_hip1_IkFkBlend'))
        self.ulfbert_body_UIs['ulfbert_icon_75'] = cmds.symbolButton(image=image_path+"/cms_spine_hipsB_ctrl.png", h=45, vis=True, command=partial (self.select_ulfbert_character_controller,"spine_hipsB_ctrl"))
        self.ulfbert_body_UIs['ulfbert_icon_76'] = cmds.symbolButton(image=image_path+"/cms_fk2ik_L_Hip.png", h=45, vis=True, command=partial (self.fk2ik_ulfbert_character,'.L_hip1_IkFkBlend'))
        self.ulfbert_body_UIs['ulfbert_icon_77'] = cmds.symbolButton(image=image_path+"/cms_ik2fk_L_Hip.png",h=45, vis=True, command=partial (self.ik2fk_ulfbert_character,'.L_hip1_IkFkBlend'))
        self.ulfbert_body_UIs['ulfbert_icon_78'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_79'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_80'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_6'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_7'] = cmds.symbolButton(image=image_path+"/cms_fk2ik_R_Leg.png",h=45, vis=True, command=partial (self.fk2ik_ulfbert_character,'.R_leg1_IkFkBlend'))
        self.ulfbert_body_UIs['ulfbert_icon_8'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_9'] = cmds.symbolButton(image=image_path+"/cms_R_up_leg_off_ctrl.png",h=45, vis=True, command=partial (self.select_ulfbert_character_controller,"R_up_leg_off_ctrl"))
        self.ulfbert_body_UIs['ulfbert_icon_10'] = cmds.symbolButton(image=image_path+"/cms_R_leg_hip_fk_ctrl.png",h=45, vis=True, command=partial (self.select_ulfbert_character_controller,"R_leg_hip_fk_ctrl"))
        self.ulfbert_body_UIs['ulfbert_icon_11'] = cmds.symbolButton(image=image_path+"/cms_spine_hipsA_ctrl.png", h=45, vis=True,command=partial (self.select_ulfbert_character_controller,"spine_hipsA_ctrl"))
        self.ulfbert_body_UIs['ulfbert_icon_12'] = cmds.symbolButton(image=image_path+"/cms_L_leg_hip_fk_ctrl.png", h=45, vis=True, command=partial (self.select_ulfbert_character_controller,"L_leg_hip_fk_ctrl"))
        self.ulfbert_body_UIs['ulfbert_icon_13'] = cmds.symbolButton(image=image_path+"/cms_L_up_leg_off_ctrl.png",h=45, vis=True, command=partial (self.select_ulfbert_character_controller,"L_up_leg_off_ctrl"))
        self.ulfbert_body_UIs['ulfbert_icon_14'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_15'] = cmds.symbolButton(image=image_path+"/cms_fk2ik_L_Leg.png",h=45, vis=True, command=partial (self.fk2ik_ulfbert_character,'.L_leg1_IkFkBlend'))
        self.ulfbert_body_UIs['ulfbert_icon_16'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_17'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_18'] = cmds.symbolButton(image=image_path+"/cms_ik2fk_R_Leg.png", h=45, vis=True, command=partial (self.ik2fk_ulfbert_character,'.R_leg1_IkFkBlend'))
        self.ulfbert_body_UIs['ulfbert_icon_1'] = cmds.symbolButton(image=image_path+"/cms_R_leg_knee_ik_ctrl.png", h=45, vis=True, command=partial (self.select_ulfbert_character_controller,"R_leg_knee_ik_ctrl"))
        self.ulfbert_body_UIs['ulfbert_icon_2'] = cmds.symbolButton(image=image_path+"/cms_R_leg_off_ctrl.png", h=45, vis=True, command=partial (self.select_ulfbert_character_controller,"R_leg_off_ctrl"))
        self.ulfbert_body_UIs['ulfbert_icon_3'] = cmds.symbolButton(image=image_path+"/cms_R_leg_leg_fk_ctrl.png", h=45, vis=True, command=partial (self.select_ulfbert_character_controller,"R_leg_leg_fk_ctrl"))
        self.ulfbert_body_UIs['ulfbert_icon_4'] = cmds.symbolButton(image=image_path+"/cms_root_ctrl.png", h=45, vis=True, command=partial (self.select_ulfbert_character_controller,"root_ctrl"))
        self.ulfbert_body_UIs['ulfbert_icon_5'] = cmds.symbolButton(image=image_path+"/cms_L_leg_leg_fk_ctrl.png", h=45, vis=True, command=partial (self.select_ulfbert_character_controller,"L_leg_leg_fk_ctrl"))
        self.ulfbert_body_UIs['ulfbert_icon_6'] = cmds.symbolButton(image=image_path+"/cms_L_leg_off_ctrl.png", h=45, vis=True, command=partial (self.select_ulfbert_character_controller,"L_leg_off_ctrl"))
        self.ulfbert_body_UIs['ulfbert_icon_7'] = cmds.symbolButton(image=image_path+"/cms_L_leg_knee_ik_ctrl.png", h=45, vis=True, command=partial (self.select_ulfbert_character_controller,"L_leg_knee_ik_ctrl"))
        self.ulfbert_body_UIs['ulfbert_icon_8'] = cmds.symbolButton(image=image_path+"/cms_ik2fk_L_Leg.png", h=45, vis=True, command=partial (self.ik2fk_ulfbert_character,'.L_leg1_IkFkBlend'))
        self.ulfbert_body_UIs['ulfbert_icon_9'] = cmds.symbolButton( h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_10'] = cmds.symbolButton( h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_11'] = cmds.symbolButton( h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_12'] = cmds.symbolButton( h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_13'] = cmds.symbolButton(image=image_path+"/cms_R_down_leg_off_ctrl.png", h=45, vis=True, command=partial (self.select_ulfbert_character_controller,"R_down_leg_off_ctrl"))
        self.ulfbert_body_UIs['ulfbert_icon_14'] = cmds.symbolButton(image=image_path+"/cms_R_leg_knee_fk_ctrl.png", h=45, vis=True, command=partial (self.select_ulfbert_character_controller,"R_leg_knee_fk_ctrl"))
        self.ulfbert_body_UIs['ulfbert_icon_15'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_16'] = cmds.symbolButton(image=image_path+"/cms_L_leg_knee_fk_ctrl.png", h=45, vis=True, command=partial (self.select_ulfbert_character_controller,"L_leg_knee_fk_ctrl"))
        self.ulfbert_body_UIs['ulfbert_icon_17'] = cmds.symbolButton(image=image_path+"/cms_L_down_leg_off_ctrl.png", h=45, vis=True, command=partial (self.select_ulfbert_character_controller,"L_down_leg_off_ctrl"))
        self.ulfbert_body_UIs['ulfbert_icon_18'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_1'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_2'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_3'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_4'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_5'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_6'] = cmds.symbolButton(image=image_path+"/cms_R_foot_middle_ctrl.png", h=45, vis=True, command=partial (self.select_ulfbert_character_controller,"R_foot_middle_ctrl"))
        self.ulfbert_body_UIs['ulfbert_icon_7'] = cmds.symbolButton(image=image_path+"/cms_R_leg_ankle_fk_ctrl.png", h=45, vis=True, command=self.ulfbert_R_Leg_fkik)
        self.ulfbert_body_UIs['ulfbert_icon_8'] = cmds.symbolButton(image=image_path+"/cms_master_ctrl.png", h=45, vis=True)
        self.ulfbert_body_UIs['ulfbert_icon_9'] = cmds.symbolButton(image=image_path+"/cms_L_leg_ankle_fk_ctrl.png", h=45, vis=True, command=self.ulfbert_L_Leg_fkik)
        self.ulfbert_body_UIs['ulfbert_icon_10'] = cmds.symbolButton(image=image_path+"/cms_L_foot_middle_ctrl.png", h=45, vis=True, command=partial (self.select_ulfbert_character_controller,"L_foot_middle_ctrl"))
        self.ulfbert_body_UIs['ulfbert_icon_11'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_12'] = cmds.symbolButton(h=45, vis=False)
        self.ulfbert_body_UIs['ulfbert_icon_13'] = cmds.symbolButton(image=image_path + "/cms_graph_editor_45",h=45, vis=True, command=self.ulfbert_body_graph_editor)
        cmds.setParent('..')


        cmds.showWindow(self.ulfbert_body_UIs["ulfbert_body_win"])

##################################################################################################################################################
#
#
#ANIM_UI_character_body_function//ulfbert
#
#
##################################################################################################################################################

    def ulfbert_debug(self, *args):
        if cmds.window("Ulfbert_Debug", exists=True):
            cmds.deleteUI("Ulfbert_Debug")
        ulfbert_debug_windows = cmds.window('Ulfbert_Debug',title="Debug Info",mnb=True, mxb=False,w=400,h=130,sizeable=False)
        ulfbert_debug_layout = cmds.columnLayout(w = 250, h=180, columnAttach=('both', 10), rowSpacing=5, columnWidth=250)
        cmds.separator(h=5,vis=True, st='none')
        ulfbert_debug_text = cmds.text(label="Please describe your problem or suggestion.")
        ulfbert_debug_text_field = cmds.textField('ulfbert_debugTextField',h=20,text = "")
        ulfbert_debug_button = cmds.button(label="Send to Admin",bgc=(0.6,0.2,0.3),command=self.ulfbert_sendDebug)
        cmds.separator(h=10, st='none')
        cmds.showWindow()

    def ulfbert_sendDebug(self, *args):
        ulfbert_query_debug_text = cmds.textField('ulfbert_debugTextField', text=True, query=True)
        file = open("Y:/Production/rnd/ahosseini/helga_debug_cms/debug_file.txt", "a")
        file.write("//New Bug:"+ulfbert_query_debug_text+"//\n")
        file.close()
        cmds.warning("successful sending to Arash")
        if cmds.window("Ulfbert_Debug", exists=True):
            cmds.deleteUI("Ulfbert_Debug")

    def ulfbert_about(self, *args):
        if cmds.window("ulfbert_about", exists=True):
            cmds.deleteUI("ulfbert_about")
        ulfbert_about_windows = cmds.window("ulfbert_about",title="About",mnb=True, mxb=False,w=400,h=130,sizeable=False)
        ulfbert_about_form_layout = cmds.formLayout('ulfbert_about_dialog_UI')
        ulfbert_about_colum_layout = cmds.columnLayout(columnAttach=('both', 10), rowSpacing=5, columnWidth=400)
        cmds.separator(h=50,vis=True, st='none')
        ulfbert_about_text = cmds.text('ulfbert_about_text_a',label=about, align = 'center')
        cmds.showWindow()

    def ulfbert_namespace(self, *args):
        ulfbert_namespace_list = pm.system.listNamespaces()
        ulfbert_namespace_menuItem=cmds.optionMenu('ulfbert_namespace_optionmenu_a', q=True, itemListLong=True)
        if ulfbert_namespace_menuItem:
            cmds.deleteUI(ulfbert_namespace_menuItem)
        for self.namespace_name in ulfbert_namespace_list:
            cmds.menuItem(label=self.namespace_name, parent=self.ulfbert_body_UIs['ulfbert_namespace_optionmenu_a'])
        if len(ulfbert_namespace_list)==0:
            self.ulfbert_change_namespace_text_color_red()
        else:
            self.ulfbert_change_namespace_text_color_green()

    def ulfbert_change_namespace_text_color_green(self, *args):
        self.query_ulfbert_selected_namespace=cmds.optionMenu('ulfbert_namespace_optionmenu_a', q=True, v=True)
        cmds.text('ulfbert_namespace_select_a', e=True, label=self.query_ulfbert_selected_namespace)
        cmds.text('ulfbert_namespace_select_a', e=True, bgc=Color.green_a)

        if cmds.window('ulfbert_hand_body_window', exists = True):
            cmds.text('ulfbert_namespace_hand_select_a', e=True, label=self.query_ulfbert_selected_namespace)
            cmds.text('ulfbert_namespace_hand_select_a', e=True, bgc=Color.green_a)

        if cmds.window('character_save_pose_window', exists=True):
            cmds.text('character_namespace_message_a', e=True, label=self.query_ulfbert_selected_namespace)
            cmds.text('character_namespace_message_a', e=True, bgc=Color.green_a)
            self.set_name_save_pose()

        if cmds.window('character_load_pose_window', exists=True):
            cmds.text('character_save_pose_a_x', e=True, label=self.query_ulfbert_selected_namespace)
            cmds.text('character_save_pose_a_x', e=True, bgc=Color.green_a)

    def ulfbert_change_namespace_text_color_red(self, *args):
        cmds.text('ulfbert_namespace_select_a', e=True, label="No Namespaces in Scene!")
        cmds.text('ulfbert_namespace_select_a',e=True, bgc=Color.red)

        if cmds.window('ulfbert_hand_body_window', exists = True):
            cmds.text('ulfbert_namespace_hand_select_a', e=True, label="No Namespaces in Scene!")
            cmds.text('ulfbert_namespace_hand_select_a', e=True, bgc=Color.red)

        if cmds.window('character_save_pose_window', exists=True):
            cmds.text('character_namespace_message_a', e=True, label="No Namespaces in Scene!")
            cmds.text('character_namespace_message_a', e=True, bgc=Color.red)

        if cmds.window('character_load_pose_window', exists=True):
            cmds.text('character_save_pose_a_x', e=True, label="No Namespaces in Scene!")
            cmds.text('character_save_pose_a_x', e=True, bgc=Color.red)

    def ulfbert_create_reference(self, *args):
        mel.eval('CreateReference')

    def ulfbert_reference_editor(self, *args):
        mel.eval('ReferenceEditor')

    def ulfbert_L_arm_fkik(self, *args):
        ulfbert_L_arm_fkik_namespace_list = pm.system.listNamespaces()
        if len(ulfbert_L_arm_fkik_namespace_list)==0:
            cmds.warning('No Character in Scene')
        else:
            query_ulfbert_L_arm_fkik_controller=cmds.optionMenu('ulfbert_namespace_optionmenu_a', q=True, v=True)
            ulfbert_L_arm_fkik_current_name=(str(query_ulfbert_L_arm_fkik_controller)+":"+("master_ctrl"))
            query_ulfbert_L_arm_fkik_value=cmds.getAttr(ulfbert_L_arm_fkik_current_name+'.L_arm3_IkFkBlend')
            if query_ulfbert_L_arm_fkik_value==0.0:
                cmds.select(str(query_ulfbert_L_arm_fkik_controller)+":"+str("L_arm_wrist_ik_ctrl"))
            else:
                cmds.select(str(query_ulfbert_L_arm_fkik_controller)+":"+str("L_arm_wrist_fk_ctrl"))

    def ulfbert_R_arm_fkik(self, *args):
        ulfbert_R_arm_fkik_namespace_list = pm.system.listNamespaces()
        if len(ulfbert_R_arm_fkik_namespace_list)==0:
            cmds.warning('No Character in Scene')
        else:
            query_ulfbert_R_arm_fkik_controller=cmds.optionMenu('ulfbert_namespace_optionmenu_a', q=True, v=True)
            ulfbert_R_arm_fkik_current_name=(str(query_ulfbert_R_arm_fkik_controller)+":"+("master_ctrl"))
            query_ulfbert_R_arm_fkik_value=cmds.getAttr(ulfbert_R_arm_fkik_current_name+'.R_arm3_IkFkBlend')
            if query_ulfbert_R_arm_fkik_value==0.0:
                cmds.select(str(query_ulfbert_R_arm_fkik_controller)+":"+str("R_arm_wrist_ik_ctrl"))
            else:
                cmds.select(str(query_ulfbert_R_arm_fkik_controller)+":"+str("R_arm_wrist_fk_ctrl"))


    def ulfbert_L_Leg_fkik(self, *args):
        ulfbert_L_leg_fkik_namespace_list = pm.system.listNamespaces()
        if len(ulfbert_L_leg_fkik_namespace_list)==0:
            cmds.warning('No Character in Scene')
        else:
            query_ulfbert_L_leg_fkik_controller=cmds.optionMenu('ulfbert_namespace_optionmenu_a', q=True, v=True)
            ulfbert_L_leg_fkik_current_name=(str(query_ulfbert_L_leg_fkik_controller)+":"+("master_ctrl"))
            query_ulfbert_L_leg_fkik_value=cmds.getAttr(ulfbert_L_leg_fkik_current_name+'.L_leg1_IkFkBlend')
            if query_ulfbert_L_leg_fkik_value==0.0:
                cmds.select(str(query_ulfbert_L_leg_fkik_controller)+":"+str("L_leg_ankle_ik_ctrl"))
            else:
                cmds.select(str(query_ulfbert_L_leg_fkik_controller)+":"+str("L_leg_ankle_fk_ctrl"))

    def ulfbert_R_Leg_fkik(self, *args):
        ulfbert_R_leg_fkik_namespace_list = pm.system.listNamespaces()
        if len(ulfbert_R_leg_fkik_namespace_list)==0:
            cmds.warning('No Character in Scene')
        else:
            query_ulfbert_R_leg_fkik_controller=cmds.optionMenu('ulfbert_namespace_optionmenu_a', q=True, v=True)
            ulfbert_R_leg_fkik_current_name=(str(query_ulfbert_R_leg_fkik_controller)+":"+("master_ctrl"))
            query_ulfbert_R_leg_fkik_value=cmds.getAttr(ulfbert_R_leg_fkik_current_name+'.R_leg1_IkFkBlend')
            if query_ulfbert_R_leg_fkik_value==0.0:
                cmds.select(str(query_ulfbert_R_leg_fkik_controller)+":"+str("R_leg_ankle_ik_ctrl"))
            else:
                cmds.select(str(query_ulfbert_R_leg_fkik_controller)+":"+str("R_leg_ankle_fk_ctrl"))

    def delete_ulfbert_character_body_UI(self, *args):
        self.quit_UI_window('ulfbert_body_window')

    def call_save_pose(self, *args):
        Save_character_pose_UI()

    def call_load_pose(self, *args):
        Load_character_pose_UI()

    def ulfbert_select_spine(self, *args):
        ulfbert_select_spine_namespace_list = pm.system.listNamespaces()
        if len(ulfbert_select_spine_namespace_list)==0:
            cmds.warning('No Character in Scene')
        else:
            query_ulfbert_select_spien_namespace=cmds.optionMenu('ulfbert_namespace_optionmenu_a', q=True, v=True)
            ulfbert_spine_controller=["spine_hipsB_ctrl", "spine_chestB_ctrl"]
            for s in ulfbert_spine_controller:
                cmds.select(str(query_ulfbert_select_spien_namespace)+":"+str(s), add=True)


##################################################
#
#
#ANIM_UI_ulfbert_reset
#
#
##################################################



    def ulfbert_reset_pose(self, *args):
        '''ulfbert_reset_ui'''
        if cmds.window("ulfbert_reset", exists=True):
            cmds.deleteUI("ulfbert_reset")
        cmds.window("ulfbert_reset",title="Reset",mnb=True, mxb=False,w=135,h=50,sizeable=False)
        cmds.columnLayout('ulfbert_reset_column_a', columnAttach=('both', 0), rowSpacing=3, columnWidth=135)
        cmds.rowColumnLayout('ulfbert_reset_layout',columnAttach=(20,'both',20), numberOfColumns=3, columnWidth=[(1,45), (2,45),(3,45)])
        cmds.symbolButton(image=image_path+ "/cms_reset_t_main.png",h=45,vis=True,parent='ulfbert_reset_layout', command=self.ulfbert_reset_translate)
        cmds.symbolButton(image=image_path+ "/cms_reset_r_main.png",h=45,vis=True,parent='ulfbert_reset_layout', command=self.ulfbert_reset_rotate)
        cmds.symbolButton(image=image_path+ "/cms_reset_s_main.png",h=45,vis=True,parent='ulfbert_reset_layout', command=self.ulfbert_reset_scale)

        cmds.setParent('..')
        cmds.showWindow()

    def ulfbert_reset_translate(self, *args):
        ulfbert_reset_t_object=cmds.ls(sl=True)
        cmds.xform(a=True, t=(0,0,0))

    def ulfbert_reset_rotate(self, *args):
        ulfbert_reset_ro_object=cmds.ls(sl=True)
        cmds.xform(a=True, ro=(0,0,0))

    def ulfbert_reset_scale(self, *args):
        ulfbert_reset_s_object=cmds.ls(sl=True)
        cmds.xform(a=True, s=(1,1,1))


    def ulfbert_body_graph_editor(self, *args):
        mel.eval('GraphEditor')


    def ulfbert_reset_body_controller(self, *args):
        ulfbert_reset_object=cmds.ls(sl=True)
        cmds.xform(a=True, t=(0,0,0))
        cmds.xform(a=True, ro=(0,0,0))
        cmds.xform(a=True, s=(1,1,1))

##################################################
#
#
#ANIM_UI_ulfbert_mirror
#
#
##################################################



    def ulfbert_mirror_pose(self, *args):
        '''ulfbert_mirror_ui'''
        if cmds.window("ulfbert_mirror", exists=True):
            cmds.deleteUI("ulfbert_mirror")
        cmds.window("ulfbert_mirror",title="Mirror Pose",mnb=True, mxb=False,w=300,h=300,sizeable=False)
        cmds.columnLayout('ulfbert_mirror_column_a', columnAttach=('both', 20), rowSpacing=3, columnWidth=300)
        cmds.rowColumnLayout('ulfbert_mirror_layout',columnAttach=(20,'both',20), numberOfColumns=2, columnWidth=[(1,150), (2,100)])
        #cmds.separator(h=5,vis=True, st='none')
        cmds.radioCollection()
        cmds.radioButton('ulfbert_mirror_R2L', h=50, label='Right2Left',align='center', parent='ulfbert_mirror_layout')
        cmds.radioButton( 'ulfbert_mirror_L2R', h=50, label='Left2Right', align='center' ,parent='ulfbert_mirror_layout')
        cmds.symbolButton(vis=False,parent='ulfbert_mirror_layout')
        cmds.button(label="Mirror",parent='ulfbert_mirror_layout', w=30, command=self.ulfbert_mirror_ui_action)
        cmds.setParent('..')
        cmds.showWindow()


    def ulfbert_mirror_ui_action(self, *args):
        '''ulfbert_mirror_ui_function'''
        ulfbert_query_R2L=cmds.radioButton( 'ulfbert_mirror_R2L',sl=True, q=True)
        ulfbert_query_L2R=cmds.radioButton( 'ulfbert_mirror_L2R',sl=True, q=True)

        if ulfbert_query_L2R==True:
            self.ulfbert_mirror_L2R_action()
        else:
            pass
        if ulfbert_query_R2L==True:
            self.ulfbert_mirror_R2L_action()

    def ulfbert_mirror_L2R_action(self, *args):
        ulfbert_L2R_list = cmds.ls(sl=True)
        ulfbert_mirror_L2R_namespace = pm.system.listNamespaces()
        if len(ulfbert_mirror_L2R_namespace)==0:
            cmds.warning('No Character in Scene')
        else:
            query_ulfbert_L_mirror_L2R=cmds.optionMenu('ulfbert_namespace_optionmenu_a', q=True, v=True)
            #print query_ulfbert_L_mirror_L2R
            if len(ulfbert_L2R_list) == 1:
                self.ulfbert_L2R_object=pm.ls(sl = True, fl = True)[0]
                #print self.ulfbert_L2R_object
                split_l_namespace=self.ulfbert_L2R_object.split(":")[1]
                final_side_result=split_l_namespace.replace("L", "R")
                self.final_side_name_result=query_ulfbert_L_mirror_L2R+":"+final_side_result
                #print final_side_name_result

                self.ulfbert_get_trans_data(self.ulfbert_L2R_object)
                self.ulfbert_get_rotate_data(self.ulfbert_L2R_object)
                self.ulfbert_get_scale_data(self.ulfbert_L2R_object)

                self.ulfbert_L2R_translate()
                self.ulfbert_L2R_rotate()
                self.ulfbert_L2R_scale()

            else:
                cmds.warning('Select Control!')

    def ulfbert_L2R_translate(self, *args):
            if self.ulfbert_L2R_object.translateX.isLocked() == False:
                self.ulfbert_set_transX_data(self.final_side_name_result)
            if self.ulfbert_L2R_object.translateY.isLocked() == False:
                self.ulfbert_set_transY_data(self.final_side_name_result)
            if self.ulfbert_L2R_object.translateZ.isLocked() == False:
                self.ulfbert_set_transZ_data(self.final_side_name_result)
                pass
    def ulfbert_L2R_rotate(self, *args):
            if self.ulfbert_L2R_object.rotateX.isLocked() == False:
                self.ulfbert_set_rotateX_data(self.final_side_name_result)
            if self.ulfbert_L2R_object.rotateY.isLocked() == False:
                self.ulfbert_set_rotateY_data(self.final_side_name_result)
            if self.ulfbert_L2R_object.rotateZ.isLocked() == False:
                self.ulfbert_set_rotateZ_data(self.final_side_name_result)
                pass
    def ulfbert_L2R_scale(self, *args):
            if self.ulfbert_L2R_object.scaleX.isLocked() == False:
                self.ulfbert_set_scaleX_data(self.final_side_name_result)
            if self.ulfbert_L2R_object.scaleY.isLocked() == False:
                self.ulfbert_set_scaleY_data(self.final_side_name_result)
            if self.ulfbert_L2R_object.scaleZ.isLocked() == False:
                self.ulfbert_set_scaleZ_data(self.final_side_name_result)

    def ulfbert_mirror_R2L_action(self, *args):
        ulfbert_R2L_list = cmds.ls(sl=True)
        ulfbert_mirror_R2L_namespace = pm.system.listNamespaces()
        if len(ulfbert_mirror_R2L_namespace)==0:
            cmds.warning('No Character in Scene')
        else:
            query_ulfbert_L_mirror_R2L=cmds.optionMenu('ulfbert_namespace_optionmenu_a', q=True, v=True)
            if len(ulfbert_R2L_list) == 1:
                self.ulfbert_R2L_object=pm.ls(sl = True, fl = True)[0]

                split_r_namespace=self.ulfbert_R2L_object.split(":")[1]
                final_r_side_result=split_r_namespace.replace("R","L")
                self.final_r_side_name_result=query_ulfbert_L_mirror_R2L+":"+final_r_side_result

                self.ulfbert_get_trans_data(self.ulfbert_R2L_object)
                self.ulfbert_get_rotate_data(self.ulfbert_R2L_object)
                self.ulfbert_get_scale_data(self.ulfbert_R2L_object)

                self.ulfbert_R2L_translate()
                self.ulfbert_R2L_rotate()
                self.ulfbert_R2L_scale()

            else:
                cmds.warning('Select Control!')

    def ulfbert_R2L_translate(self, *args):
            if self.ulfbert_R2L_object.translateX.isLocked() == False:
                self.ulfbert_set_transX_data(self.final_r_side_name_result)
            if self.ulfbert_R2L_object.translateY.isLocked() == False:
                self.ulfbert_set_transY_data(self.final_r_side_name_result)
            if self.ulfbert_R2L_object.translateZ.isLocked() == False:
                self.ulfbert_set_transZ_data(self.final_r_side_name_result)
                pass
    def ulfbert_R2L_rotate(self, *args):
            if self.ulfbert_R2L_object.rotateX.isLocked() == False:
                self.ulfbert_set_rotateX_data(self.final_r_side_name_result)
            if self.ulfbert_R2L_object.rotateY.isLocked() == False:
                self.ulfbert_set_rotateY_data(self.final_r_side_name_result)
            if self.ulfbert_R2L_object.rotateZ.isLocked() == False:
                self.ulfbert_set_rotateZ_data(self.final_r_side_name_result)
                pass
    def ulfbert_R2L_scale(self, *args):
            if self.ulfbert_R2L_object.scaleX.isLocked() == False:
                self.ulfbert_set_scaleX_data(self.final_r_side_name_result)
            if self.ulfbert_R2L_object.scaleY.isLocked() == False:
                self.ulfbert_set_scaleY_data(self.final_r_side_name_result)
            if self.ulfbert_R2L_object.scaleZ.isLocked() == False:
                self.ulfbert_set_scaleZ_data(self.final_r_side_name_result)

    def ulfbert_get_trans_data(self, name):
        self.ulfbert_val_trans_x = cmds.getAttr(name+'.translateX')
        self.ulfbert_val_trans_y = cmds.getAttr(name+'.translateY')
        self.ulfbert_val_trans_z = cmds.getAttr(name+'.translateZ')

    def ulfbert_get_rotate_data(self, name):
        self.ulfbert_val_rotate_x = cmds.getAttr(name+'.rotateX')
        self.ulfbert_val_rotate_y = cmds.getAttr(name+'.rotateY')
        self.ulfbert_val_rotate_z = cmds.getAttr(name+'.rotateZ')

    def ulfbert_get_scale_data(self, name):
        self.ulfbert_val_scale_x = cmds.getAttr(name+'.scaleX')
        self.ulfbert_val_scale_y = cmds.getAttr(name+'.scaleY')
        self.ulfbert_val_scale_z = cmds.getAttr(name+'.scaleZ')

    def ulfbert_set_transX_data(self, name):
        cmds.setAttr(name+'.translateX', self.ulfbert_val_trans_x)

    def ulfbert_set_transY_data(self, name):
        cmds.setAttr(name+'.translateY', self.ulfbert_val_trans_y)

    def ulfbert_set_transZ_data(self, name):
        cmds.setAttr(name+'.translateZ', self.ulfbert_val_trans_z)

    def ulfbert_set_rotateX_data(self, name):
        cmds.setAttr(name+'.rotateX', self.ulfbert_val_rotate_x)

    def ulfbert_set_rotateY_data(self, name):
        cmds.setAttr(name+'.rotateY', self.ulfbert_val_rotate_y)

    def ulfbert_set_rotateZ_data(self, name):
        cmds.setAttr(name+'.rotateZ', self.ulfbert_val_rotate_z)

    def ulfbert_set_scaleX_data(self, name):
        cmds.setAttr(name+'.scaleX', self.ulfbert_val_scale_x)

    def ulfbert_set_scaleY_data(self, name):
        cmds.setAttr(name+'.scaleY', self.ulfbert_val_scale_y)

    def ulfbert_set_scaleZ_data(self, name):
        cmds.setAttr(name+'.scaleZ', self.ulfbert_val_scale_z)

########################################################################################################################










#########################################################################################################################
#
#
#ANIM_UI_character_hand_UI
#
#
#########################################################################################################################
class Ulfbert_hand_UI(Base):
    def __init__(self, ulfbert_hand_parent_width = 455, ulfbert_hand_parent_height =270, ulfbert_hand_child_width = 450, ulfbert_hand_child_height = 240):

        super(Ulfbert_hand_UI, self).__init__()

        self.ulfbert_hand_body_UIs = {}
        #self.delete_window('helga_anim_choice_window')
        self.ulfbert_hand_parent_width = ulfbert_hand_parent_width
        self.ulfbert_hand_parent_height = ulfbert_hand_parent_height
        self.ulfbert_hand_child_width = ulfbert_hand_child_width
        self.ulfbert_hand_child_height = ulfbert_hand_child_height
        self.ulfbert_hand_body_UIs["ulfbert_hand_body_win"] = cmds.window('ulfbert_hand_body_window', title = 'Ulfbert Hand UI',
                                                widthHeight = (self.ulfbert_hand_parent_width,self.ulfbert_hand_parent_height),
                                                menuBar = True, sizeable = False, topEdge= 0, leftEdge= 0, minimizeButton=True, maximizeButton=False)

        self.ulfbert_hand_body_main_UI()

    def ulfbert_hand_body_main_UI(self, *args):
        self.ulfbert_hand_body_UIs['ulfbert_hand_column_a_x'] = cmds.columnLayout('ulfbert_hand_column_a_x', columnAttach=('both', 100), rowSpacing=3,h=20, columnWidth=self.ulfbert_hand_child_width, parent =self.ulfbert_hand_body_UIs["ulfbert_hand_body_win"])
        self.ulfbert_hand_body_UIs['ulfbert_namespace_hand_select_a']=cmds.text('ulfbert_namespace_hand_select_a', label="No Namespace selected!", h=20, bgc=Color.red)


        self.ulfbert_hand_body_UIs['ulfbert_hand_column_a'] = cmds.columnLayout('ulfbert_hand_column_a', columnAttach=('both', 0), rowSpacing=3, columnWidth=self.ulfbert_hand_child_width, parent =self.ulfbert_hand_body_UIs["ulfbert_hand_body_win"] )
        ########to go'''
        self.ulfbert_hand_body_UIs['ulfbert_hand_rowColumn_a'] = cmds.rowColumnLayout('ulfbert_hand_rowColumn_a', w= self.ulfbert_hand_child_width, h=self.ulfbert_hand_child_height, numberOfColumns=15,
                                                            columnWidth=[(1,30), (2,30), (3,30),(4,30), (5,30),(6,30), (7,30), (8,30),(9,30), (10,30),(11,30),(12,30),(13,30),(14,30),(15,30)], parent= self.ulfbert_hand_body_UIs['ulfbert_hand_column_a'] )

        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_1'] = cmds.symbolButton(h=30, vis=False)
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_2'] = cmds.symbolButton(h=30, vis=False)
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(h=30, vis=False)
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_1'] = cmds.symbolButton(h=30, vis=False)
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_2'] = cmds.symbolButton(h=30, vis=False)
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(h=30, vis=False)
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_1'] = cmds.symbolButton(h=30, vis=False)
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_2'] = cmds.symbolButton(h=30, vis=False)
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(h=30, vis=False)
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_1'] = cmds.symbolButton(h=30, vis=False)
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_2'] = cmds.symbolButton(h=30, vis=False)
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(h=30, vis=False)
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_1'] = cmds.symbolButton(h=30, vis=False)
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_2'] = cmds.symbolButton(h=30, vis=False)
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(h=30, vis=False)
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_1'] = cmds.symbolButton(h=30, vis=False)
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(h=30, vis=False)
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_1'] = cmds.symbolButton(image=image_path+"/cms_R_thumb_all.png",h=30, vis=True, command=self.ulfbert_select_R_thumb)
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_2'] = cmds.symbolButton(h=30, vis=False)
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_2'] = cmds.symbolButton(image=image_path+"/cms_R_fingers_all.png",h=30, vis=True, command=self.ulfbert_select_all_R_fingers)
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(h=30, vis=False)
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_1'] = cmds.symbolButton(h=30, vis=False)
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_2'] = cmds.symbolButton(h=30, vis=False)
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(h=30, vis=False)
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_1'] = cmds.symbolButton(h=30, vis=False)
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_1'] = cmds.symbolButton(image=image_path+"/cms_L_fingers_all.png",h=30, vis=True, command=self.ulfbert_select_all_L_fingers)
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_2'] = cmds.symbolButton(h=30, vis=False)
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(image=image_path+"/cms_L_thumb_all.png",h=30, vis=True, command=self.ulfbert_select_L_thumb)
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(h=30, vis=False)
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_2'] = cmds.symbolButton(h=30, vis=False)

        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_2'] = cmds.symbolButton(h=30, vis=False)
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(h=30, vis=False)

        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_2'] = cmds.symbolButton(image=image_path+"/cms_R_thumb_0_ctrl.png",h=30, vis=True, command=partial (self.select_ulfbert_hand_controller,"R_thumb_0_ctrl"))

        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(image=image_path+"/cms_R_index_all.png",h=30, vis=True, command=self.ulfbert_select_R_index)
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_1'] = cmds.symbolButton(image=image_path+"/cms_R_middle_all.png",h=30, vis=True, command=self.ulfbert_select_R_middle)
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_2'] = cmds.symbolButton(image=image_path+"/cms_R_ring_all.png",h=30, vis=True, command=self.ulfbert_select_R_ring)
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(image=image_path+"/cms_R_pink_all.png",h=30, vis=True, command=self.ulfbert_select_R_pink)

        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_1'] = cmds.symbolButton(h=30, vis=False)

        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_2'] = cmds.symbolButton(image=image_path+"/cms_L_pink_all.png",h=30, vis=True, command=self.ulfbert_select_L_pink)
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(image=image_path+"/cms_L_ring_all.png",h=30, vis=True, command=self.ulfbert_select_L_ring)
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_1'] = cmds.symbolButton(image=image_path+"/cms_L_middle_all.png",h=30, vis=True, command=self.ulfbert_select_L_middle)
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_2'] = cmds.symbolButton(image=image_path+"/cms_L_index_all.png",h=30, vis=True, command=self.ulfbert_select_L_index)

        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(image=image_path+"/cms_L_thumb_0_ctrl.png",h=30, vis=True, command=partial (self.select_ulfbert_hand_controller,"L_thumb_0_ctrl"))

        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_2'] = cmds.symbolButton(h=30, vis=False)
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(h=30, vis=False)
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(h=30, vis=False)

        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(image=image_path+ "/cms_R_thumb_1_ctrl",h=30, vis=True, command=partial (self.select_ulfbert_hand_controller,"R_thumb_1_ctrl"))

        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(h=30, vis=False)

        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(image=image_path+ "/cms_R_index_0_ctrl",h=30, vis=True, command=partial (self.select_ulfbert_hand_controller,"R_index_0_ctrl"))
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(image=image_path+ "/cms_R_middle_0_ctrl",h=30, vis=True, command=partial (self.select_ulfbert_hand_controller,"R_middle_0_ctrl"))
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(image=image_path+ "/cms_R_ring_0_ctrl",h=30, vis=True, command=partial (self.select_ulfbert_hand_controller,"R_ring_0_ctrl"))
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(image=image_path+ "/cms_R_pink_0_ctrl",h=30, vis=True, command=partial (self.select_ulfbert_hand_controller,"R_pink_0_ctrl"))

        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(h=30, vis=False)

        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(image=image_path+ "/cms_L_pink_0_ctrl",h=30, vis=True, command=partial (self.select_ulfbert_hand_controller,"L_pink_0_ctrl"))
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(image=image_path+ "/cms_L_ring_0_ctrl",h=30, vis=True, command=partial (self.select_ulfbert_hand_controller,"L_ring_0_ctrl"))
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(image=image_path+ "/cms_L_middle_0_ctrl",h=30, vis=True, command=partial (self.select_ulfbert_hand_controller,"L_middle_0_ctrl"))
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(image=image_path+ "/cms_L_index_0_ctrl",h=30, vis=True, command=partial (self.select_ulfbert_hand_controller,"L_index_0_ctrl"))

        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(h=30, vis=False)

        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(image=image_path+"/cms_L_thumb_1_ctrl.png",h=30, vis=True, command=partial (self.select_ulfbert_hand_controller,"L_thumb_1_ctrl"))

        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(h=30, vis=False)

        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(image=image_path+"/cms_R_thumb_2_ctrl",h=30, vis=True, command=partial (self.select_ulfbert_hand_controller,"R_thumb_2_ctrl"))

        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(h=30, vis=False)
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(h=30, vis=False)

        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(image=image_path+"/cms_R_index_1_ctrl",h=30, vis=True, command=partial (self.select_ulfbert_hand_controller,"R_index_1_ctrl"))
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(image=image_path+"/cms_R_middle_1_ctrl",h=30, vis=True, command=partial (self.select_ulfbert_hand_controller,"R_middle_1_ctrl"))
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(image=image_path+"/cms_R_ring_1_ctrl",h=30, vis=True, command=partial (self.select_ulfbert_hand_controller,"R_ring_1_ctrl"))
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(image=image_path+"/cms_R_pink_1_ctrl",h=30, vis=True, command=partial (self.select_ulfbert_hand_controller,"R_pink_1_ctrl"))

        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(h=30, vis=False)

        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(image=image_path+"/cms_L_pink_1_ctrl",h=30, vis=True, command=partial (self.select_ulfbert_hand_controller,"L_pink_1_ctrl"))
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(image=image_path+"/cms_L_ring_1_ctrl",h=30, vis=True, command=partial (self.select_ulfbert_hand_controller,"L_ring_1_ctrl"))
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(image=image_path+"/cms_L_middle_1_ctrl",h=30, vis=True, command=partial (self.select_ulfbert_hand_controller,"L_middle_1_ctrl"))
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(image=image_path+"/cms_L_index_1_ctrl",h=30, vis=True, command=partial (self.select_ulfbert_hand_controller,"L_index_1_ctrl"))

        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(h=30, vis=False)
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(h=30, vis=False)

        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(image=image_path+"/cms_L_thumb_2_ctrl.png",h=30, vis=True, command=partial (self.select_ulfbert_hand_controller,"L_thumb_2_ctrl"))

        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(h=30, vis=False)
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_1'] = cmds.symbolButton(h=30, vis=False)
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_2'] = cmds.symbolButton(h=30, vis=False)

        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(image=image_path+"/cms_R_index_2_ctrl", h=30, vis=True, command=partial (self.select_ulfbert_hand_controller,"R_index_2_ctrl"))
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(image=image_path+"/cms_R_middle_2_ctrl",h=30, vis=True, command=partial (self.select_ulfbert_hand_controller,"R_middle_2_ctrl"))
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(image=image_path+"/cms_R_ring_2_ctrl",h=30, vis=True, command=partial (self.select_ulfbert_hand_controller,"R_ring_2_ctrl"))
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(image=image_path+"/cms_R_pink_2_ctrl",h=30, vis=True, command=partial (self.select_ulfbert_hand_controller,"R_pink_2_ctrl"))

        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(h=30, vis=False)

        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(image=image_path+"/cms_L_pink_2_ctrl",h=30, vis=True, command=partial (self.select_ulfbert_hand_controller,"L_pink_2_ctrl"))
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(image=image_path+"/cms_L_ring_2_ctrl",h=30, vis=True, command=partial (self.select_ulfbert_hand_controller,"L_ring_2_ctrl"))
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(image=image_path+"/cms_L_middle_2_ctrl",h=30, vis=True, command=partial (self.select_ulfbert_hand_controller,"L_middle_2_ctrl"))
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(image=image_path+"/cms_L_index_2_ctrl",h=30, vis=True, command=partial (self.select_ulfbert_hand_controller,"L_index_2_ctrl"))

        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(h=30, vis=False)
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_1'] = cmds.symbolButton(h=30, vis=False)
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_2'] = cmds.symbolButton(h=30, vis=False)
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(h=30, vis=False)
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_1'] = cmds.symbolButton(h=30, vis=False)
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_2'] = cmds.symbolButton(h=30, vis=False)

        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(image=image_path+"/cms_R_index_3_ctrl", h=30, vis=True, command=partial (self.select_ulfbert_hand_controller,"R_index_3_ctrl"))
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(image=image_path+"/cms_R_middle_3_ctrl",h=30, vis=True, command=partial (self.select_ulfbert_hand_controller,"R_middle_3_ctrl"))
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(image=image_path+"/cms_R_ring_3_ctrl",h=30, vis=True, command=partial (self.select_ulfbert_hand_controller,"R_ring_3_ctrl"))
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(image=image_path+"/cms_R_pink_3_ctrl",h=30, vis=True, command=partial (self.select_ulfbert_hand_controller,"R_pink_3_ctrl"))

        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(h=30, vis=False)

        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(image=image_path+"/cms_L_pink_3_ctrl",h=30, vis=True, command=partial (self.select_ulfbert_hand_controller,"L_pink_3_ctrl"))
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(image=image_path+"/cms_L_ring_3_ctrl",h=30, vis=True, command=partial (self.select_ulfbert_hand_controller,"L_ring_3_ctrl"))
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(image=image_path+"/cms_L_middle_3_ctrl",h=30, vis=True, command=partial (self.select_ulfbert_hand_controller,"L_middle_3_ctrl"))
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(image=image_path+"/cms_L_index_3_ctrl",h=30, vis=True, command=partial (self.select_ulfbert_hand_controller,"L_index_3_ctrl"))

        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(h=30, vis=False)
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_1'] = cmds.symbolButton(h=30, vis=False)
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_2'] = cmds.symbolButton(h=30, vis=False)
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(h=30, vis=False)
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_1'] = cmds.symbolButton(h=30, vis=False)
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_2'] = cmds.symbolButton(h=30, vis=False)
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(h=30, vis=False)
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_1'] = cmds.symbolButton(h=30, vis=False)
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_2'] = cmds.symbolButton(h=30, vis=False)
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(h=30, vis=False)
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_1'] = cmds.symbolButton(h=30, vis=False)
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_2'] = cmds.symbolButton(h=30, vis=False)
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(h=30, vis=False)
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_1'] = cmds.symbolButton(h=30, vis=False)
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_2'] = cmds.symbolButton(h=30, vis=False)
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_3'] = cmds.symbolButton(h=30, vis=False)
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_1'] = cmds.symbolButton(h=30, vis=False)
        self.ulfbert_hand_body_UIs['ulfbert_hand_icon_2'] = cmds.symbolButton(image=image_path+"/cms_graph_editor_30",h=30, vis=True, command=self.ulfbert_hand_graph_editor)
        cmds.setParent('..')


        cmds.showWindow(self.ulfbert_hand_body_UIs["ulfbert_hand_body_win"])



    def ulfbert_hand_graph_editor(self, *args):
        mel.eval('GraphEditor')


    def ulfbert_select_all_R_fingers(self, *args):
        ulfbert_hand_all_R_fingers_namespace_list = pm.system.listNamespaces()
        if len(ulfbert_hand_all_R_fingers_namespace_list)==0:
            cmds.warning('No Character in Scene')
        else:
            #cmds.select(clear=True)
            query_ulfbert_hand_R_fingers_controller=cmds.optionMenu('ulfbert_namespace_optionmenu_a', q=True, v=True)
            ulfbert_all_R_fingers=["R_index_1_ctrl", "R_index_2_ctrl", "R_index_3_ctrl", "R_middle_1_ctrl", "R_middle_2_ctrl", "R_middle_3_ctrl", "R_ring_1_ctrl",
                                    "R_ring_2_ctrl", "R_ring_3_ctrl", "R_pink_1_ctrl", "R_pink_2_ctrl", "R_pink_3_ctrl", "R_thumb_2_ctrl", "R_thumb_1_ctrl"]
            for f in ulfbert_all_R_fingers:
                cmds.select(str(query_ulfbert_hand_R_fingers_controller)+":"+str(f), add=True)

    def ulfbert_select_all_L_fingers(self, *args):
        ulfbert_hand_all_L_fingers_namespace_list = pm.system.listNamespaces()
        if len(ulfbert_hand_all_L_fingers_namespace_list)==0:
            cmds.warning('No Character in Scene')
        else:
            #cmds.select(clear=True)
            query_ulfbert_hand_L_fingers_controller=cmds.optionMenu('ulfbert_namespace_optionmenu_a', q=True, v=True)
            ulfbert_all_L_fingers=["L_index_1_ctrl", "L_index_2_ctrl", "L_index_3_ctrl", "L_middle_1_ctrl", "L_middle_2_ctrl", "L_middle_3_ctrl", "L_ring_1_ctrl",
                                    "L_ring_2_ctrl", "L_ring_3_ctrl", "L_pink_1_ctrl", "L_pink_2_ctrl", "L_pink_3_ctrl", "L_thumb_2_ctrl", "L_thumb_1_ctrl"]
            for f in ulfbert_all_L_fingers:
                cmds.select(str(query_ulfbert_hand_L_fingers_controller)+":"+str(f), add=True)


    def ulfbert_select_R_thumb(self, *args):
        ulfbert_all_r_thumb=["R_thumb_1_ctrl", "R_thumb_2_ctrl"]
        query_ulfbert_R_thumb_namespace=cmds.optionMenu('ulfbert_namespace_optionmenu_a', q=True, v=True)
        for f in ulfbert_all_r_thumb:
            cmds.select(str(query_ulfbert_R_thumb_namespace)+":"+str(f), add=True)


    def ulfbert_select_R_index(self, *args):
        ulfbert_all_r_index=["R_index_1_ctrl", "R_index_2_ctrl", "R_index_3_ctrl"]
        query_ulfbert_R_index_namespace=cmds.optionMenu('ulfbert_namespace_optionmenu_a', q=True, v=True)
        for f in ulfbert_all_r_index:
            cmds.select(str(query_ulfbert_R_index_namespace)+":"+str(f), add=True)

    def ulfbert_select_R_middle(self, *args):
        ulfbert_all_r_middle=["R_middle_1_ctrl", "R_middle_2_ctrl", "R_middle_3_ctrl"]
        query_ulfbert_R_middle_namespace=cmds.optionMenu('ulfbert_namespace_optionmenu_a', q=True, v=True)
        for f in ulfbert_all_r_middle:
            cmds.select(str(query_ulfbert_R_middle_namespace)+":"+str(f), add=True)

    def ulfbert_select_R_ring(self, *args):
        ulfbert_all_r_ring=["R_ring_1_ctrl", "R_ring_2_ctrl", "R_ring_3_ctrl"]
        query_ulfbert_R_ring_namespace=cmds.optionMenu('ulfbert_namespace_optionmenu_a', q=True, v=True)
        for f in ulfbert_all_r_ring:
            cmds.select(str(query_ulfbert_R_ring_namespace)+":"+str(f), add=True)

    def ulfbert_select_R_pink(self, *args):
        ulfbert_all_r_pink=["R_pink_1_ctrl", "R_pink_2_ctrl", "R_pink_3_ctrl"]
        query_ulfbert_R_pink_namespace=cmds.optionMenu('ulfbert_namespace_optionmenu_a', q=True, v=True)
        for f in ulfbert_all_r_pink:
            cmds.select(str(query_ulfbert_R_pink_namespace)+":"+str(f), add=True)

    def ulfbert_select_L_thumb(self, *args):
        ulfbert_all_l_thumb=["L_thumb_1_ctrl", "L_thumb_2_ctrl"]
        query_ulfbert_L_thumb_namespace=cmds.optionMenu('ulfbert_namespace_optionmenu_a', q=True, v=True)
        for f in ulfbert_all_l_thumb:
            cmds.select(str(query_ulfbert_L_thumb_namespace)+":"+str(f), add=True)

    def ulfbert_select_L_index(self, *args):
        ulfbert_all_l_index=["L_index_1_ctrl", "L_index_2_ctrl","L_index_3_ctrl"]
        query_ulfbert_L_index_namespace=cmds.optionMenu('ulfbert_namespace_optionmenu_a', q=True, v=True)
        for f in ulfbert_all_l_index:
            cmds.select(str(query_ulfbert_L_index_namespace)+":"+str(f), add=True)

    def ulfbert_select_L_middle(self, *args):
        ulfbert_all_l_middle=["L_middle_1_ctrl", "L_middle_2_ctrl", "L_middle_3_ctrl"]
        query_ulfbert_L_middle_namespace=cmds.optionMenu('ulfbert_namespace_optionmenu_a', q=True, v=True)
        for f in ulfbert_all_l_middle:
            cmds.select(str(query_ulfbert_L_middle_namespace)+":"+str(f), add=True)

    def ulfbert_select_L_ring(self, *args):
        ulfbert_all_l_ring=["L_ring_1_ctrl", "L_ring_2_ctrl", "L_ring_3_ctrl"]
        query_ulfbert_L_ring_namespace=cmds.optionMenu('ulfbert_namespace_optionmenu_a', q=True, v=True)
        for f in ulfbert_all_l_ring:
            cmds.select(str(query_ulfbert_L_ring_namespace)+":"+str(f), add=True)

    def ulfbert_select_L_pink(self, *args):
        ulfbert_all_l_pink=["L_pink_1_ctrl", "L_pink_2_ctrl", "L_pink_3_ctrl"]
        query_ulfbert_L_pink_namespace=cmds.optionMenu('ulfbert_namespace_optionmenu_a', q=True, v=True)
        for f in ulfbert_all_l_pink:
            cmds.select(str(query_ulfbert_L_pink_namespace)+":"+str(f), add=True)


class Save_character_pose_UI(Base):
    def __init__(self, character_parent_width = 320, character_parent_height = 540, character_child_width = 505, character_child_height = 295):

        super(Save_character_pose_UI, self).__init__()
        self.delete_window('character_save_pose_window')


        self.character_save_pose = {}
        self.character_parent_width = character_parent_width
        self.character_parent_height = character_parent_height
        self.character_child_width = character_child_width
        self.character_child_height = character_child_height
        self.character_save_pose['character_save_pose_win'] = cmds.window('character_save_pose_window', title = 'Character Save Pose',
                                                widthHeight = (self.character_parent_width,self.character_parent_height),menuBar = True, sizeable = False, topEdge= 0, leftEdge= 0, minimizeButton=True, maximizeButton=False)

        self.character_save_pose_main_UI()

    def character_save_pose_main_UI(self, *args):
        self.character_save_pose['character_save_pose_column_a_x'] = cmds.columnLayout('character_save_pose_column_a_x', columnAttach=('both',5), rowSpacing=3, parent=self.character_save_pose['character_save_pose_win'])
        self.character_save_pose['character_namespace_message_a']=cmds.text('character_namespace_message_a', label="No Namespace selected!",align='center',  w=305, h=20, bgc=Color.red, parent=self.character_save_pose['character_save_pose_column_a_x'])
        self.character_save_pose['character_save_pose_button_x']=cmds.button('character_save_pose_button_x', label="Refresh Namespace", w=305, command=self.refresh_save_pose_namespace)
        self.character_save_pose['character_save_pose_column_c'] = cmds.columnLayout('character_save_pose_column_c', columnAttach=('both', 5), rowSpacing=1, columnWidth=self.character_child_width, parent=self.character_save_pose['character_save_pose_win'] )
        self.character_save_pose['character_save_pose_text_a_x']=cmds.text('character_save_pose_text_a_x', label="Select Body Part:", align="left")
        self.character_save_pose['character_save_pose_separator_a_x']=cmds.separator('character_save_pose_separator_a_x', h=7, st='none')
        self.character_save_pose['character_save_pose_column_a'] = cmds.rowColumnLayout('character_save_pose_column_a', numberOfColumns=2,rowSpacing=(1, 2),
                                                             columnWidth=[(1,150), (2,150)], parent=self.character_save_pose['character_save_pose_column_c'])


        self.character_save_pose['character_save_pose_button_R_arm_controller']=cmds.button('character_save_pose_button_R_arm_controller',h=20, label='R arm', parent=self.character_save_pose['character_save_pose_column_a'], command=self.select_character_R_arm)
        self.character_save_pose['character_save_pose_button_L_arm_controller']=cmds.button('character_save_pose_button_L_arm_controller',h=20, label='L arm', parent=self.character_save_pose['character_save_pose_column_a'], command=self.select_character_L_arm)
        self.character_save_pose['character_save_pose_button_R_fingers_controller']=cmds.button('character_save_pose_button_R_fingers_controller',h=20, label='R Fingers', parent=self.character_save_pose['character_save_pose_column_a'], command=self.select_character_R_fingers)
        self.character_save_pose['character_save_pose_button_L_fingers_controller']=cmds.button('character_save_pose_button_L_fingers_controller',h=20, label='L Fingers', parent=self.character_save_pose['character_save_pose_column_a'], command=self.select_character_L_fingers)
        self.character_save_pose['character_save_pose_button_R_Leg_controller']=cmds.button('character_save_pose_button_R_Leg_controller',h=20, label='R Leg', parent=self.character_save_pose['character_save_pose_column_a'], command=self.select_character_R_leg)
        self.character_save_pose['character_save_pose_button_L_Leg_controller']=cmds.button('character_save_pose_button_L_Leg_controller',h=20, label='L Leg', parent=self.character_save_pose['character_save_pose_column_a'], command=self.select_character_L_leg)
        self.character_save_pose['character_save_pose_button_Body_controller']=cmds.button('character_save_pose_button_body_controller',h=20, label='Body', parent=self.character_save_pose['character_save_pose_column_a'], command=self.select_character_main_body)
        self.character_save_pose['character_save_pose_button_selected_controller']=cmds.button('character_save_pose_button_selected_controller',h=20, label='Selected', parent=self.character_save_pose['character_save_pose_column_a'])
        cmds.setParent('..')
        self.character_save_pose['character_save_pose_column_b'] = cmds.columnLayout('character_save_pose_column_b', rowSpacing=1,  columnWidth=self.character_child_width, parent=self.character_save_pose['character_save_pose_column_c'] )
        self.character_save_pose['character_save_pose_selected_controller']=cmds.textScrollList('character_save_pose_selected_controller',w=300, h=100, parent=self.character_save_pose['character_save_pose_column_b'])
        self.character_save_pose['character_save_pose_checkbox_formlayout']=cmds.formLayout('character_save_pose_checkbox_formlayout', h=30,w=300,parent= self.character_save_pose['character_save_pose_column_b'])
        self.character_save_pose['character_save_pose_checkbox_panLayout']=cmds.paneLayout('character_save_pose_checkbox_panLayout', configuration='vertical2',w=300,parent= self.character_save_pose['character_save_pose_checkbox_formlayout'])
        self.character_save_pose['character_save_pose_radioCollection']=cmds.radioCollection('character_save_pose_radioCollection')
        self.character_save_pose['character_save_pose_checkbox_current_namespace']=cmds.radioButton('character_save_pose_checkbox_current_namespace', sl=True, label="Current Namespace", onc=self.save_pose_radioButton_Current_namespace)
        self.character_save_pose['character_save_pose_checkbox_custom_name']=cmds.radioButton('character_save_pose_checkbox_custom_name',label="Custom Name", onc=self.save_pose_radioButton_custom_namespace)
        self.character_save_pose['charcater_save_pose_separator_d'] =cmds.separator(h=10,st='none')
        self.character_save_pose['character_save_pose_text_a']=cmds.text('character_save_pose_text_a',label='Save Pose',w=300, align='center', parent=self.character_save_pose['character_save_pose_column_b'])
        self.character_save_pose['character_save_pose_text_b']=cmds.text('character_save_pose_text_b',label='Character Name',w=300, align='left', parent=self.character_save_pose['character_save_pose_column_b'])
        self.character_save_pose['character_save_pose_scroll_c']=cmds.textField('character_save_pose_scroll_c',w=300, h=30,ed=False,  parent=self.character_save_pose['character_save_pose_column_b'])
        self.character_save_pose['character_save_pose_text_c']=cmds.text('character_save_pose_text_c',label='Describe the Pose',w=300, align='left', parent=self.character_save_pose['character_save_pose_column_b'])
        self.character_save_pose['character_save_pose_scroll_b']=cmds.scrollField('character_save_pose_scroll_b',w=300, wordWrap=True,ed=True,h=100, parent=self.character_save_pose['character_save_pose_column_b'])
        self.character_save_pose['charcater_save_pose_separator_b'] =cmds.separator(h=5,st='none')
        self.character_save_pose['character_save_pose_button_a']=cmds.button('character_save_pose_button_a',w=300, h=50, label='Save Pose', command=self.check_perspective, parent=self.character_save_pose['character_save_pose_column_b'])
        self.character_save_pose['charcater_save_pose_separator_x'] =cmds.separator(h=100,st='none', parent=self.character_save_pose['character_save_pose_column_b'])

        cmds.showWindow(self.character_save_pose['character_save_pose_win'])
        self.refresh_save_pose_namespace()
        self.set_name_save_pose()



    def save_pose_radioButton_Current_namespace(self, *args):
        cmds.textField('character_save_pose_scroll_c', e=True, ed=False)


    def save_pose_radioButton_custom_namespace(self, *args):
        cmds.textField('character_save_pose_scroll_c', e=True, ed=True)


    def refresh_save_pose_namespace(self, *args):
        query_main_body_UI_namespace=cmds.text('ulfbert_namespace_select_a',q=True, label=True)
        print query_main_body_UI_namespace
        if query_main_body_UI_namespace.startswith(":"):
            cmds.text('character_namespace_message_a', e=True, bgc=Color.green_a)
            cmds.text('character_namespace_message_a', e=True, label=query_main_body_UI_namespace)
            self.set_name_save_pose()
        else:
            cmds.text('character_namespace_message_a', e=True, bgc=Color.red)
            cmds.text('character_namespace_message_a', e=True, label="No Namespace selected or in Scene!")
            cmds.warning("No Namespace selected or in Scene!")


    def check_perspective(self, *args):
        path = "Y:/Production/rnd/ahosseini/helga_dont_show_again/helga_dont_show_again.txt"

        if os.path.isfile(path):
            file = open(path, "r")
            content = file.read()
            file.close()
            print content
            if content=="dont show again":
                self.save_pose_action_b()

        else:
            # Info Popup
            if cmds.window("check_perspective", exists=True):
                cmds.deleteUI("check_perspective")
            cmds.window("check_perspective",title="Check Perspektive",mnb=True, mxb=False,w=300,h=150,sizeable=False)
            cmds.columnLayout(w = 250, h=160, columnAttach=('both', 20), rowSpacing=5, columnWidth=250)
            cmds.separator(h=5,vis=True, st='none')
            cmds.text(label="Dont forget to choice the ", align='center')
            cmds.text(label="right Perspektive in the Viewer!!!", align='center')
            cmds.separator(h=5, vis=True, st='none')
            cmds.button(h=30, label='Save Pose', command=self.save_pose_action)
            cmds.separator(h=3, vis=True, st='none')
            cmds.checkBox('check_perspective_checkBox', label='Dont Show this message again!')
            cmds.separator(h=3, vis=True, st='none')
            cmds.showWindow()


    def select_character_R_arm(self, *args):
        select_character_R_arm_namespace = pm.system.listNamespaces()
        if len(select_character_R_arm_namespace)==0:
            cmds.warning('No Character in Scene')
        else:
            query_select_character_R_arm_namespace=cmds.optionMenu('ulfbert_namespace_optionmenu_a', q=True, v=True)
            character_R_arm_list=[str('R_arm_wrist_fk_ctrl'),str('R_arm_elbow_fk_ctrl'),
                                   str('R_arm_elbow_ik_ctrl'),str('R_index_0_ctrl'),str('R_index_1_ctrl'),
                                   str('R_index_2_ctrl'),str('R_index_3_ctrl'),str('R_middle_0_ctrl'),
                                   str('R_middle_1_ctrl'),str('R_middle_2_ctrl'),str('R_middle_3_ctrl'),
                                   str('R_ring_0_ctrl'),str('R_ring_1_ctrl'),str('R_ring_2_ctrl'),
                                   str('R_ring_3_ctrl'),str('R_pink_0_ctrl'),str('R_pink_1_ctrl'),
                                   str('R_pink_2_ctrl'),str('R_pink_3_ctrl'),str('R_thumb_0_ctrl'),
                                   str('R_thumb_1_ctrl'),str('R_thumb_2_ctrl'),str('R_up_arm_off_ctrl'),
                                   str('R_down_arm_off_ctrl'),str('R_arm_off_ctrl'),str('R_arm_wrist_ik_ctrl'),
                                     str('R_arm_shoulder_fk_ctrl')]
            cmds.textScrollList('character_save_pose_selected_controller',e=True,ra=True)
            for a in character_R_arm_list:
                cmds.textScrollList('character_save_pose_selected_controller', e=True, append=a)


    def select_character_L_arm(self, *args):
        select_character_L_arm_namespace = pm.system.listNamespaces()
        if len(select_character_L_arm_namespace)==0:
            cmds.warning('No Character in Scene')
        else:
            query_select_character_L_arm_namespace=cmds.optionMenu('ulfbert_namespace_optionmenu_a', q=True, v=True)
            character_L_arm_list=[str('L_arm_shoulder_fk_ctrl'), str('L_arm_wrist_fk_ctrl'),
                                 str('L_arm_elbow_fk_ctrl'), str('L_arm_elbow_ik_ctrl'), str('L_index_0_ctrl'),
                                  str('L_index_1_ctrl'), str('L_index_2_ctrl'), str('L_index_3_ctrl'),
                                  str('L_middle_0_ctrl'), str('L_middle_1_ctrl'), str('L_middle_2_ctrl'),
                                   str('L_middle_3_ctrl'), str('L_ring_0_ctrl'), str('L_ring_1_ctrl'),
                                   str('L_ring_2_ctrl'), str('L_ring_3_ctrl'), str('L_pink_0_ctrl'),
                                   str('L_pink_1_ctrl'), str('L_pink_2_ctrl'), str('L_pink_3_ctrl'),
                                   str('L_thumb_0_ctrl'), str('L_thumb_1_ctrl'), str('L_thumb_2_ctrl'),
                                   str('L_up_arm_off_ctrl'), str('L_down_arm_off_ctrl'), str('L_arm_off_ctrl'),
                                   str('L_arm_wrist_ik_ctrl')]
            cmds.textScrollList('character_save_pose_selected_controller',e=True,ra=True)
            for a in character_L_arm_list:
                cmds.textScrollList('character_save_pose_selected_controller', e=True, append=a)




    def select_character_R_leg(self, *args):
        select_character_R_leg_namespace = pm.system.listNamespaces()
        if len(select_character_R_leg_namespace)==0:
            cmds.warning('No Character in Scene')
        else:
            query_select_character_R_leg_namespace=cmds.optionMenu('ulfbert_namespace_optionmenu_a', q=True, v=True)
            character_R_leg_list=[str('R_leg_ankle_fk_ctrl'), str('R_leg_knee_fk_ctrl'), str('R_foot_middle_ctrl'), str('R_up_leg_off_ctrl'),
                                    str('R_down_leg_off_ctrl'), str('R_leg_off_ctrl'), str('R_leg_ankle_ik_ctrl'), str('R_leg_knee_ik_ctrl'),
                                    str('R_leg_leg_fk_ctrl'), str('R_leg_hip_ik_ctrl'), str('R_leg_hip_fk_ctrl')]
            cmds.textScrollList('character_save_pose_selected_controller',e=True,ra=True)
            for a in character_R_leg_list:
                cmds.textScrollList('character_save_pose_selected_controller', e=True, append=a)




    def select_character_L_leg(self, *args):
        select_character_L_leg_namespace = pm.system.listNamespaces()
        if len(select_character_L_leg_namespace)==0:
            cmds.warning('No Character in Scene')
        else:
            query_select_character_L_leg_namespace=cmds.optionMenu('ulfbert_namespace_optionmenu_a', q=True, v=True)
            character_L_leg_list=[str('L_leg_ankle_fk_ctrl'), str('L_foot_middle_ctrl'), str('L_leg_ankle_ik_ctrl'), str('L_leg_knee_ik_ctrl'),
                                    str('L_down_leg_off_ctrl'), str('L_leg_knee_fk_ctrl'), str('L_leg_off_ctrl'), str('L_up_leg_off_ctrl'),
                                    str('L_leg_leg_fk_ctrl'), str('L_leg_hip_ik_ctrl'), str('L_leg_hip_fk_ctrl')]
            cmds.textScrollList('character_save_pose_selected_controller',e=True,ra=True)
            for a in character_L_leg_list:
                cmds.textScrollList('character_save_pose_selected_controller', e=True, append=a)



    def select_character_R_fingers(self, *args):
        select_character_R_fingers_namespace = pm.system.listNamespaces()
        if len(select_character_R_fingers_namespace)==0:
            cmds.warning('No Character in Scene')
        else:
            query_select_character_R_fingers_namespace=cmds.optionMenu('ulfbert_namespace_optionmenu_a', q=True, v=True)
            character_R_fingers_list=[str('R_thumb_0_ctrl'), str('R_index_0_ctrl'), str('R_middle_0_ctrl'), str('R_ring_0_ctrl'), str('R_pink_0_ctrl'),
                                        str('R_thumb_1_ctrl'), str('R_index_1_ctrl'), str('R_index_2_ctrl'), str('R_index_3_ctrl'), str('R_middle_1_ctrl'),
                                        str('R_middle_2_ctrl'), str('R_middle_3_ctrl'), str('R_ring_1_ctrl'), str('R_ring_2_ctrl'), str('R_ring_3_ctrl'),
                                        str('R_pink_1_ctrl'), str('R_pink_2_ctrl'), str('R_pink_3_ctrl'), str('R_thumb_2_ctrl')]
            cmds.textScrollList('character_save_pose_selected_controller',e=True,ra=True)
            for a in character_R_fingers_list:
                cmds.textScrollList('character_save_pose_selected_controller', e=True, append=a)


    def select_character_L_fingers(self, *args):
        select_character_L_fingers_namespace = pm.system.listNamespaces()
        if len(select_character_L_fingers_namespace)==0:
            cmds.warning('No Character in Scene')
        else:
            query_select_character_L_fingers_namespace=cmds.optionMenu('ulfbert_namespace_optionmenu_a', q=True, v=True)
            character_L_fingers_list=[str('L_thumb_0_ctrl'),str('L_index_0_ctrl'),str('L_middle_0_ctrl'),str('L_ring_0_ctrl'),str('L_pink_0_ctrl'),
                                       str('L_thumb_1_ctrl'),str('L_index_1_ctrl'),str('L_index_2_ctrl'),str('L_index_3_ctrl'),str('L_middle_1_ctrl'),
                                       str('L_middle_2_ctrl'),str('L_middle_3_ctrl'),str('L_ring_1_ctrl'),str('L_ring_2_ctrl'),str('L_ring_3_ctrl'),
                                       str('L_pink_1_ctrl'),str('L_pink_2_ctrl'),str('L_pink_3_ctrl'),str('L_thumb_2_ctrl')]
            cmds.textScrollList('character_save_pose_selected_controller',e=True,ra=True)
            for a in character_L_fingers_list:
                cmds.textScrollList('character_save_pose_selected_controller', e=True, append=a)


    def select_character_main_body(self, *args):
        select_character_main_body_namespace = pm.system.listNamespaces()
        if len(select_character_main_body_namespace)==0:
            cmds.warning('No Character in Scene')
        else:
            self.query_select_character_main_body_namespace=cmds.optionMenu('ulfbert_namespace_optionmenu_a', q=True, v=True)
            character_main_body_list=[str('head_head_ctrl'), str('head_jaw_ctrl'), str('head_chin_ctrl'), str('spine_hipsA_ctrl'), str('spine_hipsB_ctrl'),
            str('L_leg_hip_fk_ctrl'), str('L_leg_leg_fk_ctrl'), str('L_leg_ankle_fk_ctrl'), str('L_leg_knee_fk_ctrl'),
            str('L_leg_hip_ik_ctrl'), str('L_foot_middle_ctrl'), str('L_up_leg_off_ctrl'), str('L_down_leg_off_ctrl'),
            str('L_leg_off_ctrl'), str('R_leg_hip_fk_ctrl'), str('R_leg_leg_fk_ctrl'), str('R_leg_ankle_fk_ctrl'),
            str('R_leg_knee_fk_ctrl'), str('R_leg_hip_ik_ctrl'), str('R_foot_middle_ctrl'), str('R_up_leg_off_ctrl'),
            str('R_down_leg_off_ctrl'), str('R_leg_off_ctrl'), str('spine_chestA_ctrl'), str('spine_chestB_ctrl'),
            str('head_neck_ctrl'), str('L_arm_clavicle_fk_ctrl'), str('L_arm_shoulder_fk_ctrl'), str('L_arm_wrist_fk_ctrl'),
            str('L_arm_elbow_fk_ctrl'), str('L_arm_elbow_ik_ctrl'), str('L_arm_clavicle_ik_ctrl'), str('L_index_0_ctrl'),
            str('L_index_1_ctrl'), str('L_index_2_ctrl'), str('L_index_3_ctrl'), str('L_middle_0_ctrl'), str('L_middle_1_ctrl'),
            str('L_middle_2_ctrl'), str('L_middle_3_ctrl'), str('L_ring_0_ctrl'), str('L_ring_1_ctrl'), str('L_ring_2_ctrl'),
            str('L_ring_3_ctrl'), str('L_pink_0_ctrl'), str('L_pink_1_ctrl'), str('L_pink_2_ctrl'), str('L_pink_3_ctrl'),
            str('L_thumb_0_ctrl'), str('L_thumb_1_ctrl'), str('L_thumb_2_ctrl'), str('L_up_arm_off_ctrl'), str('L_down_arm_off_ctrl'),
            str('L_arm_off_ctrl'), str('R_arm_clavicle_fk_ctrl'), str('R_arm_shoulder_fk_ctrl'), str('R_arm_wrist_fk_ctrl'),
            str('R_arm_elbow_fk_ctrl'), str('R_arm_elbow_ik_ctrl'), str('R_arm_clavicle_ik_ctrl'), str('R_index_0_ctrl'),
            str('R_index_1_ctrl'), str('R_index_2_ctrl'), str('R_index_3_ctrl'), str('R_middle_0_ctrl'), str('R_middle_1_ctrl'),
            str('R_middle_2_ctrl'), str('R_middle_3_ctrl'), str('R_ring_0_ctrl'), str('R_ring_1_ctrl'), str('R_ring_2_ctrl'),
            str('R_ring_3_ctrl'), str('R_pink_0_ctrl'), str('R_pink_1_ctrl'), str('R_pink_2_ctrl'), str('R_pink_3_ctrl'),
            str('R_thumb_0_ctrl'), str('R_thumb_1_ctrl'), str('R_thumb_2_ctrl'), str('R_up_arm_off_ctrl'), str('R_down_arm_off_ctrl'),
            str('R_arm_off_ctrl'), str('L_arm_wrist_ik_ctrl'), str('R_arm_wrist_ik_ctrl'), str('spine_middle1_ctrl'),
            str('L_leg_ankle_ik_ctrl'), str('L_leg_knee_ik_ctrl'), str('R_leg_ankle_ik_ctrl'), str('R_leg_knee_ik_ctrl')]

            cmds.textScrollList('character_save_pose_selected_controller',e=True,ra=True)
            for a in character_main_body_list:
                cmds.textScrollList('character_save_pose_selected_controller', e=True, append=a)



    def save_pose_action(self, *args):
        if cmds.window("check_perspective", exists=True):
            query_check_perspective_checkBox = cmds.checkBox('check_perspective_checkBox', value=True, q=True)
        if query_check_perspective_checkBox == True:
            file = open("Y:/Production/rnd/ahosseini/helga_dont_show_again/helga_dont_show_again.txt", "a")
            file.write("dont show again")
            file.close()
            self.save_pose_action_b()
        else:
            self.save_pose_action_b()


    def save_pose_action_b(self, *args):
        self.delete_window('check_perspective')
        self.query_character_name = cmds.textField('character_save_pose_scroll_c', text=True, query=True)
        self.query_pose_describe = cmds.scrollField('character_save_pose_scroll_b', text=True, query=True)
        self.query_selected_body_part = cmds.textScrollList('character_save_pose_selected_controller', q=True, ai=True)
        # print (self.query_selected_body_part)
        # print (self.query_character_name)
        # print (self.query_pose_describe)
        self.save_pose()
        self.save_pose_screen_save()
        self.delete_window('character_save_pose_window')


    def save_pose(self, *args):

        doc = Document()

        root_node = doc.createElement("Pose")
        doc.appendChild(root_node)

        # grab all visible objects, which type is transform
        selection = self.query_selected_body_part
        selection_b=[]
        for member_b in selection:
            new_member=str(self.query_select_character_main_body_namespace)+str(":")+str(member_b)
            selection_b.append(new_member)
        print selection_b

        for member in selection_b:
            nodeName = member #    Fix Later

            # XML create object element
            object_node = doc.createElement("Ctrl")
            root_node.appendChild(object_node)

            # Save Name
            object_node.setAttribute("name", str(nodeName))

            # set attributes
            for attrName in cmds.listAttr(nodeName, k=True):
                self.saveValue(nodeName, attrName, object_node)
                cmds.warning('Pose successful saved')

        now_character_save_pose = time.localtime(time.time())
        self.current_time_character_save_pose = time.strftime("%a, %d %m %y", now_character_save_pose)
        self.character_save_pose_get_user=getpass.getuser()
        xml_file = open("Y:/Production/rnd/ahosseini/helga_save_pose/"+self.query_character_name+"_"+self.query_pose_describe+"_"+self.character_save_pose_get_user+"_"+self.current_time_character_save_pose+".xml" , "w")
        xml_file.write(doc.toprettyxml())
        xml_file.close()


    def save_pose_screen_save(self, *args):
        screen_image_path = ("Y:/Production/rnd/ahosseini/helga_save_pose/helga_save_pose_image/")+ self.query_character_name+"_"+self.query_pose_describe+"_"+self.character_save_pose_get_user+"_"+self.current_time_character_save_pose+'.jpg'
        screen_view= openMayaUi.M3dView.active3dView()
        screen_image = openMaya.MImage()
        screen_view.readColorBuffer(screen_image, True)
        screen_image.resize(300, 300, True)
        screen_image=screen_image.writeToFile(screen_image_path, 'jpg')




class Load_character_pose_UI(Base):
    def __init__(self, character_load_parent_width = 320, character_load_parent_height =640, character_load_child_width = 315, character_load_child_height = 465):

        super(Load_character_pose_UI, self).__init__()
        self.delete_window('character_load_pose_window')


        self.character_load_pose = {}
        self.character_load_parent_width = character_load_parent_width
        self.character_load_parent_height = character_load_parent_height
        self.character_load_child_width = character_load_child_width
        self.character_load_child_height = character_load_child_height
        self.character_load_pose['character_load_pose_win'] = cmds.window('character_load_pose_window', title = 'Character Load Pose',
                                                widthHeight = (self.character_load_parent_width,self.character_load_parent_height),menuBar = True, sizeable = False, topEdge= 0, leftEdge= 0, minimizeButton=True, maximizeButton=False)

        self.character_load_pose_main_UI()

    def character_load_pose_main_UI(self, *args):
        self.character_load_pose['character_load_pose_column_a'] = cmds.columnLayout('character_load_pose_column_a', columnAttach=('both', 5), rowSpacing=1, columnWidth=self.character_load_child_width )
        self.character_load_pose['character_save_pose_a_x']=cmds.text('character_save_pose_a_x', label="No Namespace selected!", h=20, bgc=Color.red)
        self.character_load_pose['separator_d'] = cmds.separator(h=15, vis=True, st='none')
        self.character_load_pose['character_load_text_a'] = cmds.text('character_load_text_a', label="Saved Pose", align ='left')
        self.character_load_pose['separator_e'] = cmds.separator(h=7, vis=True, st='none')
        self.character_load_pose['character_load_saved_pose']=cmds.textScrollList('character_load_saved_pose',w=300, h=200, sc=self.change_saved_image, parent=self.character_load_pose['character_load_pose_column_a'] )
        self.character_load_pose['character_load_pose_button_x']=cmds.button('character_load_pose_button_x', label="Refresh List", command=self.load_saved_poses)
        self.character_load_pose['character_load_pose_separator_k']=cmds.separator(h=5, vis=True, st='in')
        self.character_load_pose['character_save_separator_g'] = cmds.separator(h=5, st='none')
        self.character_load_pose['character_load_text_b'] = cmds.text('character_load_text_b', label="Pose Image", align='left')
        self.character_load_pose['character_save_separator_g'] = cmds.separator(h=5, st='none')
        load_image_path= cmds.internalVar(upd=False)+ "Y:/Production/rnd/ahosseini/helga_save_pose/helga_save_pose_image/" + "main_image_load.jpg"
        self.character_load_pose['laod_image_area_a'] = cmds.image('laod_image_area_a', w=300, h=180, image=load_image_path, parent=self.character_load_pose['character_load_pose_column_a'] )
        self.character_load_pose['character_load_pose_describe']=cmds.text('character_load_pose_describe', h=20, align='left', label="Describe:")
        self.character_load_pose['character_load_pose_separator_h']=cmds.separator(h=5, vis=True, st='in')
        self.character_load_pose['character_save_pose_paneLayout']=cmds.paneLayout( 'character_save_pose_paneLayout', configuration='quad' , h=50)
        self.character_load_pose['character_load_text_c']=cmds.text('character_load_text_c', h=20, label="Select Character", align='center')
        self.character_load_pose['character_select_optionMenu']=cmds.optionMenu('character_select_optionMenu', label="", parent=self.character_load_pose['character_save_pose_paneLayout'])
        self.character_load_pose['character_load_text_f']=cmds.text('character_load_text_f', h=20, label="Date", align='left')
        self.character_load_pose['character_load_text_g']=cmds.text('character_load_text_g', h=20, label="Artist", align='center')
        self.character_load_pose['character_load_pose_separator_j'] = cmds.separator(h=7, vis=True, st='in')
        self.character_load_pose['character_load_pose_button_a'] = cmds.button('character_load_pose_button_a', label='Load Pose', h=50, command=self.load_pose, parent=self.character_load_pose['character_load_pose_column_a'])

        self.load_saved_poses()
        self.refresh_load_pose_namespace()
        self.character_load_pose_namespace()
        cmds.showWindow(self.character_load_pose['character_load_pose_win'])


    def character_load_pose_namespace(self, *args):
        character_namespace_list = pm.system.listNamespaces()
        character_namespace_menuItem=cmds.optionMenu('character_select_optionMenu', q=True, itemListLong=True)
        # if ulfbert_namespace_menuItem:
        #     cmds.deleteUI(ulfbert_namespace_menuItem)
        for self.namespace_laod in character_namespace_list:
            cmds.menuItem(label=self.namespace_laod, parent=self.character_load_pose['character_select_optionMenu'])


    def change_saved_image(self, *args):
        query_selected_pose = cmds.textScrollList('character_load_saved_pose', si=True, q=True)
        self.set_first_member=query_selected_pose[0]
        split_first_member = self.set_first_member.split(".")[0]
        cmds.image('laod_image_area_a', e=True, image="Y:/Production/rnd/ahosseini/helga_save_pose/helga_save_pose_image/"+split_first_member+ ".jpg")
        split_date_data=split_first_member.split("_")[-1]
        split_artist_data=split_first_member.split("_")[-2]
        split_describe_data=split_first_member.split("_")[-3]
        cmds.text('character_load_pose_describe', e=True, label=str("Describe: ")+ str(split_describe_data))
        cmds.text('character_load_text_f', e=True, label=split_date_data)
        cmds.text('character_load_text_g', e=True, label=split_artist_data)



    def refresh_load_pose_namespace(self, *args):
        query_main_body_UI_namespace=cmds.text('ulfbert_namespace_select_a',q=True, label=True)
        #print query_main_body_UI_namespace
        if query_main_body_UI_namespace.startswith(":"):
            cmds.text('character_save_pose_a_x', e=True, bgc=Color.green_a)
            cmds.text('character_save_pose_a_x', e=True, label=query_main_body_UI_namespace)
        else:
            cmds.text('character_save_pose_a_x', e=True, bgc=Color.red)
            cmds.text('character_save_pose_a_x', e=True, label="No Namespace selected or in Scene!")
            cmds.warning("No Namespace selected or in Scene!")



    def load_saved_poses(self, *args):
        cmds.textScrollList('character_load_saved_pose', e=True, ra=True)
        pose_libary_path = ("Y:/Production/rnd/ahosseini/helga_save_pose/")
        load_file_path = os.listdir(pose_libary_path)
        # print load_file_path
        for pose in load_file_path:
            if pose.rpartition(".")[2]=="xml":
                cmds.textScrollList('character_load_saved_pose', e=True, append=pose)




    def load_pose(self, *args):
        self.query_load_pose_name=cmds.optionMenu('character_select_optionMenu', q=True, v=True)

        dom = parse("Y:/Production/rnd/ahosseini/helga_save_pose/"+self.set_first_member)
         # visit every object node
        for node in dom.getElementsByTagName('Ctrl'):

            nodeName = str(node.getAttribute("name"))
            split_nodeName=nodeName.split(":")[1]
            split_nodeName_Ctrl=nodeName.split(":")[2]
            split_nodeName=self.query_load_pose_name
            nodeName=split_nodeName+":"+split_nodeName_Ctrl
            for attrName in cmds.listAttr(nodeName, k=True):
                self.setValue(nodeName, attrName, node)

        cmds.warning('Pose load successfuly')



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
#Standardized run() method. Used to call modules functionality
#
#
#################################################################################
def run():
    """Standardized run() method. Used to call modules functionality"""

    Helga_cms_login_UI()







#################################################################################
#
#
#Test when run without importing (Running in main namespace)
#
#
#################################################################################
if(__name__ == '__main__'):
    Helga_cms_login_UI()