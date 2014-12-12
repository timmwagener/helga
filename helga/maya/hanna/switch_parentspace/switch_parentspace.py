


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

        self.follow_sources = ['', 'ulfbert_rig:L_Arm_Wrist_ToParent_Ctrl',
                                   'ulfbert_rig:R_Arm_Wrist_ToParent_Ctrl',
                                   'snorri_rig:L_Arm_Wrist_ToParent_Ctrl',
                                   'snorri_rig:R_Arm_Wrist_ToParent_Ctrl',
                                   'helga_rig:L_Arm_Wrist_ToParent_Ctrl',
                                   'helga_rig:R_Arm_Wrist_ToParent_Ctrl']

        self.con_grp_tankard = 'grp_CON_PS_DONT_TOUCH'


    def run(self):

        self.logger.debug('--- run()')

        global win

        if pm.window(self.window_name, q = True, ex = True):
            pm.deleteUI(self.window_name)

        if pm.windowPref(self.window_name, q = True, ex = True):
            pm.windowPref(self.window_name, r = True)

        win = pm.window(self.window_name, title = self.window_name, w = 150, h = 100,
                        te = 210, le = 70)

        layout1 = pm.rowColumnLayout(numberOfColumns = 1, cw = [(1,100)])


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

        pm.menuItem( label = '-select-')
        for obj in self.follow_values:
            pm.menuItem( label = obj)
        pm.text(label = '')

        pm.button('b_switch_PS_tankard', label = "-", c = self.switch_PS_tankard, enable = False)
        pm.text(label = '')

        pm.button('b_select_switch_obj_tankard', label = "-", c = self.select_switch_obj_tankard, enable = False)
        pm.text(label = '')

        win.show()


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


    def set_constraints_tankard(self):

        self.logger.debug('--- set_constraints_tankard()')

        children = pm.listRelatives(self.namespace_tankard + self.con_grp_tankard, c = True, type = 'transform')

        self.logger.debug(children)
        self.logger.debug(len(children))

        for child in children:

            pm.select(child)
            tmp_con_grp =  pm.pickWalk(type = 'nodes', direction = 'down')[0]

            self.logger.debug(tmp_con_grp)

            tmp_constraints = pm.listRelatives(tmp_con_grp, c = True, type = 'parentConstraint')
            
            chunks = child.split('_')
            tmp_value = chunks[-1]
            self.logger.debug(tmp_value)

            self.logger.debug(tmp_constraints)

            if len(tmp_constraints) != 0:

                self.logger.debug('constraint set')

            else:

                self.logger.debug('no constraint yet - setting constraint')

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
        
        if tmp_sel[0] != (self.namespace_tankard + self.root_obj_tankard):

            print(tmp_sel[0])
            print(self.namespace_tankard + self.root_obj_tankard)

            pm.warning('Select root controller of initialized tankard or initialize selected!')

        else:
            pm.select(self.switch_obj_tankard)