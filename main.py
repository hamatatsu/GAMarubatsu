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


# %% generate
def generate():
  # generate random int 1~9
  population = np.random.randint(1, VALUE_MAX+1, (POPULATION_NUM, CHROMOSOME_LEN))
  return population


# %% 配列番号生成
def makeindex(board):
  makeindex = np.dot(board.ravel(), THREE)
  return makeindex


# %% 並び判定
def wincheck(board, turnflag):
  win = np.any(np.all(board[WINLANE] == turnflag, axis=1))
  return win


# %% まるばつゲーム
def marubatsu(batsu, maru):
  # 勝敗 先攻 1, 後攻 -1, 引き分け 0
  result = 0
  board = np.zeros(9)
  # 勝敗が付くまでループ
  for turn in range(9):
    # 手番 先攻 1, 後攻 2
    turnflag = turn % 2 + 1
    index = makeindex(board)
    # 既に印がある時
    if board[index] != 0:
      # 手番の逆が勝利
      result = turnflag * 2 - 3
      break
    board[index] = turnflag
    # 3つ並んだ時
    if wincheck(board, turnflag):
      # 手番が勝利
      result = 3 - turnflag * 2
      break
  return result


# %% evaluate
def evaluate():
  return 0


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
  return 0


# %% testcode
if __name__ == "__main__":
  main()
# %%
