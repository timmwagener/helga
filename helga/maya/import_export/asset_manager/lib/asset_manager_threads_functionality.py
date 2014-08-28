

"""
asset_manager_threads_functionality
==========================================

Module that handles everything related with AssetManager and Threads.
It spawns a number of Daemon threads that are always on and checking for a global
queue to retrieve work, if available. The queue contains callables that
represent closures.
"""




#Import
#------------------------------------------------------------------
#python
import logging
import Queue
import time
import hashlib
import multiprocessing
#PySide
from PySide import QtGui
from PySide import QtCore









#WorkerThread class
#------------------------------------------------------------------
class WorkerThread(QtCore.QThread):
    """
    Thread executing tasks from a given tasks queue
    """

    #Signals
    #------------------------------------------------------------------

    restart = QtCore.Signal()
    setup_timer = QtCore.Signal()

    


    
    def __init__(self, 
                    queue, 
                    logging_level = logging.DEBUG,
                    thread_id = 0,
                    interval = 2000):
        """
        WorkerThread thread that watches the queue from within infinite
        run method call. run() is the only method thats actually
        called from within an own thread. All other methods execute
        in the main thread.
        """

        #super
        self.parent_class = super(WorkerThread, self)
        self.parent_class.__init__()

        self.setObjectName(self.__class__.__name__)

        #instance variables
        #------------------------------------------------------------------

        #queue
        self.queue = queue

        #interval
        self.interval = interval

        #thread_id
        self.thread_id = thread_id

        #first_execution
        self.first_execution = True

        #quit_threads
        self.quit_threads = False


        #logger
        #------------------------------------------------------------------
        
        #logger
        self.logger = logging.getLogger(self.__class__.__name__ +' - ' + str(self.thread_id))
        self.logging_level = logging_level
        self.logger.setLevel(self.logging_level)


        #Connections
        #------------------------------------------------------------------
        
        self.restart.connect(self.on_restart)
        self.setup_timer.connect(self.on_setup_timer)
        


    @QtCore.Slot()
    def on_restart(self):
        """
        Restart thread under certain conditions
        """

        #is finished?
        if (self.isFinished()):
            
            #start
            self.start()


    @QtCore.Slot()
    def on_setup_timer(self):
        """
        Setup self.thread_timer
        """

        #thread_timer
        self.thread_timer = QtCore.QTimer()
        self.thread_timer.setObjectName('thread_timer')
        self.thread_timer.timeout.connect(self.restart)
        self.thread_timer.start(self.interval)

        #log
        self.logger.debug('thread_timer created')



    
    def run(self):
        """
        Run method. Only method that executes in its own thread.
        """

        #Startup
        #------------------------------------------------------------------
        if(self.first_execution):

            #log
            self.logger.debug('Thread first execution')
            
            #setup_timer
            self.setup_timer.emit()
            
            #first_execution
            self.first_execution = False



        #Code
        #------------------------------------------------------------------
        else:
                        
            try:
                func, args, kwargs = self.queue.get(block=False)
            except Queue.Empty:
                self.logger.debug('Queue empty')
                return
            
            try:
                func(*args, **kwargs)
            except Exception, e:
                self.logger.debug('{0}'.format(e))
            finally:
                self.queue.task_done()
                    









#AssetManagerThreadsFunctionality class
#------------------------------------------------------------------
class AssetManagerThreadsFunctionality(QtCore.QObject):
    """
    Class that manages the QThread daemon threads.
    """

    

    #Signals
    #------------------------------------------------------------------

    do_update_threads = QtCore.Signal()

    



    def __new__(cls, *args, **kwargs):
        """
        AssetManagerThreadsFunctionality instance factory.
        """

        #asset_manager_threads_functionality_instance
        asset_manager_threads_functionality_instance = super(AssetManagerThreadsFunctionality, cls).__new__(cls, args, kwargs)

        return asset_manager_threads_functionality_instance

    
    def __init__(self,
                    max_threads = 32,
                    logging_level = logging.DEBUG,
                    max_thread_protection = True,
                    queue = None):
        """
        Customize instance.
        """

        #super
        self.parent_class = super(AssetManagerThreadsFunctionality, self)
        self.parent_class.__init__()

        self.setObjectName(self.__class__.__name__)


        #logger
        #------------------------------------------------------------------
        #logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logging_level = logging_level
        self.logger.setLevel(self.logging_level)


        #instance variables
        #------------------------------------------------------------------

        #max_threads
        self.max_threads = max_threads
        if (max_thread_protection):
            if(self.max_threads > multiprocessing.cpu_count()):
                self.max_threads = multiprocessing.cpu_count()
        
        #thread_count
        self.thread_count = self.max_threads

        #thread_list
        self.thread_list = []

        #queue
        self.queue = queue
        if not(self.queue):
            
            #create
            self.queue = Queue.Queue()
            
            #log
            self.logger.debug('No queue passed as argument. Creating queue.')

        #connect
        self.do_update_threads.connect(self.update_threads)


        

        
        



    #Getter & Setter
    #------------------------------------------------------------------

    @QtCore.Slot(int)
    def set_thread_count(self, value):
        """
        Set self.thread_count
        """

        if (value > self.max_threads):
            self.thread_count = self.max_threads

        elif (value > 0 and value <= self.max_threads):
            self.thread_count = value

        #value smaller 0 = invalid.
        else:
            return

        #update
        self.do_update_threads.emit()


    def get_thread_count(self):
        """
        Return self.thread_count
        """

        return self.thread_count


    def get_max_threads(self):
        """
        Return self.max_threads
        """

        return self.max_threads



    #Methods
    #------------------------------------------------------------------

    def setup_threads(self):
        """
        Start daemon threads.
        """

        #create and initialize max. number threads
        for index in range(self.max_threads):
            
            #worker_thread
            worker_thread = WorkerThread(self.queue, thread_id = index)
            #append worker_thread
            self.thread_list.append(worker_thread)
            #start worker_thread
            worker_thread.start()

            #log
            self.logger.debug('Started thread {0}'.format(index))

        
    @QtCore.Slot()
    def add_to_queue(self, func, *args, **kwargs):
        """
        Adds work to the queue
        """
        
        #add
        self.queue.put((func, args, kwargs))


    @QtCore.Slot()
    def start_threads(self):
        """
        Call start on thread objects thread_timer.
        """

        #iterate and set
        for index, thread in enumerate(self.thread_list):
            
            #if index < thread_count
            if (index < self.thread_count):

                #set timer
                thread.thread_timer.start()


    @QtCore.Slot()
    def stop_threads(self):
        """
        Call stop on thread objects thread_timer.
        """

        #iterate and set
        for thread in self.thread_list:
            
            #set timer
            thread.thread_timer.stop()


    @QtCore.Slot()
    def update_threads(self):
        """
        Stop all threads and restart them. This would be done when
        the self.thread_count variable has been changed.
        """

        #stop threads
        self.stop_threads()

        #start threads
        self.start_threads()


    @QtCore.Slot()
    def print_queue_size(self):
        """
        Print the current size of the queue.
        """

        self.logger.debug('Queue size: {0}'.format(self.queue.qsize()))


    @QtCore.Slot(int)
    def set_interval(self, interval):
        """
        Loop through thread_list and set self.thread_timer interval.
        """

        try:
            
            #iterate and set
            for thread in self.thread_list:
                
                #set timer
                thread.thread_timer.setInterval(interval)
            
            #log
            self.logger.debug('Set interval to: {0} ms'.format(interval))
        
        except:
            
            #log
            self.logger.debug('Error setting timer to interval: {0}'.format(interval))


    @QtCore.Slot()
    def test_setup(self, count = 100):
        """
        Test parallel execution
        """

        for i in range(count):
            
            def mul(x, y):
                print x * y
            
            self.add_to_queue(mul, i, i + 1)

        #log
        self.logger.debug('Added work to queue')


