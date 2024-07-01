import pygame
import random
import math

pygame.init()

# defining the constant values for the game
FPS = 100

WIDTH,HEIGHT = 800,800
ROWS = 4
COLS = 4 

RECT_HEIGHT = HEIGHT//ROWS
RECT_WIDTH  = HEIGHT// COLS

OUTLINE_COLOR = (187,174,160) #grey
OUTLINE_THICKNESS = 10
BACKGROUND_COLOR = (205,192,180) #light grey
FONT_COLOR  = (119,110,101) #dark grey

FONT = pygame.font.SysFont('consolas', 60,bold = True)

MOVE_VEL = 20 #speed at which the tiles will move when taken action on (pixels/sec)

WINDOW = pygame.display.set_mode((WIDTH,HEIGHT)) # defining the specified sized window using pygame.dislpay
ICON = pygame.image.load('logo.png') # load the icon image
pygame.display.set_icon(ICON) # set the window icon
pygame.display.set_caption("2048 Game") #title 

#defining the tiles (IMPORTANT)
class Tile:
    COLORS = [
        (237,229,218), 
        (238,225,201), 
        (243,178,122), 
        (246,150,101), 
        (247,124,95), 
        (247,95,59), 
        (237,208,115), 
        (237,204,99), 
        (236,202,80),

    ]

    def __init__(self,value,row,col):
        self.value = value
        self.row = row
        self.col = col
        self.x = col * RECT_WIDTH
        self.y = row * RECT_HEIGHT

    def getColor(self):
        color_index = int(math.log2(self.value)) - 1 #indexing starts from 0 
        color = self.COLORS[color_index]
        return color

    def draw(self,window):
        #drawing the tile
        color = self.getColor()
        pygame.draw.rect(window,color,(self.x,self.y,RECT_WIDTH,RECT_HEIGHT))

        #including the text
        text = FONT.render(str(self.value),1,FONT_COLOR)
        window.blit(
            text,
            (self.x + (RECT_WIDTH / 2 - text.get_width() / 2),
             self.y + (RECT_HEIGHT / 2 -text.get_height() / 2 )
            ),
        )
    
    def setPosition(self,ceil = False):
        if ceil:
            self.row = math.ceil(self.y / RECT_HEIGHT)
            self.col = math.ceil(self.x / RECT_WIDTH)
        else:
            self.row = math.floor(self.y / RECT_HEIGHT)
            self.col = math.floor(self.x / RECT_WIDTH)
        

    def move(self, delta):
        self.x += delta[0]
        self.y += delta[1]






def drawGrid(window): #drawing the horizontal and vertial line in the window
    for row in range (1,ROWS): 
        y = row * RECT_HEIGHT
        pygame.draw.line(window,OUTLINE_COLOR,(0,y),(WIDTH,y),OUTLINE_THICKNESS)
    
    for column in range(1,COLS):    
        x = column * RECT_WIDTH
        pygame.draw.line(window,OUTLINE_COLOR,(x,0),(x,HEIGHT),OUTLINE_THICKNESS)

    pygame.draw.rect(window,OUTLINE_COLOR,(0,0,WIDTH,HEIGHT), OUTLINE_THICKNESS)



def board(window,tiles): #fucntion for board drawing
    window.fill(BACKGROUND_COLOR)

    for tile in tiles.values():
        tile.draw(window)

    drawGrid(window)
    pygame.display.update() #applying changes to screen. it will be updated in order

def getRandomPos(tiles):
    row = None
    col = None
    while True:
        row = random.randrange(0,ROWS)
        col = random.randrange(0,COLS)

        if f"{row}{col}" not in tiles:
            break
    
    return row,col

def moveTiles(window,tiles,clock,direction):
    updated = True
    blocks = set()

    if direction == "left":
        sortFunc = lambda x : x.col
        reverse  = False
        delta = (-MOVE_VEL,0) #specifing velocity (- due to left movement)
        boundaryCheck = lambda tile : tile.col == 0
        getNextTile = lambda tile: tiles.get(f"{tile.row}{tile.col-1}")
        mergeCheck = lambda tile, next_tile : tile.x > next_tile.x + MOVE_VEL # to get to position just berfore merging, when partial merge has taken place
        moveCheck = (
        lambda tile,next_tile : tile.x > next_tile.x + RECT_WIDTH + MOVE_VEL
        )
        ceil = True

    
    elif direction == "right":
        sortFunc = lambda x : x.col
        reverse  = True
        delta = (MOVE_VEL,0) #specifing velocity (- due to left movement)
        boundaryCheck = lambda tile : tile.col == COLS - 1
        getNextTile = lambda tile: tiles.get(f"{tile.row}{tile.col+1}")
        mergeCheck = lambda tile, next_tile : tile.x < next_tile.x - MOVE_VEL # to get to position just berfore merging, when partial merge has taken place
        moveCheck = (
        lambda tile,next_tile : tile.x + RECT_WIDTH + MOVE_VEL < next_tile.x 
        )
        ceil = False

    elif direction == "up":
        sortFunc = lambda x : x.row
        reverse  = False
        delta = (0,-MOVE_VEL) #specifing velocity (- due to left movement)
        boundaryCheck = lambda tile : tile.row == 0
        getNextTile = lambda tile: tiles.get(f"{tile.row-1}{tile.col}")
        mergeCheck = lambda tile, next_tile : tile.y > next_tile.y + MOVE_VEL # to get to position just berfore merging, when partial merge has taken place
        moveCheck = (
        lambda tile,next_tile : tile.y > next_tile.y + RECT_HEIGHT + MOVE_VEL
        )
        ceil = True
    
    elif direction == "down":
        sortFunc = lambda x : x.row
        reverse  = True
        delta = (0,MOVE_VEL) #specifing velocity (- due to left movement)
        boundaryCheck = lambda tile : tile.row == ROWS - 1 
        getNextTile = lambda tile: tiles.get(f"{tile.row+1}{tile.col}")
        mergeCheck = lambda tile, next_tile : tile.y < next_tile.y - MOVE_VEL # to get to position just berfore merging, when partial merge has taken place
        moveCheck = (
        lambda tile,next_tile : tile.y + RECT_HEIGHT + MOVE_VEL < next_tile.y 
        )
        ceil = False

    while updated:
        clock.tick(FPS)
        updated = False
        sortedTiles = sorted(tiles.values(), key = sortFunc, reverse= reverse)

        for i, tile in enumerate(sortedTiles):
            if boundaryCheck(tile):
                continue
            
            next_tile = getNextTile(tile)
            if not next_tile:
                tile.move(delta)
            
            elif (
                tile.value == next_tile.value 
                and tile not in blocks
                and next_tile not in blocks
            ):
                if mergeCheck(tile,next_tile):
                    tile.move(delta)
                else:
                    next_tile.value *=2
                    sortedTiles.pop(i)
                    blocks.add(next_tile)
            
            elif moveCheck(tile,next_tile):
                tile.move(delta)

            else:
                continue

            tile.setPosition(ceil)
            updated = True
        updateTiles(window,tiles,sortedTiles)
    
    endMove(tiles)


def endMove(tiles):
    if len(tiles) == 16:
        return "lost"
    
    row,col  = getRandomPos(tiles)
    tiles[f"{row}{col}"] = Tile(random.choice([2,4]),row,col)


def updateTiles(window,tiles, sortedTiles):
    tiles.clear()
    for tile in sortedTiles:
        tiles[f"{tile.row}{tile.col}"] = tile
    
    board(window,tiles)

def generteTiles():
    tiles = {}
    for _ in range(2):
        row,col = getRandomPos(tiles)
        tiles[f'{row}{col}'] = Tile(2,row,col)
    return tiles

def start_menu(window):
    menu_run = True
    logo = pygame.image.load('logo.png')  # Load the logo image
    logo_rect = logo.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))  # Position the logo above the menu text

    while menu_run:
        window.fill(BACKGROUND_COLOR)  # Use the background color you've defined
        
        window.blit(logo, logo_rect)  # Render the logo

        text_padding = 20
        welcome_text_y_pos = logo_rect.bottom + text_padding

        # Add "Welcome!" text
        welcome_text = FONT.render('Welcome!', True, FONT_COLOR)
        window.blit(welcome_text, (WIDTH // 2 - welcome_text.get_width() // 2, welcome_text_y_pos))

        # Adjust the position of the "Press SPACE to Start" text
        menu_text_y_pos = welcome_text_y_pos + welcome_text.get_height() + text_padding

        menu_text = FONT.render('Press SPACE to Start', True, FONT_COLOR)
        window.blit(menu_text, (WIDTH // 2 - menu_text.get_width() // 2, menu_text_y_pos))
        
        # Small text at the bottom of the screen
        small_font = pygame.font.Font(None, 24)  # Create a smaller font. Adjust size as needed.
        small_text = small_font.render('by- Eshan Dutta', True, FONT_COLOR)
        small_text_x_pos = WIDTH // 2 - small_text.get_width() // 2
        small_text_y_pos = HEIGHT - small_text.get_height() - 10  # Adjust padding at the bottom as needed
        window.blit(small_text, (small_text_x_pos, small_text_y_pos))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_run = False
                pygame.quit()
                exit()  # Make sure to exit the program if the window is closed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    menu_run = False  # Exit the menu loop to start the game
        
        pygame.display.update()

#Main loop
def main(window):
    start_menu(window)
    clock = pygame.time.Clock() #regulate the speed of the loop
    run = True

    tiles = generteTiles()


    while run:
        clock.tick(FPS)

        #looping for each press,action taken on the screen
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT: #to exit the game
                run = False
                break
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a :
                  moveTiles(window,tiles,clock,"left")
                
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d :
                  moveTiles(window,tiles,clock,"right")  
                
                if event.key == pygame.K_UP or event.key == pygame.K_w :
                  moveTiles(window,tiles,clock,"up")  
                
                if event.key == pygame.K_DOWN or event.key == pygame.K_s :
                  moveTiles(window,tiles,clock,"down")  

        board(window,tiles)

    pygame.quit()

if __name__ == "__main__":
    main(WINDOW)