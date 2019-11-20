# -*- coding=utf-8 -*-
# __author__ : "zbh"
# __date__ :  2019/11/20

import os

import requests
'''
断点续传：客户端软件断点续传指的是在下载或上传时，将下载或上传任务（一个文件或一个压缩包）人为的划分为几个部分，
并在写入文件之后刷新断点位置，如果碰到网络故障，可以从已经上传或下载的部分开始继续上传下载未完成的部分，
而没有必要从头开始上传下载。从而达到节省时间，提高速度的目的。
'''

def break_down():
    # 1：首先获得将要下载或下载到一半的文件的大小（获得断点，字节数）。（这里以下载centos7镜像为例，可以使用其他链接测试）
    try:
        downed_bytes = os.path.getsize("centos.ios")
    except FileNotFoundError:
        fd = open("centos.ios", mode="wb")
        fd.close()
        downed_bytes = os.path.getsize("centos.ios")
    except PermissionError:
        print("You don't have permission to access this file.")

    # 在没有完全下载完成之前，多次断开网络，模拟网络故障。
    # 当看到输出结果有增长时，表示续传成功。整个文件传完，程序自动结束。第一次输出结果为0.
    print("已经下载的字节：%s" % downed_bytes)
    # 2：从断点位置请求数据，继续下载 重要参数：headers={"Range":"bytes=%d-" % downed_bytes}, stream=True
    html = requests.get(url="http://mirrors.aliyun.com/centos/7/isos/x86_64/CentOS-7-x86_64-NetInstall-1908.iso",
                        stream=True, headers={"Range": "bytes=%d-" % downed_bytes})

    # 3：将请求的内容追加进原文件并刷新已经下载的字节数（位置）
    with open("centos.ios", "ab") as f:
        for chunk in html.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()


if __name__ == '__main__':
    break_down()

'''
下面是我通过多次断开程序，记录的 ‘已经下载的字节’递增情况
已经下载的字节：0
已经下载的字节：54502400
已经下载的字节：77283328
已经下载的字节：117981184
已经下载的字节：143215616
已经下载的字节：186091520
已经下载的字节：246622208
已经下载的字节：303182848
已经下载的字节：425626624
已经下载的字节：520067072
已经下载的字节：578813952 下载完成，程序自动结束
'''