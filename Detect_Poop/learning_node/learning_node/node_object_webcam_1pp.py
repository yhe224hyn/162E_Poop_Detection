#!/usr/bin/env python3 
# -*- coding: utf-8 -*-

"""
@作者: 古月居(www.guyuehome.com)
@说明: ROS2节点示例-通过摄像头识别检测图片中出现的苹果
"""

import rclpy                            # ROS2 Python接口库
from rclpy.node import Node             # ROS2 节点类

import cv2                              # OpenCV图像处理库
import numpy as np                      # Python数值计算库

# lower_brown = np.array([10, 30, 40])    # Poop的HSV阈值下限
# upper_brown = np.array([50, 200, 230])  # Poop的HSV阈值上限

lower_brown = np.array([5, 30, 40])    # Poop的HSV阈值下限
upper_brown = np.array([50, 200, 230])  # Poop的HSV阈值上限

# For approxiate Poop Shape
# Load the sample image of the poop
img = cv2.imread('src/162E_Poop_Detection/Detect_Poop/learning_node/learning_node/sample3.png')

# Convert the image to grayscale and apply edge detection
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 100, 200)

# Find the contour of the poop shape
contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contour = max(contours, key=cv2.contourArea)

# Store the poop shape as a numpy array
poop_shape = np.array(contour)


def object_detect(image):
    max_area = 0
    max_cnt = None
    second_max_area = 0
    second_max_cnt = None
    hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask_red = cv2.inRange(hsv_img, lower_brown, upper_brown)

    contours, hierarchy = cv2.findContours(mask_red, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    for cnt in contours:
        if cnt.shape[0] < 400:
            continue

        area = cv2.contourArea(cnt)
        shape_match = cv2.matchShapes(poop_shape, cnt, 1, 0.0)
        print(shape_match)

        if area > max_area and shape_match < 0.3:
            # the contour roughly fits the poop shape
            second_max_area = max_area
            second_max_cnt = max_cnt
            max_area = area
            max_cnt = cnt
        elif area > second_max_area and shape_match < 0.3:
            # the contour roughly fits the poop shape, but not as well as the largest contour
            second_max_area = area
            second_max_cnt = cnt

    if max_cnt is not None:
        (x, y, w, h) = cv2.boundingRect(max_cnt)
        # print("draw the big match!")  
        cv2.drawContours(image, [max_cnt], -1, (0, 255, 0), 2)
        cv2.circle(image, (int(x+w/2), int(y+h/2)), 5, (0, 255, 0), -1)
    elif second_max_cnt is not None:
        (x, y, w, h) = cv2.boundingRect(second_max_cnt)
        # print("draw the second match")
        cv2.drawContours(image, [second_max_cnt], -1, (0, 255, 0), 2)
        cv2.circle(image, (int(x+w/2), int(y+h/2)), 5, (0, 255, 0), -1)

    # max_area = 0
    # max_cnt = None
    # hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)                       # 图像从BGR颜色模型转换为HSV模型
    # mask_red = cv2.inRange(hsv_img, lower_brown, upper_brown)                  # 图像二值化

    # contours, hierarchy = cv2.findContours(mask_red, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE) # 图像中轮廓检测

    # for cnt in contours:
    #     if cnt.shape[0] < 500:
    #         continue

    #     area = cv2.contourArea(cnt)
    #     if area > max_area:
    #         max_area = area
    #         max_cnt = cnt

    # if max_cnt is not None:
    #     (x, y, w, h) = cv2.boundingRect(max_cnt)
    #     cv2.drawContours(image, [max_cnt], -1, (0, 255, 0), 2)
    #     cv2.circle(image, (int(x+w/2), int(y+h/2)), 5, (0, 255, 0), -1)


    cv2.imshow("object", image)                                            # 使用OpenCV显示处理后的图像效果
    cv2.waitKey(500)

def main(args=None):                                                       # ROS2节点主入口main函数
    rclpy.init(args=args)                                                  # ROS2 Python接口初始化
    node = Node("node_object_webcam_1pp")                                      # 创建ROS2节点对象并进行初始化
    node.get_logger().info("ROS2节点示例：检测图像中的Poop")

    cap = cv2.VideoCapture(0)

    
    while rclpy.ok():
        ret, image = cap.read()          # 读取一帧图像
         
        if ret == True:
            object_detect(image)          # 苹果检测
        
    node.destroy_node()                  # 销毁节点对象
    rclpy.shutdown()                     # 关闭ROS2 Python接口