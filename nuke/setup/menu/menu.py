


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

from helga.nuke.reconstruction.renderReconstruct import renderReconstruct
if(doReload): reload(renderReconstruct)

from helga.nuke.reconstruction.sceneReconstruct import sceneReconstruct
if(doReload): reload(sceneReconstruct)



#Globals
#------------------------------------------------------------------
ICONS_PATH = r'//bigfoot/grimmhelga/Production/scripts/deploy/helga/nuke/setup/icons/'





#Methods
#------------------------------------------------------------------










#Create menu (Nodes)
#------------------------------------------------------------------

try:
	#Main Menubar
	helga_main_menu = nuke.menu('Nodes').addMenu('Helga', icon= ICONS_PATH + r'iconKugeltiereMenuMain.png' )


	#reconstruction_menu
	reconstruction_menu = helga_main_menu.addMenu('Reconstruction')

	#RenderReconstruct Menu
	renderReconstructMenu = reconstruction_menu.addMenu('RenderReconstruction')
	#cmds
	renderReconstructMenu.addCommand( 'Reconstruct all Elements', lambda: renderReconstruct.RenderReconstruct().reconstructAll())
	renderReconstructMenu.addCommand( 'Reconstruct Light Elements', lambda: renderReconstruct.RenderReconstruct().reconstructLightREs())
	renderReconstructMenu.addCommand( 'Reconstruct Framebuffer Elements', lambda: renderReconstruct.RenderReconstruct().reconstructFramebufferREs())
	renderReconstructMenu.addCommand( 'Reconstruct Data Elements', lambda: renderReconstruct.RenderReconstruct().reconstructDataREs())
	renderReconstructMenu.addCommand( 'Reconstruct Multi Matte Elements', lambda: renderReconstruct.RenderReconstruct().reconstructMultiMatteREs())
	renderReconstructMenu.addCommand( 'Reconstruct Shadow Elements', lambda: renderReconstruct.RenderReconstruct().reconstructShadowREs())

	#SceneReconstruct Menu
	sceneReconstructMenu = reconstruction_menu.addMenu('SceneReconstruction')
	#cmds
	sceneReconstructMenu.addCommand( 'Reconstruct Alembic', lambda: sceneReconstruct.SceneReconstruct().reconstruct_alembic())
	sceneReconstructMenu.addCommand( 'Reconstruct Camera from Vray exr', lambda: sceneReconstruct.SceneReconstruct().create_exr_cam_vray())
	sceneReconstructMenu.addCommand( 'Reconstruct Light', lambda: sceneReconstruct.SceneReconstruct().reconstruct_light())

	#SuccessMsg
	print('Successfully set Helga Menu')

except:
	#FailMsg
	print('Error setting Helga menu')







	
	
	
	
	
	
	
	
	
	
	





