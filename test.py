from app_config.config_helper import ConfigHelper
import cv2
from attendence_manager.attendance_util import Attendence_Record
from attention_manager.attention_util import AttentionUtil
from motion_detection.detectionUtil import VideoFeed
from device_manager.deviceUtil import DeviceManager
# conf = Config_Helper()
# print(conf.sensor_count)
# print(conf.get_camera_sensors())

#read all the images
# train_images = []
# for i in range(1,11):
#     train_images.append(cv2.imread("attendance/train/"+str(i)+".jpg"))



# def show_images():
#     for i in range(0,10):
#         cv2.imshow("Image", train_images[i])
#         cv2.waitKey(0)
#         cv2.destroyAllWindows()

att_agent = DeviceManager("bulb1","bulb")

# att_agent.get_student_emotion("sarthak")

img = att_agent.update_state()

#show the image
# cv2.imshow("Image", img)
# cv2.waitKey(5000)



