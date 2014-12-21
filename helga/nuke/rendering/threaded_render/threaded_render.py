


"""
threaded_render module
==========================================

This module offers functionality to render the currently selected
write node in a multithreaded fashion. It divides the global framecount
into parts and starts new nuke instances to render those chunks.

To use it, execute the following:

..code ::

    from helga.nuke.rendering.threaded_render import threaded_render
    reload(threaded_render)
    threaded_render.run()


-----------------------

**Author:** `Timm Wagener <mailto:wagenertimm@gmail.com>`_
*Version:* 0.1
"""






#Imports
#------------------------------------------------------------------

#python
import sys
import os
import multiprocessing
import subprocess
import logging
import threading
#nuke
import nuke











#Globals
#------------------------------------------------------------------
NUKE_PATH = nuke.EXE_PATH
FIRST_FRAME = nuke.root().firstFrame()
LAST_FRAME = nuke.root().lastFrame()
THREADCOUNT = 0
SCRIPTPATH = nuke.root().name()












#TimedExportProcess class
#------------------------------------------------------------------
class TimedExportProcess(object):
    """
    Helper class to run a timed process.
    """

    def __new__(cls, *args, **kwargs):
        """
        TimedExportProcess instance factory.
        """

        #timed_export_process_instance
        timed_export_process_instance = super(TimedExportProcess, cls).__new__(cls, args, kwargs)

        return timed_export_process_instance

    
    def __init__(self,
                    command,
                    env_dict,
                    timeout = 600,
                    logging_level = logging.DEBUG):
        """
        Customize TimedExportProcess instance.
        Parameter timeout is in seconds NOT in ms.
        """

        #instance variables
        #------------------------------------------------------------------

        #command
        self.command = command
        #env_dict
        self.env_dict = env_dict
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


    def run(self):
        """
        Method to start timed process.
        """

        import os
        import subprocess
        import logging
        import threading
        
        def target():
            """
            Target method to do the actual work.
            Wrapped by thread that terminates on timeout.
            """

            #log
            print(self.command)

            #process
            self.process = subprocess.Popen(r'{0}'.format(self.command),
                                        env = self.env_dict,
                                        creationflags = subprocess.CREATE_NEW_CONSOLE)

            
        #thread
        thread = threading.Thread(target = target)
        #start
        thread.start()
        #wait for timeout
        thread.join(self.timeout)
        
        #on timeout
        if(thread.is_alive()):

            #terminate process
            print('Terminating process')
            self.process.terminate()
            
            #finish thread
            thread.join()
        
        #exitcode
        exitcode = self.process.returncode
        self.logger.debug('Process returned with exitcode: {0}'.format(exitcode))

        return exitcode









#Functions
#------------------------------------------------------------------

def threaded_render(first_frame, last_frame, threadcount):
    """
    Start render jobs.
    """
    
    #all cores?
    if (threadcount == 0):

        #threadcount = cpu_count
        threadcount = multiprocessing.cpu_count()


    #write_node_list
    write_node_list = [node for
                            node in 
                            nuke.selectedNodes() if 
                            (node.Class() == 'Write' and 
                            node["disable"].value() == False)]
    #check
    if not(len(write_node_list)):
        
        #log
        print('No write node selected. Please select some write nodes.')
        return

    #write_node
    write_node = write_node_list[0]

    #save script
    nuke.scriptSave()

    #env_dict
    env_dict = os.environ.copy()

    #frame_count
    frame_count = last_frame - first_frame
    #frame_chunk_size
    frame_chunk_size = frame_count // threadcount
    #remainder
    remainder = frame_count % threadcount
    

    
    #thread_list
    thread_list = []

    #iterate threads
    for index in range(threadcount):

        #current_first_frame
        current_first_frame = first_frame + (index * frame_chunk_size)

        #current_last_frame
        current_last_frame = current_first_frame + (frame_chunk_size - 1)

        #last chunk?
        if(index == (threadcount - 1)):

            #current_last_frame
            current_last_frame = current_first_frame + (frame_chunk_size + remainder)
        
        #command
        command = '"{0}" -X {1} -F {2}-{3} -x -V 2 {4}'.format(NUKE_PATH, write_node.name(), current_first_frame, current_last_frame, SCRIPTPATH)

        #target
        target = get_export_closure(command, env_dict)
        #append to thread_list
        thread_list.append(threading.Thread(target = target))


    #iterate and start
    for thread in thread_list:

        #start
        thread.start()


def threaded_render_gui():
    """
    Create GUI to enter basic info.
    """

    #pnl_render_gui
    pnl_render_gui = nuke.Panel("Batch Render Threads")
    pnl_render_gui.addSingleLineInput("First Frame:", FIRST_FRAME)
    pnl_render_gui.addSingleLineInput("Last Frame:", LAST_FRAME)
    pnl_render_gui.addSingleLineInput("Threads:", find_optimal_thread_count(FIRST_FRAME, LAST_FRAME))
            
    pnl_render_gui.addButton("Cancel")
    pnl_render_gui.addButton("OK")
    pnl_render_gui.setWidth(200)
    result = pnl_render_gui.show()

    
    #start
    if result == 1:

        #variables
        first_frame = int(pnl_render_gui.value("First Frame:"))
        last_frame = int(pnl_render_gui.value("Last Frame:"))
        threadcount = int(pnl_render_gui.value("Threads:"))

        #threaded_render
        threaded_render(first_frame, last_frame, threadcount)
        

    #cancel
    else:
        print "Canceled!"


def find_optimal_thread_count(first_frame, last_frame):
    """
    Return optimal thread count
    """

    #cpu_count
    cpu_count = multiprocessing.cpu_count()

    #frame_count
    frame_count = last_frame - first_frame

    #thread_count
    thread_count = cpu_count

    #remainder
    remainder = frame_count % thread_count

    #iterate until modulo 0
    for index in range(cpu_count):

        #current_thread_count
        current_thread_count = cpu_count - index

        #current_remainder
        current_remainder = frame_count % current_thread_count

        #current_remainder < remainder
        if (current_remainder < remainder):

            #remainder
            remainder = current_remainder

            #thread_count
            thread_count = current_thread_count

    #return
    return thread_count


def get_export_closure(command, env_dict, timeout = 600):
        """
        Return a function object.
        """

        def export_function():
            """
            Function object to be returned and
            put to queue to be called by threads run().
            """

            #timed_process_instance
            timed_process_instance = TimedExportProcess(command, env_dict, timeout)
            timed_process_instance.run()
            

        return export_function


def run():
    """
    Run
    """

    #threaded_render_gui
    threaded_render_gui()







#Import Guard
#------------------------------------------------------------------

if(__name__ == '__main__'):

    #run
    threaded_render_gui()