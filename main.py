print("yes")
from machine import UART,Pin
a = Pin(5,Pin.OUT)
import uos

import time
ch =''
while True:      
    print("beforeCHHH",ch)
    uos.dupterm(None, 1)
    uart = UART(0, 115200)
    if uart.any():
        #ch = uart.read()
        #uart.write(ch)
        uos.dupterm(UART(0, 115200), 1)
        #print("uartRead",uart.read())
        print("chchch",ch)
        if(uart.read() == b'Hel'):
         a.on()
        else:
           a.off()
        print("exited")
    print("final end")
    time.sleep(1)
    print("slept")
