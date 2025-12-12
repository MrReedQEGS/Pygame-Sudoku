import pygame,random
import sys

# --- Config ---
WINDOW_W, WINDOW_H = 640, 720
FPS = 60

GRID_SIZE = 9                  # 9x9 cells
CELL_SIZE = 40                 # pixels per cell
LINE_THICKNESS_THIN = 2
LINE_THICKNESS_THICK = 4

TEXT = "Sudoku"
FONT_SIZE = 48

# Layout: grid centered; text centered above it
GRID_W = GRID_SIZE * CELL_SIZE
GRID_H = GRID_SIZE * CELL_SIZE
TOP_MARGIN = 80
GAP_TEXT_TO_GRID = 20

pygame.init()
screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
pygame.display.set_caption("Simple sudoku game")
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, FONT_SIZE)
text_surf = font.render(TEXT, True, (0, 0, 0))
text_rect = text_surf.get_rect(center=(WINDOW_W // 2, TOP_MARGIN + text_surf.get_height() // 2))

grid_x0 = (WINDOW_W - GRID_W) // 2
grid_y0 = text_rect.bottom + GAP_TEXT_TO_GRID

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
Y_PADDING = 6

theNumbers = []


#It is not a valid grid in terms of game play.  This is just a test function to allow me to 
#make sure the numbers line up when it is all printed out.
def RandomGrid():
  for i in range(GRID_SIZE):
    newRow = []
    for j in range(GRID_SIZE):
      newRow.append(random.randint(1,9))
    theNumbers.append(newRow)

def RemoveRandomOnes():
  for i in range(30):
    j = random.randint(0,8)
    i = random.randint(0,8)
    theNumbers[j][i] = ""

def PrintGrid():
  for i in range(GRID_SIZE):
    print(theNumbers[i])
  

def DrawGrid():
  # Grid lines: 9x9 cells -> 10 lines each direction
  for i in range(GRID_SIZE + 1):
    x = grid_x0 + i * CELL_SIZE
    y = grid_y0 + i * CELL_SIZE
    
    
    #The sudoku grid has some lines thicker than others!
    lineThickness = LINE_THICKNESS_THIN
    if(i % 3 == 0):
      lineThickness = LINE_THICKNESS_THICK
    
    # vertical line
    pygame.draw.line(screen, BLACK, (x, grid_y0), (x, grid_y0 + GRID_H), lineThickness)
    # horizontal line
    pygame.draw.line(screen, BLACK, (grid_x0, y), (grid_x0 + GRID_W, y), lineThickness)

def DrawNumbers():
  for j in range(GRID_SIZE):
    for i in range(GRID_SIZE):
      number_surf = font.render(str(theNumbers[j][i]), True, (0, 0, 0))
      number_rect = number_surf.get_rect(center=(grid_x0 + CELL_SIZE//2 + i*CELL_SIZE, grid_y0 + Y_PADDING  + j*CELL_SIZE + number_surf.get_height() // 2))
      screen.blit(number_surf, number_rect)
    
  

running = True
RandomGrid()
RemoveRandomOnes()
PrintGrid()
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

  # Background
  screen.fill(WHITE)

  # Text (centered above grid)
  screen.blit(text_surf, text_rect)

  DrawGrid()
  DrawNumbers()
  
  pygame.display.flip()
  clock.tick(FPS)

pygame.quit()
sys.exit()
