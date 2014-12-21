


"""
SwitchParentspace
==========================================

Tool to switch parentspaces for helga props.

To use it, execute the following:

..code ::

    from helga.maya.hanna.switch_parentspace import switch_parentspace
    reload(switch_parentspace)
    switch_parentspace.SwitchParentspace().run()


-----------------------

**Author:** `Hanna Binswanger <mailto:hanna.binswanger@filmakademie.de>`_
*Version:* 0.1
"""






#python
import logging

#maya
import pymel.core as pm
from functools import partial

class SwitchParentspace:

    def __init__(self):

        """Docstring"""

        self.logger = logging.getLogger('SwitchParentspace')
        #self.logger.setLevel(logging.WARNING)
        self.logger.setLevel(logging.INFO)
        #self.logger.setLevel(logging.DEBUG)
        
        #logger.warning('info_msg')
        #logger.info('info_msg')

        self.logger.debug('--- switch_Parentspace ___init()___ ---')
        self.window_name = 'SwitchParentspace'

        self.optionMenu_default_value = '-select-'

        self.confirm_overwrite = 0
        


        
        '''
        TANKARD
        '''
        self.namespace_tankard = ''
        self.root_obj_tankard = 'manip_tankard'
        self.switch_obj_tankard = 'manip_tankard_matchPS'
        self.switch_attr_tankard = 'manip_tankard.Follow'
        self.follow_values = ['World',
                              'UlfbertHandL',
                              'UlfbertHandR',
                              'SnorriHandL',
                              'SnorriHandR',
                              'HelgaHandL',
                              'HelgaHandR']

        self.follow_nodes = ['con_CON_World', 'con_CON_UlfbertHandL', 'con_CON_UlfbertHandR', 'con_CON_SnorriHandL', 'con_CON_SnorriHandR', 'con_CON_HelgaHandL', 'con_CON_HelgaHandR']

        self.follow_sources = ['L_Arm_Wrist_ToParent_Ctrl', 'R_Arm_Wrist_ToParent_Ctrl']

        self.ns_ulfbert = []
        self.ns_snorri = []
        self.ns_helga = []

        self.con_grp_tankard = 'grp_CON_PS_DONT_TOUCH'


    def run(self):

        self.logger.debug('--- run()')


        #get namespaces
        self.get_scene_namespaces()

        global win

        if pm.window(self.window_name, q = True, ex = True):
            pm.deleteUI(self.window_name)

        if pm.windowPref(self.window_name, q = True, ex = True):
            pm.windowPref(self.window_name, r = True)

        win = pm.window(self.window_name, title = self.window_name, w = 150, h = 100,
                        te = 210, le = 70)

        layout1 = pm.rowColumnLayout(numberOfColumns = 1, cw = [(1,150)])

        '''
        character namespaces
        '''

        pm.optionMenu('optionMenu_ns_ulfbert', label = ' Ulfbert:')
        pm.menuItem( label = self.optionMenu_default_value)
        for obj in self.ns_ulfbert:
            pm.menuItem( label = obj)
        pm.optionMenu('optionMenu_ns_snorri', label = ' Snorri:')
        pm.menuItem( label = self.optionMenu_default_value)
        for obj in self.ns_snorri:
            pm.menuItem( label = obj)
        pm.optionMenu('optionMenu_ns_helga', label = ' Helga:')
        pm.menuItem( label = self.optionMenu_default_value)
        for obj in self.ns_helga:
            pm.menuItem( label = obj)

        pm.text(label = '')

        '''
        TANKARD
        '''
        pm.text(label = '--TANKARD--')
        pm.button('b_initialize_tankard', label = "Initialize", c = self.initialize_tankard,
                   annotation = 'Select tankard root and press >Initialize> button')
        pm.text(label = '')

        pm.text(label = 'Select Parent Space:')
        pm.text(label = '')
        pm.optionMenu('optionMenu_tankard', enable = False)

        pm.menuItem( label = self.optionMenu_default_value)
        for obj in self.follow_values:
            pm.menuItem( label = obj)
        pm.text(label = '')

        pm.button('b_switch_PS_tankard', label = "-", c = self.switch_PS_tankard, enable = False)
        pm.text(label = '')

        pm.button('b_select_switch_obj_tankard', label = "-", c = self.select_switch_obj_tankard, enable = False)
        pm.text(label = '')

        win.show()

    def get_scene_namespaces(self):

        self.logger.debug('--- get_namespaces()')

        tmp_namespaces = pm.namespaceInfo(listOnlyNamespaces = 1)

        self.logger.debug('namespaces: ')
        self.logger.debug(tmp_namespaces)

        for obj in tmp_namespaces:

            chunks = obj.split('_')

            for chunk in chunks:

                if chunk == 'ulfbert':
                    self.ns_ulfbert.append(obj + ':')

                if chunk == 'snorri':
                    self.ns_snorri.append(obj + ':')

                if chunk == 'helga':
                    self.ns_helga.append(obj + ':')

        self.logger.debug(self.ns_ulfbert)
        self.logger.debug(self.ns_snorri)
        self.logger.debug(self.ns_helga)


    def initialize_tankard(self, x):

        self.logger.debug('--- initialize_tankard()')

        self.namespace_tankard = ''
        self.root_obj_tankard = 'manip_tankard'
        self.switch_obj_tankard = 'manip_tankard_matchPS'
        self.switch_attr_tankard = 'manip_tankard.Follow'
        pm.optionMenu('optionMenu_tankard', e = True, v = '-select-')

        # Get selection
        tmp_sel = pm.ls(sl = True)
        self.logger.debug('selection: ' + str(tmp_sel))
        
        if not tmp_sel:
            pm.warning('Select root controller of Tankard!')
            return

        # Get the namespace
        chunk = tmp_sel[0]
        chunk_splitted = ''

        if ':' in chunk:
            chunk_splitted = chunk.split(':')

            if not chunk_splitted[-1] == self.root_obj_tankard:
                pm.warning('Select root controller of Tankard!')
                return

            iterator = 0

            while iterator < len(chunk_splitted)-1:

                self.namespace_tankard = self.namespace_tankard + chunk_splitted[iterator] + ':'
                self.logger.debug('NAMESPACE: ' + self.namespace_tankard)
                iterator += 1

        else:

            if not chunk == self.root_obj_tankard:
                pm.warning('Select root controller of Tankard!')
                return

        self.logger.debug('FINAL NAMESPACE: ' + self.namespace_tankard)

        self.switch_obj_tankard = self.namespace_tankard + self.switch_obj_tankard
        self.switch_attr_tankard = self.namespace_tankard + self.switch_attr_tankard

        self.set_constraints_tankard()

        #pm.button('binitialize_tankard', e = True, label = '-', enable = False)
        pm.optionMenu('optionMenu_tankard', e = True, enable = True)
        pm.button('b_switch_PS_tankard', e = True, label = 'SWITCH!', enable = True)
        pm.button('b_select_switch_obj_tankard', e = True, label = '"Select Switch Object"', enable = True)

    def get_namespace(self, in_obj):

        self.logger.debug('--- get_namespace()')

        iterator = 0
        tmp_namespace = ''

        self.logger.debug(in_obj)

        if ':' in in_obj:
            chunk_splitted = in_obj.split(':')

            while iterator < len(chunk_splitted)-1:

                tmp_namespace = tmp_namespace + chunk_splitted[iterator] + ':'
                iterator += 1

        return tmp_namespace



    def set_constraints_tankard(self):

        self.logger.debug('--- set_constraints_tankard()')

        ns_ulfbert = pm.optionMenu('optionMenu_ns_ulfbert', q=1, value=1)
        ns_snorri = pm.optionMenu('optionMenu_ns_snorri', q=1, value=1)
        ns_helga = pm.optionMenu('optionMenu_ns_helga', q=1, value=1)

        self.logger.debug('ns_ulfbert: ' + str(ns_ulfbert))
        self.logger.debug('ns_snorri: ' + str(ns_snorri))
        self.logger.debug('ns_helga: ' + str(ns_helga))

        if ns_ulfbert == self.optionMenu_default_value:
            self.logger.warning('No namespace selected! - switch might not behave correctly')

        if ns_snorri == self.optionMenu_default_value:
            self.logger.warning('No namespace selected! - switch might not behave correctly')

        if ns_helga == self.optionMenu_default_value:
            self.logger.warning('No namespace selected! - switch might not behave correctly')


        #check existing constraints
        for iterator, obj in enumerate(self.follow_nodes):

            tmp_constraints = pm.listRelatives(self.namespace_tankard + obj, c = True, type = 'parentConstraint')
            self.logger.debug(tmp_constraints)

            if len(tmp_constraints) == 1:

                self.logger.debug('constraint set for ' + obj)

                tmp_constraint_targets = pm.parentConstraint(tmp_constraints[0], q=1, tl=1 )

                self.logger.debug(tmp_constraint_targets)

                if len(tmp_constraint_targets) == 1:

                    tmp_namespace_old = self.get_namespace(tmp_constraint_targets[0])

                    self.logger.debug('NAMESPACE OLD: ' + tmp_namespace_old)

                    if iterator == 1:

                        self.logger.debug('NAMESPACE NEW: ' + ns_ulfbert)

                        if ns_ulfbert != self.optionMenu_default_value:

                            if tmp_namespace_old != ns_ulfbert:
                                self.confirm_overwrite = cmds.confirmDialog( title='Confirm', message='Do you want to overwrite existing parent space of Ulfbert with new one?',
                                                                    button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )

                                if self.confirm_overwrite:
                                    self.logger.debug('overwrite confirmed')

                                    tmp_con_grp = ns_ulfbert + str(self.follow_sources[0])

                                    if pm.objExists(tmp_con_grp):

                                        pm.delete(tmp_constraints)
                                        pm.parentConstraint(tmp_con_grp, self.namespace_tankard + obj, maintainOffset = True)

                                    else:
                                        self.logger.warning('Source not found: ' + tmp_con_grp + ' -Ignore warning if character is not needed-')

                                else:
                                    self.logger.debug('overwrite canceled')

                    if iterator == 2:

                        self.logger.debug('NAMESPACE NEW: ' + ns_ulfbert)

                        if ns_ulfbert != self.optionMenu_default_value:

                            if self.confirm_overwrite:
                                self.logger.debug('overwrite confirmed')

                                tmp_con_grp = ns_ulfbert + str(self.follow_sources[1])

                                if pm.objExists(tmp_con_grp):

                                    pm.delete(tmp_constraints)
                                    pm.parentConstraint(tmp_con_grp, self.namespace_tankard + obj, maintainOffset = True)

                                else:
                                    self.logger.warning('Source not found: ' + tmp_con_grp + ' -Ignore warning if character is not needed-')

                        else:
                            self.logger.debug('overwrite canceled')

                    if iterator == 3:

                        self.logger.debug('NAMESPACE NEW: ' + ns_snorri)

                        if ns_snorri != self.optionMenu_default_value:

                            if tmp_namespace_old != ns_snorri:
                                self.confirm_overwrite = cmds.confirmDialog( title='Confirm', message='Do you want to overwrite existing parent space of snorri with new one?',
                                                                    button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )

                                if self.confirm_overwrite:
                                    self.logger.debug('overwrite confirmed')

                                    tmp_con_grp = ns_snorri + str(self.follow_sources[0])

                                    if pm.objExists(tmp_con_grp):

                                        pm.delete(tmp_constraints)
                                        pm.parentConstraint(tmp_con_grp, self.namespace_tankard + obj, maintainOffset = True)

                                    else:
                                        self.logger.warning('Source not found: ' + tmp_con_grp + ' -Ignore warning if character is not needed-')

                                else:
                                    self.logger.debug('overwrite canceled')

                    if iterator == 4:

                        self.logger.debug('NAMESPACE NEW: ' + ns_snorri)

                        if ns_snorri != self.optionMenu_default_value:

                            if self.confirm_overwrite:
                                self.logger.debug('overwrite confirmed')

                                tmp_con_grp = ns_snorri + str(self.follow_sources[1])

                                if pm.objExists(tmp_con_grp):

                                    pm.delete(tmp_constraints)
                                    pm.parentConstraint(tmp_con_grp, self.namespace_tankard + obj, maintainOffset = True)

                                else:
                                    self.logger.warning('Source not found: ' + tmp_con_grp + ' -Ignore warning if character is not needed-')

                        else:
                            self.logger.debug('overwrite canceled')

                    if iterator == 5:

                        self.logger.debug('NAMESPACE NEW: ' + ns_helga)

                        if ns_helga != self.optionMenu_default_value:

                            if tmp_namespace_old != ns_helga:
                                self.confirm_overwrite = cmds.confirmDialog( title='Confirm', message='Do you want to overwrite existing parent space of helga with new one?',
                                                                    button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )

                                if self.confirm_overwrite:
                                    self.logger.debug('overwrite confirmed')

                                    tmp_con_grp = ns_helga + str(self.follow_sources[0])

                                    if pm.objExists(tmp_con_grp):

                                        pm.delete(tmp_constraints)
                                        pm.parentConstraint(tmp_con_grp, self.namespace_tankard + obj, maintainOffset = True)

                                    else:
                                        self.logger.warning('Source not found: ' + tmp_con_grp + ' -Ignore warning if character is not needed-')

                                else:
                                    self.logger.debug('overwrite canceled')

                    if iterator == 6:

                        self.logger.debug('NAMESPACE NEW: ' + ns_helga)

                        if ns_helga != self.optionMenu_default_value:

                            if self.confirm_overwrite:
                                self.logger.debug('overwrite confirmed')

                                tmp_con_grp = ns_helga + str(self.follow_sources[1])

                                if pm.objExists(tmp_con_grp):

                                    pm.delete(tmp_constraints)
                                    pm.parentConstraint(tmp_con_grp, self.namespace_tankard + obj, maintainOffset = True)

                                else:
                                    self.logger.warning('Source not found: ' + tmp_con_grp + ' -Ignore warning if character is not needed-')

                        else:
                            self.logger.debug('overwrite canceled')


            else:

                self.logger.debug('no constraint yet - setting constraint for ' + obj)

                if iterator == 1:

                    if ns_ulfbert != self.optionMenu_default_value:

                        tmp_con_grp = ns_ulfbert + str(self.follow_sources[0])

                        if pm.objExists(tmp_con_grp):

                            pm.parentConstraint(tmp_con_grp, self.namespace_tankard + obj, maintainOffset = True)

                        else:
                            self.logger.warning('Source not found: ' + tmp_con_grp + ' -Ignore warning if character is not needed-')
                    else:
                            self.logger.warning('Select namespace for ulfbert!')

                if iterator == 2:

                    if ns_ulfbert != self.optionMenu_default_value:

                        tmp_con_grp = ns_ulfbert + str(self.follow_sources[1])

                        if pm.objExists(tmp_con_grp):

                            pm.parentConstraint(tmp_con_grp, self.namespace_tankard + obj, maintainOffset = True)

                        else:
                            self.logger.warning('Source not found: ' + tmp_con_grp + ' -Ignore warning if character is not needed-')


                if iterator == 3:

                    if ns_snorri != self.optionMenu_default_value:

                        tmp_con_grp = ns_snorri + str(self.follow_sources[0])

                        if pm.objExists(tmp_con_grp):

                            pm.parentConstraint(tmp_con_grp, self.namespace_tankard + obj, maintainOffset = True)

                        else:
                            self.logger.warning('Source not found: ' + tmp_con_grp + ' -Ignore warning if character is not needed-')

                    else:
                            self.logger.warning('Select namespace for snorri!')

                if iterator == 4:

                    if ns_snorri != self.optionMenu_default_value:

                        tmp_con_grp = ns_snorri + str(self.follow_sources[1])

                        if pm.objExists(tmp_con_grp):

                            pm.parentConstraint(tmp_con_grp, self.namespace_tankard + obj, maintainOffset = True)

                        else:
                            self.logger.warning('Source not found: ' + tmp_con_grp + ' -Ignore warning if character is not needed-')

                if iterator == 5:

                    if ns_helga != self.optionMenu_default_value:

                        self.logger.debug('NAMESPACE NEW: ' + ns_helga)

                        tmp_con_grp = ns_helga + str(self.follow_sources[0])

                        if pm.objExists(tmp_con_grp):

                            pm.parentConstraint(tmp_con_grp, self.namespace_tankard + obj, maintainOffset = True)

                        else:
                            self.logger.warning('Source not found: ' + tmp_con_grp + ' -Ignore warning if character is not needed-')
                    else:
                            self.logger.warning('Select namespace for helga!')

                if iterator == 6:

                    if ns_helga != self.optionMenu_default_value:

                        self.logger.debug('NAMESPACE NEW: ' + ns_helga)

                        tmp_con_grp = ns_helga + str(self.follow_sources[1])

                        if pm.objExists(tmp_con_grp):

                            pm.parentConstraint(tmp_con_grp, self.namespace_tankard + obj, maintainOffset = True)

                        else:
                            self.logger.warning('Source not found: ' + tmp_con_grp + ' -Ignore warning if character is not needed-')

                '''
                for iterator, obj in enumerate(self.follow_values):

                    if obj == tmp_value:

                        if iterator == 0:
                            self.logger.debug('world - no constraint needed!')

                        else:

                            if pm.objExists(self.follow_sources[iterator]):

                                pm.parentConstraint(self.follow_sources[iterator], tmp_con_grp, maintainOffset = True)

                            else:

                                self.logger.warning('Source not found: ' + self.follow_sources[iterator] +
                                                    ' -Ignore warning if character is not needed-')

                    if iterator == len(self.follow_values):

                        self.logger.warning('PS value not recognized!')

                '''

                self.logger.debug('DONE - setting constraint')

        pm.select(self.namespace_tankard + self.root_obj_tankard)

        self.logger.debug('DONE - set_constraints_tankard()')

    def switch_PS_tankard(self, x):

        self.logger.debug('--- switch_PS_tankard()')

        tmp_sel = pm.ls(sl = True)
        self.logger.debug('selection: ' + str(tmp_sel))
        
        if tmp_sel[0] != (self.namespace_tankard + self.root_obj_tankard):

            pm.warning('Select root controller of initialized tankard or initialize selected!')

        else:

            sel_val = pm.optionMenu('optionMenu_tankard', query = True, value = True)
            sel_item = pm.optionMenu('optionMenu_tankard', query = True, select = True)
            
            self.logger.debug(sel_val)
            self.logger.debug(sel_item)

            if sel_item == 1:

                pm.warning('Select parent space!')
                return

            tmp_oldTrans = pm.xform(self.switch_obj_tankard, ws = 1, q = 1, t = 1)
            tmp_oldRot = pm.xform(self.switch_obj_tankard, ws = 1, q = 1, ro = 1)
            self.logger.debug(tmp_oldTrans)

            currentTime = pm.currentTime()
            autoKeyState = pm.autoKeyframe(q = True, state = True)

            self.logger.debug(currentTime)
            self.logger.debug(autoKeyState)

            if autoKeyState:
                pm.autoKeyframe(state = 0)

            pm.setKeyframe(self.switch_obj_tankard, time = currentTime - 1)
            pm.setKeyframe(self.switch_attr_tankard, time = currentTime - 1)
            
            self.logger.debug('---if')

            for iterator, obj in enumerate(self.follow_values):
                if sel_val == obj:
                    pm.setAttr(self.switch_attr_tankard, iterator)

            tmp_trans = pm.xform(self.switch_obj_tankard, ws = 1, q = 1, t = 1)
            tmp_rot = pm.xform(self.switch_obj_tankard, ws = 1, q = 1, ro = 1)
            self.logger.debug(tmp_trans)

            pm.xform(self.switch_obj_tankard, ws = 1, t = tmp_oldTrans)
            pm.xform(self.switch_obj_tankard, ws = 1, ro = tmp_oldRot)        

            tmp_trans = pm.xform(self.switch_obj_tankard, ws=1, q=1, t=1)
            self.logger.debug(tmp_trans)

            pm.setKeyframe(self.switch_obj_tankard, time = currentTime)
            pm.setKeyframe(self.switch_attr_tankard, time = currentTime)
            
            if autoKeyState:
                pm.autoKeyframe(state = 1)

        self.logger.debug('--- DONE: switch(): ')


    def select_switch_obj_tankard(self, x):

        self.logger.debug('--- select_switch_obj_tankard()')

        tmp_sel = pm.ls(sl = True)
        self.logger.debug('selection: ' + str(tmp_sel))

        if len(tmp_sel) != 0:
            if tmp_sel[0] == (self.namespace_tankard + self.root_obj_tankard):

                pm.select(self.switch_obj_tankard)
            else:
                pm.warning('Select root controller of initialized tankard or initialize selected!')

        else:
            pm.warning('Select root controller of initialized tankard or initialize selected!')