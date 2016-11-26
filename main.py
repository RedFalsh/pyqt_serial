#! usr/bin/python
# coding=utf-8

from PyQt5.QtWidgets import QDialog,QApplication,QMainWindow,QMessageBox,QWidget
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import css
from  main_ui import Ui_MainWindow
import threading
from my_serial import SerialHelper
from my_plot import MyStaticMplCanvas
import logging
import binascii
import time

import serial
import serial.tools.list_ports
import os

class mywindow(QMainWindow , Ui_MainWindow):
    # checkBox_isClearClooseLine_Signal = pyqtSignal()
    # plot_updateSignal = pyqtSignal()
    def __init__(self):
        super(mywindow,self).__init__()
        self.setupUi(self)
        self.setStyleSheet(css.cssstyle)#加载css格式
        self.UpdateSerialShow()


        self.pushButton_OpenSerial.clicked.connect(self.OpenCloserSer)
        self.radioButton_RecvSetting_ASCII.setChecked(True)
        self.radioButton_SendSetting_ASCII.setChecked(True)
        self.pushButton_Send.clicked.connect(self.SerialSend)
        self.pushButton_clear.clicked.connect(self.SerialClear)
        self.lineEdit_RepeatSend_ms.setText('1')
        self.checkBox_RepeatSend.clicked.connect(self.RepeatSend)


        self.plot = MyStaticMplCanvas(QWidget(self))
        self.verticalLayout_matplot.addWidget(self.plot)
        self.pushButton_LineUpdate.clicked.connect(self.line_show)
        self.pushButton_LineClear.clicked.connect(self.plot.clear_figure)

    def UpdateSerialShow(self):
        self.comboBox_port.clear()
        port_list = list(serial.tools.list_ports.comports())
        if len(port_list) > 0:
            for every_port_list in port_list:
                self.comboBox_port.addItem(every_port_list[0]+':'+every_port_list[1])

    def OpenCloserSer(self):
        Port = (self.comboBox_port.currentText())
        BaudRate = (self.comboBox_baudrate.currentText())
        ByteSize = (self.comboBox_bytesize.currentText())
        Parity = (self.comboBox_parity.currentText())
        Stopbits = (self.comboBox_stopbits.currentText())

        end = Port.find(':')
        Port = Port[0:end]
        print(Port,Port,BaudRate,ByteSize,Parity,Stopbits)
        if self.pushButton_OpenSerial.text() == "open":
            try:
                self.ser = SerialHelper(Port = Port,BaudRate=BaudRate,ByteSize=ByteSize,Parity=Parity,Stopbits=Stopbits,Dtr=True,Rts=True)
                self.ser.start()
                if self.ser.alive:
                    '''串口打开成功要打开串口接收线程'''
                    # self.thread_read = threading.Thread(target=self.SerialRead)
                    # self.thread_read.setDaemon(True)
                    # self.thread_read.start()

                    self.timer_read = QTimer()
                    self.timer_read.timeout.connect(self.SerialRead)
                    self.timer_read.start(100)

                    #QMessageBox.warning(self,"Yes","打开串口成功",QMessageBox.Yes)
                    self.comboBox_port.setEnabled(False)
                    self.pushButton_OpenSerial.setText("close")

            except Exception as e:
                QMessageBox.warning(self,"错误",logging.error(e),QMessageBox.Yes)

        elif self.pushButton_OpenSerial.text() == "close":
            if self.ser.stop():
                self.timer_read.stop()
                self.comboBox_port.setEnabled(True)
                self.pushButton_OpenSerial.setText("open")

    def SerialRead(self):
        '''串口接收'''
        if self.ser.alive:
            try:
                n = self.ser.l_serial.inWaiting()
                if n:
                    if self.radioButton_RecvSetting_HEX.isChecked():
                        self.receive_data = self.ser.l_serial.read(n)
                        'binascii.b2a_hex()转换btyes为十六进制btyes'
                        self.receive_data = binascii.b2a_hex(self.receive_data)
                        'decode将bytes转换为str'
                        self.receive_data = str(self.receive_data.decode())
                        self.plot.point_y += self.receive_data

                    if self.radioButton_RecvSetting_ASCII.isChecked():
                        self.receive_data = self.ser.l_serial.read(n).decode("gbk")

                    # if self.checkBox_RepeatSend.isChecked():


                    Cusor = self.textBrowser_Recv.textCursor()
                    Cusor.movePosition(QTextCursor.End)
                    self.textBrowser_Recv.append(self.receive_data)
            except Exception as e:
                logging.error(e)

    def RepeatSend(self):
        '''重复发送'''
        try:
            if self.ser.alive:
                if self.checkBox_RepeatSend.isChecked():
                    self.timer_RepeatSend = QTimer()
                    self.timer_RepeatSend.timeout.connect(self.SerialSend)

                    time = self.lineEdit_RepeatSend_ms.text()
                    s_ms = self.comboBox_s_ms.currentText()
                    if time:
                        if s_ms == 'ms':
                            self.timer_RepeatSend.start(int(time))
                        else:
                            self.timer_RepeatSend.start(int(time)*1000)
                else:
                    self.timer_RepeatSend.stop()
        except:
            QMessageBox.warning(self, "错误", '串口没有打开！', QMessageBox.Yes)
            self.checkBox_RepeatSend.setChecked(False)

    def SerialSend(self):
        '''串口发送'''
        try:
            if self.ser.alive:
                data = self.textEdit_SendSerial.toPlainText()
                if self.radioButton_SendSetting_HEX.isChecked():
                    err = self.ser.write(str(data), isHex=True)
                    if err == 'error':
                        QMessageBox.warning(self, "错误", '十六进制格式发送错误！', QMessageBox.Yes)
                        self.timer_RepeatSend.stop()
                        self.checkBox_RepeatSend.setChecked(False)
                if self.radioButton_SendSetting_ASCII.isChecked():
                    self.ser.write(str(data), isHex=False)
        except:
            QMessageBox.warning(self, "错误", '串口没有打开！', QMessageBox.Yes)

    def SerialClear(self):
        '''清楚数据'''
        self.textBrowser_Recv.setText("")
        self.textEdit_SendSerial.setText("")

    def line_show(self):
        # self.plot.point_y += data
        if self.checkBox_LineShow.isChecked():
            self.plot.update_figure()
        # else:
        #     self.checkBox_RepeatSend.setChecked(False)
import sys
app = QApplication(sys.argv)
form = mywindow()
form.show()
app.exec_()
# if __name__=="__main__":
#     import sys
#     app=QApplication(sys.argv)
#     myshow=mywindow()
#     myshow.show()
#     sys.exit(app.exec_())
