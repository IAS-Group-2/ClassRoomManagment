import cv2
from app_config.config_helper import ConfigHelper
from attendence_manager.face_recog import FaceRecognition

class Attendence_Record:
    def __init__(self):
        self.app_conf = ConfigHelper()
        self.MODEL_FR = self.get_model()
        
    def get_model(self):
        MODEL_FR = FaceRecognition(self.get_train_data())
        return MODEL_FR

    def get_train_data(self):
        train_images = []
        train_lables = ["Gagan", "Karan", "Sarthak"]
        for i in range(1,4):
            img = cv2.imread("attendence_manager/data/train/"+str(i)+".png")
            train_images.append((train_lables[i-1], img))
        return train_images

    def get_recordings(self):
        record_frames = []
        for i in range(1,100):
            img = cv2.imread("attendence_manager/data/recordings/"+str(i)+".jpg")
            record_frames.append(img)
        return record_frames

    def get_attendence(self):
        names = self.MODEL_FR.recognise(self.get_recordings())
        return names

    def send_mail(self,content):
        prof_mail = self.app_conf.get_mail_prof()
        print(content)