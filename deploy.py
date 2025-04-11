import pygame

from src.hex.board import HexBoard
from src.hex.player import MCTSPlayer, Player, RandomPlayer

def draw_hex_board(matrix, screen, cell_size=60, font_size=24):
  pygame.font.init()
  #font = pygame.font.Font(None, font_size)
  screen.fill((255, 255, 255))  # Fill the screen with white

  colors = {
      0: (255, 255, 255),  # White for 0
      1: (255, 0, 0),      # Red for 1
      2: (0, 0, 255),      # Blue for 2
  }
  
  for row in range(len(matrix)):
    for col in range(len(matrix[row])):
      x = col * cell_size + (row * cell_size // 2)
      y = row * (cell_size * 3 // 4)
      
      color = colors[matrix[row][col]]
      pygame.draw.polygon(
        screen,
        color,
        [
          (x + cell_size // 2, y),
          (x + cell_size, y + cell_size // 4),
          (x + cell_size, y + cell_size * 3 // 4),
          (x + cell_size // 2, y + cell_size),
          (x, y + cell_size * 3 // 4),
          (x, y + cell_size // 4),
        ]
      )
      pygame.draw.polygon(
        screen,
        #colors[matrix[row][col]],
        (200, 200, 200),
        [
          (x + cell_size // 2, y),
          (x + cell_size, y + cell_size // 4),
          (x + cell_size, y + cell_size * 3 // 4),
          (x + cell_size // 2, y + cell_size),
          (x, y + cell_size * 3 // 4),
          (x, y + cell_size // 4),
        ],
        1,
      )
      """
      if not matrix[row][col]:
        text = font.render(str( (row,col) ), True, (0, 0, 0))
        text_rect = text.get_rect(center=(x + cell_size // 2, y + cell_size // 2))
        screen.blit(text, text_rect)
      """

  pygame.display.flip()

def run_hex_game(ai_1:str='random', ai_2:str='mcts', N:int=11) -> None:
  """ 
  pygame.init()
  
  # Fix this to use the correct screen size
  screen = pygame.display.set_mode((1000, 600))
  pygame.display.set_caption(f"Hex Board Game: {ai_1} Player vs. {ai_2} Player")

  """

  #matrix = [[random.choice([0, 1, 2]) for _ in range(N)] for _ in range(N)]
  #matrix = [[(row,col) for col in range(N)] for row in range(N)]

  # init game
  game:HexBoard = HexBoard(N)
  # init ai
  p1:Player = RandomPlayer(1)
  p2:Player = MCTSPlayer(2)
  p_current = p1
  
  while True:
    while True:
      print("Turn AI: ", p_current.player_id)
      move:tuple = p_current.play(game)
      result = game.place_piece(move[0], move[1],p_current.player_id)
      if result:
        p_current = p2 if p_current.player_id == p1.player_id else p1
        break
      
    #print(game.board)
    if game.check_connection(1):
      print(f"Player 1 wins! => AI: {ai_1} Color: RED")
      #  pygame.image.save(screen, f"hex_game_{ai_1}_vs_{ai_2}.png")
      break
    if game.check_connection(2):
      print(f"Player 2 wins! => AI: {ai_2} Color: BLUE")
      #  pygame.image.save(screen, f"hex_game_{ai_1}_vs_{ai_2}.png")
      break
  
  return
  running = True
  aux = 1
  
  while running:
    
    t = pygame.time.get_ticks()/1000
    if aux == t:
      aux += 1
      
      while True:
        print("Turn AI: ", p_current.player_id)
        move:tuple = p_current.play(game)
        result = game.place_piece(move[0], move[1],p_current.player_id)
        if result:
          p_current = p2 if p_current.player_id == p1.player_id else p1
          break
    
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
    
    draw_hex_board(game.board, screen, cell_size=60, font_size=24)
    
    if game.check_connection(1):
      print(f"Player 1 wins! => AI: {ai_1} Color: RED")
      pygame.image.save(screen, f"hex_game_{ai_1}_vs_{ai_2}.png")
      break
    if game.check_connection(2):
      print(f"Player 2 wins! => AI: {ai_2} Color: BLUE")
      pygame.image.save(screen, f"hex_game_{ai_1}_vs_{ai_2}.png")
      break
      
  pygame.quit()




if __name__ == "__main__":
  run_hex_game()