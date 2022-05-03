import cv2
from app_config.config_helper import ConfigHelper
from platformApi import Consumer,Producer
import os
import pickle
import numpy as np
import random

class AttentionUtil:
    def __init__(self):
        self.TOPIC = "app_1"
        self.app_conf = ConfigHelper()
        self.producer = Producer()
        self.consumer = Consumer(self.TOPIC)
        #data format
        # msg = {"route" : "func4","source":TOPIC,"param":[{"value": np.fromstring(data, np.uint8) }]}


    def get_files(self,path):
        files = []
        for f in os.listdir(path):
            if os.path.isfile(os.path.join(path, f)):
                files.append(f)
        return files

    def get_student_emotion(self,name):
        
        recording_path = "attention_manager/data/"+name+"/"
        std_recording = self.get_files(recording_path)
        emotions = [1]
        # print("Recordings Found: "+str(len(std_recording)))
        # emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Sad", 4: "Neutral", 5: "Happy", 6: "Surprised"}
        for file in std_recording:
            
            # print(recording_path+file)
            frame = cv2.imread(recording_path+file)
            frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
            ret, buffer = cv2.imencode('.jpg', frame) 
            frame = buffer.tobytes()
            # msg = {"route" : "func4","source":self.TOPIC,"param":[{"value": np.fromstring(frame, np.uint8) }]}
            # self.producer.putData("pkg_24", pickle.dumps(msg, 0))
            # # self.producer.flush()
            # data = self.consumer.getData()
            # emotions.append(data.value)
            #generate a generate emotion
            emotion = random.randint(0,80)
            if emotion<40:
                emotions.append(-1)
            elif emotion==44:
                emotions.append(0)
            else:
                emotions.append(1)
            # emotions.append(emotion)
        
        # li = [5,4,3,2,3,4,4,3,4,3,5]
        #print highest occuring number in li
        # print(max(set(li), key=li.count))

        #return highest occuring number from emotions
        return  max(set(emotions), key=emotions.count)


    def get_emotions(self):
        emotions = {}
        for student in self.app_conf.get_students():
            emotions[student["student_name"]] = self.get_student_emotion(student["student_name"].lower())
        return emotions
