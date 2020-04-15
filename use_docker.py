import cv2
import numpy as np
import json
import requests

class detector(object):
    def __init__(self,host,port,api,cam_id = 0):
        self.host = host
        self.port = port
        self.api = api
        self.cam_id = cam_id
        self.url = "http://{}:{}/{}/{}".format(host,port, api, cam_id)
    def post_image(self,frame):
        frame_encoded = cv2.imencode(".jpg", frame)[1]
        Send_file = {'image': frame_encoded.tostring()}
        jsondata = requests.post(self.url,files=Send_file)

        #output
        if jsondata.status_code == 200:
            return jsondata.json()
        else:
            return None

#=============================7001===============================================================
class climb_detector(detector):
    def __init__(self):
        host = "192.168.200.233"
        port = 7001
        api = "api_detect_climb"
        detector.__init__(self,host,port,api)
    def detect(self,frame):
        json = self.post_image(frame)
        if json is not None:
            print(json)
            return False
        else:
            return None
#=============================7002===============================================================
class violence_detector(detector):
    def __init__(self):
        host = "192.168.200.233"
        port = 7002
        api = "api_detect_violence"
        detector.__init__(self,host,port,api)
    def detect(self,frame):
        json = self.post_image(frame)
        if json is not None:
            print(json)
            return False
        else:
            return None
#=============================7003===============================================================
class abnormal_detector(detector):
    def __init__(self):
        host = "192.168.200.233"
        port = 7003
        api = "api_detect_crowd_abnormal"
        detector.__init__(self,host,port,api)
    def detect(self,frame):
        json = self.post_image(frame)
        if json is not None:
            print(json)
            return False
        else:
            return None
#=============================7004===============================================================
class firearm_detector(detector):
    def __init__(self):
        host = "192.168.200.233"
        port = 7004
        api = "api_detect_firearm"
        detector.__init__(self,host,port,api)
    def detect(self,frame):
        json = self.post_image(frame)
        if json is not None:
            print(json)
            return False
        else:
            return None
#=============================7005===============================================================
class count_detector(detector):
    def __init__(self):
        host = "192.168.200.233"
        port = 7005
        api = "api_crowd_count"
        detector.__init__(self,host,port,api)
    def detect(self,frame):
        json = self.post_image(frame)
        if json is not None:
            print(json)
            return False
        else:
            return None
#=============================7006===============================================================
class fire_detector(detector):
    def __init__(self):
        host = "192.168.200.233"
        port = 7006
        api = "api_detect_fire"
        detector.__init__(self,host,port,api)
    def detect(self,frame):
        json = self.post_image(frame)
        if json is not None:
            return json['fire']['status'] == 'yes'
        else:
            return None
#=============================7007===============================================================
#=============================7008===============================================================
#=============================7009===============================================================

class detector_leader():
    def __init__(self):
        self.detector_num = 6
        self.workers = [None] * self.detector_num
        self.workers[0] = climb_detector()
        self.workers[1] = violence_detector()
        self.workers[2] = abnormal_detector()
        self.workers[3] = firearm_detector()
        self.workers[4] = count_detector()
        self.workers[5] = fire_detector()
    def set_flags(self,flags):
        assert(len(flags) == self.detector_num)
        self.flags = flags

    def detect(self,frame):
        states = [False] * self.detector_num
        for idx in range(self.detector_num):
            states[idx] = self.workers[idx].detect(frame) if self.flags[idx] else False
        return states

if __name__ == "__main__":
    frame = cv2.imread("video/fire_1.jpg")
    fire = fire_detector()
    json = fire.detect(frame)
    print(json)


