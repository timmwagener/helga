

"""
auto_droplet_loader
==========================================

Just there to provide a run function to import auto_droplet.

-----------------------
"""





#Run
#------------------------------------------------------------------
if(__name__ == '__main__'):
    

    #Import
    #------------------------------------------------------------------
    
    #python
    import os
    import sys
    import functools
    import logging
    import subprocess
    
    #PyQt
    from PyQt4 import QtCore
    from PyQt4 import QtGui
    from PyQt4 import uic

    #qdarkstyle
    import qdarkstyle
    

    #Import variable
    do_reload = True
    
    #auto_droplet
    import auto_droplet
    if(do_reload): reload(auto_droplet)

    

    #Run
    #------------------------------------------------------------------

    #app
    app = QtGui.QApplication(sys.argv)

    #load darkstyle
    app.setStyleSheet(qdarkstyle.load_stylesheet(pyside=False))
    
    #auto_droplet_instance
    auto_droplet_instance = auto_droplet.AutoDroplet(parent = None)
    auto_droplet_instance.show()

    #exec
    app.exec_()