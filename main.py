from pprint import pprint
from itertools import *

class Combination:
    def __init__(self, positions, figures):
        self.positions = [(*pos, f) for pos, f in zip(positions, figures)]
        self.gameboard = [[ 0 for col in range(8)] for row in range(8)]
        for r, c in positions:
            self.gameboard[r][c] = -1
        for r, c, f in self.positions:
            if f == "queen":
                self.queen(r, c)
            elif f == "king":
                self.king(r, c)
            elif f == "rook":
                self.rook(r, c)
            elif f == "knight":
                self.knight(r, c)
            elif f == "bishop":
                self.bishop(r, c)
            else:
                raise "Error in figures"

    def queen(self, r, c):
        i = r
        j = c
        #идем по горизонтали и вертикали
        while j > 0:
            j -= 1
            if self.gameboard[i][j] == -1:
                break
            self.gameboard[i][j] += 1
        j = c
        while j < 7:
            j += 1
            if self.gameboard[i][j] == -1:
                break
            self.gameboard[i][j] += 1
        j = c
        while i > 0:
            i -= 1
            if self.gameboard[i][j] == -1:
                break
            self.gameboard[i][j] += 1
        i = r
        while i < 7:
            i += 1
            if self.gameboard[i][j] == -1:
                break
            self.gameboard[i][j] += 1
        #идем по диагонаялям
        i = r
        j = c
        while i > 0 and j > 0:
            i -= 1
            j -= 1
            if self.gameboard[i][j] == -1:
                break
            self.gameboard[i][j] += 1
        i = r
        j = c
        while i > 0 and j < 7:
            i -= 1
            j += 1
            if self.gameboard[i][j] == -1:
                break
            self.gameboard[i][j] += 1
        i = r
        j = c
        while i < 7 and j > 0:
            i += 1
            j -= 1
            if self.gameboard[i][j] == -1:
                break
            self.gameboard[i][j] += 1
        i = r
        j = c
        while i < 7 and j < 7:
            i += 1
            j += 1
            if self.gameboard[i][j] == -1:
                break
            self.gameboard[i][j] += 1

    def king(self, r, c):
        i = r
        j = c
        for di, dj in (1, 0), (-1, 0), (0, 1), (0, -1), (-1, -1), (-1, 1), (1, -1), (1, 1):
            if 0 <= i + di < 8 and 0 <= j + dj < 8:
                if self.gameboard[i + di][j + dj] == -1:
                    continue
                self.gameboard[i + di][j + dj] += 1

    def knight(self, r, c):
        i = r
        j = c
        for di, dj in (2, 1), (2, -1), (-2, -1), (-2, 1), (1, 2), (-1, 2), (1, -2), (-1, -2):
            if 0 <= i + di < 8 and 0 <= j + dj < 8:
                if self.gameboard[i + di][j + dj] == -1:
                    continue
                self.gameboard[i + di][j + dj] += 1

    def rook(self, r, c):
        i = r
        j = c
        # идем по горизонтали и вертикали
        while j > 0:
            j -= 1
            if self.gameboard[i][j] == -1:
                break
            self.gameboard[i][j] += 1
        j = c
        while j < 7:
            j += 1
            if self.gameboard[i][j] == -1:
                break
            self.gameboard[i][j] += 1
        j = c
        while i > 0:
            i -= 1
            if self.gameboard[i][j] == -1:
                break
            self.gameboard[i][j] += 1
        i = r
        while i < 7:
            i += 1
            if self.gameboard[i][j] == -1:
                break
            self.gameboard[i][j] += 1

    def bishop(self, r, c):
        i = r
        j = c
        # идем по диагонаялям
        i = r
        j = c
        while i > 0 and j > 0:
            i -= 1
            j -= 1
            if self.gameboard[i][j] == -1:
                break
            self.gameboard[i][j] += 1
        i = r
        j = c
        while i > 0 and j < 7:
            i -= 1
            j += 1
            if self.gameboard[i][j] == -1:
                break
            self.gameboard[i][j] += 1
        i = r
        j = c
        while i < 7 and j > 0:
            i += 1
            j -= 1
            if self.gameboard[i][j] == -1:
                break
            self.gameboard[i][j] += 1
        i = r
        j = c
        while i < 7 and j < 7:
            i += 1
            j += 1
            if self.gameboard[i][j] == -1:
                break
            self.gameboard[i][j] += 1

class USSRchan:
    def __init__(self, positions):
        self.combinations = []
        for perm in permutations(["king", "queen", "knight", "bishop", "rook"], 5):
            self.combinations.append(Combination(positions, perm))

    def get_statistic(self, r, c):
        dict_stat = {}
        for comb in self.combinations:
            dict_stat[comb.gameboard[r][c]] = 1 + dict_stat.get(comb.gameboard[r][c], 0)
        # print("r =", r, " c =", c, max(dict_stat.values()))
        return max(dict_stat.values())

    def move(self, answer = None, position = None):
        if answer is not None:
            r, c = position
            combinations = [comb for comb in self.combinations if comb.gameboard[r][c] == answer]
            self.combinations = combinations
        min_stat = len(self.combinations) + 1
        pos = []
        for r in range(8):
            for c in range(8):
                cur_stat = self.get_statistic(r, c)
                if min_stat > cur_stat:
                    min_stat = cur_stat
                    pos = (r, c)
        return pos if len(self.combinations) > 1 else None

    def get_result(self):
        return self.combinations[0].positions

    def game(self):
        game_over = False
        answer = None
        position = None
        while not game_over:
            if len(self.combinations) == 1:
                game_over = True
            else:
                ask = self.move(answer, position)
                if ask is not None:
                    print(ask, "?")
                    answer = int(input())
                position = ask
        return self.get_result()


ussrchan = USSRchan([(0, 7), (3, 6), (5, 5), (7, 3), (7, 4)])
print(ussrchan.game())




def test_combination():
    position = [(4, 4), (3, 2)]
    figures = ["queen", "knight"]
    proba_comb = Combination(position, figures)
    print(proba_comb.positions)
    pprint(proba_comb.gameboard)

# test_combination()