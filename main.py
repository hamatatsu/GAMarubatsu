# %% ライブラリインポート
import datetime
import os
import random

import matplotlib.pyplot as plt
import numpy as np


# %% 有効盤面インデックス作成
def create_board_index():
  allcode = np.arange(pow(3, 9))
  # 全盤面生成
  decoded = np.array([decode(i) for i in allcode])
  # 決着判定
  batsu_win = np.where([wincheck(decoded[i, :], 1) for i in allcode])
  maru_win = np.where([wincheck(decoded[i, :], 2) for i in allcode])
  # 手番判定
  batsu_turns = np.array([np.sum(decoded[i, :] == 1) for i in allcode])
  maru_turns = np.array([np.sum(decoded[i, :] == 2) for i in allcode])
  sub_turns = batsu_turns - maru_turns
  turns = np.where((sub_turns < 0) | (1 < sub_turns))[0]
  # 全埋め判定
  fill = np.where([np.sum(np.where(decoded[i, :] > 0, 1, 0)) == 9 for i in allcode])[0]
  # 除外
  index = np.setdiff1d(allcode, batsu_win)
  index = np.setdiff1d(index, maru_win)
  index = np.setdiff1d(index, turns)
  index = np.setdiff1d(index, fill)
  return index


# %% 生成用インデックス作成
def create_generation_index():
  decoded = np.array([decode(i) for i in BOARD_INDEX])
  index = np.array([np.where(decoded[i, :] == 0)[0] for i in range(CHROMOSOME_LEN)], dtype=np.object)
  return index


# %% 空いてるマスをランダムに選択
def generation_num(index):
  # 盤面の0の部分から一つ選ぶ
  num = np.random.choice(GENERATION_INDEX[index])
  return num
generation_num_np = np.frompyfunc(generation_num, 1, 1)


# %% 初期集団の生成
def generation():
  tmp = np.tile(np.arange(CHROMOSOME_LEN), (POPULATION_NUM, 1))
  population = generation_num_np(tmp)
  population = population.astype(np.int32)
  return population


# %% 符号化
def encode(board):
  index = np.dot(board, THREE)
  index = np.where(BOARD_INDEX == index)[0][0]
  return index


# %% 3進法変換
def to3(array, num):
  quotient = int(num / 3)
  array = np.append(array, num % 3)
  if(quotient != 0):
    return to3(array, quotient)
  return array


# %% 復号
def decode(index):
  board = to3(np.empty(0, np.int32), index)
  board.resize(NUM_MAX, refcheck=False)
  return board


# %% 並び判定
def wincheck(board, turnflag):
  win = np.any(np.all(board[WINLANE] == turnflag, axis=1))
  return win


# %% まるばつゲーム
def marubatsu(batsu, maru):
  # 勝敗 先攻 1, 後攻 2, 引き分け 0
  result = 0
  board = np.zeros(NUM_MAX)
  # 勝敗が付くまでループ
  for turn in range(NUM_MAX):
    # 手番 先攻 1, 後攻 2
    turnflag = turn % 2 + 1
    # 印の位置
    if turnflag == 1:
      index = batsu[encode(board)]
    else:
      index = maru[encode(board)]
    # 既に印がある時
    if board[index] != 0:
      # 手番の逆が勝利
      result = 3 - turnflag
      break
    # 印をつける
    board[index] = turnflag
    print(np.reshape(np.where(board == 1, 'x', np.where(board == 2, 'o', ' ')), [3, 3]))
    # 3つ並んだ時
    if wincheck(board, turnflag):
      # 手番が勝利
      result = turnflag
      break
  print(result)
  return result


# %% 評価
def evaluation(population, random=False):
  # スコア記録 引き分け 勝ち 負け
  scores = np.zeros([POPULATION_NUM, 3])
  # enemies = generation()
  # 総当たり
  for bi in range(POPULATION_NUM):
    for mi in range(bi):
      result = marubatsu(population[bi], population[mi])
      scores[bi, result] += 1
      scores[mi, (3-result) % 3] += 1
    # ランダムな相手
    # if random:
    #   for enemy in enemies:
    #     result = marubatsu(population[bi], enemy)
    #     scores[bi, result] += 1
  return scores


# %% 選択
def selection(population, fitnesses):
  index = np.random.choice(POPULATION_ARRAY, size=POPULATION_NUM, p=fitnesses)
  population = population[index]
  return population


# %% 交叉
def crossover(population):
  index = np.random.choice(POPULATION_ARRAY, size=CROSSOVER_NUM, replace=False)
  crossed = np.copy(population)
  # 2つづつ取り出し2点交叉
  for i, j in index.reshape([-1, 2]):
    r = random.randint(1, CHROMOSOME_LEN-1)
    crossed[i] = np.concatenate([population[i][:r], population[j][r:]])
    crossed[j] = np.concatenate([population[j][:r], population[j][r:]])
  return crossed


# %% 突然変異
def mutation(population):
  p_index = np.random.choice(POPULATION_ARRAY, size=MUTATION_NUM)
  c_index = np.random.randint(0, CHROMOSOME_LEN, MUTATION_NUM)
  random = generation_num_np(c_index)
  population[p_index, c_index] = random
  return population


# %% 表示
def print_text(gen, scores):
  print(f'{gen}世代')
  top = np.where(scores[:, 2] == np.min(scores[:, 2]))[0][0]
  loserate = scores[top, 2]/np.sum(scores[top])
  print(f' 敗率: {loserate} 成績:{scores[top]}')


# %% ファイルに保存
def save_record(gen, population, scores):
  np.savez(f'{RECORD_PATH}/{gen:06}', population=population, scores=scores)


# %% グローバル変数
RECORD_PATH = 'records/'
POPULATION_NUM = 5
GEN_MAX = 1
NUM_MAX = 9
CROSSOVER_RATE = 0.8
MUTATION_RATE = 0.05
# 日付
date = datetime.datetime.now()
date = date.strftime('%y%m%d-%H%M%S/')
# 記録パス
RECORD_PATH = RECORD_PATH + date
# 公比3の等比数列
THREE = np.power(3, np.arange(9))
# 並び判定用配列
WINLANE = np.array([
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    [0, 3, 6], [1, 4, 7], [2, 5, 8],
    [0, 4, 8], [2, 4, 6]
])
# ポイント 引き分け 勝ち 負け
POINT = [1, 3, 0]
# %% 前処理
# 有効盤面インデックス
BOARD_INDEX = create_board_index()
CHROMOSOME_LEN = len(BOARD_INDEX)
# 生成用インデックス
GENERATION_INDEX = create_generation_index()
# 選択用インデックス
POPULATION_ARRAY = np.arange(POPULATION_NUM)
# 交叉数
CROSSOVER_NUM = int(POPULATION_NUM * CROSSOVER_RATE)
# 突然変異数
MUTATION_NUM = int(POPULATION_NUM * CHROMOSOME_LEN * MUTATION_RATE)
# 記録フォルダ作成
# os.mkdir(RECORD_PATH)


# %% main
print('初期集団生成')
population = generation()

for gen in range(1, GEN_MAX+1):
  scores = evaluation(population)
  print_text(gen, scores)
  # 第1世代、1/10世代を記録
  # if gen == 1 or gen % (GEN_MAX/10) == 0:
    # save_record(gen, population, scores)

  points = np.dot(scores, POINT)
  points = points - np.min(points)
  # points = POPULATION_NUM * 2 - scores[:,2]
  fitnesses = points / np.sum(points)
  population = selection(population, fitnesses)
  population = crossover(population)
  population = mutation(population)
