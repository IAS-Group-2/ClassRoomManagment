from flask import *  
import pymongo
from platformApi import Consumer,Producer
import numpy as np
import cv2
from app_config.config_helper import ConfigHelper 
from attendence_manager.attendance_util import Attendence_Record
from attention_manager.attention_util import AttentionUtil
from motion_detection.detectionUtil import VideoFeed
from device_manager.deviceUtil import DeviceManager

# def getdata():
#     CONNECTION_STRING = "mongodb://20.228.199.180:3000/"
#     client = pymongo.MongoClient(CONNECTION_STRING)
#     db = client["VMDatabase"]
#     collection = db.vm_details
#     result=collection.find({})
#     return result

app = Flask(__name__)
conf_helper = ConfigHelper()
producer = Producer()





def gen_frames(topic):
    con = Consumer(topic)
    global detect
    while True:
        img = con.getData()
        nparr = np.frombuffer(img, np.uint8)
        # producer.send('model', headers=[('topic',b'app_1')], value=msg.value)
        # producer.flush()
        #print(head)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        try:
            ret, buffer = cv2.imencode('.jpg', cv2.flip(frame,1))
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        except Exception as e:
            pass

def detect_motion(sensor):
    feed = VideoFeed(sensor)
    while True:
        frame = feed.get_frame()

        if frame != None:
            global_frame = frame
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

device_state = {"bulb1":"on","bulb2":"off","bulb3":"on","fan1":"off","fan2":"on","fan3":"off"}
def update_device(id,type="bulb"):
    device = DeviceManager(id)
    while True:
        new_feed = device.update_state(device_state[id])
        yield (b'--frame\r\n'
                        b'Content-Type: image/jpg\r\n\r\n' + new_feed + b'\r\n\r\n')

@app.route('/')  
def home():
    dict={}
    res = not bool(dict)
    return render_template('login.html',res = res , dict = dict)


@app.route('/video_feed/<topic>')
def video_feed(topic):
    return Response(gen_frames(topic), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/motion_feed/<sensor>')
def motion_feed(sensor):
    return Response(detect_motion(sensor), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/device_update/<id>')
def device_update(id):
    return Response(update_device(id), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/signal_device/<id>/<state>')
def signal_device(id,state):
    device_state[id] = state
    return "Got it"
    # return Response(update_device(id), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/motionDetection')
def motionDetection():
    cameras = conf_helper.get_camera_sensors()
    return render_template('motion_detection.html',camera_data = cameras)

@app.route('/registerClass')  
def registerClass():
    return render_template('registerClass.html')


@app.route('/storeFormdata',methods = ['POST', 'GET'])  
def storeFormdata():
    # Here We have to store Data to DataBase 
    return redirect('/')


@app.route('/dashboard',methods = ['POST', 'GET'])  
def dashboard():
    # Here We have to store Data to DataBase 
    return render_template('dashboard.html')



@app.route('/recordAttendance',methods = ['POST', 'GET'])  
def recordAttendance():
    cameras = conf_helper.get_camera_sensors()
    camera_count = len(cameras)
    return render_template('recordAttendance.html', camera_count = camera_count, camera_data = cameras)

@app.route('/attentionDashboard',methods = ['POST', 'GET'])  
def attentionDashboard():
    agent_attention = AttentionUtil()
    emotions = agent_attention.get_emotions()
    student_data = conf_helper.get_students()
    return render_template('attentionDashboard.html', emotions = emotions, student_data = student_data)

@app.route('/process_attendence')  
def process_attendence():
    agent_att = Attendence_Record()
    attendence = agent_att.get_attendence()
    agent_att.send_mail(attendence)
    return render_template('registerClass.html')

@app.route('/deviceDashBoard')  
def deviceDashBoard():
    return render_template('device_dashboard.html')

@app.route('/settings')  
def settings():
    return render_template('settings.html')

if __name__ == '__main__':  
    app.run(debug = True,port=5002)  