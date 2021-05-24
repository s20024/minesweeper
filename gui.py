# モジュールのインポート
import random
import sys
import time

import pygame
from pygame.locals import *


# 爆弾をセットする関数
def bomb_set(bord_whole, bomb_number, bord_h, bord_w, fast_h, fast_w):
    for _ in range(bomb_number):
        while True:
            h, w = random.randint(1, bord_h), random.randint(1, bord_w)
            if h == fast_h and w == fast_w:
                continue
            if bord_whole[h][w]["bomb"] == False:
                bord_whole[h][w]["bomb"] = True
                break
    return bord_whole


# 爆弾を検知して、周りに番号を降る関数
def bomb_counter(bord_whole, bord_h, bord_w):
    for line in range(1, bord_h + 1):
        for cell in range(1, bord_w + 1):
            counter = 0
            for i in range(-1, 2):
                for j in range(-1, 2):
                    # なぜかエラーが出るからWall書かないといけない、、、
                    if bord_whole[line + i][cell + j]["wall"]:
                        continue
                    if bord_whole[line + i][cell + j]["bomb"]:
                        counter = counter + 1
            bord_whole[line][cell]["number_bomb"] = counter

    return bord_whole


# 処理をする関数
def cal(bord_whole, h, w, bord_h, bord_w):
    count = 0
    serch_list = []
    serch_list.append([h, w])
    while True:
        try:
            bord_whole[serch_list[count][0]][serch_list[count][1]]["open_close"] = True
            if (
                bord_whole[serch_list[count][0]][serch_list[count][1]]["number_bomb"]
                == 0
            ):
                if [
                    serch_list[count][0] - 1,
                    serch_list[count][1],
                ] not in serch_list and not bord_whole[serch_list[count][0] - 1][
                    serch_list[count][1]
                ][
                    "wall"
                ]:
                    serch_list.append([serch_list[count][0] - 1, serch_list[count][1]])

                if [
                    serch_list[count][0],
                    serch_list[count][1] - 1,
                ] not in serch_list and not bord_whole[serch_list[count][0]][
                    serch_list[count][1] - 1
                ][
                    "wall"
                ]:
                    serch_list.append([serch_list[count][0], serch_list[count][1] - 1])

                if [
                    serch_list[count][0],
                    serch_list[count][1] + 1,
                ] not in serch_list and not bord_whole[serch_list[count][0]][
                    serch_list[count][1] + 1
                ][
                    "wall"
                ]:
                    serch_list.append([serch_list[count][0], serch_list[count][1] + 1])

                if [
                    serch_list[count][0] + 1,
                    serch_list[count][1],
                ] not in serch_list and not bord_whole[serch_list[count][0] + 1][
                    serch_list[count][1]
                ][
                    "wall"
                ]:
                    serch_list.append([serch_list[count][0] + 1, serch_list[count][1]])

        except:
            break

        count = count + 1
    return bord_whole


# 出力する関数
def pri():
    screen.fill((255, 255, 255))
    for i, line in enumerate(bord_whole):
        for j, cell in enumerate(line):
            # ゲームオーバのときの爆弾の表示
            if game_over and cell["bomb"]:
                screen.blit(img_bomb, (j * 40, i * 40))
                continue

            # 旗の表示
            if cell["flag"]:
                screen.blit(img_flag, (j * 40, i * 40))
                continue

            # 壁の表示
            if cell["wall"]:
                pygame.draw.rect(screen, (0, 0, 0), Rect(j * 40, i * 40, 40, 40))
                continue

            # 数字の表示
            if cell["number_bomb"] != 0 and cell["open_close"]:
                screen.blit(
                    font.render(str(cell["number_bomb"]), True, (0, 0, 0)),
                    [j * 40, i * 40],
                )
                continue

            # 何もないところの表示
            if cell["open_close"]:
                pygame.draw.rect(screen, (255, 255, 255), Rect(j * 40, i * 40, 40, 40))
            else:
                pygame.draw.rect(screen, (157, 204, 224), Rect(j * 40, i * 40, 40, 40))
    pygame.display.update()


# 最初のデータ取得
args = sys.argv
try:
    bord_h, bord_w, bomb_number = map(int, args[1:4])
    while True:
        if bomb_number > bord_h * bord_w:
            bomb_number = int(input("爆弾の数を半角数字で入力してください>"))
        else:
            break

# データを取るときにエラーが出た場合の処理
except:
    bord_h = int(input("マインスイーパーの高さを半角数字で入れてください>"))
    bord_w = int(input("マインスイーパーの横の長さを半角数字で入れてください>"))
    bomb_number = int(input("爆弾の数を半角数字で入力してください>"))
    while True:
        if bomb_number > bord_h * bord_w:
            bomb_number = int(input("爆弾の数を半角数字で入力してください>"))
        else:
            break


# 初期設定等
bord_whole = []
wall_cell = {
    "open_close": True,
    "bomb": False,
    "number_bomb": 0,
    "wall": True,
    "flag": False,
}
wall_line = [{**wall_cell, **{"wall_number": i}} for i in range(bord_w + 2)]
bord_whole.append(wall_line)
for i in range(bord_h):
    bord_whole.append(
        [{**wall_cell, **{"wall_number": i + 1}}]
        + [
            {
                "open_close": False,
                "bomb": False,
                "number_bomb": 0,
                "wall": False,
                "flag": False,
            }
            for _ in range(bord_w)
        ]
        + [{**wall_cell, **{"wall_number": i + 1}}]
    )
bord_whole.append(wall_line)

# pygameの設定
pygame.init()
screen = pygame.display.set_mode(((bord_w + 2) * 40, (bord_h + 2) * 40))
screen.fill((255, 255, 255))
pygame.display.update()
font = pygame.font.Font(None, 55)
img_bomb = pygame.image.load("bomb.png")
img_bomb = pygame.transform.scale(img_bomb, (40, 40))
img_flag = pygame.image.load("flag.png")
img_flag = pygame.transform.scale(img_flag, (40, 40))
game_over = False
pri()


# ゲームの本体
fast = True
while True:
    event = pygame.event.poll()
    if event.type == QUIT:
        pygame.quit()
    if event.type == MOUSEMOTION:
        px, py = event.pos
    if event.type == MOUSEBUTTONDOWN and event.button == 1:
        h, w = py // 40, px // 40
        if bord_whole[h][w]["flag"]:
            continue

        if fast:
            bord_whole[h][w]["open_close"] = True
            bord_whole = bomb_set(bord_whole, bomb_number, bord_h, bord_w, h, w)
            bord_whole = bomb_counter(bord_whole, bord_h, bord_w)
            bord_whole = cal(bord_whole, h, w, bord_h, bord_w)
            fast = False
            pri()
        else:
            bord_whole = cal(bord_whole, h, w, bord_h, bord_w)
        b_c = 0
        c_c = 0
        for line in bord_whole:
            for cell in line:
                if not cell["open_close"]:
                    c_c = c_c + 1
                if cell["bomb"]:
                    b_c = b_c + 1
        if c_c == b_c:
            pri()
            font = pygame.font.Font(None, 40)
            screen.blit(
                font.render(("YOU ARE WINNER!!"), True, (255, 0, 0)),
                [bord_w * 40 // 8 + 40, bord_h * 40 // 8 + 40],
            )
            pygame.display.update()
            time.sleep(5)
            break
        if bord_whole[h][w]["bomb"]:
            game_over = True
            pri()
            font = pygame.font.Font(None, 40)
            screen.blit(
                font.render(("GAME OVER!!"), True, (255, 0, 0)),
                [bord_w * 40 // 8 + 40, bord_h * 40 // 8 + 40],
            )
            pygame.display.update()
            time.sleep(5)
            break
        pri()

    if event.type == MOUSEBUTTONDOWN and event.button == 3:
        h, w = py // 40, px // 40
        if bord_whole[h][w]["flag"]:
            bord_whole[h][w]["flag"] = False
        else:
            bord_whole[h][w]["flag"] = True
        pri()
