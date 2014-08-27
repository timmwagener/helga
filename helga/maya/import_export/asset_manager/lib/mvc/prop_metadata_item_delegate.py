
"""
prop_metadata_item_delegate
==========================================

Subclass of QStyledItemDelegate to format view
"""











#Import
#------------------------------------------------------------------
#python
import logging
#PySide
from PySide import QtGui
from PySide import QtCore













#PropMetadataItemDelegate class
#------------------------------------------------------------------
class PropMetadataItemDelegate(QtGui.QStyledItemDelegate):
    """
    Subclass of QStyledItemDelegate.
    """

    def __new__(cls, *args, **kwargs):
        """
        PropMetadataItemDelegate instance factory.
        """

        #prop_metadata_item_delegate_instance
        prop_metadata_item_delegate_instance = super(PropMetadataItemDelegate, cls).__new__(cls, args, kwargs)

        return prop_metadata_item_delegate_instance

    
    def __init__(self, 
                logging_level = logging.DEBUG,
                parent=None):
        """
        Customize instance.
        """
        
        #super class constructor
        self.superclass = super(PropMetadataItemDelegate, self)
        self.superclass.__init__(parent)



        #slots
        #------------------------------------------------------------------

        
        

        #instance variables
        #------------------------------------------------------------------

        
        
        #logger
        #------------------------------------------------------------------
        #logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logging_level = logging_level
        self.logger.setLevel(self.logging_level)


    def sizeHint(self, option, index):
        """
        Returns the size for a type a certain index represents.
        -----------------------

        Types handled:
        #. Lists
        """
        
        #valid
        if(index.isValid()):
            
            #data
            data = index.data(QtCore.Qt.DisplayRole)

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

            #other type
            else:
                
                #superclass sizeHint
                return self.superclass.sizeHint(option, index)

        #not valid invoke super class
        else:
            #superclass sizeHint
            return self.superclass.sizeHint(option, index)

    
    def paint(self, painter, option, index):
        """
        Define the look of the current item based on its type.
        -----------------------

        Types handled:
        #. Lists
        """

        #check type
        if(index.isValid()):

            #data
            data = index.data(QtCore.Qt.DisplayRole)

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

            #other type
            else:
                
                #superclass paint
                self.superclass.paint(painter, option, index)

            #restore painter
            painter.restore()

        #not valid invoke super class
        else:
            #superclass paint
            self.superclass.paint(painter, option, index)


    def createEditor(self, parent, option, index):
        """
        Virtual method of itemDelegate that creates an editor widget and returns
        it when EditRole requests it.
        """
        
        #index invalid
        if not(index.isValid()):
            #log
            self.logger.debug('Index {0} not valid.'.format(index))
            #evaluate in superclass
            return self.superclass.createEditor(self, parent, option, index)
        
        
        #row & col
        row = index.row()
        col = index.column()

        #column asset_name
        if(col == 1):

            #evaluate in superclass
            return self.superclass.createEditor(parent, option, index)


        #other columns
        else:
            
            #evaluate in superclass
            return self.superclass.createEditor(parent, option, index)


    def updateEditorGeometry(self, editor, option, index):
        """
        Virtual method of itemDelegate to update the editor geometry.
        """

        #index invalid
        if not(index.isValid()):
            #log
            self.logger.debug('Index {0} not valid.'.format(index))
            #evaluate in superclass
            return self.superclass.updateEditorGeometry(editor, option, index)
        
        
        #row & col
        row = index.row()
        col = index.column()

        #mouse_pos
        mouse_pos = QtGui.QCursor.pos()
        

        #column asset_name
        if(col == 1):

            #evaluate in superclass
            return self.superclass.updateEditorGeometry(editor, option, index)


        #other columns
        else:
            
            #evaluate in superclass
            return self.superclass.updateEditorGeometry(editor, option, index)


    def setEditorData(self, editor, index):
        """
        Virtual method of itemDelegate that sets the editor data after
        the editor is initialized.
        """

        if not(index.isValid()):
            #log
            self.logger.debug('Index {0} not valid.'.format(index))
            #evaluate in superclass
            self.superclass.setEditorData(self, editor, index)
        
        
        #row & col
        row = index.row()
        col = index.column()

        #column asset_name
        if(col == 1):

            try:
                #evaluate in superclass
                self.superclass.setEditorData(editor, index)
                
            except:
                pass


        #other columns
        else:
            
            #evaluate in superclass
            self.superclass.setEditorData(editor, index)


    


    def setModelData(self, editor, model, index):
        """
        Set data into model.
        """

        if not(index.isValid()):
            #log
            self.logger.debug('Index {0} not valid.'.format(index))
            #evaluate in superclass
            self.superclass.setModelData(self, editor, model, index)
        
        
        #row & col
        row = index.row()
        col = index.column()

        #column asset_name
        if(col == 1):

            #evaluate in superclass
            self.superclass.setModelData(editor, model, index)


        #other columns
        else:
            #evaluate in superclass
            self.superclass.setModelData(editor, model, index)

        