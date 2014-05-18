

#reconstruct_globals Module
#------------------------------------------------------------------

'''
Description:
Globals
'''

'''
ToDo:

'''






#Globals
#------------------------------------------------------------------

PREFIX = 'gh'
ALEMBIC_DICTIONARY_KEY = 'alembic_details'
NUKE_EXR_METADATA_PREFIX = 'exr/'
ALEMBIC_READ_NODE_BACKDROP_COLOR = [128, 255, 0]
LIGHT_DICTIONARY_KEY = 'light_details'
LIGHT_NODE_BACKDROP_COLOR = [255, 255, 0]







#Methods
#------------------------------------------------------------------
def align_nodes(nodes, direction = 'x'):
	"""Align nodes either horizontally or vertically."""
	
	if len( nodes ) < 2:
		return
	if direction.lower() not in ('x', 'y'):
		raise ValueError, 'direction argument must be x or y'

	positions = [ float( n[ direction.lower()+'pos' ].value() ) for n in nodes]
	avrg = sum( positions ) / len( positions )
	for n in nodes:
		if direction == 'x':
			for n in nodes:
				n.setXpos( int(avrg) )
		else:
			for n in nodes:
				n.setYpos( int(avrg) )

	return avrg