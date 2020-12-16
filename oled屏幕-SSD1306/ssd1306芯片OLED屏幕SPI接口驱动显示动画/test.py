import time
import json

def cover_hline(y, b_lin):
    """把数据转换成hline形式"""
    x_a = False   # 判断标记，如果遇到1，就是需要显示的时候，设置为True
    x_setp = 0  # 用于累加X步进，就是连续有多少个1
    h_line = []  # 保存每一行的数据集合
    b_l = len(b_lin)
    for ai in range(0, b_l):  # 依次读取每一行的128个数据,进行处理
        if int(b_lin[ai]) == 0 or ai == 127:   # 判断当前数据是否为1，如果为1是需要显示，0为不显示，或者石是否最后一行
            # 进入为0的阶段，不显示
            if x_a:   # 判断标记是否为真，如果为真，表示，刚结束显示，需要处理数据
                # 一段的显示数据， x_setp  为累加的显示步进长度，
                # i - x-setp, 就是显示开始的坐标位置，
                # y 是我们传递进来的目前处理的是哪一行数据，
                if ai == 127 and int(b_lin[ai]) == 1:
                    x_setp += 1
                h_line.append([ai - x_setp, y, x_setp])
                x_setp = 0  # 处理完成后恢复步进统计
                x_a = False  # 重新复位标记
            else:
                continue
        else:

            if not x_a:  # 判断是否是第一个1，
                x_a = True  # 如果是第一个1，打开标记
            x_setp += 1  # 进行步进统计
    return h_line


fw = open("a.data", "w+")
for i in range(1, 1643):
    # if i != 166 : continue
    f = open(f"after\\{i}.pbm", "rb")  # 循环读取每一个帧文件
    f.readline()  # 第一行信息不需要
    width, height = [int(v) for v in f.readline().split()]   # 第二行，宽和高信息不需要
    data = bytearray(f.read())   # 显示数据
    f.close()   # 把打开的文件关闭

    line = ""  # 定义行内容保存变量
    y = 0   # 定义Y轴偏移变量
    fram = []  # 用于保存处理后的变量
    for i in data:  # 读取每一个数据，每一个数据是两个十六进制组成
        if i == 0:  # 如果数据为0，直接数据为8个0加速处理
            a1 = "00000000"
        else:
            # 如果不全是0，进行数据位补齐操作。
            a1 = bin(i).replace("0b", "")
            while len(a1) < 8:
                a1 = "0" + a1

        line += a1   # 进行一行的数据为拼接
        if len(line) == 128:  # 如果数据位长度为128，说明一行的数据完成，进行处理
            l = cover_hline(y, line)  # 调用函数进行处理
            if len(l) > 0:  # 判断处理后的数据是否有有效数据，无效数据不然当前帧屏幕全黑
                for al in l:
                    #  读取每一个数据块，保存到每一帧的变量中
                    fram.append(al)
            #print(line, l)
            y += 1   # 进行第二行数据处理
            # print(line.replace("1", "-"))
            line = ""  # 数据变量清空
    #print(fram)
    fw.write(str(fram) + "\n")  # 每一帧数据处理完成写入到文件中
    #time.sleep(0.1)

fw.close()
