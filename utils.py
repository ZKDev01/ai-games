from copy import deepcopy
from math import inf
from typing import List
from random import choice

from board import HexBoard, is_terminal_game
from mcts import Node,MCTS


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


change_player = lambda x: 1 if x == 2 else 1

def minimax (game:HexBoard,player_id:int) -> tuple:
  depth = int(0.5*game.size)
  best_move,best_value = MAX(
    game=game,
    move=None,
    player_id=player_id,
    depth=depth
  )
  return best_move

def MAX(game:HexBoard,move:tuple,player_id:int,depth:int,alpha=-inf,beta=+inf) -> tuple:
  if is_terminal(game):
    return move,-1
  if not depth:
    return move,heuristic(
      player_id=player_id,
      game=game
    )
  
  best_move = None
  best_value = -inf
  for tup in game.get_possible_moves():
    x,y = tup
    # clon and play
    clon = game.clone()
    id = player_id
    result = clon.place_piece(x,y,id)
    if not result:
      continue
    
    # play min
    _,value = MIN(
      clon,
      (x,y),
      player_id,
      depth-1,
      alpha=alpha,
      beta=beta
    )
  
    # alpha-beta cut
    alpha = max(alpha,value)
    if alpha >= beta:
      break
    
    # update values
    if value > best_value:
      best_value = value
      best_move = (x,y)
  
  return best_move,best_value

def MIN(game:HexBoard,move:tuple,player_id:int,depth:int,alpha=-inf,beta=+inf) -> tuple:
  if is_terminal(game):
    return move,1
  if not depth:
    return move,heuristic(
      player_id=change_player(player_id),
      game=game
    )
  
  best_move = None
  best_value = inf
  for tup in game.get_possible_moves():
    x,y = tup
    
    # clon and play
    clon = game.clone()
    id = change_player(player_id)
    result = clon.place_piece(x,y,id)
    if not result:
      continue
    
    _,value = MAX(
      clon,
      (x,y),
      player_id,
      depth-1,
      alpha=alpha,
      beta=beta
    )
    
    # alpha-beta cut
    beta = min(beta,value)
    if beta <= alpha:
      break
    
    # update values
    if value < best_value:
      best_value = value
      best_move = (x,y)
  
  return best_move,best_value


def is_terminal(game:HexBoard) -> bool:
  if game.check_connection(1) or game.check_connection(2):
    return True
  return False


def heuristic(game:HexBoard, player_id:int) -> float:
  size = game.size
  center_r = (size - 1) // 2 
  center_c = (size - 1) // 2  
  max_distance = (size - 1) // 2  
  player_score = 0.0
  opponent_score = 0.0
  
  for row in range(size):
    for col in range(size):
      owner = game.board[row][col]
      if not owner:
        continue  

      distance = max(abs(row - center_r), abs(col - center_c))
      centrality = (max_distance - distance) / max_distance if max_distance != 0 else 1.0

      if owner == player_id:
        player_score += centrality
      else:
        opponent_score += centrality

  total = max(player_score, opponent_score)  
  if total == 0:
    return 0
  return (player_score - opponent_score) / total