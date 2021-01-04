# 使用socket实现继电器远程控制
### 一、材料准备
我们继续上次的视屏，环境为上次环境
https://github.com/dcl-lily/esp8266/tree/main/%E7%BB%A7%E7%94%B5%E5%99%A8(Relay)/%E8%AE%A4%E8%AF%86%E7%BB%A7%E7%94%B5%E5%99%A8


### 二、本次主要是Socket编程    

首现我们需要保证开发板能连接上网络

```python
net = network.WLAN(network.STA_IF)
if not net.isconnected():
    net.active(True)
    net.connect("Lily", "Meiyoumima")
    while not net.isconnected():
        time.sleep(1)
```

初始化Socket对象
```
socket.socket()
```
设定对象监听的IP地址以及端口，以列表的形式传递
```
socket.bind(('0.0.0.0', 80))
```
开始监听在指定IP对应的端口上
```
socket.listen(1)
```
阻塞等待客户端连接发送数据
```
连接对象,客户端连接IP地址 = socket.accept()
```
读取指定长度数据
```
连接对象.recv(1024)
```
给客户端发送数据
```
连接对象..send(str)
```



