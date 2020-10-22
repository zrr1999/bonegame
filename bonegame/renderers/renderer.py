#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/10/10 15:55
# @Author : 詹荣瑞
# @File : renderer.py
# @desc : 本代码未经授权禁止商用
import cv2
import numpy as np
from .renderer_base import RendererBase


class Renderer(object):

    def __init__(self, height=480, width=640, colors=((0, 0, 0), (255, 0, 0), (0, 255, 0))):
        self.core = RendererBase
        self.core.title = "GoBang"
        self.core.window_size = (width, height)
        self.h = height
        self.w = width
        self.colors = colors

    def __call__(self, mat, win_name):
        self.show(mat, win_name)

    def show(self, mat, win_name="image"):
        m, n = mat.shape
        km, kn = self.h // m // 2, self.w // n // 2
        out = np.zeros((self.h, self.w))
        for i in range(m):
            y = 2 * i + 1
            for j in range(n):
                x = 2 * j + 1
                if mat[i, j]:
                    color = 255/mat[i, j]
                    cv2.circle(out, (x * kn, y * km, ), 20, color, -1)
        for i in range(m):
            i = 2 * i + 1
            out = cv2.line(out, (i * km, 0), (i * km, 2 * n * kn), 255)
        for i in range(n):
            i = 2 * i + 1
            out = cv2.line(out, (0, i * km), (2 * m * km, i * kn), 255)
        cv2.imshow(win_name, out.astype(np.uint8))


if __name__ == '__main__':
    r = Renderer()
    a = np.zeros((5, 5, 3), np.uint8)
    a[:, :2] = (255, 0, 255)
    a[:, 2:3] = (255, 255, 0)
    r.show(a)
