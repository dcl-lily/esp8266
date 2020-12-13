from machine import Pin, SPI
from ssd1306 import SSD1306_SPI  # 导入SSD控制的OLED程序
import network
import time
import framebuf

# 连接无线网络的，这里就不多说了，前面有单独视频讲解
net = network.WLAN(network.STA_IF)
if not net.isconnected():
    net.active(True)
    net.connect("Lily", "Meiyoumima")
    while not net.isconnected():
        time.sleep(1)

# OLDE连线示意，ESP8266开发板
# SCK ---> D5 ---> 14
# MOSI --> D6 ---> 12
# MIOS --> Null-->任意没有用的
# DC   --> D8 ---> 15
# RES  --> D7 ---> 13
# CS   --> Null-->本次使用6针没有该引脚,指定一个空引脚即可
# 根据上面的连线，定义各个IO接口变量
SCK = Pin(14, Pin.OUT)
MOSI = Pin(12, Pin.OUT)
MISO = Pin(0)
DC = Pin(15)
RES = Pin(13)
CS = Pin(16)
# 初始化SPI对象，sck,mosi，miso 三个参数是必须的
spi = SPI(sck=SCK, mosi=MOSI, miso=MISO)
# 初始化OLED对象，128*64 是屏幕的分辨率，所谓的大小
oled = SSD1306_SPI(128, 64, spi, dc=DC, res=RES, cs=CS)
# 打开SPI通道
oled.poweron()
# 初始化OLED显示
oled.init_display()

with open('Micropython-logo.pbm', 'r') as f:
    f.readline()
    width, height = [int(v) for v in f.readline().split()]
    data = bytearray(f.read())
    f.close()
fbuf = framebuf.FrameBuffer(data, width, height, framebuf.MONO_HLSB)
# oled.invert(1)
oled.fill(0)
oled.blit(fbuf, 0, 0)
oled.show()
