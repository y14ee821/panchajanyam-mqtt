# Complete project details at https://RandomNerdTutorials.com
from mqtt_custom import MQTTClient
import time
from utils import *
from machine import Pin

utils = utilities()
class mqttOperations:
    #obj = mqttOperations(topic = "test",message = "daddy",connectionType = "publish",client = "lohit")
    def __init__(self,**kwargs):
      self.inputs = kwargs
      print(self.inputs)
    def sub_cb(self,topic, msg):
      outputs = {}
      print((topic, msg))
      #op1:1-op2:1
      #outputs = utils.opInitialization()#fetches pin numbers from json and enables Pins in output mode 
      outputs["op1"] = machine.Pin(5,machine.Pin.OUT)
      outputs["op2"] = machine.Pin(4,machine.Pin.OUT)
      if("received" not in "msg"):
        incomingData=str(msg)[2:len(msg)+2].split("-")
        print(incomingData)
        for i in incomingData:
          try:
            print("incomingData",i)
            if(int(i.split(":")[-1])==1):
              print("split",i.split(":")[0])
              type(outputs[i.split(":")[0]])
              outputs[i.split(":")[0]].on()
            else:
              print("split",i.split(":")[0])
              type(outputs[i.split(":")[0]])
              outputs[i.split(":")[0]].off()
          except Exception as error:
            print("error",error)





    def connect_and_subscribe(self):
      try:
        client = MQTTClient(self.inputs["client"], self.inputs["broker"],port=self.inputs["port"])
        client.set_callback(self.sub_cb)
        client.connect()
        client.subscribe(self.inputs["topic"])
        print('Connected to %s MQTT broker, subscribed to %s topic' % (self.inputs["client"], self.inputs["topic"]))
        return client
      except Exception as error:
        print("Error in contacting the broker - %s"%(error))

    def executor(self):
        try:
          client = self.connect_and_subscribe()
        except Exception as error:
          print("Got Error %s, Restarting the MCU"%(error))
          utils.restart_and_reconnect()

        while True:
          try:
            new_message = client.check_msg()
            #if new_message != 'None':
            #  client.publish(self.inputs["topic"], b'received')
            time.sleep(0.25)
          except Exception as error:
            print("Got Error %s, Restarting the MCU"%(error))
            utils.restart_and_reconnect()