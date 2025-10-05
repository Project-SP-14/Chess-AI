import sys, pygame
import board
import pawn
import rook
import queen
import king
import knight
import bishop
import time

pygame.init()

size = width, height = 1024, 1024
black = 0, 0, 0
white = 255, 255, 255
green = 0, 128, 0
bpawn = pygame.image.load('./images/bpawn.png')
wpawn = pygame.image.load('./images/wpawn.png')
brook = pygame.image.load('./images/brook.png')
wrook = pygame.image.load('./images/wrook.png')
bbishop = pygame.image.load('./images/bbishop.png')
wbishop = pygame.image.load('./images/wbishop.png')
bknight = pygame.image.load('./images/bknight.png')
wknight = pygame.image.load('./images/wknight.png')
bking = pygame.image.load('./images/bking.png')
wking = pygame.image.load('./images/wking.png')
bqueen = pygame.image.load('./images/bqueen.png')
wqueen = pygame.image.load('./images/wqueen.png')
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
#testing default is human player 1, ai player 2, player1 needs no arg, ai has difficulty of 0 (easy)
b = board.Board(0,1,0,0)
turn_started = False
move_played = False
title_screen = True
game_started = False
game_ended = False
winner = False
#tracks how the piece should move at each step
moving_steps = [0,0,-1,-1]
#tracks how many frames the piece has moved for
timer = 1
    
#finds the correct sprite for the piece
def draw_pieces(piece):
    if(isinstance(piece, pawn.Pawn)):
        if (piece.white == True):
            return wpawn
        if (piece.white == False):
            return bpawn
    elif(isinstance(piece, rook.Rook)):
        if (piece.white == True):
            return wrook
        if (piece.white == False):
            return brook
    elif(isinstance(piece, bishop.Bishop)):
        if (piece.white == True):
            return wbishop
        if (piece.white == False):
            return bbishop
    elif(isinstance(piece, knight.Knight)):
        if (piece.white == True):
            return wknight
        if (piece.white == False):
            return bknight
    elif(isinstance(piece, queen.Queen)):
        if (piece.white == True):
            return wqueen
        if (piece.white == False):
            return bqueen
    elif(isinstance(piece, king.King)):
        if (piece.white == True):
            return wking
        if (piece.white == False):
            return bking
            
def draw_board(screen,board):
    tile = 0
    color = 0,0,0
    for x in range(8):
        for y in range(8):
            #if the tile is a valid move, make it green
            if ([x,y] in b.moves):
                color = green
            #otherwise make it white or black
            elif (tile%2 == 0):
                color = white
            else:
                color = black
            pygame.draw.rect(screen, color, pygame.Rect(y*128, x*128, 128, 128))
            tile = tile + 1
        #subtract one from tile so that the checkboard pattern is made
        tile = tile - 1
            
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()  
        
        elif event.type == pygame.MOUSEBUTTONDOWN and ((b.players[b.currentp] == 0 and move_played == False) or game_started == False):
            #check if right mouse button has been pressed
            mpress = pygame.mouse.get_pressed()[0]
            mpos = pygame.mouse.get_pos()
            
            if (mpress):
                #only allow interaction with the board if a game has started
                if(game_started):
                    #obtain row and column by dividing the mouse position by 128
                    column = int(mpos[0]/128)
                    row = int(mpos[1]/128)
                    if ([row,column] != b.currentpiece):
                        if (b.currentpiece == [-1,-1]):
                            b.examine(row,column)
                        else:
                            print('attempting to play move')
                            result = b.play_move(row,column)
                            if (result):
                                turn_started = False
                                move_played = True
                                moving_steps = [((b.previousmove[0]-b.previouspiece[0])*128/30),((b.previousmove[1]-b.previouspiece[1])*128/30),((b.previousmove[2]-b.previouspiece[2])*128/30),((b.previousmove[2]-b.previouspiece[2])*128/30)]
                elif(game_ended):
                    print('need to add a button to replay or go to the title screen')
                                
        elif event.type == pygame.MOUSEBUTTONUP and ((b.players[b.currentp] == 0 and move_played == False) or game_started == False):
                mpos = pygame.mouse.get_pos()
                
                #only allow interaction with the chessboard if a game has started
                if(game_started):
                    column = int(mpos[0]/128)
                    row = int(mpos[1]/128)
                    if ([row,column] != b.currentpiece):
                                result = b.play_move(row,column)
                                if (result):
                                    turn_started = False
                                    move_played = True
                                    moving_steps = [((b.previousmove[0]-b.previouspiece[0])*128/30),((b.previousmove[1]-b.previouspiece[1])*128/30),((b.previousmove[2]-b.previouspiece[2])*128/30),((b.previousmove[2]-b.previouspiece[2])*128/30)]

    if(title_screen):
        screen.fill(white)
        timer = timer + 1
        if (timer == 60):
            timer = 1
            title_screen = False
            game_started = True
    
    #only display chessboard and pieces if the game has started    
    elif(game_started):
        if(turn_started == False and move_played == False):
            b.start_turn()
            turn_started == True
        if(b.aimove == True):
            turn_started = False
            move_played = True
            moving_steps = [((b.previousmove[0]-b.previouspiece[0])*128/30),((b.previousmove[1]-b.previouspiece[1])*128/30),((b.previousmove[2]-b.previouspiece[2])*128/30),((b.previousmove[2]-b.previouspiece[2])*128/30)]
            
        #draws the tiles of the chessboard
        draw_board(screen, b)
        if (b.capturedpiecetype != None and move_played == True):
            sprite = draw_pieces(b.capturedpiecetype)
            screen.blit(sprite,(b.previousmove[1]*128,b.previousmove[0]*128))
        for x in range(8):
            for y in range(8):
                if(b.board[x][y] != None):
                    sprite = draw_pieces(b.board[x][y])
                    if (move_played and (b.previousmove[0] == x and b.previousmove[1] == y)):
                        timex = int(timer*moving_steps[0])
                        timey = int(timer*moving_steps[1])
                        screen.blit(sprite,((b.previouspiece[1]*128)+timey,(b.previouspiece[0]*128)+timex))
                        timer = timer + 1
                    elif (move_played and (b.previousmove[2] == x and b.previousmove[3] == y)):
                        timex = int(timer*moving_steps[2])
                        timey = int(timer*moving_steps[3])
                        screen.blit(sprite,((b.previouspiece[3]*128)+timey,(b.previouspiece[2]*128)+timex))
                    else:
                        screen.blit(sprite,(y*128,x*128))
                    
        if (timer == 30):
            print('finished move')
            move_played = False
            if (b.game_ended):
                game_started = False
                game_ended = True
                winner = b.winner
            if (b.aimove):
                b.aimove = False
            timer = 1
            
        
    elif(game_ended):
        draw_board(screen,board)
        for x in range(8):
            for y in range(8):
                if(b.board[x][y] != None):
                    sprite = draw_pieces(b.board[x][y])
                    screen.blit(sprite,(y*128,x*128))
                    
        pygame.draw.rect(screen,(128,0,128),pygame.Rect(256, 256, 512, 512))
        
    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()