

"""
renderthreads_command_line_engine
==========================================

This module handles the creation of the
command line string used for rendering.
"""


# Import
# ------------------------------------------------------------------
# Python
import logging
import functools


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
WRITE_NODE_REPLACEMENT_TEMPLATE = renderthreads_globals.WRITE_NODE_REPLACEMENT_TEMPLATE


# logger (Module Level)
# ------------------------------------------------------------------
logger = renderthreads_logging.get_logger(__name__)


# Command line engine
# ------------------------------------------------------------------
def get_command_line_string(flag_list,
                            nuke_path,
                            script_path,
                            write_node_name = None):
    """
    Convert given list of CommandLineFlag objects into
    a command line string that can be used for
    rendering.
    """
    
    # command_line_string
    command_line_string = '\"{0}\"'.format(nuke_path)
    command_line_string += ' '

    # iterate flag list
    for flag in sorted(flag_list):

        # check state
        if (flag.get_state()):

            # append flag
            command_line_string += flag.get_flag()
            command_line_string += ' '

    # write_node_name
    if (write_node_name):

        #replace template
        command_line_string = command_line_string.replace(WRITE_NODE_REPLACEMENT_TEMPLATE,
                                                            write_node_name)
        command_line_string += ' '

    # --
    command_line_string += '--'
    command_line_string += ' '

    # script_path
    command_line_string += '\"{0}\"'.format(script_path)

    # return
    return command_line_string