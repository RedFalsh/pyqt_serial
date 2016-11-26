#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
Serial设备通讯帮助类
'''
__author__ = "xiong"
__version__ = "v1.0"
import serial
import binascii
import logging
class SerialHelper(object):
    def __init__(self, Port, BaudRate, ByteSize, Parity, Stopbits, Dtr, Rts):
        '''
        初始化一些参数
        '''
        self.l_serial = None
        self.alive = False
        self.port = Port
        self.baudrate = BaudRate
        self.bytesize = ByteSize
        self.parity = Parity
        self.stopbits = Stopbits
        self.thresholdValue = 64
        self.receive_data = ""
        self.Dtr = Dtr
        self.Rts = Rts
    def start(self):
        '''
        开始，打开串口
        '''
        self.l_serial = serial.Serial()
        self.l_serial.port = self.port
        self.l_serial.baudrate = self.baudrate
        self.l_serial.bytesize = int(self.bytesize)
        self.l_serial.parity = self.parity
        self.l_serial.stopbits = int(self.stopbits)
        self.l_serial.timeout = 0.01
        self.l_serial.dtr = self.Dtr
        self.l_serial.rts = self.Rts
        try:
            self.l_serial.open()
            if self.l_serial.isOpen():
                self.alive = True
        except Exception as e:
            self.alive = False
            return e.args[0]
    def stop(self):
        '''
        结束，关闭串口
        '''
        self.alive = False
        if self.l_serial.isOpen():
            self.l_serial.close()
            return True

    def read(self):
        '''
        循环读取串口发送的数据
        '''
        while self.alive:
            try:
                number = self.l_serial.inWaiting()
                if number:
                    self.receive_data += self.l_serial.read(number).decode()
            except Exception as e:
                logging.error(e)
    def write(self, data, isHex=False):
        '''
        发送数据给串口设备
        '''
        if self.alive:
            if self.l_serial.isOpen():
                if isHex:
                    try:
                        data = data.replace(" ", "").replace("\n", "").replace("0x","")
                        data = binascii.unhexlify(data)
                        self.l_serial.write(data)
                    except:
                        return 'error'
                else:
                    data = data.encode(encoding="gbk")
                    self.l_serial.write(data)