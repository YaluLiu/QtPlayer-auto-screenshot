# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainForm.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from Select_Dialog import DetectDialog

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        #图片Label
        self.img_num = 10  #显示图片个数
        self.img_wnds = [None] * self.img_num
        #滑动栏显示图片

        self.imgarea = QtWidgets.QWidget()
        vbox = QtWidgets.QVBoxLayout()
        for img_cnt in range(self.img_num):
            self.img_wnds[img_cnt] = QtWidgets.QLabel()
            vbox.addWidget(self.img_wnds[img_cnt])
        self.imgarea.setLayout(vbox)


        # # 状态栏
        # self.statusbar = QtWidgets.QStatusBar(MainWindow)
        # MainWindow.setStatusBar(self.statusbar)

        self.scroll = QtWidgets.QScrollArea()
        self.scroll.setWidget(self.imgarea)
        self.scroll.hide()

        #视频窗口
        self.video_wnd = QtWidgets.QLabel()

        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self.video_wnd)
        hbox.addWidget(self.scroll)
        top_line = QtWidgets.QWidget()
        top_line.setLayout(hbox)

        # #暂停按钮
        # self.pause_btn = QtWidgets.QPushButton()
        # self.pause_btn.setIcon(QtGui.QIcon("icons/pause.jpg"))

        # self.sel_btn = QtWidgets.QPushButton("选择检测")
        # bottom_layout = QtWidgets.QHBoxLayout()
        # bottom_layout.addWidget(self.pause_btn)
        # bottom_layout.addWidget(self.sel_btn)
        # bottom_line = QtWidgets.QWidget()
        # bottom_line.setLayout(bottom_layout)

        # main_layout = QtWidgets.QVBoxLayout()
        # main_layout.addWidget(top_line)
        # main_layout.addWidget(bottom_line)

        # main_widget = QtWidgets.QWidget()
        # main_widget.setLayout(main_layout)

        # 菜单栏
        self.menu_height = 30
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setObjectName("menubar")

        # 设置主窗口
        MainWindow.setObjectName("MainWindow")
        MainWindow.setCentralWidget(top_line)
        MainWindow.setMenuBar(self.menubar)

        MainWindow.resize(641, 481 + self.menu_height)
        # self.video_wnd.setGeometry(QtCore.QRect(0, self.menu_height, 641, 481 + self.menu_height))
        # self.menubar.setGeometry(QtCore.QRect(0, 0, 641, self.menu_height))

        self.fileOpenAction = QtWidgets.QAction(MainWindow)
        self.fileOpenAction.setObjectName("fileOpenAction")

        self.streamOpenAction = QtWidgets.QAction(MainWindow)
        self.streamOpenAction.setObjectName("streamOpenAction")

        self.fileCloseAction = QtWidgets.QAction(MainWindow)
        self.fileCloseAction.setObjectName("fileCloseAction")

        #文件
        self.menu_file = QtWidgets.QMenu(self.menubar)
        self.menu_file.setObjectName("menu")

        self.menu_file.addAction(self.fileOpenAction)
        self.menu_file.addAction(self.streamOpenAction)
        self.menu_file.addAction(self.fileCloseAction)

        #编辑
        self.menu_edit = QtWidgets.QMenu(self.menubar)
        self.SelectAction = QtWidgets.QAction(MainWindow)
        self.menu_edit.addAction(self.SelectAction)
        
        self.menubar.addAction(self.menu_file.menuAction())
        self.menubar.addAction(self.menu_edit.menuAction())


        self.sel_detect_dialog = DetectDialog() 

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "主窗口"))
        self.menu_file.setTitle(_translate("MainWindow", "文件"))
        self.menu_edit.setTitle(_translate("MainWindow", "设置"))

        self.fileOpenAction.setText(_translate("MainWindow", "打开文件"))
        self.fileOpenAction.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.streamOpenAction.setText(_translate("MainWindow", "打开流"))
        self.streamOpenAction.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.fileCloseAction.setText(_translate("MainWindow", "关闭"))
        self.fileCloseAction.setShortcut(_translate("MainWindow", "Ctrl+Esc"))

        self.SelectAction.setText(_translate("MainWindow", "检测"))