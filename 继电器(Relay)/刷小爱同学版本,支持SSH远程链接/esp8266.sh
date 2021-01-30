#-----------------------------------------
#   脚本中肯定有诸多的不合理和不满意的地方，
#   这里只是一个基本的演示,具体的还得靠大家自由发挥
#   随着版本的升级，可能小爱的日志格式也会发生变化,
#   都得根据情况进行修改
#                      -----Alex(小杜Lab)
#-----------------------------------------


# 进行一个死循环,周期性监控日志文件
while true
	do
			# 判断日志文件是否存在，继续操作，不存在等待500ms继续循环
			if [ -f /tmp/mipns/mibrain/mibrain_asr.log ];then
					# 过滤日志文件中是否有自定义的关键字，这里我定义的是'灯泡两个字'
					cy=`cat /tmp/mipns/mibrain/mibrain_asr.log | grep -E "灯泡"`
					#  判断是否命中了我们的关键字
					if  [ -n "$cy" ] ;then
							# 如果命中我们关键字，这时候马上小爱要播放云端下发的语音了，我们每200ms循环一次去尝试阻断设备的播放，一共200次
							seq 1 200 | while read line;do
											# 阻断播放的命令，默认阻断后会返回0，否则返回其他
						    			code=`ubus call mediaplayer player_play_operation {\"action\":\"resume\"}|awk -F 'code":' '{print $2}'`
						    			# 这里判断是否阻断了小爱的播放,阻断后解析这个循环，否则循环200次也结束了。
						    			if [[ "$code" -eq "0" ]];then
						      				echo "== 停止成功"
						      				break
						    			fi
						    			sleep 0.2
						  			done
								#mv /tmp/mipns/mibrain/mibrain_txt_RESULT_NLP.log /tmp/mipns/mibrain/temp/mibrain_txt_RESULT_NLP.log-`date +%s`
							# 这里通过过滤日志文件，找到到我们说话TTS识别的文字
							cc=`cat /tmp/mipns/mibrain/mibrain_txt_RESULT_NLP.log |awk -F '"domain":' '{print $2}' |awk -F '"query":' '{print $2}' | awk -F ',' '{print $1}'`
							echo $cc
							#  对识别的文字进行过滤匹配,确认是否有我们定义好的动作,例如我这里是打开和关闭
							on=`echo $cc | grep "打开"`
							off=`echo $cc | grep "关闭"`
							echo "-$on-"
							echo "=$off="
							# 如果动作是打开
							if [ -n "$on" ] ; then
								# 我们使用curl直接访问我们Esp8266环境中定义的Socket链接，按照我们上次的实现，后面跟ON表示打开
								curl http://192.168.31.37/ON
								# 然后播放一段我们指定的话，直接指定中文，调用这个文件，会直接TTS转换成小爱的声音
								ubus call mibrain text_to_speech "{\"text\":\"灯泡已经打开了哦\",\"save\":0}"
							fi
							# 如果动作是关闭,处理的方式和上面一样
							if [ -n "$off" ] ;then 
								curl http://192.168.31.37/OFF
								ubus call mibrain text_to_speech "{\"text\":\"灯泡已经关闭了哦\",\"save\":0}"
							fi
					fi
					# 完成后我们把日志删除，反正也没什么用,删除日志是我们方便处理
					rm -rf /tmp/mipns/mibrain/mibrain_txt_RESULT_NLP.log
					rm -rf /tmp/mipns/mibrain/mibrain_asr.log
					
			fi
  	sleep 0.5
done

