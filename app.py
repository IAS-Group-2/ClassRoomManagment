from attendence_manager.attendance_util import Attendence_Record
from platformApi import Consumer,Producer
from app_config.config_helper import ConfigHelper 
from flask_mail import Mail
from flask import *  
import numpy as np
import json
import cv2
import os

def filewrite(classid,password):
    path = 'app_config/'
    file = open(path+'UserRegister.json','wb')
    data={
        "classid":classid,
        "password":password
    }
   
    jsonstr=json.dumps(data)
    file.write(jsonstr.encode('utf-8'))
    file.close()

app = Flask(__name__)
conf_helper = ConfigHelper()
producer = Producer()
mail = Mail()

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

def send_mail(attendance):
    attendance = str(attendance)
    mail.send_message('Hello',sender = 'sartthakrawatt@gmail.com',recipients = ['moviesme033@gmail.com'], body = attendance)
    

@app.route('/')  
def home():
    dict={}
    res = False
    filepath = 'app_config/UserRegister.json'
    if os.stat(filepath).st_size == 0:
        res=True
    else:
        res=False
        
    # print("res = ",res)
    return render_template('login.html',res = res , dict = dict)

@app.route('/video_feed/<topic>')
def video_feed(topic):
    return Response(gen_frames(topic), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/registerClass')  
def registerClass():
    return render_template('registerClass.html')

@app.route('/storeFormdata',methods = ['POST', 'GET'])  
def storeFormdata():
    # Here We have to store Data to DataBase 
    classid = request.form['classid']
    password = request.form['password']
    filewrite(classid, password)
    return redirect('/')

@app.route('/dashboard',methods = ['POST', 'GET'])  
def dashboard():
    # Here We have to store Data to DataBase 
    classid = str(request.form['classid'])
    password = str(request.form['password'])
    
    path = 'app_config/'
    file = open(path+'UserRegister.json','rb')
    userdata = json.load(file)
    if(classid == userdata['classid'] and password == userdata['password']):
        print(userdata)
        return render_template('dashboard.html')
    else:
        return redirect('/')

@app.route('/recordAttendance',methods = ['POST', 'GET'])  
def recordAttendance():
    cameras = conf_helper.get_camera_sensors()
    camera_count = len(cameras)
    return render_template('recordAttendance.html', camera_count = camera_count, camera_data = cameras)

@app.route('/process_attendence')  
def process_attendence():
    agent_att = Attendence_Record()
    attendence = agent_att.get_attendence()
    agent_att.send_mail(attendence)
    return render_template('registerClass.html')

@app.route('/settings')  
def settings():
    return render_template('settings.html')

@app.route('/detect_fire')  
def detect_fire():
    # TOPIC = config.SENSOR_1
    TOPIC = "smoke_detector_SH1"
    consumer = Consumer(TOPIC)
    signal = consumer.getData().decode('utf-8')
    signal = json.loads(signal)
    print(signal)
    return signal

@app.route('/fire')  
def fire():
    return render_template('fire.html')

app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 465,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'sartthakrawatt@gmail.com',
    MAIL_PASSWORD = 'space bar'
)

mail.init_app(app)

if __name__ == '__main__':  
    app.run(debug = True,port=5002)  
