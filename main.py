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
pygame.freetype.init()
base = 128
fontt = pygame.font.SysFont(None,32)
#TODO?: potentially make piece sizes of 100*100 and 80*80 so that the resolution can be changed to 1000 * 800 and 800 * 640
#would also need to define the size of 
black = 0, 0, 0
white = 255, 255, 255
green = 0, 128, 0
blue = 0,0,128
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
#width is 1.25 times the height since we need space to put a save board state button and information about the game
#default size of screen is 1280 * 1024
screen = pygame.display.set_mode((base*10,base*8))
clock = pygame.time.Clock()
#testing default is human player 1, ai player 2, player1 needs no arg, ai has difficulty of 0 (easy)
b = board.Board(0,1,0,0)
#holds the last used set of board arguments to use when recreating the board on a replay
b_args = [0,1,0,0]
turn_started = False
move_played = False
title_screen = True
game_started = False
game_ended = False
pawn_promotion = False
winner = False
winp1 = 0
winp2 = 0
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
            pygame.draw.rect(screen, color, pygame.Rect(y*base, x*base, base, base))
            tile = tile + 1
        #subtract one from tile so that the checkboard pattern is made
        tile = tile - 1
            
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()  
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            #check if right mouse button has been pressed
            mpress = pygame.mouse.get_pressed()[0]
            mpos = pygame.mouse.get_pos()
            
            if (mpress):
                #only allow interaction with the board if a game has started
                if(game_started and b.players[b.currentp] == 0 and move_played == False):
                    #obtain row and column by dividing the mouse position by the base resolution value
                    column = int(mpos[0]/base)
                    row = int(mpos[1]/base)
                    if ([row,column] != b.currentpiece and column <= 7):
                        if (b.currentpiece == [-1,-1]):
                            b.examine(row,column)
                        else:
                            print('attempting to play move')
                            result = b.play_move(row,column)
                            if (result):
                                turn_started = False
                                move_played = True
                                moving_steps = [((b.previousmove[0]-b.previouspiece[0])*base/30),((b.previousmove[1]-b.previouspiece[1])*base/30),((b.previousmove[2]-b.previouspiece[2])*base/30),((b.previousmove[2]-b.previouspiece[2])*base/30)]
                            else:
                                b.examine(row, column)
                                
                elif(title_screen):
                    print('make buttons for the title screen to set board args')
                
                                    
                elif(game_ended):
                    print(mpos)
                    if(mpos[0] >= 320 and mpos[0] <= 784):
                        #replay game button
                        if (mpos[1] >= 416 and mpos[1] <= 480):
                            turn_started = False
                            move_played = False
                            title_screen = False
                            game_started = True
                            game_ended = False
                            pawn_promotion = False
                            winner = False
                            #if loaded board state != None then load that board state
                            b = board.Board(b_args[0],b_args[1],b_args[2],b_args[3])
                        
                        #return to title screen button
                        elif (mpos[1] >= 512 and mpos[1] <= 576):

                            turn_started = False
                            move_played = False
                            title_screen = True
                            game_started = False
                            game_ended = False
                            pawn_promotion = False
                            winner = False
                            winp1 = 0
                            winp2 = 0
                            b = board.Board(0,1,0,0)
                        
                        
                elif(pawn_promotion):
                    if (mpos[1] >= 448 and mpos[1] <= 576):
                        if (mpos[0] >= 160 and mpos[0] <= 288):   
                            b.pawn_promote(0)
                            pawn_promotion = False
                            game_started = True
                        elif (mpos[0] >= 352 and mpos[0] <= 480):
                            b.pawn_promote(1)
                            pawn_promotion = False
                            game_started = True
                        elif (mpos[0] >= 544 and mpos[0] <= 672):
                            b.pawn_promote(2)
                            pawn_promotion = False
                            game_started = True
                        elif (mpos[0] >= 736 and mpos[0] <= 864):
                            b.pawn_promote(3)
                            pawn_promotion = False
                            game_started = True
                                
        elif event.type == pygame.MOUSEBUTTONUP:
                mpos = pygame.mouse.get_pos()
                
                #only allow interaction with the chessboard if a game has started
                if(game_started and b.players[b.currentp] == 0 and move_played == False):
                    column = int(mpos[0]/base)
                    row = int(mpos[1]/base)
                    if ([row,column] != b.currentpiece and column <= 7):
                                result = b.play_move(row,column)
                                if (result):
                                    turn_started = False
                                    move_played = True
                                    moving_steps = [((b.previousmove[0]-b.previouspiece[0])*base/30),((b.previousmove[1]-b.previouspiece[1])*base/30),((b.previousmove[2]-b.previouspiece[2])*base/30),((b.previousmove[2]-b.previouspiece[2])*base/30)]
                                else:
                                    b.examine(row, column)

    if(title_screen):
        screen.fill(white)
        timer = timer + 1
        if (timer == 60):
            timer = 1
            title_screen = False
            game_started = True
    
    elif (pawn_promotion):
        draw_board(screen, board)
        for x in range(8):
            for y in range(8):
                if(b.board[x][y] != None):
                    sprite = draw_pieces(b.board[x][y])
                    screen.blit(sprite,(y*base,x*base))
                    
        pygame.draw.rect(screen,blue,pygame.Rect(128, 384, 768, 256))
        if(not b.white):
            pygame.draw.rect(screen,black,pygame.Rect(160, 448, 128, 128))
            screen.blit(wqueen,(160,448))
            pygame.draw.rect(screen,black,pygame.Rect(352, 448, 128, 128))
            screen.blit(wknight,(352,448))
            pygame.draw.rect(screen,black,pygame.Rect(544, 448, 128, 128))
            screen.blit(wrook,(544,448))
            pygame.draw.rect(screen,black,pygame.Rect(736, 448, 128, 128))
            screen.blit(wbishop,(736,448))
        else:
            pygame.draw.rect(screen,white,pygame.Rect(160, 448, 128, 128))
            screen.blit(bqueen,(160,448))
            pygame.draw.rect(screen,white,pygame.Rect(352, 448, 128, 128))
            screen.blit(bknight,(352,448))
            pygame.draw.rect(screen,white,pygame.Rect(544, 448, 128, 128))
            screen.blit(brook,(544,448))
            pygame.draw.rect(screen,white,pygame.Rect(736, 448, 128, 128))
            screen.blit(bbishop,(736,448))
            
            
            
    #only display chessboard and pieces if the game has started    
    elif(game_started): 
        if(turn_started == False and move_played == False):
            b.start_turn()
            turn_started == True
        #if ai moved last turn then animate its move
        if(b.aimove == True):
            turn_started = False
            move_played = True
            moving_steps = [((b.previousmove[0]-b.previouspiece[0])*base/30),((b.previousmove[1]-b.previouspiece[1])*base/30),((b.previousmove[2]-b.previouspiece[2])*base/30),((b.previousmove[2]-b.previouspiece[2])*base/30)]
            
        #draws the tiles of the chessboard
        draw_board(screen, b)
        if (b.capturedpiecetype != None and move_played == True):
            sprite = draw_pieces(b.capturedpiecetype)
            screen.blit(sprite,(b.previousmove[1]*base,b.previousmove[0]*base))
        for x in range(8):
            for y in range(8):
                if(b.board[x][y] != None):
                    sprite = draw_pieces(b.board[x][y])
                    if (move_played and (b.previousmove[0] == x and b.previousmove[1] == y)):
                        timex = int(timer*moving_steps[0])
                        timey = int(timer*moving_steps[1])
                        screen.blit(sprite,((b.previouspiece[1]*base)+timey,(b.previouspiece[0]*base)+timex))
                        timer = timer + 1
                    elif (move_played and (b.previousmove[2] == x and b.previousmove[3] == y)):
                        timex = int(timer*moving_steps[2])
                        timey = int(timer*moving_steps[3])
                        screen.blit(sprite,((b.previouspiece[3]*base)+timey,(b.previouspiece[2]*base)+timex))
                    else:
                        screen.blit(sprite,(y*base,x*base))
                    
        if (timer == 30):
            print('finished move')
            move_played = False
            if (b.game_ended):
                game_started = False
                game_ended = True
                winner = b.winner
                if(winner):
                    winp1 += 1
                else:
                    winp2 += 1
            elif (b.aimove):
                b.aimove = False
                if (b.pawn_promotion):
                    b.pawn_promote(0)
                #if pawn_promotion is true then set to queen
            elif (b.pawn_promotion):
                game_started = False
                pawn_promotion = True
            timer = 1
            
        
    elif(game_ended):
        draw_board(screen,board)
        for x in range(8):
            for y in range(8):
                if(b.board[x][y] != None):
                    sprite = draw_pieces(b.board[x][y])
                    screen.blit(sprite,(y*base,x*base))
                    
                    
        #TODO: draw text onto the buttons
        pygame.draw.rect(screen,blue,pygame.Rect(256, 256, 512, 512))
        #replay game
        pygame.draw.rect(screen,white,pygame.Rect(320,416,384,64))
        #to title screen
        pygame.draw.rect(screen,white,pygame.Rect(320,512,384,64))
        score = f'{winp1} - {winp2}'
        scoremsg = fontt.render(score,True, (250, 250, 250))
        if (winner == True):
            victorymsg = fontt.render('Player 1 Wins', True, (250, 250, 250))
        else:
            victorymsg = fontt.render('Player 2 Wins', True, (250, 250, 250))
        screen.blit(victorymsg,(320,320))
        screen.blit(scoremsg,(320,384))
        
    #if we are not on the title screen then we always draw the save state and current board info area
    #only let these areas be interacted when game_started is true and the board is under human control
    if (not title_screen):
        pygame.draw.rect(screen,blue,pygame.Rect(1024, 0, 256, 1024))
        
    
    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()