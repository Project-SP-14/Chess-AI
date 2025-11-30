import sys, pygame
import board
import pawn
import rook
import queen
import king
import knight
import bishop
import time
import matchloader

pygame.init()
pygame.freetype.init()
base = 128
fontt = pygame.font.SysFont(None,32)
#colors
black = 0, 0, 0
white = 255, 255, 255
green = 0, 128, 0
blue = 0,0,128
gray = 100,100,100
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
matchl = matchloader.MatchLoader()
matchlstate = 0

#game states
turn_started = False
move_played = False
title_screen = True
game_started = False
game_ended = False
pawn_promotion = False
match_state_selector = False
rules_state = False

#win/lose information
winner = False
winp1 = 0
winp2 = 0
#tracks how the piece should move at each step
moving_steps = [0,0,-1,-1]
#tracks how many frames the piece has moved for
timer = 1
b_loaded_player = 0
b_loaded_file = None
pvsaidiff = 0
aivaidiff1 = 0
aivaidiff2 = 0

#buttons for title screen
localpvp = pygame.Rect(192, 320, 416, 64)
localpvpmsg = fontt.render('Local Player versus Player', True, black)
onlinepvp = pygame.Rect(672,320, 416, 64)
onlinepvpmsg = fontt.render('Online Player versus Player', True, black)
localpvai = pygame.Rect(192, 416, 416, 64)
localpvaimsg = fontt.render('Player versus AI', True, black)
pvaieasydiff = pygame.Rect(640,416,128,64)
easydiffmsg = fontt.render('Easy', True, black)
pvaimeddiff = pygame.Rect(800,416,128,64)
meddiffmsg = fontt.render('Medium', True, black)
pvaiharddiff = pygame.Rect(960,416,128,64)
harddiffmsg = fontt.render('Hard', True, black)
loadstate = pygame.Rect(512, 800, 256,64)
loadstatemsg = fontt.render('Load State', True, black)
loadmatch = pygame.Rect(512, 704, 256,64)
loadmatchmsg = fontt.render('Load match', True, black)
showrules = pygame.Rect(192, 704, 256,64)
showrulesmsg = fontt.render('Show Rules', True, black)
aivsai = pygame.Rect(192, 512, 896, 64)
aivaimsg = fontt.render('AI versus AI', True, black)
aivsaie1 = pygame.Rect(192, 608, 128, 64)
aivsaim1 = pygame.Rect(352, 608, 128, 64)
aivsaih1 = pygame.Rect(512, 608, 128, 64)
aivsaie2 = pygame.Rect(672, 608, 128, 64)
aivsaim2 = pygame.Rect(832, 608, 128, 64)
aivsaih2 = pygame.Rect(992, 608, 128, 64)

#pawn promotion buttons
queenback = pygame.Rect(160, 448, 128, 128)
knightback = pygame.Rect(352, 448, 128, 128)
rookback  = pygame.Rect(544, 448, 128, 128)
bishopback = pygame.Rect(736, 448, 128, 128)

#victory screen buttons
replaybutton = pygame.Rect(320,416,384,64)
replaymsg = fontt.render('Replay Game', True, black)
totitle = pygame.Rect(320,512,384,64)
titlemsg = fontt.render('Return to Title Screen', True, black)
savematch = pygame.Rect(320,608,384,64)
savematchmsg = fontt.render('Save Match to File', True, black)

#sidebar buttons
savestate = pygame.Rect(1056,32,192,32)
savestatemsg = fontt.render('Save State', True, black)

#match_state_selector sidebar
backstate = pygame.Rect(1056,960,64,32)
backstatemsg = fontt.render('<', True, black)
forwardstate = pygame.Rect(1152,960,64,32)
forwardstatemsg = fontt.render('>', True, black)
exitbutton = pygame.Rect(1056,896,192,32)
exitmsg = fontt.render('Exit', True, black)

#rules_state close button
close_button = pygame.Rect(512,896,256,64)
closemsg = fontt.render('Close Rules', True, black)

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
                            result = b.play_move(row,column)
                            if (result):
                                turn_started = False
                                move_played = True
                                moving_steps = [((b.previousmove[0]-b.previouspiece[0])*base/30),((b.previousmove[1]-b.previouspiece[1])*base/30),((b.previousmove[2]-b.previouspiece[2])*base/30),((b.previousmove[3]-b.previouspiece[3])*base/30)]
                            else:
                                b.examine(row, column)
                    elif(savestate.collidepoint(mpos)):
                        b.save_state()

                                
                elif(title_screen):
                        if(loadstate.collidepoint(mpos)):
                                b_loaded_file = b.load_state(b_loaded_file)
                                if(b.white):
                                    b_loaded_player = 0
                                else:
                                    b_loaded_player = 1
                        elif(loadmatch.collidepoint(mpos)):
                            matchl.load_match()
                            match_state_selector = True
                            title_screen = False
                            
                        #starts local player versus player game
                        elif (localpvp.collidepoint(mpos)):
                            title_screen = False
                            game_started = True
                            b_args = [0,0,0,0]
                            b = board.Board(0,0,0,0)
                            #if there is a loaded board state then put it into the board object
                            if (b_loaded_file != None):
                                b.load_state(b_loaded_file)
                                b.currentp = b_loaded_player
                                
                        elif (onlinepvp.collidepoint(mpos)):
                            print('online is not implemented')
                            
                        #starts player versus ai game
                        elif (localpvai.collidepoint(mpos)):
                            title_screen = False
                            game_started = True
                            b_args = [0,1,0,pvsaidiff]
                            b = board.Board(0,1,0,pvsaidiff)
                            if (b_loaded_file != None):
                                b.load_state(b_loaded_file)
                                b.currentp = b_loaded_player
                        #selects ai difficulty for player versus ai
                        elif(pvaieasydiff.collidepoint(mpos)):
                            pvsaidiff = 0
                        elif(pvaimeddiff.collidepoint(mpos)):
                            pvsaidiff = 1
                        elif(pvaiharddiff.collidepoint(mpos)):
                            pvsaidiff = 2      
                            
                        #starts ai versus ai game
                        elif(aivsai.collidepoint(mpos)):
                            title_screen = False
                            game_started = True
                            b_args = [1,1,aivaidiff1,aivaidiff2]
                            b = board.Board(1,1,aivaidiff1,aivaidiff2)
                            if (b_loaded_file != None):
                                b.load_state(b_loaded_file)
                                b.currentp = b_loaded_player
                                
                        #select ai player 1 difficulty
                        elif(aivsaie1.collidepoint(mpos)):
                            aivaidiff1 = 0
                        elif(aivsaim1.collidepoint(mpos)):
                            aivaidiff1 = 1
                        elif(aivsaih1.collidepoint(mpos)):
                            aivaidiff1 = 2
                        #select ai player 2 difficulty
                        elif(aivsaie2.collidepoint(mpos)):
                            aivaidiff2 = 0
                        elif(aivsaim2.collidepoint(mpos)):
                            aivaidiff2 = 1
                        elif(aivsaih2.collidepoint(mpos)):
                            aivaidiff2 = 2
                            
                        elif(showrules.collidepoint(mpos)):
                            title_screen = False
                            rules_state = True
                            
                elif(rules_state):
                    if(close_button.collidepoint(mpos)):
                        title_screen = True
                        rules_state = False                     
                
                         
                elif(match_state_selector):
                    if (backstate.collidepoint(mpos)):
                        if matchlstate > 0:
                            matchlstate -= 1
                    elif (forwardstate.collidepoint(mpos)):
                        if matchlstate < (len(matchl.boardlist)-1):
                            print(matchlstate)
                            matchlstate += 1
                    elif (savestate.collidepoint(mpos)):
                        matchl.boardlist[matchlstate].save_state()
                    elif(exitbutton.collidepoint(mpos)):
                        title_screen = True
                        match_state_selector = False
                            
                elif(game_ended):
                    #replay game button
                    if (replaybutton.collidepoint(mpos)):
                        turn_started = False
                        move_played = False
                        title_screen = False
                        game_started = True
                        game_ended = False
                        pawn_promotion = False
                        winner = False
                        #if loaded board state != None then load that board state
                        b = board.Board(b_args[0],b_args[1],b_args[2],b_args[3])
                        if (b_loaded_file != None):
                            b.load_state(b_loaded_file)
                            if(b.white):
                                b_loaded_player = 0
                            else:
                                b_loaded_player = 1
                        
                    #return to title screen button
                    elif (totitle.collidepoint(mpos)):
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
                            b_loaded_file = None
                            b_loaded_player = 0
                    elif(savematch.collidepoint(mpos)):
                        b.save_match(b_loaded_file)
                        
                        
                elif(pawn_promotion):
                    if (queenback.collidepoint(mpos)):   
                            b.pawn_promote(0)
                            pawn_promotion = False
                            game_started = True
                    elif (knightback.collidepoint(mpos)):
                        b.pawn_promote(1)
                        pawn_promotion = False
                        game_started = True
                    elif (rookback.collidepoint(mpos)):
                        b.pawn_promote(2)
                        pawn_promotion = False
                        game_started = True
                    elif (bishopback.collidepoint(mpos)):
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
                                    moving_steps = [((b.previousmove[0]-b.previouspiece[0])*base/30),((b.previousmove[1]-b.previouspiece[1])*base/30),((b.previousmove[2]-b.previouspiece[2])*base/30),((b.previousmove[3]-b.previouspiece[3])*base/30)]
                                else:
                                    b.examine(row, column)

    if(title_screen):
        screen.fill(blue)
        pygame.draw.rect(screen,gray,pygame.Rect(128, 128, 1024, 768))
        pygame.draw.rect(screen,white,localpvp)
        screen.blit(localpvpmsg,(192, 320))
        pygame.draw.rect(screen,white,onlinepvp)
        screen.blit(onlinepvpmsg,(672,320))
        pygame.draw.rect(screen,white,pvaieasydiff)
        screen.blit(easydiffmsg,(640,416))
        pygame.draw.rect(screen,white,pvaimeddiff)
        screen.blit(meddiffmsg,(800,416))
        pygame.draw.rect(screen,white,pvaiharddiff)
        screen.blit(harddiffmsg,(960,416))
        pygame.draw.rect(screen,white,localpvai)
        screen.blit(localpvaimsg,(192, 416))
        pygame.draw.rect(screen,white,loadstate)
        screen.blit(loadstatemsg,(512, 800))
        pygame.draw.rect(screen,white,aivsai)
        screen.blit(aivaimsg,(192, 512))
        pygame.draw.rect(screen,white,aivsaie1)
        screen.blit(easydiffmsg,(192, 608))
        pygame.draw.rect(screen,white,aivsaim1)
        screen.blit(meddiffmsg,(352, 608))
        pygame.draw.rect(screen,white,aivsaih1)
        screen.blit(harddiffmsg,(512, 608))
        pygame.draw.rect(screen,white,aivsaie2)
        screen.blit(easydiffmsg,(672, 608))
        pygame.draw.rect(screen,white,aivsaim2)
        screen.blit(meddiffmsg,(832, 608))
        pygame.draw.rect(screen,white,aivsaih2)
        screen.blit(harddiffmsg,(992, 608))
        pygame.draw.rect(screen,white,loadmatch)
        screen.blit(loadmatchmsg,(512, 704))
        pygame.draw.rect(screen,white,showrules)
        screen.blit(showrulesmsg,(192, 704))

    
    elif (match_state_selector):
        draw_board(screen, b)
        for x in range(8):
            for y in range(8):
                if(matchl.boardlist[matchlstate].board[x][y] != None):
                    sprite = draw_pieces(matchl.boardlist[matchlstate].board[x][y])
                    screen.blit(sprite,(y*base,x*base))
       
       
    elif (pawn_promotion):
        draw_board(screen, board)
        for x in range(8):
            for y in range(8):
                if(b.board[x][y] != None):
                    sprite = draw_pieces(b.board[x][y])
                    screen.blit(sprite,(y*base,x*base))
                    
        pygame.draw.rect(screen,blue,pygame.Rect(128, 384, 768, 256))
        if(not b.white):
            pygame.draw.rect(screen,black,queenback)
            screen.blit(wqueen,(160,448))
            pygame.draw.rect(screen,black,knightback)
            screen.blit(wknight,(352,448))
            pygame.draw.rect(screen,black,rookback)
            screen.blit(wrook,(544,448))
            pygame.draw.rect(screen,black,bishopback)
            screen.blit(wbishop,(736,448))
        else:
            pygame.draw.rect(screen,white,queenback)
            screen.blit(bqueen,(160,448))
            pygame.draw.rect(screen,white,knightback)
            screen.blit(bknight,(352,448))
            pygame.draw.rect(screen,white,rookback)
            screen.blit(brook,(544,448))
            pygame.draw.rect(screen,white,bishopback)
            screen.blit(bbishop,(736,448))
            
            
            
    #only display chessboard and pieces if the game has started    
    elif(game_started): 
        if(turn_started == False and move_played == False):
            b.start_turn()
            turn_started = True
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
            move_played = False
            if (b.game_ended):
                game_started = False
                game_ended = True
                winner = b.winner
                if(winner == 1):
                    winp1 += 1
                elif(winner == 0):
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
                                  
        pygame.draw.rect(screen,blue,pygame.Rect(256, 256, 512, 512))
        #replay game
        pygame.draw.rect(screen,white,replaybutton)
        screen.blit(replaymsg,(320,416))
        #to title screen
        pygame.draw.rect(screen,white,totitle)
        screen.blit(titlemsg,(320,512))
        pygame.draw.rect(screen,white,savematch)
        screen.blit(savematchmsg,(320,608))
        score = f'{winp1} - {winp2}'
        scoremsg = fontt.render(score,True, (250, 250, 250))
        if (winner == 1):
            victorymsg = fontt.render('Player 1 Wins', True, white)
        elif (winner == 0):
            victorymsg = fontt.render('Player 2 Wins', True, white)
        else:
            victorymsg = fontt.render('Stalemate', True, white)
        screen.blit(victorymsg,(320,320))
        screen.blit(scoremsg,(320,384))
        
    elif(rules_state):
        rules = pygame.image.load('./images/rules.png')
        screen.blit(rules,(0,0))
        pygame.draw.rect(screen,white,close_button)
        screen.blit(closemsg,(512,896))
        
    #if we are not on the title screen then we always draw the save state and current board info area
    #only let these areas be interacted when game_started is true and the board is under human control
    if (not title_screen and not rules_state):
        pygame.draw.rect(screen,blue,pygame.Rect(1024, 0, 256, 1024))
        pygame.draw.rect(screen, white,savestate)
        screen.blit(savestatemsg,(1056,32))
        if (match_state_selector):
            pygame.draw.rect(screen,white,backstate)
            screen.blit(backstatemsg,(1056,960))
            pygame.draw.rect(screen,white,forwardstate)
            screen.blit(forwardstatemsg,(1152,960))
            pygame.draw.rect(screen,white,exitbutton)
            screen.blit(exitmsg,(1056,896))
    
    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()