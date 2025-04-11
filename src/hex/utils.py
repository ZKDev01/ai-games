from copy import deepcopy
from typing import List
from random import choice


from src.hex.board import HexBoard, is_terminal_game
from src.utils.mcts import Node,MCTS

class HexMCTS(Node):
  def __init__(self,player_id:int,matrix:List[List[int]]) -> None:
    self.player_id = player_id
    self.enemy = 1 if player_id == 2 else 1
    self.matrix = matrix
    
  def find_children(self):
    if self.is_terminal():
      return set()
    
    possible_moves = []
    for i in range(len(self.matrix)):
      for j in range(len(self.matrix[0])):
        if self.matrix[i][j] == 0:
          possible_moves.append((i,j))
    return { self.make_move(i) for i in possible_moves }
    
  def find_random_child(self):
    if self.is_terminal():
      return None
    
    possible_moves = []
    for i in range(len(self.matrix)):
      for j in range(len(self.matrix[0])):
        if self.matrix[i][j] == 0:
          possible_moves.append( (i,j) )
    
    return self.make_move(choice(possible_moves))

  def reward(self) -> float:
    if not self.is_terminal():
      raise RuntimeError("reward called on nonterminal state")
    if is_terminal_game(self.matrix,self.enemy):
      return 0
    return 0.5
  
  def is_terminal(self):
    winner = is_terminal_game(self.matrix,self.player_id) or is_terminal_game(self.matrix,self.enemy)
    if winner:
      return winner
    return self.is_tie()
  
  def is_tie(self):
    for i in range(len(self.matrix)):
      for j in range(len(self.matrix[0])):
        if self.matrix[i][j] == 0:
          return False
    return True
  
  def make_move(self, move:tuple) -> 'HexMCTS':
    i,j = move
    matrix = deepcopy(self.matrix)
    matrix[i][j] = self.player_id
    return HexMCTS(self.enemy,matrix)




