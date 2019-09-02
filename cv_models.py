import sys
import cv2
import numpy as np

class Entity(object):
    def __init__(self, vid, windows, frame):
        self.vid = vid #目标ID
        self.windows = windows  #目标矩阵，x y w h
        self.center = self._set_center(windows) #目标中心
        self.trajectory = [self.center] #轨迹
        self.tracker = self._init_tracker(windows, frame) #跟踪器

    def _set_center(self, windows):
        x, y, w, h = windows
        x = (2 * x + w) / 2  #x,y更新了？
        y = (2 * y + h) / 2
        center = np.array([np.float32(x), np.float32(y)], np.float32)
        return center

    def _init_tracker(self, windows, frame):   
        x, y, w, h = windows # KCF
        tracker = cv2.Tracker_create('KCF')
        tracker.init(frame, (x, y, w, h)) #初始化一个帧与目标的坐标位置
        return tracker

    def update(self, frame):
        self.tracker.update(frame) # 更新目标位置
        ok, new_box = self.tracker.update(frame) #  retval, boundingBox =   cv.Tracker.update(  image   )

        if ok:
            x, y, w, h = int(new_box[0]), int(new_box[1]), int(new_box[2]), int(new_box[3])
            self.center = self._set_center((x, y, w, h))
            self.windows = (x, y, w, h)
            self.trajectory.append(self.center) #轨迹增加中心点
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1) #画出矩阵
            cv2.putText(frame, "vehicle", (x, y - 5),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)  #添加文字
            cv2.polylines(frame, [np.int32(self.trajectory)], 0, (0, 0, 255)) #绘制轨迹