#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/10/22 16:57
# @Author : 詹荣瑞
# @File : gobang.py
# @desc : 本代码未经授权禁止商用
import numpy as np
import cv2
from ctypes import *  # Python与C/C++的交互需要导入ctypes库
from bonegame import Board, Player, Game
from bonegame import GoBang, Renderer

Board_Length = 15  # 棋盘边长常量
Black = 1  # 棋子颜色常量
White = -1  # 棋子颜色常量
SPAN = 2  # 棋盘初始化常量
HEIGHT, WIDTH = 640, 640
WIN_NAME = "GoBang"

array = c_int * Board_Length  # c_int是C/C++中的int类型
matrix = array * Board_Length  # 生成一维数组
board = matrix()  # 生成二维数组

# 以上声明与定义在程序执行中必须一直存在

# 初始化棋盘
for i in range(Board_Length):
    for j in range(Board_Length):
        board[i][j] = SPAN  # 必须初始化为SPAN

DLL_Name = r'DT.dll'
DT_DLL = windll.LoadLibrary(DLL_Name)  # 导入动态链接库，其中文件路径可以是绝对路径或相对路径


# 声明定义Position类，接受接口函数的返回值
class Position(Structure):
    _fields_ = [("row", c_int),
                ("col", c_int)]  # 成员均是c_int类型


DT_DLL.Interface.restype = POINTER(Position)  # 指定接口函数的返回值是Position结构的指针

# 假定玩家执子颜色是Black，机器执子颜色是White
Player = Black
Robot = White


def mouse_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        bh, bw = game.board.map.shape[:2]
        h, w = game.renderer.h, game.renderer.w

        pos = (y * bh // h, x * bw // w)
        if game.down(game.players[0], pos).win:
            print(game.win)
            game.reset()
        board[pos[0]][pos[1]] = Player  # 将机器落子位置赋值机器执子颜色的int常量
        pt = DT_DLL.Interface(board, Player, Robot)  # 将当前逻辑棋盘传入接口函数，并返回机器决策的落子位置
        board[pt.contents.row][pt.contents.col] = Robot  # 将机器落子位置赋值机器执子颜色的int常量
        if game.down(game.players[1], (pt.contents.row, pt.contents.col)).win:
            print(game.win)
            game.reset()


game = GoBang(Board_Length, HEIGHT, WIDTH)
cv2.namedWindow(WIN_NAME, cv2.WINDOW_AUTOSIZE)
cv2.setMouseCallback(WIN_NAME, mouse_event)  # 创建默认鼠标事件（轮流下子）
while True:
    game.render(WIN_NAME)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
