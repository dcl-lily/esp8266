@echo off
title Auto flash micropython firmware into development board
echo All COM port List
echo ==========================
wmic path win32_pnpentity get caption /format:table| find "(COM"
echo ==========================
set /p com=please select one port number(example COM4 input 4):
esptool.py --port "COM%com%" erase_flash
echo ====================================
echo 1 flash size 512K -1.13
echo 2 flash size 1M -1.13
echo 3 flash size 2M - 1.13
echo 4 flash size 512K - 1.8.7
echo ====================================
set flash=1
set /p flash=please enter esp8266 flash size(default:1): 
if %flash% == 2 (
	echo use firmware:esp8266-1M-20201016-v1.13.bin
	goto m1
)^
else if %flash% == 3 (
	echo use esp8266-20200911-v1.13.bin
	goto m2
)^
else if %flash% == 4 (
	echo esp8266-512k-20170108-v1.8.7.bin
	goto k512-1.8.7
)^
else (
	echo use firmware:esp8266-512k-20200902-v1.13.bin
	goto k512
)
:k512
	esptool.py --port "COM%com%" --baud 460800 write_flash --flash_size=detect -fm dio 0 esp8266-512k-20200902-v1.13.bin
	goto end
:m1
	esptool.py --port "COM%com%" --baud 460800 write_flash --flash_size=detect -fm dio 0 esp8266-1m-20201016-v1.13.bin
	goto end
:m2
	esptool.py --port "COM%com%" --baud 460800 write_flash --flash_size=detect -fm dio 0 esp8266-20200911-v1.13.bin
	goto end
:k512-1.8.7	
	esptool.py --port "COM%com%" --baud 460800 write_flash --flash_size=detect -fm dio 0 esp8266-2016-05-03-v1.8.bin
	goto end
:end
	
pause