

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
import functools
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

# lib.mvc

# renderthreads_node
from mvc import renderthreads_node
if(do_reload):
    reload(renderthreads_node)


# Globals
# ------------------------------------------------------------------


# logger (Module Level)
# ------------------------------------------------------------------
logger = renderthreads_logging.get_logger(__name__)



# Scene Interaction
# ------------------------------------------------------------------
def get_nodes(filter_type=None, selected=False):
    """
    Return list of all write nodes in DAG.
    """
    # func
    func = nuke.allNodes
    
    # selected
    if (selected):
        func = nuke.selectedNodes

    # filter_type
    if (filter_type):
        func = functools.partial(func, filter_type)

    # node_list
    node_list = func()
    if not (node_list):
        # log
        logger.debug('node_list empty or None. Returning empty list.')
        return []

    return node_list


def print_nodes(filter_type=None, selected=False, convert=False):
    """
    Return list of all write nodes in DAG.
    """

    # node_list
    node_list = get_nodes(filter_type, selected)

    # convert
    if (convert):
        node_list = convert_nodes(node_list)

    # iterate and print
    for node in node_list:
        print('{0} - {1}'.format(node.name(), node.Class()))


def convert_nodes(nuke_node_list):
    """
    Return list of renderthread_nodes
    from given list of nuke nodes.
    """

    # renderthread_node_list
    renderthread_node_list = []

    # convert
    for nuke_node in nuke_node_list:
        try:
            # renderthread_node
            renderthread_node = convert_nuke_to_renderthread_node(nuke_node)
            # append
            renderthread_node_list.append(renderthread_node)
        except:
            # log
            logger.debug('Error converting nuke_node {0} to renderthread_node. Not converting.'.format(nuke_node))

    # return
    return renderthread_node_list


def node_exists(node):
    """
    Check whether or not node exists.
    """

    try:
        result = nuke.exists(node.name())
        return result
    except:
        return False

def convert_nuke_to_renderthread_node(nuke_node):
    """
    Convert a nuke to a renderthread node.
    """

    start_frame = nuke.root().knob('first_frame')
    end_frame = nuke.root().knob('last_frame')

    # write
    if (nuke_node.Class() == 'Write'):
        return renderthreads_node.RenderThreadsNodeWrite(nuke_node, start_frame, end_frame)
    # generic
    else:
        return renderthreads_node.RenderThreadsNode(nuke_node, start_frame, end_frame)
