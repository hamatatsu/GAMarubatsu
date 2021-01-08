# %% import
import matplotlib.pyplot as plt
import numpy as np

population_num = 100
chromosome_len = pow(3, 9)  # 3^9
value_max = 9

THREE = np.power(3, np.arange(9))  # 公比3の等比数列
winline = np.array([
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    [0, 3, 6], [1, 4, 7], [2, 5, 8],
    [0, 4, 8], [2, 4, 6]
])


# %% generate
def generate():
  # generate random int 1~9
  population = np.random.randint(1, value_max+1, (population_num, chromosome_len))
  return population


# %% 配列番号生成
def makeindex(board):
  makeindex = np.dot(board.ravel(), THREE)
  return makeindex


# %% まるばつゲーム
def marubatsu(batsu, maru):
  result = 0  # 勝敗 先攻 1, 後攻 -1, 引き分け 0
  board = np.zeros(9)
  # 勝敗が付くまでループ
  for turn in range(9):
    turnflag = turn % 2 + 1  # 手番 先攻 1, 後攻 2
    index = makeindex(board)
    # 既に印がある時
    if board[index] != 0:
      result = turnflag * 2 - 3  # 手番の逆が勝利
      break
    board[index] = turnflag
    # 3つ並んだ時
    if wincheck(board, 1):
      result = 3 - turnflag * 2  # 手番が勝利
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
