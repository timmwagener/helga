
"""
shot_metadata_item_delegate
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



#Import variable
do_reload = True


#table_view_editor_integer
import table_view_editor_integer
if(do_reload):reload(table_view_editor_integer)








#ShotMetadataItemDelegate class
#------------------------------------------------------------------
class ShotMetadataItemDelegate(QtGui.QStyledItemDelegate):
    """
    Subclass of QStyledItemDelegate.
    """

    def __new__(cls, *args, **kwargs):
        """
        ShotMetadataItemDelegate instance factory.
        """

        #shot_metadata_item_delegate_instance
        shot_metadata_item_delegate_instance = super(ShotMetadataItemDelegate, cls).__new__(cls, args, kwargs)

        return shot_metadata_item_delegate_instance

    
    def __init__(self, 
                logging_level = logging.DEBUG,
                parent=None):
        """
        Customize instance.
        """
        
        #super class constructor
        self.superclass = super(ShotMetadataItemDelegate, self)
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

        #column alembic path
        if(col == 1):

            #file_dialog
            file_dialog = QtGui.QFileDialog(parent)
            file_dialog.setFileMode(QtGui.QFileDialog.Directory)
            file_dialog.setViewMode(QtGui.QFileDialog.Detail)
            
            return file_dialog

        #column start
        elif(col == 3):

            #integer_editor
            integer_editor = table_view_editor_integer.TableViewEditorInteger(parent = parent)
            
            return integer_editor

        #column end
        elif(col == 4):

            combo = QtGui.QComboBox(parent)
            li = []
            li.append("Zero")
            li.append("One")
            li.append("Two")
            li.append("Three")
            li.append("Four")
            li.append("Five")
            combo.addItems(li)
            
            return combo

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

        #center_point
        center_point = QtGui.QCursor.pos()
        

        #column alembic path
        if(col == 1):

            editor.move(center_point)

        
        #column start
        elif(col == 3):

            editor.move(center_point)


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

        #column Alembic Path
        if(col == 1):

            try:
                editor.setDirectory(str(index.model().data(index)))
                
            except:
                pass


        #column start
        elif(col == 3):

            try:
                editor.set_integer(int(index.model().data(index)))
                
            except:
                pass

        
        #column end
        elif(col == 4):

            try:
                editor.blockSignals(True)
                editor.setCurrentIndex(int(index.model().data(index)))
                editor.blockSignals(False)
            except:
                editor.setCurrentIndex(-1)

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

        #column alembic path
        if(col == 1):

            model.setData(index, editor.directory().absolutePath())

        #column start
        elif(col == 3):

            model.setData(index, editor.get_integer())

        #column end
        elif(col == 4):

            model.setData(index, editor.currentIndex())

        #other columns
        else:
            #evaluate in superclass
            self.superclass.setModelData(editor, model, index)

        