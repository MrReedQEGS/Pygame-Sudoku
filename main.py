import pygame,random
import sys

DEBUG_PRINT = True

# --- Config ---
WINDOW_W, WINDOW_H = 640, 720
FPS = 60

GRID_SIZE = 9                  # 9x9 cells
CELL_SIZE = 40                 # pixels per cell
LINE_THICKNESS_THIN = 2
LINE_THICKNESS_THICK = 4
CELL_HIGHLIGHT_WIDTH = 4
ERROR_CELL = (-1,-1)

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

GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
Y_PADDING = 6

theNumbers = []
highlightedCells = []

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

def WhatCellWasClicked(x,y):
  col = (x-grid_x0)//CELL_SIZE
  row = (y-grid_y0)//CELL_SIZE
  
  #It can't be more than the GRID SIZE - 1
  if(col<0):
    return ERROR_CELL
  if(col>=GRID_SIZE):
    return ERROR_CELL
  if(row<0):
    return ERROR_CELL
  if(row>=GRID_SIZE):
    return ERROR_CELL
    
  return (col,row)

def FindNumberInCell(aCell):
  col = aCell[0]
  row = aCell[1]
  
  return theNumbers[row][col]

def HighlightCell(aCell):
  #Draw a box outline the correct size in a particular cell
  smallOffset = 2
  col = aCell[0]
  row = aCell[1]
  x = grid_x0 + col*CELL_SIZE + smallOffset
  y = grid_y0 + row*CELL_SIZE + smallOffset
  rect = pygame.Rect(x, y, CELL_SIZE-smallOffset, CELL_SIZE-smallOffset)
  pygame.draw.rect(screen, GREEN, rect, CELL_HIGHLIGHT_WIDTH)

def HighlightAllCellsNeeded():
  for cell in highlightedCells:
    HighlightCell(cell)
    
def AddAllNumsToHighlightList(someNum):
  global highlightedCells
  highlightedCells = []
  for j in range(GRID_SIZE):
    for i in range(GRID_SIZE):
      if(theNumbers[j][i] == someNum):
        highlightedCells.append((i,j))

running = True
RandomGrid()
RemoveRandomOnes()
#PrintGrid()
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    if event.type == pygame.MOUSEBUTTONDOWN:
      if event.button == 1:
        click_x, click_y = event.pos
        someCell = WhatCellWasClicked(click_x,click_y)
        if(someCell != ERROR_CELL):
          theNumClicked = FindNumberInCell(someCell)
          if(theNumClicked != ""):
            AddAllNumsToHighlightList(theNumClicked)
          else:
            highlightedCells = []
        else:
          highlightedCells = []
        
  # Background
  screen.fill(WHITE)

  # Text (centered above grid)
  screen.blit(text_surf, text_rect)

  DrawGrid()
  DrawNumbers()
  HighlightAllCellsNeeded()

  pygame.display.flip()
  clock.tick(FPS)

pygame.quit()
sys.exit()
