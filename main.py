#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/10/10 16:23
# @Author : 詹荣瑞
# @File : main.py
# @desc : 本代码未经授权禁止商用
from bonegame import Board, Player, Game
from bonegame import GoBang, Renderer
import cv2
import numpy as np

HEIGHT, WIDTH = 640, 640
SIZE = 7
WIN_NAME = "GoBang"


game = GoBang(SIZE, HEIGHT, WIDTH)
cv2.namedWindow(WIN_NAME, cv2.WINDOW_AUTOSIZE)
cv2.setMouseCallback(WIN_NAME, game.mouse_event)  # 创建默认鼠标事件（轮流下子）
while True:
    game.render(WIN_NAME)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

# while True:

# op = eval(input())
# print(game.down(*op))
