# モジュールのインポート
import random
import sys


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
    for line in bord_whole:
        for cell in line:
            if cell["wall"]:
                print(str(cell["wall_number"]).zfill(2), end="")
                continue
            if cell["number_bomb"] != 0 and cell["open_close"]:
                print(num[cell["number_bomb"]], end="")
                continue
            if cell["open_close"]:
                print("　", end="")
            else:
                print("⬜", end="")
        print()


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
wall_cell = {"open_close": True, "bomb": False, "number_bomb": 0, "wall": True}
wall_line = [{**wall_cell, **{"wall_number": i}} for i in range(bord_w + 2)]
bord_whole.append(wall_line)
for i in range(bord_h):
    bord_whole.append(
        [{**wall_cell, **{"wall_number": i + 1}}]
        + [
            {"open_close": False, "bomb": False, "number_bomb": 0, "wall": False}
            for _ in range(bord_w)
        ]
        + [{**wall_cell, **{"wall_number": i + 1}}]
    )
bord_whole.append(wall_line)
num = ["０", "１", "２", "３", "４", "５", "６", "７", "８", "９"]


pri()
try:
    fast_h, fast_w = map(int, input("クリックする場所を指定してください>").split())
except:
    while True:
        fast_h = int(input("高さを指定してください"))
        fast_w = int(input("横を指定してください"))
        if fast_h <= bord_h and fast_w <= bord_w:
            break

# ゲームの本体
bord_whole[fast_h][fast_w]["open_close"] = True
bord_whole = bomb_set(bord_whole, bomb_number, bord_h, bord_w, fast_h, fast_w)
bord_whole = bomb_counter(bord_whole, bord_h, bord_w)
bord_whole = cal(bord_whole, fast_h, fast_w, bord_h, bord_w)
while True:
    pri()
    try:
        h, w = map(int, input().split())
    except:
        while True:
            h = int(input("高さを指定してください"))
            w = int(input("横を指定してください"))
            if h <= bord_h and w <= bord_w:
                break

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
        print("YOU ARE WINNER!!")
        break
    if bord_whole[h][w]["bomb"]:
        print("GAME OVER!!")
        break
