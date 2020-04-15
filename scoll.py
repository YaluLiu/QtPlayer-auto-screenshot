import sys
from PyQt5 import QtGui,QtCore,QtWidgets
from PyQt5.QtWidgets import *
import cv2
from  queue import Queue
from  threading import Lock
from PyQt5.QtCore import Qt
 
 
class MainWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow,self).__init__()
        self.img_num = 10
        self.scale = 5
        self.fq = Queue(maxsize = self.img_num)
        self.fq_lock = Lock()
        self.UI_resized = False
        self.img_wnds = [None] * self.img_num
        self.init_UI()

    def put_fq(self,frame):
        self.img_w = int(frame.shape[1] / self.scale)
        self.img_h = int(frame.shape[0] / self.scale)
        show = cv2.resize(frame, (self.img_w,self.img_h), interpolation = cv2.INTER_AREA)
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        show = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        with self.fq_lock:
            if self.fq.full():
                self.fq.get_nowait()
            self.fq.put_nowait(show)

        #resize windows
        if not self.UI_resized:
            self.UI_resized = True
            self.scroll.show()
            self.imgarea.resize(self.img_w, self.img_h * self.img_num)#######设置scrollarea幕布的尺寸
            self.setFixedWidth(frame.shape[1] + self.img_w + 50)
            self.setFixedHeight(frame.shape[0])

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = QtGui.QImage(frame.data, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888)
        self.video_wnd.setPixmap(QtGui.QPixmap.fromImage(frame))
        self.show_fq()


    def init_UI(self):
        self.imgarea = QWidget()
        vbox = QVBoxLayout()
        for img_cnt in range(self.img_num):
            self.img_wnds[img_cnt] = QLabel()
            vbox.addWidget(self.img_wnds[img_cnt])
        self.imgarea.setLayout(vbox)
        
        self.scroll = QScrollArea()
        self.scroll.setWidget(self.imgarea)
        self.scroll.hide()

        self.video_wnd = QLabel()

        hbox = QHBoxLayout()
        hbox.addWidget(self.video_wnd)
        hbox.addWidget(self.scroll)
        w = QWidget()
        w.setLayout(hbox)
        self.setCentralWidget(w)

        menu_height = 0
        self.resize(641, 481 + menu_height)
        self.video_wnd.setGeometry(QtCore.QRect(0, menu_height, 641, 481 + menu_height))
        self.move(100,100)

    def show_fq(self):
        with self.fq_lock:
            for frame_idx in range(self.fq.qsize()):
                self.img_wnds[frame_idx].setPixmap(QtGui.QPixmap.fromImage(self.fq.queue[frame_idx]))
        
 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    cv2.waitKey(1000)
    frame = cv2.imread("video/1.jpg")
    for i in range(10):
        mainwindow.put_fq(frame)
    mainwindow.show()
    sys.exit(app.exec_())