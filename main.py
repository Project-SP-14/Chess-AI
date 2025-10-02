import sys, pygame
import board

pygame.init()

size = width, height = 1024, 1024
black = 0, 0, 0
white = 255, 255, 255
green = 0, 128, 0
purple = 128,0,128
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
b = board.Board()
b.start_turn()
    
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()  
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            #check if right mouse button has been pressed
            mpress = pygame.mouse.get_pressed()[0]
            mpos = pygame.mouse.get_pos()
            
            #obtain row and column by dividing the mouse position by 128
            column = int(mpos[0]/128)
            row = int(mpos[1]/128)
            if (mpress):
                print(row)
                print(column)
                if ([row,column] != b.currentpiece):
                    if (b.currentpiece == [-1,-1]):
                        b.examine(row,column)
                        print(b.currentpiece)
                    else:
                        print('attempting to play move')
                        result = b.play_move(row,column)
                        if (result):
                            b.start_turn()
                        #if result is true play an animation to move the piece
        elif event.type == pygame.MOUSEBUTTONUP:
            mpos = pygame.mouse.get_pos()
            column = int(mpos[0]/128)
            row = int(mpos[1]/128)
            if ([row,column] != b.currentpiece):
                        result = b.play_move(row,column)
                        if (result):
                            b.start_turn()
                        #if result is true play an animation to move the piece
    tile = 0
    color = 0,0,0
    #draws the tiles of the chessboard
    #TODO: draw an image wherever the chess pieces are
    for x in range(8):
        for y in range(8):
            #if the tile is a vllid move, make it green
            if ([x,y] in b.moves):
                color = green
            #otherwise make it white or black
            elif (tile%2 == 0):
                color = white
            else:
                color = black
            pygame.draw.rect(screen, color, pygame.Rect(y*128, x*128, 128, 128))
            if(b.board[x][y] != None):
                pygame.draw.rect(screen, purple, pygame.Rect((y*128)+1, (x*128)+1, 126, 126))
            tile = tile + 1
        #subtract one from tile so that the checkboard pattern is made
        tile = tile - 1
    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()