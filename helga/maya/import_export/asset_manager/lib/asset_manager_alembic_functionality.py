

"""
asset_manager_alembic_functionality
==========================================

AssetManager Alembic functionality. This module handles the export
functionality via ALembic from Maya.
"""




#Import
#------------------------------------------------------------------
#python
import subprocess
import logging
#PySide
from PySide import QtGui
from PySide import QtCore
#maya
import pymel.core as pm




#Import variable
do_reload = True

#helga

#global_variables
from helga.general.setup.global_variables import global_variables
if(do_reload):reload(global_variables)

#global_functions
from helga.general.setup.global_functions import global_functions
if(do_reload):reload(global_functions)










#Globals
#------------------------------------------------------------------

#FLAG_ONLY_ATTR
FLAG_ONLY_ATTR = '"flag_only"'

#ALEMBIC_OPTIONS_DICT
ALEMBIC_OPTIONS_DICT = {'help' : FLAG_ONLY_ATTR,
                        'preRollStartFrame' : 0.0,
                        'dontSkipUnwrittenFrames' : FLAG_ONLY_ATTR,
                        'verbose' : FLAG_ONLY_ATTR}

#ALEMBIC_OPTIONS_ENABLED_DICT
ALEMBIC_OPTIONS_ENABLED_DICT = {'help_enabled' : False,
                                'preRollStartFrame_enabled' : True,
                                'dontSkipUnwrittenFrames_enabled' : True,
                                'verbose_enabled' : True}

#ALEMBIC_JOB_ARG_FLAGS_DICT
ALEMBIC_JOB_ARG_FLAGS_DICT = {'attr' : None,
                                'attrPrefix' : None,
                                'eulerFilter' : FLAG_ONLY_ATTR,
                                'file' : None,
                                'frameRange' : None,
                                'frameRelativeSample' : 0.0,
                                'noNormals' : FLAG_ONLY_ATTR,
                                'renderableOnly' : FLAG_ONLY_ATTR,
                                'root' : None,
                                'step' : 1.0,
                                'selection' : FLAG_ONLY_ATTR,
                                'stripNamespaces' : FLAG_ONLY_ATTR,
                                'userAttr' : None,
                                'userAttrPrefix' : None,
                                'uvWrite' : FLAG_ONLY_ATTR,
                                'writeColorSets' : FLAG_ONLY_ATTR,
                                'writeFaceSets' : FLAG_ONLY_ATTR,
                                'wholeFrameGeo' : FLAG_ONLY_ATTR,
                                'worldSpace' : FLAG_ONLY_ATTR,
                                'writeVisibility' : FLAG_ONLY_ATTR,
                                'melPerFrameCallback': None,
                                'melPostJobCallback' : None,
                                'pythonPerFrameCallback' : None,
                                'pythonPostJobCallback' : None}

#ALEMBIC_JOB_ARG_FLAGS_ENABLED_DICT
ALEMBIC_JOB_ARG_FLAGS_ENABLED_DICT = {'attr_enabled' : False,
                                        'attrPrefix_enabled' : False,
                                        'eulerFilter_enabled' : False,
                                        'file_enabled' : True,
                                        'frameRange_enabled' : True,
                                        'frameRelativeSample_enabled' : True,
                                        'noNormals_enabled' : False,
                                        'renderableOnly_enabled' : False,
                                        'root_enabled' : True,
                                        'step_enabled' : True,
                                        'selection_enabled' : False,
                                        'stripNamespaces_enabled' : True,
                                        'userAttr_enabled' : False,
                                        'userAttrPrefix_enabled' : False,
                                        'uvWrite_enabled' : True,
                                        'writeColorSets_enabled' : False,
                                        'writeFaceSets_enabled' : False,
                                        'wholeFrameGeo_enabled' : False,
                                        'worldSpace_enabled' : True,
                                        'writeVisibility_enabled' : True,
                                        'melPerFrameCallback_enabled': False,
                                        'melPostJobCallback_enabled' : False,
                                        'pythonPerFrameCallback_enabled' : False,
                                        'pythonPostJobCallback_enabled' : False}


#ALEMBIC_ATTR_DICT
ALEMBIC_ATTR_DICT = reduce(lambda a, b: dict(a, **b), (ALEMBIC_OPTIONS_DICT,
                                                        ALEMBIC_OPTIONS_ENABLED_DICT,
                                                        ALEMBIC_JOB_ARG_FLAGS_DICT, 
                                                        ALEMBIC_JOB_ARG_FLAGS_ENABLED_DICT))



#Function factories
#------------------------------------------------------------------

def getter_function_factory(attr_name):
    """
    Return getter function based on input string
    """

    def new_func(*args, **kwargs):
        """
        Getter function
        """

        print('New getter func start')

        self = args[0]

        value = getattr(self, attr_name)

        print('New getter func end')

        return value

    return new_func


def setter_function_factory(attr_name):
    """
    Return setter function based on input string
    """

    def new_func(*args, **kwargs):
        """
        Getter function
        """

        print('New setter func start')

        self = args[0]
        value = args[1]

        setattr(self, attr_name, value)

        print('New setter func end')

    return new_func


def print_function_factory(attr_name):
    """
    Return print function based on input string
    """

    def new_func(*args, **kwargs):
        """
        Print function
        """

        print('New print func start')

        self = args[0]

        print(getattr(self, attr_name))

        print('New print func end')

    return new_func








#MetaAssetManagerAlembicFunctionality class
#------------------------------------------------------------------
class MetaAssetManagerAlembicFunctionality(type(QtCore.QObject)):
    """
    MetaAssetManagerAlembicFunctionality is the meta class for AssetManagerAlembicFunctionality.
    It customizes the class members at creation to add setter/getter methods for all
    ALembic export parameter.
    """

    def __new__(meta, cls_name, base_tuple, attr_dict):
        """
        Return new class object.
        """

        #logger
        logger = logging.getLogger(meta.__name__)
        logger.setLevel(logging.DEBUG)


        #iterate and create getter and setter functions
        for attr_name, default_value in ALEMBIC_ATTR_DICT.iteritems():


            #attribute
            #------------------------------------------------------------------
            
            #getter_name
            getter_name = 'get_'+attr_name
            #get
            attr_dict[getter_name] = getter_function_factory(attr_name)
            #log
            logger.debug('Added getter {0} for attr: {1}'.format(getter_name, attr_name))
            
            #setter_name
            setter_name = 'set_'+attr_name
            #set
            attr_dict[setter_name] = setter_function_factory(attr_name)
            #log
            logger.debug('Added setter {0} for attr: {1}'.format(setter_name, attr_name))

            #printer_name
            printer_name = 'print_'+attr_name
            #set
            attr_dict[printer_name] = print_function_factory(attr_name)
            #log
            logger.debug('Added printer {0} for attr: {1}'.format(printer_name, attr_name))

        

        #meta_class_parent
        meta_class_parent = super(MetaAssetManagerAlembicFunctionality, meta)

        #return
        return meta_class_parent.__new__(meta, cls_name, base_tuple, attr_dict)











#AssetManagerAlembicFunctionality class
#------------------------------------------------------------------
class AssetManagerAlembicFunctionality(QtCore.QObject):
    """
    AssetManagerAlembicFunctionality class.
    """

    __metaclass__ = MetaAssetManagerAlembicFunctionality


    #Signals
    #------------------------------------------------------------------

    sgnl_set_help_enabled = QtCore.Signal(bool)

    sgnl_set_preRollStartFrame = QtCore.Signal(float)
    sgnl_set_preRollStartFrame_enabled = QtCore.Signal(bool)

    sgnl_set_dontSkipUnwrittenFrames_enabled = QtCore.Signal(bool)
    sgnl_set_verbose_enabled = QtCore.Signal(bool)

    sgnl_set_attr = QtCore.Signal(str)
    sgnl_set_attr_enabled = QtCore.Signal(bool)

    sgnl_set_attrPrefix = QtCore.Signal(str)
    sgnl_set_attrPrefix_enabled = QtCore.Signal(bool)

    sgnl_set_eulerFilter_enabled = QtCore.Signal(bool)

    sgnl_set_frameRelativeSample = QtCore.Signal(float)
    sgnl_set_frameRelativeSample_enabled = QtCore.Signal(bool)

    sgnl_set_noNormals_enabled = QtCore.Signal(bool)

    sgnl_set_renderableOnly_enabled = QtCore.Signal(bool)

    sgnl_set_step = QtCore.Signal(float)
    sgnl_set_step_enabled = QtCore.Signal(bool)

    sgnl_set_selection_enabled = QtCore.Signal(bool)

    sgnl_set_stripNamespaces_enabled = QtCore.Signal(bool)

    sgnl_set_userAttr = QtCore.Signal(str)
    sgnl_set_userAttr_enabled = QtCore.Signal(bool)

    sgnl_set_userAttrPrefix = QtCore.Signal(str)
    sgnl_set_userAttrPrefix_enabled = QtCore.Signal(bool)

    sgnl_set_uvWrite_enabled = QtCore.Signal(bool)

    sgnl_set_writeColorSets_enabled = QtCore.Signal(bool)

    sgnl_set_writeFaceSets_enabled = QtCore.Signal(bool)

    sgnl_set_wholeFrameGeo_enabled = QtCore.Signal(bool)

    sgnl_set_worldSpace_enabled = QtCore.Signal(bool)

    sgnl_set_writeVisibility_enabled = QtCore.Signal(bool)



    def __new__(cls, *args, **kwargs):
        """
        AssetManagerAlembicFunctionality instance factory.
        """

        #asset_manager_alembic_functionality_instance
        asset_manager_alembic_functionality_instance = super(AssetManagerAlembicFunctionality, cls).__new__(cls, args, kwargs)

        return asset_manager_alembic_functionality_instance

    
    def __init__(self, logging_level = logging.DEBUG):
        """
        Customize instance.
        """

        #super
        self.parent_class = super(AssetManagerAlembicFunctionality, self)
        self.parent_class.__init__()


        
        #logger
        #------------------------------------------------------------------
        #logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logging_level = logging_level
        self.logger.setLevel(self.logging_level)


        
        #instance variables
        #------------------------------------------------------------------

        #alembic_options_dict
        self.alembic_options_dict = {}
        #alembic_options_enabled_dict
        self.alembic_options_enabled_dict = {}
        #alembic_job_arg_flags_dict
        self.alembic_job_arg_flags_dict = {}
        #alembic_job_arg_flags_enabled_dict
        self.alembic_job_arg_flags_enabled_dict = {}

        #create and store instance attrs for dicts
        self.create_and_store_instance_attrs(ALEMBIC_OPTIONS_DICT, 'self.alembic_options_dict')
        self.create_and_store_instance_attrs(ALEMBIC_OPTIONS_ENABLED_DICT, 'self.alembic_options_enabled_dict')
        self.create_and_store_instance_attrs(ALEMBIC_JOB_ARG_FLAGS_DICT, 'self.alembic_job_arg_flags_dict')
        self.create_and_store_instance_attrs(ALEMBIC_JOB_ARG_FLAGS_ENABLED_DICT, 'self.alembic_job_arg_flags_enabled_dict')

        #Startup
        #------------------------------------------------------------------

        #connect_signals
        self.connect_signals()



    def connect_signals(self):
        """
        No ui here. Connect signals with methods.
        """

        #sgnl_set_help_enabled
        self.sgnl_set_help_enabled.connect(self.set_help_enabled)

        
        #sgnl_set_preRollStartFrame
        self.sgnl_set_preRollStartFrame.connect(self.set_preRollStartFrame)
        #sgnl_set_preRollStartFrame_enabled
        self.sgnl_set_preRollStartFrame_enabled.connect(self.set_preRollStartFrame_enabled)

        
        #sgnl_set_dontSkipUnwrittenFrames_enabled
        self.sgnl_set_dontSkipUnwrittenFrames_enabled.connect(self.set_dontSkipUnwrittenFrames_enabled)

        
        #sgnl_set_verbose_enabled
        self.sgnl_set_verbose_enabled.connect(self.set_verbose_enabled)

        
        #sgnl_set_attr
        self.sgnl_set_attr.connect(self.set_attr)
        #sgnl_set_attr_enabled
        self.sgnl_set_attr_enabled.connect(self.set_attr_enabled)

        
        #sgnl_set_attrPrefix
        self.sgnl_set_attrPrefix.connect(self.set_attrPrefix)
        #sgnl_set_attrPrefix_enabled
        self.sgnl_set_attrPrefix_enabled.connect(self.set_attrPrefix_enabled)

        
        #sgnl_set_eulerFilter_enabled
        self.sgnl_set_eulerFilter_enabled.connect(self.set_eulerFilter_enabled)


        #sgnl_set_frameRelativeSample
        self.sgnl_set_frameRelativeSample.connect(self.set_frameRelativeSample)
        #sgnl_set_frameRelativeSample_enabled
        self.sgnl_set_frameRelativeSample_enabled.connect(self.set_frameRelativeSample_enabled)

        
        #sgnl_set_noNormals_enabled
        self.sgnl_set_noNormals_enabled.connect(self.set_noNormals_enabled)


        #sgnl_set_renderableOnly_enabled
        self.sgnl_set_renderableOnly_enabled.connect(self.set_renderableOnly_enabled)


        #sgnl_set_step
        self.sgnl_set_step.connect(self.set_step)
        #sgnl_set_step_enabled
        self.sgnl_set_step_enabled.connect(self.set_step_enabled)


        #sgnl_set_selection_enabled
        self.sgnl_set_selection_enabled.connect(self.set_selection_enabled)


        #sgnl_set_stripNamespaces_enabled
        self.sgnl_set_stripNamespaces_enabled.connect(self.set_stripNamespaces_enabled)


        #sgnl_set_userAttr
        self.sgnl_set_userAttr.connect(self.set_userAttr)
        #sgnl_set_userAttr_enabled
        self.sgnl_set_userAttr_enabled.connect(self.set_userAttr_enabled)


        #sgnl_set_userAttrPrefix
        self.sgnl_set_userAttrPrefix.connect(self.set_userAttrPrefix)
        #sgnl_set_userAttrPrefix_enabled
        self.sgnl_set_userAttrPrefix_enabled.connect(self.set_userAttrPrefix_enabled)


        #sgnl_set_uvWrite_enabled
        self.sgnl_set_uvWrite_enabled.connect(self.set_uvWrite_enabled)


        #sgnl_set_writeColorSets_enabled
        self.sgnl_set_writeColorSets_enabled.connect(self.set_writeColorSets_enabled)


        #sgnl_set_writeFaceSets_enabled
        self.sgnl_set_writeFaceSets_enabled.connect(self.set_writeFaceSets_enabled)


        #sgnl_set_wholeFrameGeo_enabled
        self.sgnl_set_wholeFrameGeo_enabled.connect(self.set_wholeFrameGeo_enabled)

        #sgnl_set_worldSpace_enabled
        self.sgnl_set_worldSpace_enabled.connect(self.set_worldSpace_enabled)

        #sgnl_set_writeVisibility_enabled
        self.sgnl_set_writeVisibility_enabled.connect(self.set_writeVisibility_enabled)
        
        
    def create_and_store_instance_attrs(self, attr_dict, instance_attr_dict_variable_name):
        """
        Create and store instance attributes
        """

        #alembic vars
        for attr_name, default_value in attr_dict.iteritems():

            #create attr
            #------------------------------------------------------------------
            
            #attr_name

            #code_object
            code_object = compile('self.{0} = {1}'.format(attr_name, default_value), 
                                    '<string>', 
                                    'exec')
            #exec
            exec(code_object)

            #log
            self.logger.debug('Created instance attr.: {0}'.format(attr_name))


            


            #add to instance_attr_dict
            #------------------------------------------------------------------

            #code_object
            code_object = compile('{0}["{1}"] = self.{1}'.format(instance_attr_dict_variable_name, attr_name), 
                                    '<string>',
                                    'exec')
            #exec
            exec(code_object)






    #Argument Value Formatter
    #------------------------------------------------------------------

    def node_list_to_abc_root_string(self, node_name_list):
        """
        Convert node name list ['node_name', 'node_name'] to abc root string
        of this form '-root node_name -root node_name '.
        Pay attention to the whitespace at the end.
        """

        #node_list_string
        node_list_string = ''
        #iterate
        for index, node_name in enumerate(node_name_list):
            
            #first element
            if not (index):
                
                #no -root no whitespace at start
                node_list_string += '{0}'.format(node_name)

                #add whitespace if len of list > 1
                if (len(node_name_list) > 1):
                    node_list_string += ' '
                

            #last element
            elif (index == len(node_name_list) - 1):
                
                #no whitespace at end
                node_list_string += '-root {0}'.format(node_name)
                
            
            #normal
            else:
                #append string (with whitespace at end)
                node_list_string += '-root {0} '.format(node_name)

        return node_list_string


    def float_list_to_framerange_string(self, float_list):
        """
        Convert float list of type [float, float] to string
        of type '1.0 10.0'
        """

        #framerange_string
        framerange_string = '{0} {1}'.format(float_list[0], float_list[1])

        return framerange_string




    #Maya
    #------------------------------------------------------------------

    def string_to_list(self, string_to_convert):
        """
        Convert given string to a list
        """

        return [str(string_to_convert)]


    @QtCore.Slot()
    def get_export_command(self):
        """
        Build and return Alembic export command. The command syntax is MEL.
        """

        #abc_command
        abc_command = 'AbcExport'

        
        #Options
        #------------------------------------------------------------------

        #attr in options dict
        for attr_name in sorted(self.alembic_options_dict.keys()):

            #arg enabled?
            if(eval('self.get_{0}_enabled()'.format(attr_name))):

                #attr_value
                attr_value = eval('self.get_{0}()'.format(attr_name))
                
                #arg has no value / flag only
                if (attr_value == "flag_only"):

                    #append
                    abc_command = abc_command +' ' +'-' +attr_name

                #else append attr name and value
                else:

                    #append
                    abc_command = abc_command +' ' +'-' +attr_name +' ' +str(attr_value)

        
        
        #jobArg
        #------------------------------------------------------------------

        #append
        abc_command = abc_command +' ' +'-' +'jobArg' +' ' +'"'



        #jobArg Flags
        #------------------------------------------------------------------

        #first_flag
        first_flag = True

        #iterate
        for attr_name in sorted(self.alembic_job_arg_flags_dict.keys()):

            #arg enabled?
            if(eval('self.get_{0}_enabled()'.format(attr_name))):

                #attr_value
                attr_value = eval('self.get_{0}()'.format(attr_name))
                
                #attr has no value / flag only
                if (attr_value == "flag_only"):

                    #first element no space upfront
                    if (first_flag):
                        
                        #append
                        abc_command = abc_command +'-' +attr_name
                        #first_flag
                        first_flag = False

                    #else
                    else:
                        
                        #append
                        abc_command = abc_command +' ' +'-' +attr_name

                #attr has value
                else:

                    #first element no space upfront
                    if (first_flag):
                        
                        #append
                        abc_command = abc_command +'-' +attr_name +' ' +str(attr_value)
                        #first_flag
                        first_flag = False

                    #else
                    else:

                        #append
                        abc_command = abc_command +' ' +'-' +attr_name +' ' +str(attr_value)





        #append
        abc_command = abc_command +'"'

        #print .abc cmd
        print('{0}'.format(abc_command))

        #return
        return abc_command


    def export(self, node_name_list, frameRange_list, file_string):
        """
        Export alembic file
        """

        #set user parameter
        #------------------------------------------------------------------

        #root
        root_value = self.node_list_to_abc_root_string(node_name_list)
        self.set_root(root_value)

        #frameRange
        framerange_value = self.float_list_to_framerange_string(frameRange_list)
        self.set_frameRange(framerange_value)

        #file
        self.set_file(file_string)


        #export
        #------------------------------------------------------------------

        #abc_command
        abc_command = self.get_export_command()
        
        #log
        self.logger.debug('AbcExport command: {0}'.format(abc_command))

        #export
        pm.mel.eval(abc_command)


