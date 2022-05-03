from platformApi import Consumer,Producer
import cv2

class DeviceManager:
    def __init__(self,id):
        # self.app_conf = ConfigHelper()
        self.producer = Producer()
        self.consumer = Consumer(id)
        if id[:4] == 'bulb':
            self.type = 'bulb'
        else:
            self.type = 'fan'
    
    def update_state(self,state):
        img = None
        if self.type=='bulb':
            # data = self.consumer.getData()
            data = 'off'
            if state=='on':
                img = cv2.imread('static/img/img_bulbon.jpg')
                
            else:
                img = cv2.imread('static/img/img_bulboff.jpg')
        
        else:
            if state=='on':
                img = cv2.imread('static/img/fan_on.jpg')
            else:
                img = cv2.imread('static/img/fan_off.jpg')


        ret, jpeg = cv2.imencode('.jpg', img)
        return jpeg.tobytes()
    
