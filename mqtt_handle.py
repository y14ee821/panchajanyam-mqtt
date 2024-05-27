# Complete project details at https://RandomNerdTutorials.com
from mqtt_custom import MQTTClient
import time
import uos
from utils import *
from machine import UART,Pin
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
        
        self.uartCommunication(msg)
        for i in incomingData:
          try:
            #print("incomingData",i)
            if(int(i.split(":")[-1])==1):
              #print("split",i.split(":")[0])
              type(outputs[i.split(":")[0]])
              outputs[i.split(":")[0]].on()
            else:
              #print("split",i.split(":")[0])
              type(outputs[i.split(":")[0]])
              outputs[i.split(":")[0]].off()
          except Exception as error:
            #print("error",error)
            continue





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
            #print("new_message",new_message)
            # if new_message != 'None':
             #print("Message received")
            
            client.publish(self.inputs["topic"], b'received')
            time.sleep(0.25)
            self.inputsStatus = {"ip1":machine.Pin(12,machine.Pin.IN), "ip2":machine.Pin(14,machine.Pin.IN)}
            #print(self.inputsStatus["ip1"].value(),self.inputsStatus["ip2"].value())
            #client.publish(self.inputsStatus["topic"]+"/status",f'"ip1":{self.inputsStatus["ip1"]},"ip2":{self.inputs["ip2"]}')
            # try:
            #    self.uartRead()
            # except Exception as uartError:
            #    print("Error in reading the UART",uartError) 
          except Exception as error:
            print("Got Error %s, Restarting the MCU"%(error))
            utils.restart_and_reconnect()

    def uartCommunication(self,incomingData):    
      #print("incomingData",incomingData)  
      data = incomingData.decode()

      self.inputs["REPL_FLAG"] and uos.dupterm(None, 1)#to deattach uart0 to repl
      uart = UART(0, 115200)
      uart.write(data)
      self.inputs["REPL_FLAG"] and  uos.dupterm(uart, 1)#to attach uart0 to repl
    def uartRead(self):
      uos.dupterm(None, 1)
      uart = UART(0, 115200)
      if uart.any():
        ch = uart.read(3)       
        uos.dupterm(UART(0, 115200), 1)
        print(ch)
              