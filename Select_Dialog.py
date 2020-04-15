import sys
from PyQt5.QtWidgets import QDialog,QGroupBox,QCheckBox,QPushButton
from PyQt5.QtWidgets import QHBoxLayout,QVBoxLayout
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
import json

class DetectDialog(QDialog):
    def __init__(self, parent=None):
        super(DetectDialog, self).__init__(parent) 
        
        self.read_config()
        self.init_UI()

    def read_config(self):
        json_cfg = {}
        with open("docker-config.json","r") as f:
            json_cfg = json.load(f)
        self.detector_num = len(json_cfg['docker_list'])
        self.names = [None] * self.detector_num
        self.flags = [None] * self.detector_num
        self.det_box = [None] * self.detector_num
        for idx in range(self.detector_num):
            image_name =  json_cfg["docker_list"][idx]["image_name"]
            if image_name.startswith("detect_"):
                self.names[idx] = image_name[7:]
            else:
                self.names[idx] = image_name
            self.flags[idx] = True
        
    def init_UI(self):
        #选择框
        groupBox = QGroupBox("docker选择")
        groupBox.setFlat( False )
        
        layout = QVBoxLayout()

        for idx in range(self.detector_num):
            self.det_box[idx]= QCheckBox(self.names[idx])
            layout.addWidget(self.det_box[idx])

        # 初始只有一个为True
        self.det_box[5].setChecked(True)

        groupBox.setLayout(layout)

        #退出按钮
        exit_btn = QPushButton("确定")
        exit_btn.clicked.connect(self.close)


        mainLayout = QVBoxLayout()
        mainLayout.addWidget(groupBox)
        mainLayout.addWidget(exit_btn)
        
        self.setLayout(mainLayout)
        self.setWindowFlags(Qt.FramelessWindowHint)

    def show_dialog(self):
        self.exec_()
        return self.flags
    
    def closeEvent(self,evt):
        for idx in range(self.detector_num):
            self.flags[idx] = self.det_box[idx].isChecked()

if __name__ == "__main__":
    app = QApplication(sys.argv)  
    win = DetectDialog()  
    win.show()
    sys.exit(app.exec_())