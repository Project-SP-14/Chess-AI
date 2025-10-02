import sys, pygame
import board
import pawn
import rook
import queen
import king
import knight
import bishop

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
b.start_turn()
    
def draw_pieces(screen, board):
    if(isinstance(b.board[x][y], pawn.Pawn)):
        if (b.board[x][y].white == True):
            screen.blit(wpawn,(y*128,x*128))
        if (b.board[x][y].white == False):
            screen.blit(bpawn,(y*128,x*128))
    elif(isinstance(b.board[x][y], rook.Rook)):
        if (b.board[x][y].white == True):
            screen.blit(wrook,(y*128,x*128))
        if (b.board[x][y].white == False):
            screen.blit(brook,(y*128,x*128))
    elif(isinstance(b.board[x][y], bishop.Bishop)):
        if (b.board[x][y].white == True):
            screen.blit(wbishop,(y*128,x*128))
        if (b.board[x][y].white == False):
            screen.blit(bbishop,(y*128,x*128))
    elif(isinstance(b.board[x][y], knight.Knight)):
        if (b.board[x][y].white == True):
            screen.blit(wknight,(y*128,x*128))
        if (b.board[x][y].white == False):
            screen.blit(bknight,(y*128,x*128))
    elif(isinstance(b.board[x][y], queen.Queen)):
        if (b.board[x][y].white == True):
            screen.blit(wqueen,(y*128,x*128))
        if (b.board[x][y].white == False):
            screen.blit(bqueen,(y*128,x*128))
    elif(isinstance(b.board[x][y], king.King)):
        if (b.board[x][y].white == True):
            screen.blit(wking,(y*128,x*128))
        if (b.board[x][y].white == False):
            screen.blit(bking,(y*128,x*128))
            
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()  
        
        elif event.type == pygame.MOUSEBUTTONDOWN and b.players[b.currentp] == 0:
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
                draw_pieces(screen, b.board)
                
            tile = tile + 1
        #subtract one from tile so that the checkboard pattern is made
        tile = tile - 1
    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()