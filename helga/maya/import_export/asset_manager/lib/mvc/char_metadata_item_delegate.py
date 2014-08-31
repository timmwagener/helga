
"""
char_metadata_item_delegate
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


#asset_manager

#asset_manager_globals
from lib import asset_manager_globals
if(do_reload):reload(asset_manager_globals)

#table_view_editor_bool
from lib.mvc import table_view_editor_bool
if(do_reload):reload(table_view_editor_bool)






#Globals
#------------------------------------------------------------------

#AssetManager Icons
ICON_TRUE = asset_manager_globals.ICON_TRUE
ICON_FALSE = asset_manager_globals.ICON_FALSE






#CharMetadataItemDelegate class
#------------------------------------------------------------------
class CharMetadataItemDelegate(QtGui.QStyledItemDelegate):
    """
    Subclass of QStyledItemDelegate.
    """

    def __new__(cls, *args, **kwargs):
        """
        CharMetadataItemDelegate instance factory.
        """

        #char_metadata_item_delegate_instance
        char_metadata_item_delegate_instance = super(CharMetadataItemDelegate, cls).__new__(cls, args, kwargs)

        return char_metadata_item_delegate_instance

    
    def __init__(self, 
                logging_level = logging.DEBUG,
                parent=None):
        """
        Customize instance.
        """
        
        #super class constructor
        self.superclass = super(CharMetadataItemDelegate, self)
        self.superclass.__init__(parent)


        #instance variables
        #------------------------------------------------------------------

        #pxm_bool_true
        self.pxm_bool_true = QtGui.QPixmap(ICON_TRUE)
        #pxm_bool_false
        self.pxm_bool_false = QtGui.QPixmap(ICON_FALSE)
        
        
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
        #. bool
        """

        #check type
        if(index.isValid()):

            #data
            data = index.data(QtCore.Qt.DisplayRole)

            #row & col
            row = index.row()
            col = index.column()

            

            #list
            if(type(data) is list):

                #save painter
                painter.save()
                
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

                #restore painter
                painter.restore()



            #bool
            elif(type(data) is bool):

                #save painter
                painter.save()

                #width, height, center
                option_rect = option.rect
                width = option_rect.width()
                height = option_rect.height()
                center = option_rect.center()

                #margin
                margin = 5

                #pxm_bool
                if (data):
                    pxm_bool = self.pxm_bool_true.scaledToHeight(height - (margin * 2))
                else:
                    pxm_bool = self.pxm_bool_false.scaledToHeight(height - (margin * 2))

                #correct center to accomodate image in the center
                center.setX(center.x() - (pxm_bool.width() / 2))
                center.setY(center.y() - (pxm_bool.height() / 2))

                #draw pixmap
                painter.drawPixmap(center, pxm_bool)

                #restore painter
                painter.restore()

            
            #other type
            else:
                
                #superclass paint
                self.superclass.paint(painter, option, index)

        
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

        
        #column export proxy
        if(col == 2):

            #bool_editor
            bool_editor = table_view_editor_bool.TableViewEditorBool(parent = parent)
            
            return bool_editor


        #column export rendergeo
        elif(col == 3):

            #bool_editor
            bool_editor = table_view_editor_bool.TableViewEditorBool(parent = parent)
            
            return bool_editor


        #column export locator
        elif(col == 4):

            #bool_editor
            bool_editor = table_view_editor_bool.TableViewEditorBool(parent = parent)
            
            return bool_editor


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
        

        #column export proxy
        if(col == 2):

            #height
            height = option.rect.height()
            #set height
            option.rect.setHeight(height * 2)

            #editor geometry
            editor.setGeometry(option.rect)
            #move
            editor.move(mouse_pos)


        #column export rendergeo
        elif(col == 3):

            #height
            height = option.rect.height()
            #set height
            option.rect.setHeight(height * 2)

            #editor geometry
            editor.setGeometry(option.rect)
            #move
            editor.move(mouse_pos)


        #column export locator
        elif(col == 4):

            #height
            height = option.rect.height()
            #set height
            option.rect.setHeight(height * 2)

            #editor geometry
            editor.setGeometry(option.rect)
            #move
            editor.move(mouse_pos)


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

        
        #column export proxy
        if(col == 2):

            try:
                editor.set_value(index.model().data(index))
                
            except:
                pass


        #column export rendergeo
        elif(col == 3):

            try:
                editor.set_value(index.model().data(index))
                
            except:
                pass


        #column export locator
        elif(col == 4):

            try:
                editor.set_value(index.model().data(index))
                
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

        
        #column export proxy
        if(col == 2):

            model.setData(index, editor.get_value())


        #column export rendergeo
        elif(col == 3):

            model.setData(index, editor.get_value())


        #column export locator
        elif(col == 4):

            model.setData(index, editor.get_value())


        #other columns
        else:
            #evaluate in superclass
            self.superclass.setModelData(editor, model, index)




        