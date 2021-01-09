import network
import time
from machine import Pin
import socket

# 配置网络模块，如果不会，请参考之前的视屏[]
net = network.WLAN(network.STA_IF)
if not net.isconnected():
    net.active(True)
    # 这里连接无线， Lily  无线名称，后面是密码
    net.connect("Lily", "Meiyoumima")
    while not net.isconnected():
        time.sleep(1)
print(net.ifconfig())

relay_in = Pin(13, Pin.OUT)
# 简单的一个网页显示模版文件，显示当前状态，有两个开关控制灯泡打开与关闭
html = """<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <title>小杜Lab-开关控制</title>
    </head>
    <body>
            <h1>当前灯泡状态：%s</h1>
            <br><br>
            <a href="/ON""><button>开灯</button></a>
            <a href="/OFF""><button>关灯</button></a><br />
    </body>
</html>
"""

# 生成一个Socket对象
s = socket.socket()
# Socket对象绑定到监听地址
s.bind(('0.0.0.0', 80))
# 开始监听数据
s.listen(1)

LedState = "初始化"
while True:
    # socket 阻塞等待外部连接进行建立
    cl, addr = s.accept()
    print('client connected from', addr)
    # 连接建立后等待客户端发送数据，这里要理解我们建立连接的时候也是发送了数据。
    # 后续判断逻辑都不满足,最后会返回页面
    request = cl.recv(1024)
    # 对请求的结果查找是否包含ON字段，如果包含就执行给继电器为1操作打开继电器
    if request.decode()[:20].find("ON") != -1:
        relay_in.value(1)
        LedState = "打开"
    # 和上面一样，当检测到时off，就是关闭灯泡时候，执行关闭灯泡
    elif request.decode()[:20].find("OFF") != -1:
        relay_in.value(0)
        LedState = "关闭"
    # 返回通过我们模版渲染的简单网页给客户端
    response = html % LedState
    cl.send(response)
    # 结束本次会话连接,继续循环进行下一次连接
    cl.close()