


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
doReload = True

from helga.nuke.reconstruction.renderReconstructVRay import renderReconstruct as renderReconstructVRay
if(doReload): reload(renderReconstructVRay)

from helga.nuke.reconstruction.sceneReconstructVRay import sceneReconstruct as sceneReconstructVRay
if(doReload): reload(sceneReconstructVRay)

from helga.general.setup.global_variables import global_variables
if(doReload): reload(global_variables)

from helga.general.setup.doc_link import doc_link
if(doReload): reload(doc_link)



#Globals
#------------------------------------------------------------------
SCRIPTS_ROOT_PATH = r'//bigfoot/grimmhelga/Production/scripts/deploy'
ICONS_PATH = SCRIPTS_ROOT_PATH + r'/helga/nuke/setup/icons/'





#Methods
#------------------------------------------------------------------










#Create menu (Nodes)
#------------------------------------------------------------------

try:
	#Main Menubar
	helga_main_menu = nuke.menu('Nodes').addMenu('Helga', icon= ICONS_PATH + r'iconHelgaMenuMain.png' )


	
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

	

	#SuccessMsg
	print('Successfully set Helga Menu')

except:
	#FailMsg
	print('Error setting Helga menu')







	
	
	
	
	
	
	
	
	
	
	





