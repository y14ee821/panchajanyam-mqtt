from mqtt_custom import MQTTClient
import time
import uos
import gc
gc.collect()
from utils import *
from machine import UART,Pin
utils = utilities()
class mqttOperations:
    def __init__(self,**kwargs):
      self.inputs = kwargs
      self.inputsFromUno = {
                          "ip1":machine.Pin(4,machine.Pin.IN),
                          "ip2":machine.Pin(12,machine.Pin.IN),
                          "ip3":machine.Pin(13,machine.Pin.IN),
                          "ip4":machine.Pin(14,machine.Pin.IN),
                           }
      print(self.inputs)     
    def sub_cb(self,topic, msg):
      gc.collect()
      print((topic, msg))
      if("received" not in "msg"):
        self.uartCommunication(msg)       
    def connect_and_subscribe(self):
      clientName = self.inputs["client"]+str(time.ticks_ms())
      try:
        gc.collect()
        client = MQTTClient(clientName, self.inputs["broker"],port=self.inputs["port"])
        client.set_callback(self.sub_cb)
        client.connect()
        client.subscribe(self.inputs["topic"])
        print('Connected to %s MQTT broker, subscribed to %s topic with client %s' % (self.inputs["broker"], self.inputs["topic"],clientName))
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
          gc.collect()
          try:
            new_message = client.check_msg()
            time.sleep_ms(1000)
            opString = utils.stringFormatterForJSClient(self.inputsFromUno)
            client.publish(self.inputs["topic"]+"/status",opString)
            gc.collect()
          except Exception as error:
            print("Got Error %s, Restarting the MCU"%(error))
            utils.restart_and_reconnect()

    def uartCommunication(self,incomingData):    
      gc.collect()
      data = incomingData.decode()
      self.inputs["REPL_FLAG"] and uos.dupterm(None, 1)#to deattach uart0 to repl
      uart = UART(0, 115200)
      uart.write(data)
      self.inputs["REPL_FLAG"] and  uos.dupterm(uart, 1)#to attach uart0 to repl
    def espOutputControl(incomingData,outputs):#Not using this in current project
       # incoming data -->  data from MQTT Broker
       #   Example: incomingData=str(msg)[2:len(msg)+2].split("-")  
       # outputs --> list of defined ESP outputs
       #  Example:outputs["op1"] = machine.Pin(5,machine.Pin.OUT)
       #          outputs["op2"] = machine.Pin(4,machine.Pin.OUT) 

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
