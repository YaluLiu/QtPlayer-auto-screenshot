# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainForm.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication , QMainWindow, QMessageBox , QFileDialog, QInputDialog
from PyQt5.QtWidgets import QWidget, QLabel,QLineEdit,QScrollArea
from Ui_MainWindow import Ui_MainWindow
import cv2
import numpy as np 

#检测事件库
import time
from use_docker import detector_leader
from  threading import Lock,Thread
import queue


class PlayerForm( QMainWindow , Ui_MainWindow):  
    def __init__(self):  
        super(PlayerForm,self).__init__()  
        self.setupUi(self)

        # 播放视频初始化
        self.timer_play = QtCore.QTimer()
        self.video_path = None
        self.cap = cv2.VideoCapture()
        self.frame_idx = 0

        # 关联信号与事件
        self.event_connect()

        self.scale = 5      ## 图片缩小比例
        self.img_q = queue.Queue(maxsize = self.img_num)
        self.img_lock = Lock()
        self.detetor = detector_leader()
        self.detetor.set_flags(self.sel_detect_dialog.flags)
        self.detect_fq = queue.Queue()

    def event_connect(self):
        self.fileCloseAction.triggered.connect(self.close)
        self.fileOpenAction.triggered.connect(self.openFile)
        self.streamOpenAction.triggered.connect(self.openStream)
        self.SelectAction.triggered.connect(self.sel_detect)
        self.timer_play.timeout.connect(self.play_frame)

    def openFile(self):
        file,ok= QFileDialog.getOpenFileName(self,"打开","D:/Github/video","All Files (*);;Text Files (*.txt)") 
        if ok:         
            self.video_path = file
            self.play()

    def openStream(self):
        # url输入
        text, ok = QInputDialog.getText(self,
        'Input Dialog', 
        'input rtsp:',
        QLineEdit.Normal,
        "rtsp://linye:linye123@192.168.200.253:554/Streaming/Channels/301")
        if ok:         
            self.video_path = text
            self.play()
    
    # 播放视频
    def play(self):
        self.clean()
        if self.timer_play.isActive() == False:
            self.cap.open(self.video_path)
            if not self.cap.isOpened():
                QMessageBox.warning(
                    self, "警告",
                    "无法打开视频\n"
                    "请检查视频格式是否正确"
                )
            else:
                self.resize_by_video()
        else:
            self.clean()

    def resize_by_video(self):
        # get vcap property 

        # video-frame w,h
        self.frame_w = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # float
        self.frame_h = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) # float
        # image-view w,h
        self.img_w = int(self.frame_w / self.scale)
        self.img_h = int(self.frame_h / self.scale)

        # resize 图片栏
        self.scroll.show()
        self.imgarea.resize(self.img_w, self.img_h * self.img_num)#######设置scrollarea幕布的尺寸
        self.setFixedWidth(self.frame_w + self.img_w + 50)
        self.setFixedHeight(self.frame_h + self.menu_height)

        #开启播放任务
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.timer_play.start(self.fps)
        #开启检测任务
        self.exit_flag = False
        t = Thread(target = self.detect_frame)
        t.start()

        # #状态栏
        # self.statusbar.showMessage("Fire")

    def play_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            QMessageBox.information(
                    self, "提示",
                    "播放完毕"
                )
            self.clean()
            return
        
        # frame 转换成 QPixmap
        # frame_show = cv2.resize(frame, self.frame_size, interpolation = cv2.INTER_AREA)
        frame_show = np.copy(frame)
        frame_show = cv2.cvtColor(frame_show, cv2.COLOR_BGR2RGB)
        frame_showImage = QtGui.QImage(frame_show.data, self.frame_w, self.frame_h, QtGui.QImage.Format_RGB888)
        #显示视频
        self.video_wnd.setPixmap(QtGui.QPixmap.fromImage(frame_showImage))
        #显示图片
        with self.img_lock:
            for img_idx in range(self.img_q.qsize()):
                self.img_wnds[img_idx].setPixmap(QtGui.QPixmap.fromImage(self.img_q.queue[img_idx]))

        #每隔一秒post一帧
        self.frame_idx += 1
        if self.frame_idx == 24:
            self.frame_idx = 0
            self.detect_fq.put(frame)

    # 检测图片
    def detect_frame(self):
        while not self.exit_flag:
            try:
                frame = self.detect_fq.get(timeout = 1)
                states = self.detetor.detect(frame)
                if True in states:
                    self.put_img(frame)
            except queue.Empty:
                continue
            except Exception as e:
                print("Error",e)
                break

    # 更新图片数组
    def put_img(self,frame):
        img_view = cv2.resize(frame, (self.img_w,self.img_h), interpolation = cv2.INTER_AREA)
        img_view = cv2.cvtColor(img_view, cv2.COLOR_BGR2RGB)
        img_view = QtGui.QImage(img_view.data, self.img_w, self.img_h, QtGui.QImage.Format_RGB888)
        with self.img_lock:
            if self.img_q.full():
                self.img_q.get_nowait()
            self.img_q.put_nowait(img_view)

    # 释放内存
    def clean(self):
        self.exit_flag = True
        if self.cap.isOpened():
            self.cap.release()
        if self.timer_play.isActive():
            self.timer_play.stop()
        self.video_wnd.clear()
        for img_idx in range(self.img_num):
            self.img_wnds[img_idx].clear()
        while not self.img_q.empty():
            self.img_q.get()
        while not self.detect_fq.empty():
            self.detect_fq.get()
        self.frame_idx = 0
        self.scroll.hide()

    def sel_detect(self):
        detect_flags = self.sel_detect_dialog.show_dialog()
        self.detetor.set_flags(detect_flags)

    # 退出程序
    def closeEvent(self, event):
        reply = QMessageBox.question(self,
                                               "退出",
                                               "是否关闭播放器？",
                                               QMessageBox.Yes | QMessageBox.No,
                                               QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.clean()
            event.accept()
        else:
            event.ignore()