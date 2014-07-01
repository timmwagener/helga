


#menu.py (startup procedures / gui only)
#------------------------------------------------------------------








#Imports
#------------------------------------------------------------------

#python
import sys
import os

#nuke
import nuke
from nukescripts import panels
import functools


#Reload Bool
do_reload = True

from helga.nuke.reconstruction.renderReconstructVRay import renderReconstruct as renderReconstructVRay
if(do_reload): reload(renderReconstructVRay)

from helga.nuke.reconstruction.sceneReconstructVRay import sceneReconstruct as sceneReconstructVRay
if(do_reload): reload(sceneReconstructVRay)

from helga.general.setup.global_variables import global_variables
if(do_reload): reload(global_variables)

from helga.general.setup.doc_link import doc_link
if(do_reload): reload(doc_link)

from helga.general.directory_wizard import directory_wizard
if(do_reload): reload(directory_wizard)














#Create menu (Nodes)
#------------------------------------------------------------------

try:
    #Main Menubar
    helga_main_menu = nuke.menu('Nodes').addMenu('Helga', icon= global_variables.NUKE_ICONS_PATH + r'iconHelgaMenuMain.png' )


    
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






#Add favorites to file browser
#------------------------------------------------------------------

try:
    #display_type
    display_type = nuke.IMAGE | nuke.SCRIPT | nuke.GEO | nuke.FONT | nuke.PYTHON

    #favorite_icon
    favorite_icon = global_variables.NUKE_ICONS_PATH + r'iconHelgaMenuMain.png'
    
    #favorite_dict
    favorite_dict = {'helga_assets':['helga_assets', r'//bigfoot/grimmhelga/Production/3d/maya/scenes/assets/', display_type, favorite_icon],
    'helga_shots':['helga_shots', r'//bigfoot/grimmhelga/Production/3d/maya/scenes/shots/', display_type, favorite_icon],
    'helga_props':['helga_props', r'//bigfoot/grimmhelga/Production/3d/maya/scenes/assets/work/props', display_type, favorite_icon],
    'helga_rnd':['helga_rnd', r'//bigfoot/grimmhelga/Production/rnd/', display_type, favorite_icon]
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
    

    
    
    
    
    
    
    
    
    
    
    

#LumaNukeGizmos startup procedure
#------------------------------------------------------------------

try:
    if __name__ == '__main__':
        gizManager = globals().get('gizManager', None)
        if gizManager is None:
            print 'Problem finding GizmoPathManager - check that init.py was setup correctly'
        else:
            gizManager.addGizmoMenuItems()
            del gizManager

    #SuccessMsg
    nuke.tprint('Successfully added LumaNukeGizmo menu items')
    
except:
    
    #FailMsg
    nuke.tprint('Error adding LumaNukeGizmo menu items')