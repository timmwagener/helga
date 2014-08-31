
"""
asset_manager_dock_widget
==========================================

Subclass of QDockWidget to provide ability for custom type checks.
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

#lib

#asset_manager_globals
from lib import asset_manager_globals
if(do_reload):reload(asset_manager_globals)


#lib.gui

#asset_manager_stylesheets
from lib.gui import asset_manager_stylesheets
if(do_reload):reload(asset_manager_stylesheets)






#Globals
#------------------------------------------------------------------












#AssetManagerDockWidget class
#------------------------------------------------------------------
class AssetManagerDockWidget(QtGui.QDockWidget):
    """
    Subclass of QWidget to allow for custom styling
    """

    def __new__(cls, *args, **kwargs):
        """
        AssetManagerDockWidget instance factory.
        """

        #asset_manager_dock_widget_instance
        asset_manager_dock_widget_instance = super(AssetManagerDockWidget, cls).__new__(cls, args, kwargs)

        return asset_manager_dock_widget_instance

    
    def __init__(self, 
                logging_level = logging.DEBUG,
                parent=None):
        """
        AssetManagerDockWidget instance customization.
        """

        #parent_class
        self.parent_class = super(AssetManagerDockWidget, self)
        self.parent_class.__init__(parent)

        #objectName
        self.setObjectName(self.__class__.__name__)
        
        #instance variables
        #------------------------------------------------------------------
        
        

        #logger
        #------------------------------------------------------------------
        #logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logging_level = logging_level
        self.logger.setLevel(self.logging_level)


        
        #stylesheets
        #------------------------------------------------------------------

        
        
        


        
        #Init procedure
        #------------------------------------------------------------------

        #setup_ui
        self.setup_ui()

        #connect_ui
        self.connect_ui()

        #style_ui
        self.style_ui()









    #UI setup methods
    #------------------------------------------------------------------
    
    def setup_ui(self):
        """
        Setup UI.
        """

        pass


    def connect_ui(self):
        """
        Connect UI widgets with slots or functions.
        """
        
        pass


    def style_ui(self):
        """
        Style UI widgets.
        """
        
        #set_stylesheet
        self.setStyleSheet(asset_manager_stylesheets.get_stylesheet())




    #Getter & Setter
    #------------------------------------------------------------------

    
    


    #Methods
    #------------------------------------------------------------------

    


    #Events
    #------------------------------------------------------------------

    def closeEvent(self, event):
        """
        Customized closeEvent
        """

        #log
        self.logger.debug('Close Event')

        try:
            
            #stop_all_threads_and_timer
            self.widget().stop_all_threads_and_timer()
        
        except:
            
            #log
            self.logger.debug('Error stopping threads and timers for widget().')
        

        #parent close event
        self.parent_class.closeEvent(event)

    




