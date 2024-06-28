import pygame
import random
import math

pygame.init()

# defining the constant values for the game
FPS = 60

WIDTH,HEIGHT = 800,800
ROWS = 4
COLS = 4 

RECT_HEIGHT = HEIGHT//ROWS
RECT_WIDTH  = HEIGHT// COLS

OOUTLINE_COLOR = (187,174,160) #grey
OUTLINE_THICKNESS = 10
BACKGROUND_COLOR = (205,192,180) #light grey
FONT_COLOR  = (119,110,101) #dark grey

FONT = pygame.font.SysFont('Fira Code', 60,bold = True)

MOVE_VEL = 20 #speed at which the tiles will move when taken action on (pixels/sec)

WINDOW = pygame.display.set_mode((WIDTH,HEIGHT)) # defining the specified sized window using pygame.dislpay
ICON = pygame.image.load('logo.png') # load the icon image
pygame.display.set_icon(ICON) # set the window icon
pygame.display.set_caption("2048 Game") #title 

#Main loop
def main(window):
    clock = pygame.time.Clock() #regulate the speed of the loop
    run = True

    while run:
        clock.tick(FPS)

        #looping for each press,action taken on the screen
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT: #to exit the game
                run = False
                break
            
    pygame.quit()

if __name__ == "__main__":
    main(WINDOW)