# -*- coding: utf-8 -*-

import sys     
from PyQt5.QtWidgets import QApplication
from PlayerForm import PlayerForm

if __name__=="__main__":  
    app = QApplication(sys.argv)  
    win = PlayerForm()  
    win.show()  
    sys.exit(app.exec_()) 
