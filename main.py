import pyautogui
import time
import os.path
import datetime
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

width = 70
coord_cells = [[(70 + width * column, 105 + width * row) for column in range(8)] for row in range(8)]

give_answer_btn = (480, 650)
play_btn = (475, 80)

class USSRchan:
    count_click_for_figures = {"knight": 1, "rook": 2, "bishop": 3, "queen": 4, "king": 5}

    def __init__(self):
        positions = self.get_figures_position()
        self.combinations = []
        for perm in permutations(["king", "queen", "knight", "bishop", "rook"], 5):
            self.combinations.append(Combination(positions, perm))

    def get_figures_position(self):
        list_questions = list(pyautogui.locateAllOnScreen('resources/question.png', confidence=0.975))
        result = set()
        for x, y, w, h in list_questions:
            x -= 70
            y -= 105
            j = x // width + 1
            i = y // width + 1
            result.add((i, j))
        return list(result)

    def get_statistic(self, r, c):
        dict_stat = {}
        for comb in self.combinations:
            dict_stat[comb.gameboard[r][c]] = 1 + dict_stat.get(comb.gameboard[r][c], 0)
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
        figures_pos = self.combinations[0].positions
        for x, y, f in figures_pos:
            pyautogui.moveTo(*coord_cells[x][y])
            time.sleep(0.1)
            for _ in range(self.count_click_for_figures[f]):
                pyautogui.click(*coord_cells[x][y])
                time.sleep(0.1)
        pyautogui.moveTo(give_answer_btn)
        time.sleep(0.1)
        pyautogui.click(clicks=2, interval=0.2)
        return figures_pos

    def get_answer(self, ask):
        left_top = tuple(n - width // 2 for n in coord_cells[ask[0]][ask[1]])
        for file_name in os.listdir('numbers'):
            try:
                file_path = os.path.join('numbers', file_name)
                if pyautogui.locateOnScreen(file_path, region=(*left_top, width, width), confidence=0.85) is None:
                    continue
                return int(file_name[0])
            except pyautogui.ImageNotFoundException:
                pass
        raise ValueError

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
                    pyautogui.moveTo(coord_cells[ask[0]][ask[1]])
                    time.sleep(0.1)
                    pyautogui.click()
                    time.sleep(0.1)
                    try:
                        answer = self.get_answer(ask)
                    except ValueError:
                        cur_file_name = str(datetime.datetime.now()).split('.')[0] + '.png'
                        cur_file_name = cur_file_name.replace(':', '_')
                        pyautogui.screenshot(os.path.join('fails', cur_file_name))
                        game_over = True
                position = ask
        return self.get_result()

if __name__ == '__main__':
    for _ in range(10):
        pyautogui.moveTo(play_btn)
        time.sleep(0.1)
        pyautogui.click()
        ussrchan = USSRchan()
        ussrchan.game()
        time.sleep(0.1)
        pyautogui.click()