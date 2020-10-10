#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/10/10 16:23
# @Author : 詹荣瑞
# @File : main.py
# @desc : 本代码未经授权禁止商用
from bonegame import Board, Player, Game
from bonegame import GoBang, Renderer

renderer = Renderer(640, 640)
game = GoBang(7)

game.down(0, (2, 2))

# while True:
#     op = eval(input())
#     print(game.down(*op))
