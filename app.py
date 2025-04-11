import argparse

#from src.hex.game import run_hex_game
#from experimental.tmp.utils.hex import run_hex_game

def main():
  parser = argparse.ArgumentParser(description="Ejecutar diferentes juegos")
  parser.add_argument("game", choices=["hex"])
  parser.add_argument("ai", choices=["random", "minimax", "mcts"])
  args = parser.parse_args()

  if args.game == "hex":
    ...
    

if __name__ == "__main__":
  main()
  
