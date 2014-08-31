
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



#Import variable
do_reload = True


#asset_manager

#asset_manager_globals
from lib import asset_manager_globals
if(do_reload):reload(asset_manager_globals)

#table_view_editor_bool
from lib.mvc import table_view_editor_bool
if(do_reload):reload(table_view_editor_bool)

#asset_manager_item_delegate_functionality
from lib.mvc import asset_manager_item_delegate_functionality
if(do_reload):reload(asset_manager_item_delegate_functionality)





#Globals
#------------------------------------------------------------------











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


        #instance variables
        #------------------------------------------------------------------

        #item_delegate_functionality
        self.item_delegate_functionality = asset_manager_item_delegate_functionality.AssetManagerItemDelegateFunctionality(item_delegate = self)
        
        
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
        
        #index invalid
        if not(index.isValid()):

            #superclass sizeHint
            return self.superclass.sizeHint(option, index)
            
        
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

    
    def paint(self, painter, option, index):
        """
        Define the look of the current item based on its type.
        -----------------------

        Types handled:
        #. Lists
        #. bool
        #. str and unicode
        """

        #index invalid
        if not(index.isValid()):
            
            #superclass paint
            self.superclass.paint(painter, option, index)
            return

        
        #data
        data = index.data(QtCore.Qt.DisplayRole)

        #row & col
        row = index.row()
        col = index.column()

        

        #list
        if(type(data) is list):

            #paint_list_as_string_with_lines
            self.item_delegate_functionality.paint_list_as_string_with_lines(painter, option, data)


        #bool
        elif(type(data) is bool):

            #paint_bool_as_icon
            self.item_delegate_functionality.paint_bool_as_icon(painter, option, data)


        #str and unicode
        elif(type(data) is str or
            type(data) is unicode):

            #duplicats in column
            if (self.item_delegate_functionality.duplicates_in_column(index)):

                #paint background with error color
                self.item_delegate_functionality.paint_background_with_color(painter, option, index)

            #empty string
            if not (data):

                #paint background with error color
                self.item_delegate_functionality.paint_background_with_color(painter, option, index)


            #superclass paint
            self.superclass.paint(painter, option, index)

        
        #other type
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

