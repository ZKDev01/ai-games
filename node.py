from typing import Dict,Set
from abc import ABC, abstractmethod


class Node(ABC):
  """ 
  Representación de un estado del juego
  Minimax busca en un game tree la mejor jugada
  MCTS construye un game tree a partir de nodos 
  """
  
  @abstractmethod
  def find_children(self) -> Set['Node']:
    "All possible successors of this board state"
    return set()

  @abstractmethod
  def find_random_child(self) -> 'Node':
    "Random successor of this board state (for more efficient simulation)"
    return None

  @abstractmethod
  def is_terminal(self) -> bool:
    "Returns True if the node has no children"
    return True

  @abstractmethod
  def reward(self) -> float:
    "Assumes `self` is terminal node. 1=win, 0=loss, .5=tie, etc"
    return 0

