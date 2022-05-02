from kafka import KafkaProducer
from kafka.errors import KafkaError
from kafka import KafkaConsumer,  TopicPartition
import threading
import random

KAFKA_IP = "20.213.151.51"
KAFKA_PORT = "9092"

CLIENT_ID = "CO1"+str(random.randint(0,1000))

class Producer:
    def __init__(self):
        self.pip=KAFKA_IP+":"+KAFKA_PORT
        self.cid = str(random.randint(0,10000))#CLIENT_ID
        #self.header = HEADER
        self.producer = KafkaProducer(client_id= self.cid, bootstrap_servers=[self.pip] )

    def putData(self,topic,data):
        self.producer.send(str(topic), value=data )
     

class Consumer:
    def __init__(self, TOPIC_L):
        self.pip=KAFKA_IP+":"+KAFKA_PORT
        self.topic = TOPIC_L
        self.cid = str(random.randint(0,10000))#CLIENT_IDCLIENT_ID
        self.consumer = KafkaConsumer(self.topic, bootstrap_servers=[self.pip])
        print(self.cid)
        
    def getData(self):
        for message in self.consumer:
            return message.value

    def subscribe_Loop_Helper(self):
        for message in self.consumer:
            self.processLoopRequest(message)

    def getDataLoop(self):
        x = threading.Thread(target=self.subscribe_Loop_Helper)
        x.start()
