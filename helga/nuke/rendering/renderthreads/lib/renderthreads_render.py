

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
    sgnl_task_done = QtCore.Signal()

    # Creation and Initialization
    # ------------------------------------------------------------------
    def __new__(cls, *args, **kwargs):
        """
        RenderCommand instance factory.
        """

        # render_command_instance
        render_command_instance = super(RenderCommand, cls).__new__(cls, args, kwargs)

        return render_command_instance

    
    def __init__(self,
                    command,
                    timeout,
                    display_shell,
                    identifier,
                    priority):
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

        # command
        self.command = command
        # timeout
        self.timeout = timeout
        # display_shell
        self.display_shell = display_shell
        # identifier
        self.identifier = identifier
        # priority
        self.priority = priority

        # process
        self.process = None
        # enabled
        self.enabled = True
        

        # logger
        self.logger = renderthreads_logging.get_logger(self.__class__.__name__)


    # Operator overrides
    # ------------------------------------------------------------------
    def __call__(self):
        """()"""

        # run
        self.run()

    def __cmp__(self, other):
        """Implement all comparison methods"""

        # priority equal
        if (self.priority == other.priority):
            return cmp(self.identifier, other.identifier)
        
        # else
        else:
            return cmp(self.priority, other.priority)
    
    

    # Methods
    # ------------------------------------------------------------------

    def run(self):
        """
        Method to start timed process.
        """

        # not enabled
        if not (self.enabled):

            # notify gui
            self.sgnl_task_done.emit()

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

            # creation_flags
            creation_flags = 0

            # display_shell
            if (self.display_shell):
                creation_flags = subprocess.CREATE_NEW_CONSOLE

            # process
            self.process = subprocess.Popen('{0}'.format(self.command),
                                            env = env_dict,
                                            creationflags = creation_flags)

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
        self.sgnl_task_done.emit()

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

    @QtCore.Slot(str, bool)
    def set_enabled_for_identifier(self, identifier, value):
        """
        Set self.enabled if identifier check
        is successfull.
        """

        # check identifier
        if (self.identifier == identifier):

            # set enabled
            self.enabled = value

    def get_priority(self):
        """
        Return self.priority.
        """

        return self.priority

    @QtCore.Slot(int)
    def set_priority(self, value):
        """
        Set self.priority.
        """

        self.priority = value

    @QtCore.Slot(str, int)
    def set_priority_for_identifier(self, identifier, value):
        """
        Set self.priority if identifier check
        is successfull.
        """

        # check identifier
        if (self.identifier == identifier):

            # set priority
            self.priority = value

    def get_timeout(self):
        """
        Return self.timeout.
        """

        return self.timeout

    @QtCore.Slot(int)
    def set_timeout(self, value):
        """
        Set self.timeout.
        """

        # set
        self.timeout = value

    def get_display_shell(self):
        """
        Return self.display_shell.
        """

        return self.display_shell

    @QtCore.Slot(bool)
    def set_display_shell(self, value):
        """
        Set self.display_shell.
        """

        self.display_shell = value

    def get_identifier(self):
        """
        Return self.identifier.
        """

        return self.identifier

    def set_identifier(self, value):
        """
        Set self.identifier.
        """

        self.identifier = value
