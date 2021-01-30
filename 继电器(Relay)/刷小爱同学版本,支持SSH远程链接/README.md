# 刷小爱AI音响固件版本，让小爱同学支持SSH登录，支持自定义折腾
### 一、本视频目的  
 想要小爱AI音响支持我们我们自定义操作，默认只能老老实实的给主义贡献你那可怜的资金
在一些老版本中有一些可以利用的漏洞，我们可以拿到底层的权限，能让我们折腾一下，
在新版本中暂时没有发现可以利用的漏洞,所以我们需要降版本才能实现.
破解的过程也是比较复，如果能力不行的同学，只能向资本主义交钱吧，我尽量做的详细些，

##### 注：理论上 只能对小爱AI音响操作 

### 二、需要准备     
1、小米AI音响   
2、USB TO TTL USB转串口  
3、杜邦线  
4、十字螺丝刀  
5、电烙铁  
6、小米账号和密码  
7、一个Linux系统(我这里使用Centos7)  


### 三、拆开小爱AI音响  

拆开小爱AI音响，把TTL串口引出，使用串口工具链接上串口。

需要用到:螺丝刀、电烙铁、杜邦线。  

主板接口 | 接口定义 | TTL 
--|-- |-- 
TPM24 | RX | TX  
TPM25 | TX | RX
TPM26 | GND| GND

目前的版本还没有找到可以利用的BUG进入信息，我们把版本降回之前的版本，

这里我根据Vicshs的版本写了一个在线页面  
https://www.qnjslm.com/xiaoai/  
Github
https://github.com/Vicshs/xiaoai 


登录后选择需要升级的设备，以及升级的版本，设备即可降级成功

我比较中意的版本 mico_all_c731c_1.52.1.bin

刷入成功后Console没有密码可以直接登录

生成RSAkey文件。
dropbearkey -t rsa -f /data/dropbear_rsa_host_key
使用key文件启动ssh服务
dropbear -r /data/dropbear_rsa_host_key
服务启用就可以直接远程SSH链接，使用如下命令查看当前的IP地址
```
root@mico:/# ip address
```
目前遗留问题:  
设备重启后SSH服务不会自动启动，可以理解系统是安装还原精灵一样。  
目前流传多种方法，破解  
1、 在盒子里面接一个小的单片接链接Console，重启后自动向console发送命令  
2、 对版本升级的镜像文件进行处理(接下来讲到)


### 四、对升级后的固件进行重新编写
这一步主要的作用是，让小爱开机打开SSH，关闭自动升级，

##### Ⅰ、小爱Ai音响上操作

首先确认当前根分区要么是mtdblock4要么是mtdblock5
为什么是两个分区,每次新升级的版本,都会写到旧的分区上，
已变升级失败能回切版本，两个分区来回交替使用


```shell
root@mico:/# mount
/dev/mtdblock4 on / type squashfs (ro,noatime)
```
我这里目前是mtdblock4,如过你的当前分区是5，下面命令部分请替换

其次确认当前data目录空间是否充足，可用空间大约需要比根分区大20%
```
root@mico:/# cd /data
root@mico:/data# mkdir Alex
root@mico:/# df -h
/dev/mtdblock4           28.1M     28.1M         0 100% /
/dev/ubi0_0             136.5M     33.5M     98.3M  25% /data
```
如果查看/data分区容量不足,使用下面命令创建一个内存临时空间,并挂在到我们要处理的目录  
非必要操作视情况而定
```
root@mico:/data#mount -t tmpfs -o size=50m tmpfs /data/Alex/

```
把当前版本文件,克隆出来以便我们进行修改/dev/mtdblock4根据情况选择
```
root@mico:/data# cd Alex
root@mico:/data/Alex# dd if=/dev/mtdblock4 of=/data/Alex/m4.img
```

把clone出来的文件上传到我们准备的linux主机上进行操作。  
传linux 主机上的原因是，小爱带的系统不能安装相关工具  
192.168.31.52  是我远程Linux主机的IP地址，可以百度安装个workStation
或者其他,
```
root@mico:/data/Alex# scp m4.img root@192.168.31.52:/opt/m4.img
```

#### Ⅱ、以下在Linux 主机上操作
我们在准备好的linux主机上对固件文件，解封装，修改
我这里以centos7.6做演示

首先安装基础软件，需要这台机器联网，并且又可用的yum源
```
[root@autohomeserver ~]# cd /opt
[root@autohomeserver opt]# yum install -y squashfs-tools
```
查看固件文件信息，这里主要记住Block size大小、压缩模式、xattrs是否开启    
重新封装会需要,我这里大小是131072, 封装是xz、xattrs不支持    
```
[root@autohomeserver opt]# unsquashfs -s m4.img
Compression xz
Block size 131072
Xattrs are not stored
```

将系统固件文件解开，在当前目录
```
[root@autohomeserver opt]# unsquashfs -dest tochang m4.img
```
对解开的系统文件进修改,这里我做一个简单的示例  
加入一个开机启动文件，以后有什么需要开机启动的放到该文件里里面  
在rc.local 添加一个/data/start.sh 记住添加到exit 前面  
#注：自有data目录重启数据不会丢失   
```
[root@autohomeserver opt]# cd tochang/etc/
[root@autohomeserver etc]# vi rc.local 
# Put your custom commands here that should be executed once
# the system init finished. By default this file does nothing.
/data/start.sh
exit 0
```
取消自动升级任务,防止版本自动升级,一夜回到解放前   
使用井号注释/bin/ota
```
[root@autohomeserver etc]# cd crontabs/
[root@autohomeserver crontabs]# vi root 
# At 03:00.
#0 3 * * * /bin/ota slient  # check ota
```
以上是基本的,可以根据需要进行小修改.  
进行重新封装131072,xz、Xattrs是我们第一步查看得到的信息  
```
[root@autohomeserver crontabs]# cd /opt
[root@autohomeserver opt]# mksquashfs tochang m4_out.img -b 131072 -comp xz -no-xattrs

```
#### Ⅲ、回到小爱音响上进行操作
把之前生产m4.img删除、回收空间，copy我们修改后的文件，重新写回falsh分区  

这里建议写到备分区上,就是非当前分区，例如我们当前活动的是mtdblock4，那我们写入到mtdblock5分区上
```
root@mico:/data/Alex# pwd
/data/Alex
root@mico:/data/Alex# rm -r m4.img 
root@mico:/data/Alex# scp root@192.168.31.52:/opt/m4_out.img .
root@mico:/data/Alex# dd if=m4_out.img of=/dev/mtdblock5
```
##### *特别注意刷写过程中是否有报错，常见的分区不足这是应为封装问题  
如果遇到错误  我们暂停操作，通过APP升级到最新版本或者通过页面在刷一个其他版本，防止设备变砖  


切换启动分区，重启设备进验证
```
如果需要切换到mtdblock5执行
root@mico:/data/Alex# /usr/bin/fw_env -s boot_part boot1

如果需要切换到mtdblock4执行
root@mico:/data/Alex# /usr/bin/fw_env -s boot_part boot0

重启设备

root@mico:/data/Alex# reboot

```

启动没问题后,在data目录创建我们指定的启动文件,让开机自动开启ssh

```
root@mico:/# vi /data/start.sh
dropbear -r /data/dropbear_rsa_host_key

root@mico:/# chmod a+x /data/start.sh
root@mico:/# reboot
```
重启验证没有问题,我们就可以把小爱安装还原了,焊接的Console线可以留在设备内，方便下次折腾。 



### 五、简单的设置让小爱同学支持控制我们的ESP8266

实现思路，默认系统里面是没有给与接口,如果有能力可以破解文件，注入钩子，UP目前没有这个实力也暂时没有时间去尝试.  
我们通过一凡查找,以及前辈们留下的路，小爱在识别语音和云端下发执行支持数据的时候会写本地日志文件,
我们时刻监听这个文件，当出现我们需要的关键字时候，进行处理。  这里我简单写了一个shell脚本结合上一次Socket控制
灯泡的环境，实现使用小爱同学控制灯泡，具体脚本内容查看脚本文件esp8266.sh 脚本也有详细描述。





