

"""
renderthreads_nuke
==========================================

This module encapsulates renderthreads nuke
functionality.
"""


# Import
# ------------------------------------------------------------------
# Python
import logging
# nuke
import nuke


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


# logger (Module Level)
# ------------------------------------------------------------------
logger = renderthreads_logging.get_logger(__name__)



# Scene Interaction
# ------------------------------------------------------------------
def get_write_nodes():
    """
    Return list of all write nodes in DAG.
    """

    # write_node_list
    write_node_list = [node for node in nuke.allNodes() if (node.Class() == 'Write')]
    if not (write_node_list):
        # log
        logger.debug('write_node_list empty or None. Returning empty list.')
        return []

    # temp
    print(write_node_list)

    return write_node_list


def get_selected_write_nodes():
    """
    Return list of selected write nodes in DAG.
    """

    # write_node_list
    write_node_list = [node for node in nuke.selectedNodes() if (node.Class() == 'Write')]
    if not (write_node_list):
        # log
        logger.debug('selected write_node_list empty or None. Returning empty list.')
        return []

    # temp
    print(write_node_list)

    return write_node_list
