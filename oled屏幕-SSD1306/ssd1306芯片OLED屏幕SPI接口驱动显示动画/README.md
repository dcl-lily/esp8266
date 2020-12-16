# SSD1306 oled屏幕驱动显示动画
### 一、材料准备
我们需要提前准备的材料:  
1、0.96寸SPI接口的OLED屏幕 * 1 块  
2、esp8266开发板 * 1块  
3、母到母杜邦线 * 4条  
4、micropython开发环境(包含IDE，以及程序上传相关耗材)  

### 二、屏幕介绍  
从左向右依次为  
GND  3.3v输入负极  
VCC   3.3v输入正极  
SCL   时钟  (部分屏幕上是D0)  
SDA  MOSI数据    (部分屏幕上是D1)  
RST  硬件复位  
D/C  数据命令  
CS  (7针屏幕上多的一针)  


### 三、屏幕和开发板连线方式  

屏幕| 开发板|GPIO
--|--|--
GND |GND|	
VCC	|3.3V|	
SCL	|D5	|14
SDA	|D6	|12
RST	|D7	|13
D/C	|D8	|15

### 四、BPM  
PBM 格式说明  
 
头  |	类型	|	编码
--| -- | -- 
P1  |	位图	|	ASCII
P2  |	灰度图|	ASCII
P3  |	像素图|	ASCII
P4  |	位图	|	二进制
P5  |	灰度图|	二进制
P6  |	像素图|	二进制

### 五、首先对图片进行取帧转换成PBM格式  
需要用到cv2和numpy，在电脑的python环境下出处理  
安装插件，首先确认电脑的pip 正常
  
```python
  pip install opencv-python  
```

然后使用文件GetFrame.py获取视频的PBM帧格式文件  

这里我们可可以直接使用帧格式文件，进行TV播放，  

无赖的是我们的开发板容量有限，就算转换成帧格式，一个三分钟视频也有5M大小，  

无法保存到开发板上运行，这里我们可以有两种解决方案，  

① 在开发板上配饰SD读卡器，把数据保存在SD卡上，  

② 把数据保存在网络上，通过网络进行下发。  

由于手上资源有限，我们另辟路径使用其他方法。

在上次的视频中学习过.line，hline的方法，我们把PBM数据在进行一边处理，处理成hline数据。  

最终处理完成，大小为2.4M大小，可以勉强接受了  

处理过程为test.py 文件中实现。代码已经些注释，

下一步，修改man.py文件，适配我们显示，上传数据以及代码，然后大功告成。  

***注意*：***  
	数据上传非常慢，需要等待

遇到内存错误
```python
Traceback (most recent call last):  
  File "main.py", line 51, in <module>  
MemoryError: memory allocation failed, allocating 3112 bytes  
```

稍微修改解决,原始代码    
```python
with open('a.data', 'r') as f:
    for b in f:
    	c= json.loads(b)
        image(c)
```

修改后代码

```python
with open('a.data', 'r') as f:
    for b in f:
        image(json.loads(b))
```

一行代码的错,你细品，如果能明白为啥报错，就是大师级别了  

