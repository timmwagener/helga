



"""
convert_functionality
==========================================

Module to handle the conversion with droplets.

-----------------------
"""







#Import
#------------------------------------------------------------------
#python
import sys
import os
import functools
import logging
import subprocess
#PyQt
from PyQt4 import QtGui
from PyQt4 import QtCore


#do_reload
do_reload = True

#threads_functionality
import threads_functionality
if (do_reload): reload(threads_functionality)

#droplet_process
import droplet_process
if (do_reload): reload(droplet_process)













#Globals
#------------------------------------------------------------------
















#ConvertFunctionality class
#------------------------------------------------------------------

class ConvertFunctionality(QtCore.QObject):
    """
    ConvertFunctionality
    """

    #signals
    sgnl_increment_progressbar_range = QtCore.pyqtSignal()
    sgnl_reset_progressbar_range = QtCore.pyqtSignal()


    
    def __init__(self,
                logging_level = logging.DEBUG):
        """
        Initialize ConvertFunctionality instance
        """
        
        #base_class
        self.base_class = super(ConvertFunctionality, self)
        self.base_class.__init__()
        
        
        
        #instance variables
        #------------------------------------------------------------------

        #threads_functionality
        self.threads_functionality = threads_functionality.ThreadsFunctionality()


        
        #logger
        #------------------------------------------------------------------
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logging_level = logging_level
        self.logger.setLevel(self.logging_level)

        #stream_handler
        stream_handler = logging.StreamHandler(sys.stdout)
        #add
        self.logger.addHandler(stream_handler)



        #startup procedure
        #------------------------------------------------------------------

        #setup_threads
        self.setup_threads()
        

    
    #Startup Methods
    #------------------------------------------------------------------

    def setup_threads(self):
        """
        Setup threads.
        """

        #set thread count
        self.threads_functionality.set_thread_count(1)

        #setup threads
        self.threads_functionality.setup_threads()


    
    #Main Method
    #------------------------------------------------------------------

    def convert_check(self, droplet_list, file_list):
        """
        Check if all parms are ok for conversion.
        """

        #droplet_list empty
        if not (droplet_list):
            #log
            self.logger.debug('Droplet list empty. Please add droplets.')
            return False


        #file_list empty
        if not (file_list):
            #log
            self.logger.debug('File list empty. Please add files.')
            return False


        return True



    def convert(self, droplet_list, file_list):
        """
        Convert
        """

        #check
        if not (self.convert_check(droplet_list, file_list)):
            #log
            self.logger.debug('Conversion check failed. Please fix parameters and try again.')
            return False


        #droplet_index
        droplet_index = 0


        #iterate and start
        for file_path in file_list:

            #droplet_path
            droplet_path = droplet_list[droplet_index]

            #droplet_closure
            droplet_closure = droplet_process.get_droplet_closure(droplet_path, file_path)

            #progressbar range signal
            self.sgnl_increment_progressbar_range.emit()

            #add to queue
            self.threads_functionality.add_to_queue(droplet_closure)


            #droplet_index ++
            droplet_index = droplet_index + 1
            if (droplet_index == len(droplet_list)):
                droplet_index = 0


    def stop(self):
        """
        Stop conversion
        """

        #reset
        self.threads_functionality.reset_queue()

        #sgnl_reset_progressbar_range
        self.sgnl_reset_progressbar_range.emit()

            




    #Test Method
    #------------------------------------------------------------------
    
    #test_method
    def test_method(self):
        """
        Test Method
        """

        #log
        self.logger.debug('Test Method')






