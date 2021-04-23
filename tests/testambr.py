#!/usr/bin/env python3

import time
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import smbus
from smbus import SMBus

from ads112c04 import ads112c04

I2C_sleep_time = 0.2 # seconds to sleep between each channel reading
bus0 = SMBus(0)
bus1 = SMBus(1)

#addresses = [0x40,0x41,0x43,0x44,0x45,0x46,0x47,0x49,0x4a,0x4c,0x4d,0x4f]
addresses = [0x40]
adcs=[]


for i in range(len(addresses)):
    adc0 = ads112c04.ads112c04(bus0,addresses[i])
    adc0._reset()
#write register 0, AINP=AIN1, AINN=AVSS, PGA disabled and gain to 1
    adc0._setmux(0x9)
#write register 2, set IDAC current to 100uA
    adc0._setIDAC(0x3)
#write register 3, route IDAC2 to AIN1
    adc0._setIDAC2mux(0x2)
    adcs.append(adc0)

    adc0 = ads112c04.ads112c04(bus1,addresses[i])
    adc0._reset()
#write register 0, AINP=AIN1, AINN=AVSS, PGA disabled and gain to 1
    adc0._setmux(0x9)
#write register 2, set IDAC current to 100uA
    adc0._setIDAC(0x3)
#write register 3, route IDAC2 to AIN1
    adc0._setIDAC2mux(0x2)
    adcs.append(adc0)
    
               


for i in range(len(adcs)):
#send a start/SYNC

    adcs[i]._startconversion()

    time.sleep(I2C_sleep_time)

#    print (i,hex(adcs[i]._readreg(0)))
#    print (i,hex(adcs[i]._readreg(2)))

    
    data=adcs[i]._readdata()

    print (i,data)


