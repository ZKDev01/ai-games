import math
from typing import Dict,Set,List
from collections import defaultdict

from node import Node


class MCTS:
  "Implementación de Monte Carlo Tree Search"
  
  def __init__(self, exploration_weight=1) -> None:
    self.Q:Dict[Node,int] = defaultdict(int)      # total reward of each node
    self.N:Dict[Node,int] = defaultdict(int)      # total visit count for each node
    self.children:Dict[Node,Node] = dict()        # children of each node
    self.exploration_weight = exploration_weight

  def choose(self, node:Node) -> Node:
    "Escoge el mejor sucesor de `node`. Escoge un movimiento del game tree"
    if node.is_terminal():
      raise RuntimeError(f"choose called on terminal node {node}")
    if node not in self.children:
      return node.find_random_child()

    def score(n:Node) -> float:
      "Average reward of node n"
      if self.N[n] == 0:
        return float("-inf")       
      return self.Q[n] / self.N[n] 

    return max(self.children[node], key=score)

  def do_rollout(self, node:Node) -> None:
    "Mejora el árbol en una iteración. Expande un nodo y simula su recompensa"
    path = self._select(node)
    leaf = path[-1]
    self._expand(leaf)
    reward = self._simulate(leaf)
    self._backpropagate(path, reward)

  def _select(self, node:Node) -> List[Node]:
    "Encuentra un descendiente de `node` que no ha sido explorado"
    path = []
    while True:
      path.append(node)
      if node not in self.children or not self.children[node]:
        return path
      unexplored = self.children[node] - self.children.keys()
      if unexplored:
        n = unexplored.pop()
        path.append(n)
        return path
      node = self._uct_select(node)  # descend a layer deeper

  def _expand(self, node:Node) -> None:
    "Actualiza el diccionario `children` con los de `node`"
    if node in self.children:
      return  # already expanded
    self.children[node] = node.find_children()

  def _simulate(self, node:Node) -> float:
    "Devuelve la recompensa de una simulacion aleatoria de `node`"
    invert_reward = True
    while True:
      if node.is_terminal():
        reward = node.reward()
        return 1 - reward if invert_reward else reward
      node = node.find_random_child()
      invert_reward = not invert_reward

  def _backpropagate(self, path:List[Node], reward:float) -> None:
    "Backpropagation: actualiza la recompensa de cada nodo en el camino"
    for node in reversed(path):
      self.N[node] += 1
      self.Q[node] += reward
      reward = 1 - reward  # "1 for me is 0 for my enemy"

  def _uct_select(self, node:Node) -> Node:
    "Selecciona un nodo hijo, equilibrando exploración y explotación"
    assert all(n in self.children for n in self.children[node])

    log_N_vertex = math.log(self.N[node])
    def uct(n):
      "UCT: Upper confidence bound for trees"
      return self.Q[n] / self.N[n] + self.exploration_weight * math.sqrt(log_N_vertex / self.N[n])

    return max(self.children[node], key=uct)