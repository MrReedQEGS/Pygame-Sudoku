#Prototype for a sudoku game
#Here is a new bit...v2
#Mr Reed - Dec 2025
import pygame,random
import sys

DEBUG_PRINT = True

# --- Config ---
WINDOW_W, WINDOW_H = 640, 720
FPS = 60
WINDOW_TEXT = "My suduko game"

# create the display surface object
# of specific dimension.
surface = pygame.display.set_mode((WINDOW_W,WINDOW_H))
pygame.display.set_caption(WINDOW_TEXT)

GRID_SIZE = 9                  # 9x9 cells
CELL_SIZE = 40                 # pixels per cell
LINE_THICKNESS_THIN = 2
LINE_THICKNESS_THICK = 4
CELL_HIGHLIGHT_WIDTH = 4
ERROR_CELL = (-1,-1)
BUTTON_PANEL_GAP_Y = 10
NUM_BUTTON_X_GAP = 2

TEXT = "Sudoku"
FONT_SIZE = 48
NOTE_FONT_SIZE = 19

COLORS = [
    (0, 60, 120),     # Deep Navy Blue
    (0, 120, 215),    # Bright Blue
    (0, 160, 90),     # Green
    (100, 60, 160),   # Purple
    (255, 165, 0),    # Orange
    (0, 180, 180),    # Teal
    (160, 160, 160),  # Gray
    (120, 80, 40),    # Brown
    (240, 220, 70),   # Yellow / Gold
]

# Layout: grid centered; text centered above it
GRID_W = GRID_SIZE * CELL_SIZE
GRID_H = GRID_SIZE * CELL_SIZE
TOP_MARGIN = 80
GAP_TEXT_TO_GRID = 20

EMPTY_NOTES = ["0","0","0","0","0","0","0","0","0"]

editMode = False
numGoingIntoGrid = "0"
highlightNum = "0"

#images
infoImage = pygame.image.load("./Info.jpg").convert()
infoGreyImage = pygame.image.load("./InfoGrey.jpg").convert()

#Load button images into lists
numberButtons = []
numberGreyButtons = []
for i in range(GRID_SIZE):
  fileName = "./"+str(i+1)+".jpg"
  someButton = pygame.image.load(fileName).convert()
  numberButtons.append(someButton)
  greyFileName = "./"+str(i+1)+"Grey.jpg"
  someButton = pygame.image.load(greyFileName).convert()
  numberGreyButtons.append(someButton)

pygame.init()
screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
pygame.display.set_caption("Simple sudoku game")
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, FONT_SIZE)
text_surf = font.render(TEXT, True, (0, 0, 0))
text_rect = text_surf.get_rect(center=(WINDOW_W // 2, TOP_MARGIN + text_surf.get_height() // 2))

noteFont = pygame.font.SysFont(None, NOTE_FONT_SIZE)

grid_x0 = (WINDOW_W - GRID_W) // 2
grid_y0 = text_rect.bottom + GAP_TEXT_TO_GRID

GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
Y_PADDING = 6

theNumbers = []
theNotes = []
highlightedCells = []

#Button class from the othello game that I made
class MyClickableImageButton:
  def __init__(self, x, y, newImage,newGreyImg,newParentSurface,theNewCallback):
    self.img=newImage
    self.greyImg = newGreyImg
    self.rect=self.img.get_rect()
    self.rect.topleft=(x,y)
    self.clicked=False
    self.parentSurfce=newParentSurface
    self.theCallback = theNewCallback

  def DrawSelf(self):
    #The button will be grey until the mouse hovers over it!
    self.parentSurfce.blit(self.greyImg, (self.rect.x, self.rect.y))
    pos=pygame.mouse.get_pos()
    if self.rect.collidepoint(pos):
      if pygame.mouse.get_pressed()[0] and not self.clicked:
        self.clicked=True
        self.theCallback()
      if not pygame.mouse.get_pressed()[0]:
        self.clicked=False
        self.parentSurfce.blit(self.img, (self.rect.x, self.rect.y))
        
class MyToggleImageButton:
  def __init__(self, x, y, newImage,newGreyImg,newParentSurface,theNewCallback):
    self.img=newImage
    self.greyImg = newGreyImg
    self.rect=self.img.get_rect()
    self.rect.topleft=(x,y)
    self.grey=True
    self.parentSurfce=newParentSurface
    self.theCallback = theNewCallback
    self.currentImg = self.greyImg
    self.was_down = False
    self.is_pressed = False

  def DrawSelf(self):
    #The button toggle between the grey and black versions!
    
    pos = pygame.mouse.get_pos()
    mouse_down = pygame.mouse.get_pressed()[0]
    hover = self.rect.collidepoint(pos)

    if mouse_down and hover and not self.was_down:
      self.is_pressed = True

    if (not mouse_down) and self.was_down:
      if self.is_pressed and hover:
        
        if(self.grey == True):
          self.grey = False
          self.currentImg = self.img
        else:
          self.grey = True
          self.currentImg = self.greyImg
          
        self.theCallback(self.grey)
        
      self.is_pressed = False

    self.was_down = mouse_down
    self.parentSurfce.blit(self.currentImg, (self.rect.x, self.rect.y))


#Make some notes in each grid cell
#This is for testing
def MakeEmptyNotes():
  for i in range(GRID_SIZE):
    newRow = []
    for j in range(GRID_SIZE):
      newRow.append(EMPTY_NOTES)
    theNotes.append(newRow)

#This is for testing
def RemoveRandomNumbersFromGrid():
  for i in range(30):
    j = random.randint(0,8)
    i = random.randint(0,8)
    theNumbers[j][i] = "0"
    randomNotes = [1,2,3,4,5,6,7,8,9]
    
    #Remove some random notes to make it look more realistic
    for x in range(10):
      someNum = random.randint(0,8)
      randomNotes[someNum]="0"
    theNotes[i][j] = randomNotes
    
def MakeRandomNotes():
  for i in range(30):
    j = random.randint(0,8)
    i = random.randint(0,8)
    randomNotes = [1,2,3,4,5,6,7,8,9]
    
    #Remove some random notes to make it look more realistic
    for x in range(10):
      someNum = random.randint(0,8)
      randomNotes[someNum]="0"
    theNotes[i][j] = randomNotes
    
#It is not a valid grid in terms of game play.  This is just a test function to allow me to 
#make sure the numbers line up when it is all printed out.
#This is for testing
def RandomGrid():
  for i in range(GRID_SIZE):
    newRow = []
    for j in range(GRID_SIZE):
      newRow.append(str(random.randint(1,9)))
    theNumbers.append(newRow)
  RemoveRandomNumbersFromGrid()
  
def EmptyGrid():
  for i in range(GRID_SIZE):
    emptyRow = ["0","0","0","0","0","0","0","0","0"]
    theNumbers.append(emptyRow)

def LoadAPuzzleFromCSV():
    global theNumbers
    file = open("EasyProbSet.csv", "r")
    data = file.read().split("\n")
    random.shuffle(data)
    x = data.index("")
    del data[x]
    # print(data)
    s = random.choice(data)
    prob = []
    row = []
    i = 0
    while (True):
        count = 0
        for j in s:
            if (count < 9):
                if (j != "["):
                    if (j != "]"):
                        if (j != "," and j != " "):
                            row.append(str(j))
                            count += 1
            else:
                prob.append(row)
                row = []
                i += 1
                count = 0
        if (i == 9):
            break
    theNumbers = prob
    file.close()
    
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
      colour = (0,0,0)
      if(theNumbers[j][i] != "0"):
          currentNum = theNumbers[j][i]
          x = int(currentNum)-1
          colour = COLORS[x]
          number_surf = font.render(str(theNumbers[j][i]), True, colour)
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

def PrintNotesInCell(aCell):
  #Draw a box outline the correct size in a particular cell
  noteOffsetX = 8
  noteOffsetY = 9
  noteRowGap = 12
  noteGap = 12
  col = aCell[0]
  row = aCell[1]
  notesForThisCell = theNotes[col][row]
  
  for j in range(3):
    for i in range(3):
      if(notesForThisCell[i+(j*3)] != "0"):
        note_surf = noteFont.render(str(notesForThisCell[i+(j*3)]), True, (255, 0, 0))
        note_rect = note_surf.get_rect(center=(noteOffsetX + grid_x0 + col*CELL_SIZE + noteGap*i, noteOffsetY + grid_y0 + row*CELL_SIZE + noteRowGap*j))
        screen.blit(note_surf, note_rect)
 
def PrintAllNotes():
  for j in range(0,GRID_SIZE):
    for i in range(0,GRID_SIZE):
      PrintNotesInCell((j,i))

def RemoveNotesFromACell(theCell):
  col = theCell[0]
  row = theCell[1]
  theNotes[col][row] = EMPTY_NOTES
  

def AddNumberToACell(theCell):
  col = theCell[0]
  row = theCell[1]
  theNumbers[row][col] = numGoingIntoGrid
  
  #Notes must be removed from a cell when a number goes in!
  RemoveNotesFromACell(theCell)
  
  
#Make some buttons

def InfoButtonCallback():
  #Testing button callback
  print("Info button stuff will print out!!!")

def OneButtonCallback(isItGrey):
  global editMode,numGoingIntoGrid
  
  if(isItGrey == False):
    #We are enabling edit mode to allow this number to go into the grid
    editMode = True
    numGoingIntoGrid = "1"
  else:
    editMode = False
    numGoingIntoGrid = "0"
    
  #Reset the other buttons - only one can be on
  theTwoButton.grey=True
  theTwoButton.currentImg = theTwoButton.greyImg
  theThreeButton.grey=True
  theThreeButton.currentImg = theThreeButton.greyImg
  theFourButton.grey=True
  theFourButton.currentImg = theFourButton.greyImg
  theFiveButton.grey=True
  theFiveButton.currentImg = theFiveButton.greyImg
  theSixButton.grey=True
  theSixButton.currentImg = theSixButton.greyImg
  theSevenButton.grey=True
  theSevenButton.currentImg = theSevenButton.greyImg
  theEightButton.grey=True
  theEightButton.currentImg = theEightButton.greyImg
  theNineButton.grey=True
  theNineButton.currentImg = theNineButton.greyImg
  
  if(numGoingIntoGrid != "0"):
     AddAllNumsToHighlightList(numGoingIntoGrid)

def TwoButtonCallback(isItGrey):
  global editMode,numGoingIntoGrid
  
  if(isItGrey == False):
    #We are enabling edit mode to allow this number to go into the grid
    editMode = True
    numGoingIntoGrid = "2"
  else:
    editMode = False
    numGoingIntoGrid = "0"
  
  #Reset the other buttons - only one can be on
  theOneButton.grey=True
  theOneButton.currentImg = theOneButton.greyImg
  theThreeButton.grey=True
  theThreeButton.currentImg = theThreeButton.greyImg
  theFourButton.grey=True
  theFourButton.currentImg = theFourButton.greyImg
  theFiveButton.grey=True
  theFiveButton.currentImg = theFiveButton.greyImg
  theSixButton.grey=True
  theSixButton.currentImg = theSixButton.greyImg
  theSevenButton.grey=True
  theSevenButton.currentImg = theSevenButton.greyImg
  theEightButton.grey=True
  theEightButton.currentImg = theEightButton.greyImg
  theNineButton.grey=True
  theNineButton.currentImg = theNineButton.greyImg
  
  if(numGoingIntoGrid != "0"):
     AddAllNumsToHighlightList(numGoingIntoGrid)
  

def ThreeButtonCallback(isItGrey):
  global editMode,numGoingIntoGrid
  
  if(isItGrey == False):
    #We are enabling edit mode to allow this number to go into the grid
    editMode = True
    numGoingIntoGrid = "3"
  else:
    editMode = False
    numGoingIntoGrid = "0"
  
  #Reset the other buttons - only one can be on
  theOneButton.grey=True
  theOneButton.currentImg = theOneButton.greyImg
  theTwoButton.grey=True
  theTwoButton.currentImg = theTwoButton.greyImg
  theFourButton.grey=True
  theFourButton.currentImg = theFourButton.greyImg
  theFiveButton.grey=True
  theFiveButton.currentImg = theFiveButton.greyImg
  theSixButton.grey=True
  theSixButton.currentImg = theSixButton.greyImg
  theSevenButton.grey=True
  theSevenButton.currentImg = theSevenButton.greyImg
  theEightButton.grey=True
  theEightButton.currentImg = theEightButton.greyImg
  theNineButton.grey=True
  theNineButton.currentImg = theNineButton.greyImg
  
  if(numGoingIntoGrid != "0"):
     AddAllNumsToHighlightList(numGoingIntoGrid)
  
def FourButtonCallback(isItGrey):
  global editMode,numGoingIntoGrid
  
  if(isItGrey == False):
    #We are enabling edit mode to allow this number to go into the grid
    editMode = True
    numGoingIntoGrid = "4"
  else:
    editMode = False
    numGoingIntoGrid = "0"
  
  #Reset the other buttons - only one can be on
  theOneButton.grey=True
  theOneButton.currentImg = theOneButton.greyImg
  theTwoButton.grey=True
  theTwoButton.currentImg = theTwoButton.greyImg
  theThreeButton.grey=True
  theThreeButton.currentImg = theThreeButton.greyImg
  theFiveButton.grey=True
  theFiveButton.currentImg = theFiveButton.greyImg
  theSixButton.grey=True
  theSixButton.currentImg = theSixButton.greyImg
  theSevenButton.grey=True
  theSevenButton.currentImg = theSevenButton.greyImg
  theEightButton.grey=True
  theEightButton.currentImg = theEightButton.greyImg
  theNineButton.grey=True
  theNineButton.currentImg = theNineButton.greyImg
  
  if(numGoingIntoGrid != "0"):
     AddAllNumsToHighlightList(numGoingIntoGrid)

def FiveButtonCallback(isItGrey):
  global editMode,numGoingIntoGrid
  
  if(isItGrey == False):
    #We are enabling edit mode to allow this number to go into the grid
    editMode = True
    numGoingIntoGrid = "5"
  else:
    editMode = False
    numGoingIntoGrid = "0"
  
  #Reset the other buttons - only one can be on
  theOneButton.grey=True
  theOneButton.currentImg = theOneButton.greyImg
  theTwoButton.grey=True
  theTwoButton.currentImg = theTwoButton.greyImg
  theThreeButton.grey=True
  theThreeButton.currentImg = theThreeButton.greyImg
  theFourButton.grey=True
  theFourButton.currentImg = theFourButton.greyImg
  theSixButton.grey=True
  theSixButton.currentImg = theSixButton.greyImg
  theSevenButton.grey=True
  theSevenButton.currentImg = theSevenButton.greyImg
  theEightButton.grey=True
  theEightButton.currentImg = theEightButton.greyImg
  theNineButton.grey=True
  theNineButton.currentImg = theNineButton.greyImg
  
  if(numGoingIntoGrid != "0"):
     AddAllNumsToHighlightList(numGoingIntoGrid)

def SixButtonCallback(isItGrey):
  global editMode,numGoingIntoGrid
  
  if(isItGrey == False):
    #We are enabling edit mode to allow this number to go into the grid
    editMode = True
    numGoingIntoGrid = "6"
  else:
    editMode = False
    numGoingIntoGrid = "0"
  
  #Reset the other buttons - only one can be on
  theOneButton.grey=True
  theOneButton.currentImg = theOneButton.greyImg
  theTwoButton.grey=True
  theTwoButton.currentImg = theTwoButton.greyImg
  theThreeButton.grey=True
  theThreeButton.currentImg = theThreeButton.greyImg
  theFourButton.grey=True
  theFourButton.currentImg = theFourButton.greyImg
  theFiveButton.grey=True
  theFiveButton.currentImg = theFiveButton.greyImg
  theSevenButton.grey=True
  theSevenButton.currentImg = theSevenButton.greyImg
  theEightButton.grey=True
  theEightButton.currentImg = theEightButton.greyImg
  theNineButton.grey=True
  theNineButton.currentImg = theNineButton.greyImg
  
  if(numGoingIntoGrid != "0"):
     AddAllNumsToHighlightList(numGoingIntoGrid)

def SevenButtonCallback(isItGrey):
  global editMode,numGoingIntoGrid
  
  if(isItGrey == False):
    #We are enabling edit mode to allow this number to go into the grid
    editMode = True
    numGoingIntoGrid = "7"
  else:
    editMode = False
    numGoingIntoGrid = "0"
  
  #Reset the other buttons - only one can be on
  theOneButton.grey=True
  theOneButton.currentImg = theOneButton.greyImg
  theTwoButton.grey=True
  theTwoButton.currentImg = theTwoButton.greyImg
  theThreeButton.grey=True
  theThreeButton.currentImg = theThreeButton.greyImg
  theFourButton.grey=True
  theFourButton.currentImg = theFourButton.greyImg
  theFiveButton.grey=True
  theFiveButton.currentImg = theFiveButton.greyImg
  theSixButton.grey=True
  theSixButton.currentImg = theSixButton.greyImg
  theEightButton.grey=True
  theEightButton.currentImg = theEightButton.greyImg
  theNineButton.grey=True
  theNineButton.currentImg = theNineButton.greyImg
  
  if(numGoingIntoGrid != "0"):
     AddAllNumsToHighlightList(numGoingIntoGrid)

def EightButtonCallback(isItGrey):
  global editMode,numGoingIntoGrid
  
  if(isItGrey == False):
    #We are enabling edit mode to allow this number to go into the grid
    editMode = True
    numGoingIntoGrid = "8"
  else:
    editMode = False
    numGoingIntoGrid = "0"
  
  #Reset the other buttons - only one can be on
  theOneButton.grey=True
  theOneButton.currentImg = theOneButton.greyImg
  theTwoButton.grey=True
  theTwoButton.currentImg = theTwoButton.greyImg
  theThreeButton.grey=True
  theThreeButton.currentImg = theThreeButton.greyImg
  theFourButton.grey=True
  theFourButton.currentImg = theFourButton.greyImg
  theFiveButton.grey=True
  theFiveButton.currentImg = theFiveButton.greyImg
  theSixButton.grey=True
  theSixButton.currentImg = theSixButton.greyImg
  theSevenButton.grey=True
  theSevenButton.currentImg = theSevenButton.greyImg
  theNineButton.grey=True
  theNineButton.currentImg = theNineButton.greyImg
  
  if(numGoingIntoGrid != "0"):
     AddAllNumsToHighlightList(numGoingIntoGrid)


def NineButtonCallback(isItGrey):
  global editMode,numGoingIntoGrid
  
  if(isItGrey == False):
    #We are enabling edit mode to allow this number to go into the grid
    editMode = True
    numGoingIntoGrid = "9"
  else:
    editMode = False
    numGoingIntoGrid = "0"
  
  #Reset the other buttons - only one can be on
  theOneButton.grey=True
  theOneButton.currentImg = theOneButton.greyImg
  theTwoButton.grey=True
  theTwoButton.currentImg = theTwoButton.greyImg
  theThreeButton.grey=True
  theThreeButton.currentImg = theThreeButton.greyImg
  theFourButton.grey=True
  theFourButton.currentImg = theFourButton.greyImg
  theFiveButton.grey=True
  theFiveButton.currentImg = theFiveButton.greyImg
  theSixButton.grey=True
  theSixButton.currentImg = theSixButton.greyImg
  theSevenButton.grey=True
  theSevenButton.currentImg = theSevenButton.greyImg
  theEightButton.grey=True
  theEightButton.currentImg = theEightButton.greyImg
  
  if(numGoingIntoGrid != "0"):
     AddAllNumsToHighlightList(numGoingIntoGrid)

buttonPanelOffset = -45 
theInfoButton = MyClickableImageButton(buttonPanelOffset+grid_x0,grid_y0+CELL_SIZE*GRID_SIZE+BUTTON_PANEL_GAP_Y,infoImage,infoGreyImage,surface,InfoButtonCallback)
theOneButton = MyToggleImageButton(buttonPanelOffset+grid_x0+1*+(CELL_SIZE+NUM_BUTTON_X_GAP),grid_y0+CELL_SIZE*GRID_SIZE+BUTTON_PANEL_GAP_Y,numberButtons[0],numberGreyButtons[0],surface,OneButtonCallback)
theTwoButton = MyToggleImageButton(buttonPanelOffset+grid_x0+2*+(CELL_SIZE+NUM_BUTTON_X_GAP),grid_y0+CELL_SIZE*GRID_SIZE+BUTTON_PANEL_GAP_Y,numberButtons[1],numberGreyButtons[1],surface,TwoButtonCallback)
theThreeButton = MyToggleImageButton(buttonPanelOffset+grid_x0+3*+(CELL_SIZE+NUM_BUTTON_X_GAP),grid_y0+CELL_SIZE*GRID_SIZE+BUTTON_PANEL_GAP_Y,numberButtons[2],numberGreyButtons[2],surface,ThreeButtonCallback)
theFourButton = MyToggleImageButton(buttonPanelOffset+grid_x0+4*+(CELL_SIZE+NUM_BUTTON_X_GAP),grid_y0+CELL_SIZE*GRID_SIZE+BUTTON_PANEL_GAP_Y,numberButtons[3],numberGreyButtons[3],surface,FourButtonCallback)
theFiveButton = MyToggleImageButton(buttonPanelOffset+grid_x0+5*+(CELL_SIZE+NUM_BUTTON_X_GAP),grid_y0+CELL_SIZE*GRID_SIZE+BUTTON_PANEL_GAP_Y,numberButtons[4],numberGreyButtons[4],surface,FiveButtonCallback)
theSixButton = MyToggleImageButton(buttonPanelOffset+grid_x0+6*+(CELL_SIZE+NUM_BUTTON_X_GAP),grid_y0+CELL_SIZE*GRID_SIZE+BUTTON_PANEL_GAP_Y,numberButtons[5],numberGreyButtons[5],surface,SixButtonCallback)
theSevenButton = MyToggleImageButton(buttonPanelOffset+grid_x0+7*+(CELL_SIZE+NUM_BUTTON_X_GAP),grid_y0+CELL_SIZE*GRID_SIZE+BUTTON_PANEL_GAP_Y,numberButtons[6],numberGreyButtons[6],surface,SevenButtonCallback)
theEightButton = MyToggleImageButton(buttonPanelOffset+grid_x0+8*+(CELL_SIZE+NUM_BUTTON_X_GAP),grid_y0+CELL_SIZE*GRID_SIZE+BUTTON_PANEL_GAP_Y,numberButtons[7],numberGreyButtons[7],surface,EightButtonCallback)
theNineButton = MyToggleImageButton(buttonPanelOffset+grid_x0+9*+(CELL_SIZE+NUM_BUTTON_X_GAP),grid_y0+CELL_SIZE*GRID_SIZE+BUTTON_PANEL_GAP_Y,numberButtons[8],numberGreyButtons[8],surface,NineButtonCallback)

running = True
MakeEmptyNotes()
EmptyGrid()
#MakeRandomNotes()
#RandomGrid()
LoadAPuzzleFromCSV()
#print(theNumbers)

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
          if(theNumClicked != "0"):
            
            #Make highlights toggle on and off for repeated press in same cell
            if(highlightNum != theNumClicked):
              highlightNum = theNumClicked
              AddAllNumsToHighlightList(theNumClicked)
            else:
              highlightNum = "0"
              highlightedCells = []
              
          else:
            #We might be in edit mode - so put a number into this cell??
            if(editMode == True):
              AddNumberToACell(someCell)
              AddAllNumsToHighlightList(numGoingIntoGrid)
              highlightNum = numGoingIntoGrid
        else:
          highlightedCells = []
  
  # Background
  screen.fill(WHITE)

  # Text (centered above grid)
  screen.blit(text_surf, text_rect)

  DrawGrid()
  DrawNumbers()
  HighlightAllCellsNeeded()
  PrintAllNotes()
  
  theInfoButton.DrawSelf()
  theOneButton.DrawSelf()
  theTwoButton.DrawSelf()
  theThreeButton.DrawSelf()
  theFourButton.DrawSelf()
  theFiveButton.DrawSelf()
  theSixButton.DrawSelf()
  theSevenButton.DrawSelf()
  theEightButton.DrawSelf()
  theNineButton.DrawSelf()

  if(editMode == True):
    mouse_pos = pygame.mouse.get_pos()

    # draw a number that follows the mouse
    #posIWant = (mouse_pos[0]-10,mouse_pos[1]+10)
          
    x = int(numGoingIntoGrid)-1
    colour = COLORS[x]
    number_surf = font.render(str(numGoingIntoGrid), True, colour)
    number_rect = number_surf.get_rect(center=mouse_pos)
    screen.blit(number_surf, number_rect)

  pygame.display.flip()
  clock.tick(FPS)

pygame.quit()
sys.exit()
