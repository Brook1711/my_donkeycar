import os
import time

from donkeycar import Vehicle
from donkeycar.part.camera import PiCamera
from donkeycar.parts.datastore import Tub
from donkeycar.parts.
#初始化小车
V = Vehicle()

#初始化时间戳,并添加到小车中
clock = Timestamp()
V.add(clock, outputs=['timestamp'])

#添加摄像头模块
cam = PiCamera()
V.add(cam, outputs=['image'], threaded=Ture)

#初始化数据存储模式和路径
tub = Tub(path='./data/test_data',
          inputs=['image'],
          types=['image_array']
)

#给小车添加数据存储功能
V.add(tub, inputs= ['image'])

#数据搜集频率在每秒十次
V.start(rate_hz=10)

