import json
class ConfigHelper:
    def __init__(self):
        self.conf = self.populate_config("app_config/app_config.json")
        self.sensor_count = self.conf["sensor_count"]
        
    def populate_config(self,path):
        with open(path) as json_file:
            self.config = json.load(json_file)
        return self.config["sensor_data"]

    def get_camera_sensors(self):
        return self.conf["data"]["camera"]
    
    def get_mail_prof(self):
        return self.conf["prof_email"]
    
    def get_students(self):
        return self.conf["student_data"]
