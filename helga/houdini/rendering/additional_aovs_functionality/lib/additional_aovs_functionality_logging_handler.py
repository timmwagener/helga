

"""
additional_aovs_functionality_logging_handler
====================================================

Automaticaly call print() for log message.
"""




#Import
#------------------------------------------------------------------
#python
import logging







#PrintStreamHandler class
#------------------------------------------------------------------
class PrintStreamHandler(logging.StreamHandler):
    """
    Stream handler subclass that calls the print() statement of Python.

    It is normaly totally redundant but since Houdini is not built with Qt
    as a GUI Framework it is necessary here.
    """
    
    def __init__(self,
                    logging_level = logging.DEBUG):
        """
        Initialize PrintStreamHandler
        """

        #super class init
        super(PrintStreamHandler, self).__init__()

    
    def emit(self, record):
        """
        Custom emit for StreamHandler subclass
        """
        
        try:
            #message
            message = self.format(record)
            #stream
            stream = self.stream
            
            
            #simple print to account for the lack of a handler in Houdini
            print(message)
            
            
            #flush
            self.flush()
        
        except (KeyboardInterrupt, SystemExit):
            raise
        
        except:
            self.handleError(record)