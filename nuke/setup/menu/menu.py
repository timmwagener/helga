


#menu.py (startup procedures / gui only)
#------------------------------------------------------------------








#Imports
#------------------------------------------------------------------

#python
import sys
import os
import functools

#nuke
import nuke
from nukescripts import panels



#Reload Bool
do_reload = True

from helga.nuke.reconstruction.renderReconstructVRay import renderReconstruct as renderReconstructVRay
if(do_reload): reload(renderReconstructVRay)

from helga.nuke.reconstruction.sceneReconstructVRay import sceneReconstruct as sceneReconstructVRay
if(do_reload): reload(sceneReconstructVRay)

from helga.general.setup.global_variables import global_variables
if(do_reload): reload(global_variables)

#global_functions
from helga.general.setup.global_functions import global_functions
if(do_reload):reload(global_functions)

from helga.general.setup.doc_link import doc_link
if(do_reload): reload(doc_link)

from helga.general.directory_wizard import directory_wizard
if(do_reload): reload(directory_wizard)








#menu Globals
#------------------------------------------------------------------

#Assign all global variables to only use local ones later on
PIPELINE_SCRIPTS_BASE_PATH = global_variables.PIPELINE_SCRIPTS_BASE_PATH
NUKE_ICONS_PATH = global_variables.NUKE_ICONS_PATH
NUKE_PLUGIN_PATH = global_variables.NUKE_PLUGIN_PATH

PIPELINE_ASSETS_PATH = global_variables.PIPELINE_ASSETS_PATH
PIPELINE_SHOTS_PATH = global_variables.PIPELINE_SHOTS_PATH
PIPELINE_WORK_PROPS_PATH = global_variables.PIPELINE_WORK_PROPS_PATH
PIPELINE_RND_PATH = global_variables.PIPELINE_RND_PATH






#Custom formats
#------------------------------------------------------------------

nuke.addFormat ("960 540 0 0 960 540 1.0 HD_small")
nuke.addFormat ("1280 720 0 0 1280 720 1.0 HD_medium")
nuke.addFormat ("3840 2160 0 0 3840 2160 1.0 HD_double")
nuke.addFormat ("4096 4096 0 0 4096 4096 1.0 square_4k")
nuke.addFormat ("8192 8192 0 0 8192 8192 1.0 square_8k")





#Add favorites to file browser
#------------------------------------------------------------------

try:
    #display_type
    display_type = nuke.IMAGE | nuke.SCRIPT | nuke.GEO | nuke.FONT | nuke.PYTHON

    #favorite_icon
    favorite_icon = NUKE_ICONS_PATH + r'iconHelgaMenuMain.png'
    
    #favorite_dict
    favorite_dict = {'helga_assets':['helga_assets', PIPELINE_ASSETS_PATH, display_type, favorite_icon],
    'helga_shots':['helga_shots', PIPELINE_SHOTS_PATH, display_type, favorite_icon],
    'helga_props':['helga_props', PIPELINE_WORK_PROPS_PATH, display_type, favorite_icon],
    'helga_rnd':['helga_rnd', PIPELINE_RND_PATH, display_type, favorite_icon]
    }

    #iterate and set
    for value_list in sorted(favorite_dict.values()):
        #extract info
        favorite_name, favorite_path, favorite_display_type, favorite_icon = value_list
        #add to favorites
        nuke.addFavoriteDir( favorite_name, favorite_path, favorite_display_type, favorite_icon)

    #SuccessMsg
    nuke.tprint('Successfully added pathes to favorites')

except:

    #FailMsg
    nuke.tprint('Error adding favorites to file browser')










#Create helga menu (Nodes)
#------------------------------------------------------------------

try:
    #Main Menubar
    helga_main_menu = nuke.menu('Nodes').addMenu('Helga', icon= NUKE_ICONS_PATH + r'iconHelgaMenuMain.png' )



    #reconstruction_menu
    #------------------------------------------------------------------
    #------------------------------------------------------------------

    #reconstruction_menu
    reconstruction_menu = helga_main_menu.addMenu('Reconstruction')

    #render_reconstruct_menu
    render_reconstruct_menu = reconstruction_menu.addMenu('RenderReconstruction')


    #render_reconstruct_menu_vray
    render_reconstruct_menu_vray = render_reconstruct_menu.addMenu('VRay')

    #cmds
    render_reconstruct_menu_vray.addCommand('Reconstruct all Elements', lambda: renderReconstructVRay.RenderReconstruct().reconstructAll())
    render_reconstruct_menu_vray.addCommand('Reconstruct Light Elements', lambda: renderReconstructVRay.RenderReconstruct().reconstructLightREs())
    render_reconstruct_menu_vray.addCommand('Reconstruct Framebuffer Elements', lambda: renderReconstructVRay.RenderReconstruct().reconstructFramebufferREs())
    render_reconstruct_menu_vray.addCommand('Reconstruct Data Elements', lambda: renderReconstructVRay.RenderReconstruct().reconstructDataREs())
    render_reconstruct_menu_vray.addCommand('Reconstruct Multi Matte Elements', lambda: renderReconstructVRay.RenderReconstruct().reconstructMultiMatteREs())
    render_reconstruct_menu_vray.addCommand('Reconstruct Shadow Elements', lambda: renderReconstructVRay.RenderReconstruct().reconstructShadowREs())


    #render_reconstruct_menu_mantra
    render_reconstruct_menu_mantra = render_reconstruct_menu.addMenu('Mantra')

    #cmds
    render_reconstruct_menu_mantra.addCommand('Dummy')


    #SceneReconstruct Menu
    scene_reconstruct_menu = reconstruction_menu.addMenu('SceneReconstruction')


    #scene_reconstruct_menu_vray
    scene_reconstruct_menu_vray = scene_reconstruct_menu.addMenu('VRay')

    #cmds
    scene_reconstruct_menu_vray.addCommand('Reconstruct Alembic', lambda: sceneReconstructVRay.SceneReconstruct().reconstruct_alembic())
    scene_reconstruct_menu_vray.addCommand('Reconstruct Camera from Vray exr', lambda: sceneReconstructVRay.SceneReconstruct().create_exr_cam_vray())
    scene_reconstruct_menu_vray.addCommand('Reconstruct Light', lambda: sceneReconstructVRay.SceneReconstruct().reconstruct_light())


    #scene_reconstruct_menu_mantra
    scene_reconstruct_menu_mantra = scene_reconstruct_menu.addMenu('Mantra')

    #cmds
    scene_reconstruct_menu_mantra.addCommand('Dummy')





    #doc_link_menu
    #------------------------------------------------------------------
    #------------------------------------------------------------------

    #doc_link_menu
    doc_link_menu = helga_main_menu.addMenu('Documentation')

    #cmds
    doc_link_menu.addCommand('Open Documentation', lambda: doc_link.run())







    #third_party_gizmos_menu
    #------------------------------------------------------------------
    #------------------------------------------------------------------

    #third_party_gizmos_menu
    third_party_gizmos_menu = helga_main_menu.addMenu('Third Party Gizmos')





    #luma_nuke_gizmos_menu
    #------------------------------------------------------------------

    #LUMA_NUKE_GIZMO_BASE_PATH
    LUMA_NUKE_GIZMO_BASE_PATH = NUKE_PLUGIN_PATH + r'/LumaNukeGizmos/Gizmos'

    #luma_nuke_gizmos_menu
    luma_nuke_gizmos_menu = third_party_gizmos_menu.addMenu('LumaNukeGizmos')


    #luma_nuke_gizmo_dict
    luma_nuke_gizmo_dict = {}

    #iterate and fill gizmo dict
    for (directory_path, dir_names, file_names) in os.walk(LUMA_NUKE_GIZMO_BASE_PATH):
        #each file in each subdir
        for file_name in file_names:
            #if file is gizmo
            if(file_name.split('.')[-1] == 'gizmo'):
                
                #gizmo_name
                gizmo_name = file_name.split('.')[0]
                #parent_directory
                parent_directory = directory_path.split('\\')[-1]
                
                #first entry for folder
                if not(parent_directory in luma_nuke_gizmo_dict):
                    luma_nuke_gizmo_dict[parent_directory] = [gizmo_name]
                #else
                else:
                    luma_nuke_gizmo_dict[parent_directory].append(gizmo_name)


    #iterate and build menus
    for submenu_name, gizmo_name_list in luma_nuke_gizmo_dict.iteritems():

        #luma_nuke_gizmos_submenu
        luma_nuke_gizmos_submenu = luma_nuke_gizmos_menu.addMenu('{0}'.format(submenu_name))
        
        #iterate gizmos and build cmds
        for gizmo_name in gizmo_name_list:

            #cmds
            luma_nuke_gizmos_submenu.addCommand(gizmo_name, "nuke.createNode('{0}')".format(gizmo_name))
            








    #nuke_env_menu
    #------------------------------------------------------------------

    #NUKE_ENV_GIZMO_PATH
    NUKE_ENV_GIZMO_PATH = NUKE_PLUGIN_PATH + r'/nuke.env/gizmos'

    #nuke_env_menu
    nuke_env_menu = third_party_gizmos_menu.addMenu('nuke.env')


    #nuke_env_file_list
    nuke_env_file_list = [gizmo_name for 
                            gizmo_name in 
                            os.listdir(NUKE_ENV_GIZMO_PATH) if
                            os.path.isfile(os.path.join(NUKE_ENV_GIZMO_PATH, gizmo_name))]

    #nuke_env_gizmo_list
    nuke_env_gizmo_list = [gizmo_name.split('.')[0] for 
                            gizmo_name in 
                            nuke_env_file_list if
                            gizmo_name.split('.')[-1] == 'gizmo']


    #iterate and add commands
    for nuke_env_gizmo in nuke_env_gizmo_list:
        
        #cmds
        nuke_env_menu.addCommand(nuke_env_gizmo, "nuke.createNode('{0}')".format(nuke_env_gizmo))




    



    #separator
    helga_main_menu.addSeparator()


    


    #directory_wizard
    #------------------------------------------------------------------
    #------------------------------------------------------------------

    #cmds
    helga_main_menu.addCommand('Directory Wizard', lambda: directory_wizard.run())






    #SuccessMsg
    nuke.tprint('Successfully set Helga Menu')

except:
    
    #FailMsg
    nuke.tprint('Error setting Helga menu')




