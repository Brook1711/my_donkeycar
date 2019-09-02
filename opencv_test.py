import sys
import copy
import argparse
import cv2
import numpy as np
from keras.models import load_model

from cv_models import Entity


camera = cv2.VideoCapture(0) #对视频进行读取操作以及调用摄像头
res, frame = camera.read() #获取视频帧,返回成功/失败，帧
y_size = frame.shape[0]  
x_size = frame.shape[1]

# 导入CNN分类模型
model = load_model('model//weights.h5')

bs = cv2.createBackgroundSubtractorMOG2(detectShadows=True)    # 定义MOG2，用于动态目标检测，是基于自适应混合高斯背景建模的背景减除法，detectShadows：是否检测影子
history = 20    # MOG2训练使用的帧数
frames = 0      # 当前帧数
counter = 0     # 当前目标id

cv2.namedWindow("detection", cv2.WINDOW_NORMAL) #通过指定的名字，创建一个可以作为图像和进度条的容器窗口。WINDOW_NORMAL设置了这个值，用户便可以改变窗口的大小（没有限制)
while True:
    res, frame = camera.read()
    if not res:
        break
    fg_mask = bs.apply(frame)

    if frames < history:
        frames += 1
        continue
    th = cv2.threshold(fg_mask.copy(), 244, 255, cv2.THRESH_BINARY)[1] #固定阈值二值化:像素高于阈值时，给像素赋予新值，否则，赋予另外一种颜色.ret, dst = cv2.threshold(src, thresh, maxval, type),当像素值超过了thresh（或者小于thresh，根据type来决定），赋予maxval，因为是二值化图，只有0和255
    th = cv2.erode(th, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=2) #腐蚀图像erode(img, kernel)，MORPH_ELLIPSE：椭圆
    dilated = cv2.dilate(th, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8, 3)), iterations=2) #膨胀图像
    # 获得目标位置
    image, contours, hier = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #查找检测物体的轮廓，cv2.findContours(image, mode, method[, contours[, hierarchy[, offset ]]])，
    track_list = []
    flag_me_max = 0
    flag_enemy_max = 0
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        flag_me_max
        if cv2.contourArea(c) > 3000:#面积阈值
            img = frame[y: y + h, x: x + w, :]
            rimg = cv2.resize(img, (64, 64), interpolation=cv2.INTER_CUBIC)#将该部分图像缩放为64*64
            image_data = np.array(rimg, dtype = 'float32')
            image_data /= 255.
            roi = np.expand_dims(image_data, axis = 0)
            #分类
            flag = model.predict(roi)

            if flag[0][0] > flag_me_max:
                entity_me = Entity(counter, (x, y, w, h), frame)
            counter += 1
            
