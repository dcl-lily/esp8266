from machine import Pin, I2C, SPI
from ssd1306 import SSD1306_I2C  # 导入SSD控制的OLED程序
import network
import time
import os, sdcard
import json, framebuf

# 连接无线网络的，这里就不多说了，前面有单独视频讲解
net = network.WLAN(network.STA_IF)
if not net.isconnected():
    net.active(True)
    net.connect("Lily", "Meiyoumima")
    while not net.isconnected():
        time.sleep(1)

SCL = Pin(2, Pin.OUT)
SDA = Pin(0, Pin.OUT)
i2c = I2C(-1, scl=SCL, sda=SDA)
oled = SSD1306_I2C(128, 64, i2c)

# 初始化SD卡
SD_SCK = Pin(12)
SD_MOSI = Pin(14)
SD_MISO = Pin(13)
SD_CS = Pin(4)
spi = SPI(sck=SD_SCK, mosi=SD_MOSI, miso=SD_MISO)
spi.init()
sd = sdcard.SDCard(spi, SD_CS)
vfs = os.VfsFat(sd)   # 初始化fat文件系统
os.mount(sd, "/sd")   # 挂载SD卡到/sd目录下


def image(img_list):
    oled.fill(0)
    for i in img_list:
        oled.hline(i[0], i[1], i[2], 1)
    oled.show()


with open('/sd/a.data', 'r') as f:
    for b in f:
        image(json.loads(b))

f = open('/sd/a1.data', 'rb')
while 1:
    data = bytearray(f.read(1024))
    if not data:
        break
    oled.fill(0)
    fbuf = framebuf.FrameBuffer(data, 128, 64, framebuf.MONO_HLSB)
    oled.blit(fbuf, 0, 0)
    oled.show()
    time.sleep_ms(1)

oled.fill(0)
oled.text("The End", 32, 32, 1)
oled.show()
