

"""
renderthreads_render
==========================================

Module that handles the actual command
line rendering in Nuke.
"""


# Import
# ------------------------------------------------------------------
#python
import sys
import os
import multiprocessing
import subprocess
import logging
import threading
# PySide
from PySide import QtGui
from PySide import QtCore


# Import variable
do_reload = True

# renderthreads

# lib

# renderthreads_globals
import renderthreads_globals
if(do_reload):
    reload(renderthreads_globals)

# renderthreads_logging
import renderthreads_logging
if(do_reload):
    reload(renderthreads_logging)


# Globals
# ------------------------------------------------------------------


# RenderCommand
# ------------------------------------------------------------------
class RenderCommand(QtCore.QObject):
    """
    RenderCommand class that handles the commandline process.
    """

    # Signals
    # ------------------------------------------------------------------
    task_done = QtCore.Signal()

    # Creation and Initialization
    # ------------------------------------------------------------------
    def __new__(cls, *args, **kwargs):
        """
        RenderCommand instance factory.
        """

        # render_command_instance
        render_command_instance = super(RenderCommand, cls).__new__(cls, args, kwargs)

        return render_command_instance

    
    def __init__(self, command, timeout = 60):
        """
        Customize RenderCommand instance.
        Parameter timeout is in seconds NOT in ms.
        """

        # super and objectName
        # ------------------------------------------------------------------
        # parent_class
        self.parent_class = super(RenderCommand, self)
        self.parent_class.__init__()

        self.setObjectName(self.__class__.__name__)

        # instance variables
        # ------------------------------------------------------------------

        #command
        self.command = command
        #timeout
        self.timeout = timeout

        #process
        self.process = None
        #enabled
        self.enabled = True

        # logger
        self.logger = renderthreads_logging.get_logger(self.__class__.__name__)


    # Operator overrides
    # ------------------------------------------------------------------
    def __call__(self):
        """()"""

        # run
        self.run()

    # Methods
    # ------------------------------------------------------------------

    def run(self):
        """
        Method to start timed process.
        """

        # not enabled
        if not (self.enabled):

            # notify gui
            self.task_done.emit()

            # return 0 (0 being the code for "executed properly")
            return 0

        # import
        import os
        import subprocess
        import logging
        import threading
        
        
        def target():
            """
            Target method to do the actual work.
            Wrapped by thread that terminates on timeout.
            """

            # log
            self.logger.debug(self.command)

            # env_dict
            env_dict = os.environ.copy()

            # process
            self.process = subprocess.Popen('{0}'.format(self.command),
                                            env = env_dict,
                                            creationflags = subprocess.CREATE_NEW_CONSOLE)

            # communicate
            self.process.communicate()

            
        # thread
        thread = threading.Thread(target = target)
        # start
        thread.start()
        # wait for timeout
        thread.join(self.timeout)
        
        # on timeout
        if(thread.is_alive()):

            # log
            self.logger.debug('Terminating process')

            # terminate process
            self.process.terminate()
            
            #finish thread
            thread.join()

        # notify gui
        self.task_done.emit()

        #exitcode
        exitcode = self.process.returncode
        return exitcode


    # Getter & Setter
    # ------------------------------------------------------------------

    def get_enabled(self):
        """
        Return self.enabled.
        """

        return self.enabled

    @QtCore.Slot(bool)
    def set_enabled(self, value):
        """
        Set self.enabled.
        """

        self.enabled = value
