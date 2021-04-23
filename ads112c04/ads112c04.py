"""Main module."""

import time
import smbus
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

ADS112C04_FS = 32768
ADS112C04_REFV = 2.048


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


    def _reset(self):
        self._bus.write_byte(self._address, ADS112C04_CMD_RESET)
    
    def _readrawdata(self):
        retc = self._bus.read_i2c_block_data(self._address, ADS112C04_CMD_RDATA, 2)
        retval = retc[0]*256+retc[1]
        return retval

    def _readdata(self):
        val = self._readrawdata()
        if val > ADS112C04_FS-1:
            val = -ADS112C04_REFV+(val-ADS112C04_FS-1)*ADS112C04_REFV/ADS112C04_FS
        else:
            val = ADS112C04_REFV*val/ADS112C04_FS

        return val

    
    def _startconversion(self):
        self._bus.write_byte(self._address, ADS112C04_CMD_START)

    def _setIDAC(self, val):
        self._writereg(ADS112C04_ADDR_CR2, val & 0x7)


    def _checkdrdy(self):
        return (self._readreg(ADS112C04_ADDR_CR2) >> 7)

    def _setgain(self,val):
        cr0 = self._readreg(ADS112C04_ADDR_CR0)
        cr0  |= (val&0x7)<<3
        self._writereg(ADS112C04_ADDR_CR0, cr0)

    def _setmux(self,val):
        cr0 = self._readreg(ADS112C04_ADDR_CR0)
        cr0  |= (val&0xF)<<4
        self._writereg(ADS112C04_ADDR_CR0, cr0)

    def _setIDAC2mux(self,val):
        cr0 = self._readreg(ADS112C04_ADDR_CR3)
        cr0  |= (val&0x7)<<2
        self._writereg(ADS112C04_ADDR_CR3, cr0)
    def _setIDAC1mux(self,val):
        cr0 = self._readreg(ADS112C04_ADDR_CR3)
        cr0  |= (val&0x7)<<5
        self._writereg(ADS112C04_ADDR_CR3, cr0)




        
