
from machine import Pin, I2C
# 导入SSD1306芯片驱动程序，需要自己提前下载
# 下载地址https://raw.githubusercontent.com/adafruit/micropython-adafruit-ssd1306/master/ssd1306.py
from ssd1306 import SSD1306_I2C
import network
import time

# 配置网络模块，如果不会，请参考之前的视屏[]
net = network.WLAN(network.STA_IF)
if not net.isconnected():
    net.active(True)
    # 这里连接无线， Lily  无线名称，后面是密码
    net.connect("Lily", "Meiyoumima")
    while not net.isconnected():
        time.sleep(1)

# 定义时钟引脚，
scl = Pin(12, Pin.OUT)
# 定义数据针脚
sda = Pin(14, Pin.OUT)
# 初始化一个I2C对象
i2c = I2C(-1, scl=scl, sda=sda)
# 使用I2C对象初始化一个SSD1306屏幕驱动对象
oled = SSD1306_I2C(128, 64, i2c)
# 让屏幕所有像素点清零
oled.fill(0)
# 在x轴是0，Y轴是0的位置开始显示英文，也就是左上角开始显示
oled.text("Hello word", 0, 0)
# 显示第二行文字，英文一个字母，纵向，Y轴 占据8个像素点，这里我们为了好看，我们在偏移8个像素，从16行开始，
# 相当于我们中间有个空行，
oled.text("this is Alex Labe", 0, 16)
# 同上面的道理我们显示设备的IP地址,需要前面链接上网络
oled.text(net.ifconfig()[0], 0, 32)
# 这里显示我么脚注，我们向右偏移64个像素点进行显示
oled.text("By Alex", 64, 50)
# 显示我们上面说有的设置
oled.show()
