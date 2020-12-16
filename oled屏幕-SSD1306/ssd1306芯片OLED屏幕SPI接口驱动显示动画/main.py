from machine import Pin, SPI
from ssd1306 import SSD1306_SPI  # 导入SSD控制的OLED程序
import network
import time
import json

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


def image(img_list):
    s = time.ticks_ms()
    oled.fill(0)
    for i in img_list:
        oled.hline(2 * i[0], 2 * i[1], 2 * i[2], 1)
    oled.show()
    e = time.ticks_ms() - s
    if e < 100:
        time.sleep_ms(90 - e)


with open('bad.data', 'r') as f:
    for i in f:
        z = json.loads(i)
        image(z)

oled.fill(0)
oled.text("The End", 32, 32, 1)
oled.show()