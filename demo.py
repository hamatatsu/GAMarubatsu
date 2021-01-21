import numpy as np


WINLANE = np.array([
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    [0, 3, 6], [1, 4, 7], [2, 5, 8],
    [0, 4, 8], [2, 4, 6]
])
THREE = np.power(3, np.arange(9))
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


def wincheck(board, turnflag):
  win = np.any(np.all(board[WINLANE] == turnflag, axis=1))
  return win
def to3(array, num):
  quotient = int(num / 3)
  array = np.append(array, num % 3)
  if(quotient != 0):
    return to3(array, quotient)
  return array
def decode(index):
  board = to3(np.empty(0, np.int32), index)
  board.resize(9, refcheck=False)
  return board

def encode(board):
  index = np.dot(board, THREE)
  index = np.where(BOARD_INDEX == index)[0][0]
  return index

BOARD_INDEX = create_board_index()
r = np.load('records/201/001000.npz')
top = np.where(r['scores'][r['scores'][:, 2] == np.min(r['scores'][:, 2])])[0][0]
chromosome = r['population'][top]
while True:
  board = np.zeros(9)
  print(np.arange(9).reshape([3, 3]))
  if int(input('Who goes first? computer: 0, human: 1 ?: ')):
    while True:
      if wincheck(board, 2):
        print('computer win')
        break
      if np.sum(np.where(board > 0, 1, 0)) == 9:
        print('draw')
        break
      print(np.reshape(np.where(board == 1, 'x', np.where(board == 2, 'o', ' ')), [3, 3]))
      hand = int(input('?: '))
      board[hand] = 1
      if wincheck(board, 1):
        print(np.reshape(np.where(board == 1, 'x', np.where(board == 2, 'o', ' ')), [3, 3]))
        print('human win')
        break
      if np.sum(np.where(board > 0, 1, 0)) == 9:
        print('draw')
        break
      index = chromosome[encode(board)]
      board[index] = 2
  else:
    while True:
      index = chromosome[encode(board)]
      board[index] = 1
      print(np.reshape(np.where(board == 1, 'x', np.where(board == 2, 'o', ' ')), [3, 3]))
      if wincheck(board, 1):
        print('computer win')
        break
      if np.sum(np.where(board > 0, 1, 0)) == 9:
        print('draw')
        break
      hand = int(input('?: '))
      board[hand] = 2
      if wincheck(board, 2):
        print(np.reshape(np.where(board == 1, 'x', np.where(board == 2, 'o', ' ')), [3, 3]))
        print('human win')
        break
      if np.sum(np.where(board > 0, 1, 0)) == 9:
        print('draw')
        break
