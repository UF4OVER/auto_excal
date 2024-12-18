# -*- coding: utf-8 -*-
# -------------------------------

#  @Project : upper_computer
#  @Time    : 2024 - 12-18 18:05
#  @FileName: uart_to_i2c.py
#  @Software: PyCharm 2024.1.6 (Professional Edition)
#  @System  : Windows 11 23H2
#  @Author  : 33974
#  @Contact : 
#  @Python  : 3.10

# -------------------------------
import serial
import time


class UartToI2c:
    """
    UartToI2c类
    """

    def __init__(self, ser, channel):
        self.i2c_channel: int = channel
        self._ser = ser

    def i2c_init(self):
        """
        初始化i2c
        (1,0,0,0)
        :return:
        """
        self._ser.write(bytearray([0xFF, 0xFF, 0x01, 0x00, 0x00, 0x00, 0xED, 0XED]))

    def i2c_scan(self) -> bytes:
        """
        扫描i2c设备
        (1f,0,0,0)
        :return:
        """
        self._ser.write(bytearray([0xFF, 0xFF, 0x1F, 0x00, 0x00, 0x00, 0xED, 0XED]))
        return self._ser.readline()

    def i2c_start(self):
        """
        在总线上触发START状态（SCL为高电平时，SDA转为低电平）
        (1,1,1,1)
        :return:
        """
        self._ser.write(bytearray([0xFF, 0xFF, 0x01, 0x01, 0x01, 0x01, 0xED, 0XED]))

    def i2c_stop(self):
        """
        在总线上触发STOP状态（SCL为高电平时，SDA转为高电平）
        (0,0,0,0)
        :return:
        """
        self._ser.write(bytearray([0xFF, 0xFF, 0x00, 0x00, 0x00, 0x00, 0xED, 0XED]))

    def i2c_start_bus_write(self):
        """
        开始:: buf中的数据写入到总线，并返回写入的字节数
        (1,1,1,1)
        :return:
        """

        self._ser.write(bytearray([0xFF, 0xFF, 0xFF, 0x00, 0x00, 0xFF, 0xED, 0XED]))

    def i2c_end_bus_write(self):
        """
        结束:: buf中的数据写入到总线，并返回写入的字节数
        (1,1,1,1)
        :return:
        """

        self._ser.write(bytearray([0xFF, 0xFF, 0xED, 0x00, 0x00, 0xED, 0xED, 0XED]))

    def i2c_write(self, data: bytes):
        """
        向i2c总线写入数据
        :param data:
        :return: None
        """
        self.i2c_start_bus_write()
        time.sleep(1e-3)
        self._ser.write(data)
        time.sleep(1e-3)
        self.i2c_end_bus_write()

    def i2c_read_from(self, addr, nbytes) -> bytes:
        """
        从i2c设备读取数据
        (0x9f,3,addr,nbytes)
        :param addr:
        :param nbytes:
        :return:
        """
        self._ser.write(bytearray([0xFF, 0xFF, 0x9F, 0x03, addr, nbytes, 0xED, 0XED]))
        return self._ser.readline()

    def i2c_write_to(self, addr, nbytes):
        """
        向i2c设备写入数据
        (0x9f,0,addr,nbytes)
        :param addr:
        :param nbytes:
        :return:
        """
        self._ser.write(bytearray([0xFF, 0xFF, 0x9F, 0x03, addr, nbytes, 0xED, 0XED]))


def main():
    print("start!")
    while 1:
        pass


if __name__ == "main":
    main()
