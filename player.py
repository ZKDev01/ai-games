import random
from typing import List

from utils import minimax
from utils import MCTS,HexMCTS
from board import HexBoard

class Player:
  def __init__(self, player_id:int):
    self.player_id:int = player_id  # Identificador => [1 o 2]

  def play(self, board:HexBoard) -> tuple:
    raise NotImplementedError("Not implemented `play` method in `Player` class")

class RandomPlayer(Player):
  def __init__(self, player_id):
    super().__init__(player_id)

  def play(self, board:HexBoard) -> tuple:
    possible_moves = board.get_possible_moves()
    return random.choice(possible_moves)

class MinimaxPlayer(Player):
  def __init__(self, player_id):
    super().__init__(player_id)
  
  def play(self, board:HexBoard) -> tuple:
    move:tuple = minimax(board, self.player_id)
    return move

class MCTSPlayer(Player):
  def __init__(self, player_id:int):
    super().__init__(player_id)
    self.tree:MCTS = MCTS()
  
  def play(self, board:HexBoard) -> tuple:
    last_matrix:List[List[int]] = board.board
    node = HexMCTS(self.player_id,board.board)
    for _ in range(500):
      self.tree.do_rollout(node=node)
    best:HexMCTS = self.tree.choose(node=node)
    best_matrix = best.matrix  
    return search_move(best_matrix,last_matrix)

def search_move(best_matrix:List[List[int]],last_matrix:List[List[int]]) -> tuple:
  xi,yi = -1,-1
  for i in range(len(best_matrix)):
    for j in range(len(best_matrix[0])):
      if best_matrix[i][j] != last_matrix[i][j]:
        xi,yi = i,j
  return xi,yi
