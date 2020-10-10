#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/10/10 16:47
# @Author : 詹荣瑞
# @File : gobang.py
# @desc : 本代码未经授权禁止商用
from .game import Game
from .core import Player, Board


class GoBang(Game):

    def __init__(self, scale=7):
        board = Board(scale, scale)
        players = [Player(f"p{i}", i, f"{i}") for i in range(1, 3)]
        super(GoBang, self).__init__(board, players)
