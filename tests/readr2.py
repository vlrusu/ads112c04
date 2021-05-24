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

#adc has 2 address pins: A0 and A1. each can be tied to DGND, DVDD, SDA, or SCL.
#DGND - digital ground, DVDD - positive digital power supply, AVDD - positive analog power supply, AVSS - negative analog power supply
#SCL - serial clock line - clock data in and out of the device.
#SDA - serial data line - bidirectional communication between host and ADS112C04.
#A1	A0	I2C ADDRESS
#DGND	DGND	100 0000
#DGND	DVDD	100 0001
#DGND	SDA	100 0010
#DGND	SCL	100 0011
#DVDD	DGND	100 0100
#DVDD	DVDD	100 0101
#DVDD	SDA	100 0110
#DVDD	SCL	100 0111
#SDA	DGND	100 1000
#SDA	DVDD	100 1001
#SDA	SDA	100 1010
#SDA	SCL	100 1011
#SCL	DGND	100 1100
#SCL	DVDD	100 1101
#SCL	SDA	100 1110
#SCL	SCL	100 1111

#The codes here are given in hex rather than in binary
#these addresses go from 1000000 to 1001111
addresses = [0x40,0x41,0x43,0x44,0x45,0x46,0x47,0x49,0x4a,0x4c,0x4d,0x4f]
#addresses = [0x40,0x41]
idaccurrent = 1e-3
idacsetting = 0x6
adcs=[]

#When measuring from analog inputs AINx, using configuration register 0:
#1000: AINP (positive) = AIN0, AINN (negative) = AVSS
#1001: AINP = AIN1, AINN = AVSS
#1010: AINP = AIN2, AINN = AVSS
#1011: AINP = AIN3, AINN = AVSS

#setting current source, using configuration register 3:
#001: IDAC2 connected to AIN0
#010: IDAC2 connected to AIN1
#011: IDAC2 connected to AIN2
#100: IDAC2 connected to AIN3

#first measure 1k directly
for i in range(len(addresses)):
    adc0 = ads112c04.ads112c04(bus0,addresses[i])
    adc0._reset()
#write register 0, AINP=AIN1, AINN=AVSS, PGA disabled and gain to 1
    adc0._setmux(0x9)
#write register 2, set IDAC current to 100uA
    adc0._setIDAC(idacsetting)
#write register 3, route IDAC2 to AIN1
    adc0._setIDAC2mux(0x2)
    adcs.append(adc0)

#measure on AIN1
for i in range(len(addresses)):    
    adc0 = ads112c04.ads112c04(bus1,addresses[i])
    adc0._reset()
#write register 0, AINP=AIN1, AINN=AVSS, PGA disabled and gain to 1
    adc0._setmux(0x9)
#write register 2, set IDAC current to 100uA
    adc0._setIDAC(idacsetting)
#write register 3, route IDAC2 to AIN1
    adc0._setIDAC2mux(0x2)
    adcs.append(adc0)
    
               
r1ks=[]

for i in range(len(adcs)):
#send a start/SYNC

    adcs[i]._startconversion()

    time.sleep(I2C_sleep_time)

#    print (i,hex(adcs[i]._readreg(0)))
#    print (i,hex(adcs[i]._readreg(2)))

    
    data=adcs[i]._readdata()
    r=data/idaccurrent
    r1ks.append(r)
#    print (i,data)






#now measure  directly on AIN0
for i in range(len(adcs)):
    adc0 = adcs[i]
    adc0._reset()
#write register 0, AINP=AIN0, AINN=AVSS, PGA disabled and gain to 1
    adc0._setmux(0x8)
#write register 2, set IDAC current to 100uA
    adc0._setIDAC(idacsetting)
#write register 3, route IDAC2 to AIN0
    adc0._setIDAC2mux(0x1)

               
rg1=[]

for i in range(len(adcs)):
#send a start/SYNC

    adcs[i]._startconversion()

    time.sleep(I2C_sleep_time)

#    print (i,hex(adcs[i]._readreg(0)))
#    print (i,hex(adcs[i]._readreg(2)))

    data=adcs[i]._readdata()
    r=data/idaccurrent
    rg1.append(r)
#    print (i,data)




#now measure  directly on AIN3
for i in range(len(adcs)):
    adc0 = adcs[i]
    adc0._reset()
#write register 0, AINP=AIN3, AINN=AVSS, PGA disabled and gain to 1
    adc0._setmux(0xb)
#write register 2, set IDAC current to 100uA
    adc0._setIDAC(idacsetting)
#write register 3, route IDAC2 to AIN3
    adc0._setIDAC2mux(0x4)

               
rg2=[]

for i in range(len(adcs)):
#send a start/SYNC

    adcs[i]._startconversion()

    time.sleep(I2C_sleep_time)

#    print (i,hex(adcs[i]._readreg(0)))
#    print (i,hex(adcs[i]._readreg(2)))

    data=adcs[i]._readdata()
    r=data/idaccurrent
    rg2.append(r)
#    print (i,data)

#measure on AIN2
for i in range(len(adcs)):
    adc0 = adcs[i]
    adc0._reset()
#write register 0, AINP=AIN2, AINN=AVSS, PGA disabled and gain to 1
    adc0._setmux(0xa)
#write register 2, set IDAC current to 100uA
    adc0._setIDAC(idacsetting)
#write register 3, route IDAC2 to AIN2
    adc0._setIDAC2mux(0x3)
    
rw=[]

for i in range(len(adcs)):
#send a start/SYNC

    adcs[i]._startconversion()

    time.sleep(I2C_sleep_time)

    data=adcs[i]._readdata()
    r=data/idaccurrent
    rw.append(r)
    print(i,data)

#Print the measurements in pairs: first is (number, resistance to ground 1, 1k resistance, difference); second is (number, resistance to ground 2, 1k resistance, difference).
#reorder the measurements into a list where their number is the same as the number on the panel

count = 0
rg1_reordered = []
rg2_reordered = []
r1ks_reordered = []
rw_reordered = []

#Initialize the lists in which the measurements will be stored. Set the entries to 0 so that they can be filled in any order, rather than using append(). The entries will not be filled from beginning to end, due to the ordering of the panel.

for i in range(len(2*adcs)): #there are len(adcs) number of measurements of rg1 and len(adcs) number of measurements of rg2, but there are 2*len(adcs) number of measurements of r1ks, since those are printed twice. this means that in rg1_reordered, the even indices (starting from 0) will all have 0 as the entry, and in rg2_reordered, the odd indices will all have 0 as the entry.
    r1ks_reordered.append(0)
    rg1_reordered.append(0)
    rg2_reordered.append(0)
    rw_reordered.append(0)
	
#place the measurements in the reordered lists

for i in range(len(adcs)):
    r = rg1[i] - r1ks[i]
    if (count % 2) == 0: #if count is even
        if count<=23: #first 24 measurements
        #of the first 24 measurements, the even counts are 25 too low
            #print(count+25,rg1[i],r1ks[i],r)
            rg1_reordered[count+25] = rg1[i]
            r1ks_reordered[count+25] = r1ks[i]
            rw_reordered[count+25] = rw[i]
        else:
        #of the last 24 measurements, the even counts are 23 too high
            #print(count-23,rg1[i],r1ks[i],r)
            rg1_reordered[count-23] = rg1[i]
            r1ks_reordered[count-23] = r1ks[i]
            rw_reordered[count-23] = rw[i]
    else: #if i is odd
        if count<=23: #first 24 measurements
        #of the first 24 measurements, the odd counts are 23 too low
            #print(count+23,rg1[i],r1ks[i],r)
            rg1_reordered[count+23] = rg1[i]
            r1ks_reordered[count+23] = r1ks[i]
            rw_reordered[count+23] = rw[i]
        else:
        #of the last 24 measurements, the odd counts are 25 too high
            #print(count-25,rg1[i],r1ks[i],r)
            rg1_reordered[count-25] = rg1[i]
            r1ks_reordered[count-25] = r1ks[i]
            rw_reordered[count-25] = rw[i]
    count+=1
    r = rg2[i] - r1ks[i]
    if (count % 2) == 0:
        if count<=23:
        #of the first 24 measurements, the even counts are 25 too low
            #print(count+25,rg2[i],r1ks[i],r)
            rg2_reordered[count+25] = rg2[i]
            r1ks_reordered[count+25] = r1ks[i]
            rw_reordered[count+25] = rw[i]
        else:
        #of the last 24 measurements, the even counts are 23 too high
            #print(count-23,rg2[i],r1ks[i],r)
            rg2_reordered[count-23] = rg2[i]
            r1ks_reordered[count-23] = r1ks[i]
            rw_reordered[count-23] = rw[i]
    else:
        if count<=23:
        #of the first 24 measurements, the odd counts are 23 too low
            #print(count+23,rg2[i],r1ks[i],r)
            rg2_reordered[count+23] = rg2[i]
            r1ks_reordered[count+23] = r1ks[i]
            rw_reordered[count+23] = rw[i]
        else:
        #of the last 24 measurements, the odd counts are 25 too high
            #print(count-25,rg2[i],r1ks[i],r)
            rg2_reordered[count-25] = rg2[i]
            r1ks_reordered[count-25] = r1ks[i]
            rw_reordered[count-25] = rw[i]
    count+=1

#print the reordered lists
for i in range(len(2*adcs)):
    if (i % 2) == 0: #even numbers will print resistance to ground 2, as on the panel
        r = rg2_reordered[i] - r1ks_reordered[i]
        print(i,rg2_reordered[i],r1ks_reordered[i],r,rw_reordered[i])
    else: #odd numbers will print resistance to ground 1
        r = rg1_reordered[i] - r1ks_reordered[i]
        print(i,rg1_reordered[i],r1ks_reordered[i],r,rw_reordered[i])
