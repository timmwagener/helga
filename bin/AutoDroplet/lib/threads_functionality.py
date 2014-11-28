

"""
threads_functionality
==========================================

Module that handles everything related with Droplets and Threads.
It spawns a number of Daemon threads that are always on and checking for a global
queue to retrieve work, if available. The queue contains callables that
represent closures.
"""




#Import
#------------------------------------------------------------------
#python
import sys
import os
import logging
import Queue
import time
import hashlib
import multiprocessing
#PyQt4
from PyQt4 import QtGui
from PyQt4 import QtCore









#WorkerThread class
#------------------------------------------------------------------
class WorkerThread(QtCore.QThread):
    """
    Thread executing tasks from a given tasks queue
    """

    #Signals
    #------------------------------------------------------------------

    restart = QtCore.pyqtSignal()
    setup_timer = QtCore.pyqtSignal()
    sgnl_task_done = QtCore.pyqtSignal()

    


    
    def __init__(self, 
                    queue, 
                    logging_level = logging.DEBUG,
                    thread_id = 0,
                    thread_interval = 2000):
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

        #thread_interval
        self.thread_interval = thread_interval #ONLY IMPORTANT FOR INITIAL STARTUP INTERVAL. NOT USED AGAIN

        #thread_id
        self.thread_id = thread_id

        #first_execution
        self.first_execution = True

        #timer_created
        self.timer_created = False



        #logger
        #------------------------------------------------------------------
        
        #logger
        self.logger = logging.getLogger(self.__class__.__name__ +' - ' + str(self.thread_id))
        self.logging_level = logging_level
        self.logger.setLevel(self.logging_level)

        #stream_handler
        stream_handler = logging.StreamHandler(sys.stdout)
        #add
        self.logger.addHandler(stream_handler)


        #Connections
        #------------------------------------------------------------------
        
        self.restart.connect(self.on_restart)
        self.setup_timer.connect(self.on_setup_timer)
        

    


    


    #pyqtSlots
    #------------------------------------------------------------------
    
    @QtCore.pyqtSlot()
    def on_restart(self):
        """
        Restart thread under certain conditions
        """

        #is finished?
        if (self.isFinished()):
            
            #start
            self.start()


    @QtCore.pyqtSlot()
    def on_setup_timer(self):
        """
        Setup self.thread_timer
        """

        #thread_timer
        self.thread_timer = QtCore.QTimer()
        self.thread_timer.setObjectName('thread_timer')
        self.thread_timer.timeout.connect(self.restart)
        self.thread_timer.start(self.thread_interval)

        #log
        self.logger.debug('thread_timer created')

        #set timer_created
        self.timer_created = True



    

    #Getter & Setter
    #------------------------------------------------------------------

    def set_queue(self, queue):
        """
        Set self.queue
        """

        #set
        self.queue = queue

        #log
        self.logger.debug('Reset queue')
    

    #Run
    #------------------------------------------------------------------
    
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
                #notify queue
                self.queue.task_done()
                #notify gui
                self.sgnl_task_done.emit()
                    









#ThreadsFunctionality class
#------------------------------------------------------------------
class ThreadsFunctionality(QtCore.QObject):
    """
    Class that manages the QThread daemon threads.
    """

    

    #Signals
    #------------------------------------------------------------------

    do_update_threads = QtCore.pyqtSignal()

    



    def __new__(cls, *args, **kwargs):
        """
        ThreadsFunctionality instance factory.
        """

        #threads_functionality_instance
        threads_functionality_instance = super(ThreadsFunctionality, cls).__new__(cls, args, kwargs)

        return threads_functionality_instance

    
    def __init__(self,
                    logging_level = logging.DEBUG,
                    set_thread_count_to_half_of_max = True,
                    queue = None):
        """
        Customize instance.
        """

        #super
        self.parent_class = super(ThreadsFunctionality, self)
        self.parent_class.__init__()

        self.setObjectName(self.__class__.__name__)


        #logger
        #------------------------------------------------------------------
        #logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logging_level = logging_level
        self.logger.setLevel(self.logging_level)

        #stream_handler
        stream_handler = logging.StreamHandler(sys.stdout)
        #add
        self.logger.addHandler(stream_handler)


        #instance variables
        #------------------------------------------------------------------

        #max_threads
        self.max_threads = multiprocessing.cpu_count()
        
        #thread_count
        self.thread_count = self.max_threads
        #set_thread_count_to_half_of_max
        if (set_thread_count_to_half_of_max and 
            self.max_threads > 1):
            
            #set thread count to half of max
            self.thread_count = int(self.max_threads / 2)


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

    def get_thread_list(self):
        """
        Return self.thread_list
        """

        return self.thread_list

    
    @QtCore.pyqtSlot(int)
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


    def reset_queue(self):
        """
        Create new queue and set it on self
        and all threads.
        """

        #create and set self
        self.queue = Queue.Queue()

        #log
        self.logger.debug('Reset queue')

        #set on threads
        self.set_queue_for_threads(self.queue)


    def set_queue_for_threads(self, queue):
        """
        Set queue on threads
        """

        #stop threads
        self.stop_threads()


        #wait till all threads finished
        while (True):
            
            #check if all timer created
            if (all([thread.isFinished() for thread in self.thread_list])):

                break

            #process events
            QtCore.QCoreApplication.processEvents()

        
        #iterate and set
        for thread in self.thread_list:
            
            #set timer
            thread.set_queue(queue)

        #start threads
        self.start_threads()


    @QtCore.pyqtSlot(int)
    def set_logging_level_for_threads(self, logging_level):
        """
        Set logging level on logger for threads.
        The default logging level for threads is logging.WARNING,
        so they are mostly silent initially.
        """

        #iterate and set
        for thread in self.thread_list:
            
            try:
                
                #set logger
                thread.logger.setLevel(logging_level)

                #log
                self.logger.debug('Setting logging level for thread {0} to {1}'.format(thread.thread_id, 
                                                                                        logging_level))

            except:
                
                #log
                self.logger.debug('Error setting logging level for thread {0}'.format(thread.thread_id))



    #Methods
    #------------------------------------------------------------------

    def setup_threads(self, 
                        thread_interval = 2000, 
                        logging_level = logging.DEBUG):
        """
        Start daemon threads.
        """

        #create and initialize max. number threads
        for index in range(self.max_threads):
            
            #worker_thread
            worker_thread = WorkerThread(self.queue, 
                                            thread_id = index,
                                            thread_interval = thread_interval,
                                            logging_level = logging_level)
            #append worker_thread
            self.thread_list.append(worker_thread)
            #start worker_thread
            worker_thread.start()

            #log
            self.logger.debug('Started thread {0}'.format(index))


        #wait till all finished first time
        while (True):
            
            #check if all timer created
            if (all([thread.timer_created for thread in self.thread_list])):

                break

            #process events
            QtCore.QCoreApplication.processEvents()

        #update threads to set active threads to thread_count
        self.do_update_threads.emit()

        
    @QtCore.pyqtSlot()
    def add_to_queue(self, func, *args, **kwargs):
        """
        Adds work to the queue
        """
        
        #add
        self.queue.put((func, args, kwargs))


    @QtCore.pyqtSlot()
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


    @QtCore.pyqtSlot()
    def stop_threads(self):
        """
        Call stop on thread objects thread_timer.
        """

        #iterate and set
        for thread in self.thread_list:
            
            #set timer
            thread.thread_timer.stop()


    @QtCore.pyqtSlot()
    def update_threads(self):
        """
        Stop all threads and restart them. This would be done when
        the self.thread_count variable has been changed.
        """

        #stop threads
        self.stop_threads()

        #start threads
        self.start_threads()


    @QtCore.pyqtSlot()
    def print_queue_size(self):
        """
        Print the current size of the queue.
        """

        self.logger.debug('Queue size: {0}'.format(self.queue.qsize()))


    @QtCore.pyqtSlot(int)
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


    @QtCore.pyqtSlot()
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


