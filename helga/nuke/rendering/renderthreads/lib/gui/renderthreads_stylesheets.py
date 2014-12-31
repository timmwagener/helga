
"""
renderthreads_stylesheets
==========================================

Module that has only one method.

#. get_stylesheet
"""


#Import
#------------------------------------------------------------------
#Import variable
do_reload = True


#renderthreads

#renderthreads_globals
from .. import renderthreads_globals
if(do_reload):
    reload(renderthreads_globals)







#Globals
#------------------------------------------------------------------

"""
#Pathes
TOOL_ROOT_PATH = renderthreads_globals.TOOL_ROOT_PATH
MEDIA_PATH = renderthreads_globals.MEDIA_PATH
ICONS_PATH = renderthreads_globals.ICONS_PATH
UI_PATH = renderthreads_globals.UI_PATH

#Fonts
FUTURA_LT_LIGHT = renderthreads_globals.FUTURA_LT_LIGHT

#Header
HEADER_IMAGE = renderthreads_globals.HEADER_IMAGE

#Transparency
TABLEVIEW_EDITOR_TRANSPARENCY = renderthreads_globals.TABLEVIEW_EDITOR_TRANSPARENCY

#AssetManager colors
BRIGHT_ORANGE = renderthreads_globals.BRIGHT_ORANGE

"""





#get_stylesheet
#------------------------------------------------------------------

def get_stylesheet():
    """
    Return stylesheet string, defining all stylesheets for RenderThreads.
    """

    #str_stylesheet
    str_stylesheet = " \
\
\
/* QWidget */\
QWidget { background-color: red; \
          font-family: \"Futura LT Light\"; \
          font-size: 14pt; \
          selection-background-color: green; \
}\
\
\
"
	
	#return
    return str_stylesheet