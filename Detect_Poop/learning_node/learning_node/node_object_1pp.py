#!/usr/bin/env python3 
# -*- coding: utf-8 -*-

"""
@作者: 古月居(www.guyuehome.com)
@说明: ROS2节点示例-通过颜色识别检测图片中出现的Poop
"""

import rclpy                            # ROS2 Python接口库
from rclpy.node import Node             # ROS2 节点类

import cv2                              # OpenCV图像处理库
import numpy as np                      # Python数值计算库

lower_brown = np.array([10, 50, 60])    # Poop的HSV阈值下限
upper_brown = np.array([40, 225, 255])  # Poop的HSV阈值上限



def object_detect(image):
    hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask_brown = cv2.inRange(hsv_img, lower_brown, upper_brown)
    max_area = 0
    max_cnt = None

    contours, hierarchy = cv2.findContours(mask_brown, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    for cnt in contours:
        if cnt.shape[0] < 500:
            continue

        area = cv2.contourArea(cnt)
        if area > max_area:
            max_area = area
            max_cnt = cnt

    if max_cnt is not None:
        (x, y, w, h) = cv2.boundingRect(max_cnt)
        cv2.drawContours(image, [max_cnt], -1, (0, 255, 0), 2)
        cv2.circle(image, (int(x+w/2), int(y+h/2)), 5, (0, 255, 0), -1)
        
    cv2.imshow("object", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



# def object_detect(image):
#     hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) # 图像从BGR颜色模型转换为HSV模型
#     mask_brown = cv2.inRange(hsv_img, lower_brown, upper_brown) # 图像二值化
#     max_area = 0
#     max_cnt = None

#     contours, hierarchy = cv2.findContours(mask_brown, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE) # 图像中轮廓检测

#     for cnt in contours:    # 去除一些轮廓面积太小的噪声
#         if cnt.shape[0] < 500:
#             continue

#         area = cv2.contourArea(cnt)
#         if area > max_area:
#             max_area = area
#             max_cnt = cnt
            
#         (x, y, w, h) = cv2.boundingRect( max_cnt)    # 得到苹果所在轮廓的左上角xy像素坐标及轮廓范围的宽和高
#         cv2.drawContours(image, [max_cnt], -1, (0, 255, 0), 2)  # 将苹果的轮廓勾勒出来
#         cv2.circle(image, (int(x+w/2), int(y+h/2)), 5, (0, 255, 0), -1) # 将苹果的图像中心点画出来
	    
#     cv2.imshow("object", image)                                                    # 使用OpenCV显示处理后的图像效果
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

def main(args=None):                                                              # ROS2节点主入口main函数
    rclpy.init(args=args)                                                         # ROS2 Python接口初始化
    node = Node("node_object")                                                     # 创建ROS2节点对象并进行初始化
    node.get_logger().info("ROS2节点示例：检测图片中的Poop")

    image = cv2.imread('src/162E_Poop_Detection/Detect_Poop/learning_node/learning_node/sample2.png')  # 读取图像
    object_detect(image)                                                            # 苹果检测
    rclpy.spin(node)                                                               # 循环等待ROS2退出
    node.destroy_node()                                                            # 销毁节点对象
    rclpy.shutdown()                                                               # 关闭ROS2 Python接口