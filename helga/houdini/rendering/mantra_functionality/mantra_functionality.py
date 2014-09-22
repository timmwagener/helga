




#

"""
mantra_functionality
==========================================

Module that offers possibilities to adjust render pathes, rendersettings etc.

-----------------------

**Author:** `Timm Wagener <mailto:wagenertimm@gmail.com>`_
"""







#Import
#------------------------------------------------------------------
#python
import sys
import os
import functools
import logging
import time

#houdini
import hou





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











#MantraFunctionality class
#------------------------------------------------------------------
class MantraFunctionality(object):
    """
    MantraFunctionality
    """


    def __new__(cls, *args, **kwargs):
        """
        MantraFunctionality instance factory.
        """

        #mantra_functionality_instance
        mantra_functionality_instance = super(MantraFunctionality, cls).__new__(cls, args, kwargs)

        return mantra_functionality_instance

    
    def __init__(self):
        """
        Customize instance.
        """

        #super
        self.parent_class = super(MantraFunctionality, self)
        self.parent_class.__init__()


        #instance variables
        #------------------------------------------------------------------
        
        


        #init procedure
        #------------------------------------------------------------------

        









    #Methods
    #------------------------------------------------------------------

    def set_renderpathes_testing(self):
        """
        Set the renderpathes for testing for the selected Mantra nodes.
        """

        print('set_renderpathes_testing')

        #mantra_nodes_list
        mantra_nodes_list = self.get_selected_nodes_of_type(node_type = 'ifd')




    def set_renderpathes(self):
        """
        Set the renderpathes for the selected Mantra nodes.
        This output is ment to be used in comp.
        """

        print('set_renderpathes')



    #Utility Methods
    #------------------------------------------------------------------

    def get_selected_nodes_of_type(self, node_type = None):
        """
        Get list of selected Mantra nodes.
        """

        #node_type None
        if not (node_type):
            #log
            print('No node type given. Returning empty list')
            return []

        #selected_nodes_list
        selected_nodes_list = hou.selectedNodes()

        #matching_nodes_list
        matching_nodes_list = []

        #iterate and append
        for selected_node in selected_nodes_list:

            #selected_node_type
            selected_node_type = selected_node.type().name()

            #type matching
            if (selected_node_type == node_type):

                #append
                matching_nodes_list.append(selected_node)

        
        #return
        return matching_nodes_list




        

        
        
        

        

        



        

    #Test
    #------------------------------------------------------------------

    def dummy_method(self, msg = 'dummy'):
        """
        Dummy method
        """

        #print
        print('{0}'.format(msg))


    









    












#Test
#------------------------------------------------------------------

if (__name__ == '__main__'):

    pass