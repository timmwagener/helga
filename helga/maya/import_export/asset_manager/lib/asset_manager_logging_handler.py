

"""
asset_manager_logging_handler
==========================================

Automaticaly log to le_status from given widget.
"""




#Import
#------------------------------------------------------------------
#python
import logging
#PySide
from PySide import QtGui
from PySide import QtCore







#StatusStreamHandler class
#------------------------------------------------------------------
class StatusStreamHandler(logging.StreamHandler):
    """
    Stream handler subclass that calls the set_status() method of
    the wdgt_status object used for initialization.

    Normally the set_status() method would set a QLineEdit or
    similiar to display the log message.
    """
    
    def __init__(self,
                    wdgt_status = None,
                    logging_level = logging.DEBUG):
        """
        Initialize StatusStreamHandler
        """

        #super class init
        super(StatusStreamHandler, self).__init__()

        #logger
        #------------------------------------------------------------------
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logging_level = logging_level
        self.logger.setLevel(self.logging_level)

        #wdgt_status
        #------------------------------------------------------------------
        self.wdgt_status = wdgt_status

    
    def emit(self, record):
        """
        Custom emit for StreamHandler subclass
        """
        
        try:
            #message
            message = self.format(record)
            #stream
            stream = self.stream
            
            
            #if wdgt_status exists then log
            if(self.wdgt_status):
                #display message
                self.wdgt_status.set_status(message)
            
            
            #flush
            self.flush()
        
        except (KeyboardInterrupt, SystemExit):
            raise
        
        except:
            self.handleError(record)