
"""
environment_variables_item_delegate
==========================================

Subclass of QStyledItemDelegate to format view
"""




#Import
#------------------------------------------------------------------
#python
import logging
#PyQt4
from PyQt4 import QtGui
from PyQt4 import QtCore







#EnvironmentVariablesItemDelegate class
#------------------------------------------------------------------
class EnvironmentVariablesItemDelegate(QtGui.QStyledItemDelegate):
    """
    Subclass of QStyledItemDelegate. (...you never know, what you need to override)
    """
    
    def __init__(self, 
                logging_level = logging.DEBUG,
                parent=None): 
        
        #super class constructor
        super(EnvironmentVariablesItemDelegate, self).__init__(parent)


    def sizeHint(self, option, index):
        
        #valid
        if(index.isValid()):

        	#qvariant_data
	    	qvariant_data = index.data(QtCore.Qt.DisplayRole)
	    	#data
	    	data = qvariant_data.toPyObject()

	    	#row & col
	        row = index.row()
	        col = index.column()


	        #check types

	        #list
	        if(type(data) is list):
	        	
	        	#value_string
	        	value_string = ''
	        	for index, value in enumerate(data):
	        		
	        		#last value
	        		if(index == len(data) - 1):
	        			value_string += str(value)
	        			continue
	        		
	        		#append
	        		value_string += str(value + ';\n')


	        	#text_size
	        	q_font_metrics = QtGui.QFontMetrics(QtGui.QApplication.font())
	        	text_size = q_font_metrics.size(0, value_string)
	        	return text_size

	        #type unknown
	        else:
	        	
	        	#superclass sizeHint
	        	return super(EnvironmentVariablesItemDelegate, self).sizeHint(option, index)

        #not valid invoke super class
        else:
        	#superclass sizeHint
        	return super(EnvironmentVariablesItemDelegate, self).sizeHint(option, index)

    
    def paint(self, painter, option, index):
    	"""
    	Define the look of the current icon
    	"""

    	#check type
        if(index.isValid()):

        	#qvariant_data
	    	qvariant_data = index.data(QtCore.Qt.DisplayRole)
	    	#data
	    	data = qvariant_data.toPyObject()

	    	#row & col
	        row = index.row()
	        col = index.column()

        	#save painter
        	painter.save()

	        #list
	        if(type(data) is list):
	        	
	        	#value_string
	        	value_string = ''
	        	for index, value in enumerate(data):
	        		
	        		#last value
	        		if(index == len(data) - 1):
	        			value_string += str(value)
	        			continue
	        		
	        		#append
	        		value_string += str(value + ';\n')


	        	#draw
	        	painter.drawText(option.rect, QtCore.Qt.AlignLeft, value_string)

	        #type unknown
	        else:
	        	
	        	#superclass paint
	        	super(EnvironmentVariablesItemDelegate, self).paint(painter, option, index)

	        #restore painter
	        painter.restore()

        #not valid invoke super class
        else:
        	#superclass paint
        	super(EnvironmentVariablesItemDelegate, self).paint(painter, option, index)


