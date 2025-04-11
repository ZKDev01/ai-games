from typing import List
import copy
from src.utils.mcts import Node

direcciones = [
  ( 0, -1), # Izquierda
  ( 0,  1), # Derecha
  (-1,  0), # Arriba
  ( 1,  0), # Abajo
  (-1,  1), # Arriba derecha
  ( 1, -1)  # Abajo izquierda
]


class HexBoard:
  def __init__(self, size: int):
    """Constructor de la clase HexBoard

    Args:
        `size` (int): tamaño N del tablero (NxN)
    """
    self.size:int = size 
    # Matriz NxN (0=vacío, 1=Jugador1, 2=Jugador2)
    self.board:list[list[int]] = [[0 for _ in range(size)] for _ in range(size)]  

  def clone(self) -> 'HexBoard': 
    "Devuelve una copia del tablero actual"
    tmp = self.__class__(self.size)
    tmp.board = copy.deepcopy(self.board)
    return tmp

  def place_piece(self, row: int, col: int, player_id: int) -> bool:
    "Coloca una ficha si la casilla está vacía"
    if player_id != 1 and player_id != 2:
      raise Exception("player_id no es ni 1, ni 2")
    
    if self.board[row][col] != 0:
      return False
    self.board[row][col] = player_id
    return True

  def get_possible_moves(self) -> list:
    "Devuelve todas las casillas vacías como tuplas (fila, columna)"
    possible_moves = [ (i,j) for i in range(self.size) for j in range(self.size) ]
    return possible_moves
    
  def check_connection(self, player_id: int) -> bool:
    "Verifica si el jugador ha conectado sus dos lados"
    return is_terminal_game(
      matrix= self.board,
      id= player_id
    )

def is_terminal_game(matrix:List[List[int]],id:int) -> bool:
  "Regla: id=1 true si une el tablero horizontalmente, id=2 true si une el tablero verticalmente"
  size = len(matrix)
  visited = set()

  def dfs(x, y):
    if (x, y) in visited:
      return False
    visited.add((x, y))

    if id == 1 and y == size - 1:  # Player 1 connects horizontally
      return True
    if id == 2 and x == size - 1:  # Player 2 connects vertically
      return True

    for dx, dy in direcciones:
      nx, ny = x + dx, y + dy
      if 0 <= nx < size and 0 <= ny < size and matrix[nx][ny] == id:
        if dfs(nx, ny):
          return True
    return False

  if id == 1:  # Player 1 starts from the left edge
    for i in range(size):
      if matrix[i][0] == id and dfs(i, 0):
        return True
  elif id == 2:  # Player 2 starts from the top edge
    for j in range(size):
      if matrix[0][j] == id and dfs(0, j):
        return True

  return False


