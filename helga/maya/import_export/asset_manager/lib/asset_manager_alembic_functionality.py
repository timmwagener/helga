

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

#asset_manager

#asset_manager_functionality
from lib import asset_manager_functionality
if(do_reload):reload(asset_manager_functionality)








#Globals
#------------------------------------------------------------------

#ALEMBIC_ATTR_DICT
ALEMBIC_ATTR_DICT = {'attr' : None,
                        'attrPrefix' : None,
                        'eulerFilter' : '"is_flag"',
                        'file' : None,
                        'frameRange' : None,
                        'frameRelativeSample' : None,
                        'noNormals' : '"is_flag"',
                        'renderableOnly' : '"is_flag"',
                        'root' : None,
                        'step' : None,
                        'selection' : None,
                        'stripNamespaces' : None,
                        'userAttr' : None,
                        'userAttrPrefix' : None,
                        'uvWrite' : None,
                        'writeColorSets' : None,
                        'writeFaceSets' : None,
                        'wholeFrameGeo' : None,
                        'worldSpace' : None,
                        'writeVisibility' : None,
                        'melPerFrameCallback': None,
                        'melPostJobCallback' : None,
                        'pythonPerFrameCallback' : None,
                        'pythonPostJobCallback' : None,
                        'test_attribute' : 5}






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
class MetaAssetManagerAlembicFunctionality(type):
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



            #attribute_enabled
            #------------------------------------------------------------------
            
            #getter_name
            getter_name = 'get_' +attr_name +'_enabled'
            #get
            attr_dict[getter_name] = getter_function_factory(attr_name +'_enabled')
            #log
            logger.debug('Added getter {0} for attr: {1}'.format(getter_name, attr_name +'_enabled'))
            
            #setter_name
            setter_name = 'set_'+attr_name +'_enabled'
            #set
            attr_dict[setter_name] = setter_function_factory(attr_name +'_enabled')
            #log
            logger.debug('Added setter {0} for attr: {1}'.format(setter_name, attr_name +'_enabled'))

            #printer_name
            printer_name = 'print_' +attr_name +'_enabled'
            #set
            attr_dict[printer_name] = print_function_factory(attr_name +'_enabled')
            #log
            logger.debug('Added printer {0} for attr: {1}'.format(printer_name, attr_name +'_enabled'))

        

        #meta_class_parent
        meta_class_parent = super(MetaAssetManagerAlembicFunctionality, meta)

        #return
        return meta_class_parent.__new__(meta, cls_name, base_tuple, attr_dict)











#AssetManagerAlembicFunctionality class
#------------------------------------------------------------------
class AssetManagerAlembicFunctionality(object):
    """
    AssetManagerAlembicFunctionality class.
    """

    __metaclass__ = MetaAssetManagerAlembicFunctionality

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

        #maya_functionality
        self.maya_functionality = asset_manager_functionality.AssetManagerFunctionality()

        #alembic vars
        for attr_name, default_value in ALEMBIC_ATTR_DICT.iteritems():
            
            #attr_name

            #code_object
            code_object = compile("self.{0} = {1}".format(attr_name, default_value), 
                                    '<string>', 
                                    'exec')
            #exec
            exec(code_object)

            #log
            self.logger.debug('Created instance attr.: {0}'.format(attr_name))


            #attr_name_enabled

            #code_object
            code_object = compile("self.{0} = {1}".format(attr_name +'_enabled', default_value), 
                                    '<string>', 
                                    'exec')
            #exec
            exec(code_object)

            #log
            self.logger.debug('Created instance attr.: {0}'.format(attr_name +'_enabled'))
        
        
        




    #Maya
    #------------------------------------------------------------------

    def node_list_to_abc_root_string(self, node_list):
        """
        Convert node name list ['node_name', 'node_name'] to abc root string
        of this form '-root node_name -root node_name '.
        Pay attention to the whitespace at the end.
        """

        #node_list_string
        node_list_string = ''
        #iterate
        for index, node_name in enumerate(node_list):
            #last element
            if (index == len(node_list) - 1):
                #no whitespace at end
                node_list_string += '-root {0}'.format(node_name)
                continue
            
            #append string (with whitespace at end)
            node_list_string += '-root {0} '.format(node_name)

        return node_list_string


    def string_to_list(self, string_to_convert):
        """
        Convert given string to a list
        """

        return [str(string_to_convert)]

    
    def export(self, node_list = 'Test', abc_path = 'C:/Huso/sick', step = 1):
        """
        Export each node in node_list as abc file to abc_path.
        """

        #node_list convenience convert (allows to pass in node name instead of list)
        if (type(node_list) is str or
            type(node_list) is unicode):
            node_list = self.string_to_list(node_list)

        #node_list_string
        node_list_string = self.node_list_to_abc_root_string(node_list)
        
        #abc_command
        abc_command = 'AbcExport -j "-frameRange {0} -step {1} -ws {2} -file {3}"'.format(self.frameRange,
                                                                                            step,
                                                                                            node_list_string, 
                                                                                            abc_path)

        #log
        self.logger.debug('AbcExport command: {0}'.format(abc_command))

        #export
        pm.mel.eval(abc_command)


