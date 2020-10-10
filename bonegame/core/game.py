#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/9/27 13:05
# @Author : 詹荣瑞
# @File : game.py
# @desc : 本代码未经授权禁止商用

import numpy as np

SPACE = 0
BLACK = 1
WHITE = 2
PRINT = [' ', '*', 'O']


class Player(object):

    def __init__(self, name, number, print_style="*"):
        self.name = name
        self.number = number

        self.print = print_style


class Board(object):

    def __init__(self, height=7, width=7):
        self.map = np.zeros((height, width), np.int)

    def __str__(self):
        return str(self.map)

    def down(self, num, pos):
        """
        下子

        :param num: 下子编号
        :param pos: 下子位置
        :return:
        """
        self.map[tuple(pos)] = num


class Game(object):

    def __init__(self, board, players):
        self.board = board
        self.players = players

    def __str__(self):
        out = str(self.board)
        for p in self.players:
            out = out.replace(f"{p.number}", p.print)
        return out

    def down(self, player, pos):
        """
        判断位置是否有子，若无子则下子

        :param player: 下子玩家
        :param pos: 下子位置
        :return:
        """
        if isinstance(player, int):
            player = self.players[player]
        current_piece = self.board.map[pos]
        if current_piece == 0:
            if isinstance(player, Player):
                self.board.map[pos] = player.number
            else:
                self.board.map[pos] = self.players[player].number
        else:
            print(f"位置{pos}已有子")
        return self


class GoBang(Game):

    def __init__(self, scale=7):
        board = Board(scale, scale)
        players = [Player(f"p{i}", i, f"{i}") for i in range(1, 3)]
        super(GoBang, self).__init__(board, players)

    # def


if __name__ == '__main__':
    board = Board(7, 7)
    players = [Player(f"p{i}", i, f"p{i}") for i in range(1, 3)]

    game = Game(board, players)
    print(game.down(players[0], (2, 2)))
    # while True:
    #     op = eval(input())
    #     print(game.down(*op))
