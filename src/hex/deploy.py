
from hex.board import HexBoard
from hex.player import MCTSPlayer, MinimaxPlayer, Player, RandomPlayer

def run_hex_game(N:int=11) -> None:
  # init game
  game:HexBoard = HexBoard(N)
  # init ai
  p1:Player = MCTSPlayer(1)
  ai_1:str = 'MCTS'
  p2:Player = MinimaxPlayer(2)
  ai_2:str = 'Minimax'
  
  p_current = p1
  
  
  while True:
    print("Turn AI: ", p_current.player_id)
    while True:
      
      move:tuple = p_current.play(game)
      result = game.place_piece(move[0], move[1],p_current.player_id)
      if result:
        p_current = p2 if p_current.player_id == p1.player_id else p1
        break
      
    #print(game.board)
    if game.check_connection(1):
      print(f"Player 1 wins! => AI: {ai_1} Color: RED")
      break
    if game.check_connection(2):
      print(f"Player 2 wins! => AI: {ai_2} Color: BLUE")
      break
  
  return


if __name__ == "__main__":
  run_hex_game()