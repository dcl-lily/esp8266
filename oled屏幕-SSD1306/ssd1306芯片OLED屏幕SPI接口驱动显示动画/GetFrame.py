import cv2 as cv
import numpy as np

vc = cv.VideoCapture('Bad Apple.avi')  # 打开视频
c = 0  # 累计帧数

timeF = 4  # 隔3帧截一次图，数字越小，播放越细腻


def binary_image(image):  # 将图像处理为二值化的程序
    try:
        gray = cv.cvtColor(image, cv.COLOR_RGB2GRAY)  # 把输入图像灰度化
    except cv.error:
        return False
    h, w = gray.shape[:2]
    m = np.reshape(gray, [1, w*h])
    mean = m.sum()/(w*h)
    ret, binary = cv.threshold(gray, mean, 255, cv.THRESH_BINARY)
    return binary


if vc.isOpened():  # 判断是否正常打开
    rval, frame = vc.read()
else:
    rval = False

file_name = 1
while rval:  # 循环读取视频帧
    rval, frame = vc.read()
    if c % timeF == 0:  # 每隔timeF帧进行存储操作
        frame = binary_image(frame)  # 二值化
        frame = cv.bitwise_not(frame)  # 反相,根据视频内容来定需不需要反相
        frame = cv.resize(frame, (128, 64))  # 调整尺寸
        cv.imwrite(f"after\\{file_name}.pbm", frame)  # 保存
        file_name += 1
    c = c + 1
    cv.waitKey(0)

