import cv2
import numpy as np
import json
import requests

config_host = "192.168.200.233"
#config_host = "localhost"

class detector(object):
    def __init__(self,host,port,api,cam_id = 0):
        self.host = config_host
        self.port = port
        self.api = api
        self.cam_id = cam_id
        self.url = "http://{}:{}/{}/{}".format(host,port, api, cam_id)
    def post_frame(self,frame):
        frame_encoded = cv2.imencode(".jpg", frame)[1]
        Send_file = {'image': frame_encoded.tostring()}
        response = requests.post(self.url,files=Send_file)
        return response.json()
    
    def post_image(self,image_path):
        response = requests.post(self.url,files={'image': open(image_path, 'rb')})
        return response.json()

    def detect(self,input):
        if isinstance(input,str):
            return self.post_image(input)
        elif isinstance(input,np.ndarray):
            return self.post_frame(input)

#=============================7001===============================================================
class climb_detector(detector):
    def __init__(self):
        host = config_host
        port = 7001
        api = "api_detect_climb"
        detector.__init__(self,host,port,api)
    def update_mask(self,mask):
        api = "api_save_mask"
        if len(mask.shape) == 3 and mask.shape[2] == 3:
            mask = mask[:,:,0]
        self.mask_url = "http://{}:{}/{}/{}".format(self.host,self.port, api, self.cam_id)
        frame_encoded = cv2.imencode(".jpg", mask)[1]
        Send_file = {'image': frame_encoded.tostring()}
        json = requests.post(self.mask_url,files=Send_file)
        return json.status_code == 200

    # def detect(self,frame): #{'climb_data': [[126, 168, 112, 202]]}
    #     return self.post_frame(frame)
    def get_state(self,response):
        return len(response["climb_data"]) > 0
#=============================7002===============================================================
class violence_detector(detector):
    def __init__(self):
        host = config_host
        port = 7002
        api = "api_detect_violence"
        detector.__init__(self,host,port,api)
    # def detect(self,frame): #{'FindFight': 'True'}
    #     json = self.post_frame(frame)
    #     return json
    def get_state(self,response):
        return response["FindFight"] == "True"
#=============================7003===============================================================
class abnormal_detector(detector):
    def __init__(self):
        host = config_host
        port = 7003
        api = "api_detect_crowd_abnormal"
        detector.__init__(self,host,port,api)
    # def detect(self,frame): #{'crowd_abnormal': False, 'destroy_camera': False}
    #     json = self.post_frame(frame)
    #     return json
    def get_state(self,response):
        return response["crowd_abnormal"] or response["destroy_camera"]
#=============================7004===============================================================
class firearm_detector(detector):
    def __init__(self):
        host = config_host
        port = 7004
        api = "api_detect_firearm"
        detector.__init__(self,host,port,api)
    # def detect(self,frame): #{'guns': [[625, 579, 741, 710]]}
    #     json = self.post_frame(frame)
    #     return json
    def get_state(self,response):
        return len(response["guns"]) > 0
#=============================7005===============================================================
class count_detector(detector):
    def __init__(self):
        host = config_host
        port = 7005
        api = "api_crowd_count"
        detector.__init__(self,host,port,api)
    # def detect(self,frame):      # {'crowd_count':26.6123242}
    #     json = self.post_frame(frame)
    #     return json
    def get_state(self,response):
        return False
#=============================7006===============================================================
class fire_detector(detector):
    def __init__(self):
        host = config_host
        port = 7006
        api = "api_detect_fire"
        detector.__init__(self,host,port,api)
    # def detect(self,frame): #{'fire': {'area': [], 'status': 'yes'}}
    #     json = self.post_frame(frame)
    #     return json['fire']['status'] == 'yes'
    def get_state(self,response): #{'fire': {'area': [], 'status': 'yes'}}
        return response['fire']['status'] == 'yes'
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
            response = self.workers[idx].detect(frame) if self.flags[idx] else False
            states[idx] = self.workers[idx].get_state(response) if self.flags[idx] else False
        return states

if __name__ == "__main__":
    frame = cv2.imread("video/fire_1.jpg")
    fire = fire_detector()
    json = fire.detect(frame)
    print(json)


