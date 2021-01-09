# %% ライブラリインポート
import matplotlib.pyplot as plt
import numpy as np
import random

# %% グローバル変数
POPULATION_NUM = 100
CHROMOSOME_LEN = pow(3, 9)
VALUE_MAX = 9
MUTATION_RATE = 0.001

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
# 選択用インデックス
NUMBERS = np.arange(POPULATION_NUM)

MUTATION_NUM = int(POPULATION_NUM * CHROMOSOME_LEN * MUTATION_RATE)


# %% generate
def generate():
  # generate random int 0~8
  population = np.random.randint(0, VALUE_MAX, [POPULATION_NUM, CHROMOSOME_LEN])
  return population


# %% 符号化
def encode(board):
  index = int(np.dot(board.ravel(), THREE))
  return index


# %% 3進法変換
def to3(array, num):
  quotient = int(num / 3)
  array.append(num % 3)
  if(quotient != 0):
    return to3(array, quotient)
  return array


# %% 復号
def decode(index):
  board = np.array(to3([], index))
  board.resize(VALUE_MAX)
  return board


# %% 並び判定
def wincheck(board, turnflag):
  win = np.any(np.all(board[WINLANE] == turnflag, axis=1))
  return win


# %% まるばつゲーム
def marubatsu(batsu, maru):
  # 勝敗 先攻 1, 後攻 2, 引き分け 0
  result = 0
  board = np.zeros(VALUE_MAX)
  # 勝敗が付くまでループ
  for turn in range(VALUE_MAX):
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
    # 3つ並んだ時
    if wincheck(board, turnflag):
      # 手番が勝利
      result = turnflag
      break
  return result


# %% 評価
def evaluate(population):
  # スコア記録 引き分け 勝ち 負け
  scores = np.zeros([POPULATION_NUM, 3])
  # 総当たり
  for bi in range(POPULATION_NUM):
    for mi in range(bi):
      result = marubatsu(population[bi], population[mi])
      scores[bi, result] += 1
      scores[mi, (3-result) % 3] += 1
  return scores


# %% 選択
def selection(population, fitnesses):
  index = np.random.choice(NUMBERS, size=POPULATION_NUM, p=fitnesses)
  population = population[index]
  return population


# %% 交叉
def crossover(population):
  for i in range(0, POPULATION_NUM, 2):
    r = random.randint(0, CHROMOSOME_LEN)
    population[i] = np.concatenate([population[i][:r], population[i+1][r:]])
  return population


# %% 突然変異
def mutation(population):
  index = np.random.choice(NUMBERS, size=MUTATION_NUM)
  r = np.random.randint(0, CHROMOSOME_LEN, MUTATION_NUM)
  random = np.random.randint(0, VALUE_MAX, MUTATION_NUM)
  population[index, r] = random
  return population


# %% main
population = generate()
record = []
for i in range(10000):
  scores = evaluate(population)
  record.append(scores)
  points = np.dot(scores, POINT)
  # 正規化
  fitnesses = points / np.sum(points)
  population = selection(population, fitnesses)
  population = crossover(population)
  population = mutation(population)
  print(f'{i+1}世代')
  top = np.where(points == np.max(points))
  winrate = scores[top, 1]/np.sum(scores[top])
  print(f' Winrate: {winrate[0, 0]}')

# %% csvファイルに保存
np.savetxt('scores.csv', np.array(scores), fmt='%d')
# %%
