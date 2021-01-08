# %% ライブラリインポート
import matplotlib.pyplot as plt
import numpy as np

# %% グローバル変数
POPULATION_NUM = 100
CHROMOSOME_LEN = pow(3, 9)
VALUE_MAX = 9

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


# %% generate
def generate():
  # generate random int 0~8
  population = np.random.randint(0, VALUE_MAX, (POPULATION_NUM, CHROMOSOME_LEN))
  return population


# %% 配列番号生成
def makeindex(board):
  makeindex = int(np.dot(board.ravel(), THREE))
  return makeindex


# %% 並び判定
def wincheck(board, turnflag):
  win = np.any(np.all(board[WINLANE] == turnflag, axis=1))
  return win


# %% まるばつゲーム
def marubatsu(batsu, maru):
  # 勝敗 先攻 1, 後攻 2, 引き分け 0
  result = 0
  board = np.zeros(9)
  # 勝敗が付くまでループ
  for turn in range(9):
    # 手番 先攻 1, 後攻 2
    turnflag = turn % 2 + 1
    # 印の位置
    if turnflag == 1:
      index = batsu[makeindex(board)]
    else:
      index = maru[makeindex(board)]
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
      scores[mi, (3-result)%3] += 1
  return scores


# %% selection
def selection():
  return 0


# %% crossover
def crossover():
  return 0


# %% mutation
def mutation():
  return 0


# %% main
def main():
  population = generate()
  record = []
  for i in range(100):
    print(str(i+1)+"世代")
    scores = evaluate(population)
    record.append(scores)
    fitnesses = np.dot(scores, POINT)

  return record


# %% testcode
if __name__ == "__main__":
  main()
# %%
