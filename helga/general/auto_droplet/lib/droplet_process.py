

"""
droplet_process
==========================================

Module that holds a DropletProcess object. This object represents a closure
that is added to the queue and picked up by a WorkerThread to be executed.
The process has a timeout limit that can be set.
"""






#Import
#------------------------------------------------------------------
#python
import sys
import subprocess
import logging








#Globals
#------------------------------------------------------------------










#DropletProcess class
#------------------------------------------------------------------
class DropletProcess(object):
    """
    Helper class to run a timed process.
    """

    def __new__(cls, *args, **kwargs):
        """
        DropletProcess instance factory.
        """

        #droplet_process_instance
        droplet_process_instance = super(DropletProcess, cls).__new__(cls, args, kwargs)

        return droplet_process_instance

    
    def __init__(self,
                    droplet_path,
                    file_path,
                    timeout = 120,
                    logging_level = logging.DEBUG):
        """
        Customize DropletProcess instance.
        Parameter timeout is in seconds NOT in ms.
        """

        #instance variables
        #------------------------------------------------------------------

        #droplet_path
        self.droplet_path = droplet_path
        #file_path
        self.file_path = file_path
        #timeout
        self.timeout = timeout
        #process
        self.process = None


        #logger
        #------------------------------------------------------------------
        
        #logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logging_level = logging_level
        self.logger.setLevel(self.logging_level)
        self.logger.handlers = []

        #stream_handler
        stream_handler = logging.StreamHandler(sys.stdout)
        #add
        self.logger.addHandler(stream_handler)


    def run(self):
        """
        Method to start timed process.
        """

        import sys
        import os
        import subprocess
        import logging
        import threading
        
        def target():
            """
            Target method to do the actual work.
            Wrapped by thread that terminates on timeout.
            """
            
            #command
            command = r'"{0}" "{1}"'.format(self.droplet_path, self.file_path)

            #log
            self.logger.debug('Command: {0}'.format(command))
            
            #process
            self.process = subprocess.Popen(r'{0}'.format(command), 
                                        stdout = subprocess.PIPE,
                                        stderr = subprocess.STDOUT)
            
            #stdout_value, stderr_value
            stdout_value, stderr_value = self.process.communicate()


        #thread
        thread = threading.Thread(target = target)
        #start
        thread.start()
        #wait for timeout
        thread.join(self.timeout)
        
        #on timeout
        if(thread.is_alive()):

            #terminate process
            self.logger.debug('Terminating process')
            self.process.terminate()
            
            #finish thread
            thread.join()
        
        #exitcode
        exitcode = self.process.returncode
        self.logger.debug('Process returned with exitcode: {0}'.format(exitcode))

        return exitcode



def get_droplet_closure(droplet_path,
                        file_path,
                        timeout = 120,
                        logging_level = logging.DEBUG):
    """
    Return a function object that does the following when called:

    1. Start subprocess that runs droplet subprocess command.
    2. Wait till process is finished or finishes it when timeout is exceeded.
    """

    def conversion_function():
        """
        Function object to be returned and
        put to queue to be called by threads run().
        """

        #droplet_process_instance
        droplet_process_instance = DropletProcess(droplet_path,
                                                    file_path,
                                                    timeout,
                                                    logging_level)
        droplet_process_instance.run()
        

    return conversion_function