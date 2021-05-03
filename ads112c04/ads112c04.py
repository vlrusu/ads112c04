"""Main module."""

import time
import SMBus
from smbus import SMBus


ADS112C04_ADDR_CR0              =  0x0
ADS112C04_ADDR_CR1              =  0x1
ADS112C04_ADDR_CR2              =  0x2
ADS112C04_ADDR_CR3              =  0x3

ADS112C04_CMD_RESET              =  0x06
ADS112C04_CMD_START              =  0x08
ADS112C04_CMD_PDOWN              =  0x02
ADS112C04_CMD_RDATA              =  0x10
ADS112C04_CMD_RREG               =  0x20
ADS112C04_CMD_WREG               =  0x40



class ads112c04(object):



    def __init__(self, bus=0, address = 0):

        self._bus = bus
        self._address = address
        

    def _writereg(self, reg = 0, data = 0):
        reg = ADS112C04_CMD_WREG | (reg << 2)
        self._bus.write_byte_data(self._address, reg, data)

    def _readreg(self, reg = 0):
        reg = ADS112C04_CMD_RREG | (reg << 2)
        return self._bus.read_byte_data(self._address, reg)


    def _readdata(self):
        retc = self._bus.read_i2c_block_data(address, ADS112C04_CMD_RDATA, 2)
        retval = retc[0]*256+retc[1]
        return retval

    
    def _startconveersion(self):
        self._bus.write_byte(address, ADS112C04_CMD_START)

    def _setIDAC(self, val):
        self._writereg(ADS112C04_ADDR_CR2, val & 0x7)


    def _checkdrdy(self):
        return (self._readreg(ADS112C04_ADDR_CR2) >> 7)

    def _setgain(self,val):
        cr0 = self._readreg(ADS112C04_ADDR_CR0)
        gain = (val&0x7)<<3
        self._writereg(ADS112C04_ADDR_CR0, 
