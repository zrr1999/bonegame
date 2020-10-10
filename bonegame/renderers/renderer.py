#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/10/10 15:55
# @Author : 詹荣瑞
# @File : renderer.py
# @desc : 本代码未经授权禁止商用
import cv2
import numpy as np


class Renderer(object):

    def __init__(self, height=480, width=640):
        self.h = height
        self.w = width

    def __call__(self, mat):
        self.show(mat)

    def show(self, mat):
        h, w = mat.shape[:2]
        mat = mat.repeat(self.h//h, 0).repeat(self.w//w, 1)
        cv2.imshow("img", mat)
        cv2.waitKey()


if __name__ == '__main__':
    r = Renderer()
    a = np.zeros((5, 5, 3), np.uint8)
    a[:, :2] = (255, 0, 255)
    a[:, 2:3] = (255, 255, 0)
    r.show(a)
