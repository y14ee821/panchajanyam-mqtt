from machine import Pin
from wifiConnect import connect
from mqtt_handle import mqttOperations
from utils import *

utils = utilities()
if(connect()):# To connect to wifi
    print("Wifi Connection is good!")
    wifi = True
else:
    print("Issue with wifi, please check.")

jsonInputs = utils.jsonHandler()


class mqtt_handle:
    def __init__(self):
        pass

obj = mqttOperations(
        client = jsonInputs["client"],
        broker = jsonInputs["broker"],
        port = jsonInputs["port"],
        topic = jsonInputs["topic"])
obj.executor()
