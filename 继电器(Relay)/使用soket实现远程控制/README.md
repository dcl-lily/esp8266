# 认识MQTT物理网的远程控制
### 一、材料准备
我们需要提前准备的材料:  
1、光耦继电器模块(光耦隔离,支持高低电频驱动) * 1  
2、微动开关 * 1       
3、esp8266开发板 * 1块    
4、micropython开发环境(包含IDE，以及程序上传相关耗材)  
5、一台Linux或者windows服务器,用于搭建MQTTServer端  

### 二、MQTT服务器安装  
1、安装依赖库  
```shell
  yum -y install make gcc gcc-c++ kernel-devel m4 ncurses-devel openssl-devel wget unzip
```
2、安装Elang组件  
```
wget http://erlang.org/download/otp_src_23.2.tar.gz


	
```
3、安装EMQ  
 下载地址 https://www.emqx.io/cn/downloads#broker   
 安装产考地址 https://docs.emqx.cn/cn/edge/latest/install.html  
   
```
#下载源码文件
wget https://www.emqx.io/cn/downloads/broker/v4.2.5/emqx-centos7-4.2.5-x86_64.zip

# 解压文件
unzip emqx-centos7-4.2.5-x86_64.zip  

# 测试软件是否正常运行  
cd emqx && ./bin/emqx console

# 如果没有问题后，执行Ctrl + C 结束  

#  使用守护进程启动  
./bin/emqx start

#  查看状态  
./bin/emqx_ctl status  


可以使用网页访问查看状态,默认的端口是18083
http://ip地址:18083

默认用户名: admin
默认密码： public



```	 


### 三、连线方式  

开发板和继电器连接 
 
继电器| 开发板|GPIO
--|--|--
DC+ |3.3v|
DC-	|GND|	
IN	|D3	|12


### 四、使用软件

ioT MQTT Panel
