import pawn
import rook
import king
import knight
import bishop
import queen
import aiplayer
import time
import tkinter as tk
from tkinter import filedialog

class Board:
    def __init__(self, player1, player2, arg1, arg2):
        self.players = [player1,player2,arg1,arg2]
        self.currentp = 0
        #first two values are integers that decide player type
        #0 for local, 1 for ai, 2 for online
        #next two values holds difficulty value for ai player and ip for online player 
        self.board = [[None,None,None,None,None,None,None,None],[None,None,None,None,None,None,None,None],[None,None,None,None,None,None,None,None],[None,None,None,None,None,None,None,None],[None,None,None,None,None,None,None,None],[None,None,None,None,None,None,None,None],[None,None,None,None,None,None,None,None],[None,None,None,None,None,None,None,None]]
        self.capture_white = []
        self.capture_black = []
        self.moves = []
        self.currentpiece = [-1,-1]
        self.previouspiece = [-1,-1,-1,-1]
        self.previousmove = [-1,-1,-1,-1]
        self.capturelastfifty = []
        self.capturedpiecetype = None
        self.white = True
        self.aimove = False
        self.game_ended = False
        self.pawn_promotion = False
        self.winner = False
        self.move_list = []
        
        
        #spawn pawns on the second and seventh rows
        for x in range(8):
            self.board[1][x] = pawn.Pawn(False, False)
        for x in range(8):
            self.board[6][x] = pawn.Pawn(True, False)
        self.board[0][0] = rook.Rook(False, False)
        self.board[0][1] = knight.Knight(False, False)
        self.board[0][2] = bishop.Bishop(False, False)
        self.board[0][3] = queen.Queen(False,False)
        self.board[0][4] = king.King(False,False)
        self.board[0][5] = bishop.Bishop(False, False)
        self.board[0][6] = knight.Knight(False, False)
        self.board[0][7] = rook.Rook(False, False)
        
        self.board[7][0] = rook.Rook(True, False)
        self.board[7][1] = knight.Knight(True, False)
        self.board[7][2] = bishop.Bishop(True, False)
        self.board[7][3] = queen.Queen(True, False)
        self.board[7][4] = king.King(True, False)
        self.board[7][5] = bishop.Bishop(True, False)
        self.board[7][6] = knight.Knight(True, False)
        self.board[7][7] = rook.Rook(True, False)
        
    def examine(self, x, y):
        #store the possible moves from the last clicked piece to display on the board
        if (self.board[x][y] == None): 
            print('empty space')
            return
        self.moves = self.board[x][y].moves
        #if the clicked piece is on the same side as the current player, store it for use in play_move
        if (self.white == self.board[x][y].white):
            self.currentpiece = [x,y]
        
    def play_move(self, x, y):
        #check that the selected move is in the list of valid moves and that the piece selected to move
        #is the same piece that was examined earlier
        if (self.currentpiece == [-1,-1]):
            return False
            
        elif (self.currentpiece == [x,y]):
            return False
            
        elif ([x,y] in self.moves and self.board[self.currentpiece[0]][self.currentpiece[1]].white == self.white):
            moving = f"moving {self.currentpiece[0]},{self.currentpiece[1]} to {x},{y}"
            print(moving)
            
            if (self.board[x][y] != None):
                self.capturedpiecetype = self.board[x][y]
                if(isinstance(self.board[x][y], king.King)):
                    self.game_ended = True
                    self.winner = not self.board[x][y].white
                self.capturelastfifty.append(1)
            else:
                self.capturedpiecetype = None
                self.capturelastfifty.append(0)
                
            self.board[x][y] = self.board[self.currentpiece[0]][self.currentpiece[1]]
            self.board[self.currentpiece[0]][self.currentpiece[1]] = None
            self.board[x][y].made_first_move = True
            self.moves = []
            
            if ((x == 0 or x == 7) and isinstance(self.board[x][y], pawn.Pawn)):
                self.pawn_promotion = True
            #store the previous piece locations and previous move so that we can animate the piece movement
            if (isinstance(self.board[x][y], king.King) and (y == 2 or y == 6) and self.currentpiece[1] == 4):
                if (y == 2):
                    self.board[x][3] = self.board[x][0]
                    self.board[x][0] = None
                    self.previouspiece = [self.currentpiece[0],self.currentpiece[1],self.currentpiece[0],0]
                    self.previousmove = [x,y,x,3]
                elif (y == 6):
                    self.board[x][5] = self.board[x][7]
                    self.board[x][7] = None
                    self.previouspiece = [self.currentpiece[0],self.currentpiece[1],self.currentpiece[0],7]
                    self.previousmove = [x,y,x,5]
            else:   
                self.previouspiece = [self.currentpiece[0],self.currentpiece[1],-1,-1]
                self.previousmove = [x,y,-1,-1]
            self.move_list.append([self.currentpiece[0],self.currentpiece[1],x,y])
            self.currentpiece = [-1,-1]
            self.white = not self.white
            self.currentp = (self.currentp + 1)%2 
            if (len(self.capturelastfifty) > 50):
                self.capturelastfifty.pop(0)
                if (1 not in self.capturelastfifty):
                    self.game_ended = True
                    self.winner = 2
            return True
        else:
            self.moves = []
            self.currentpiece = [-1,-1]
            return False
            
    def pawn_promote(self,promotion_value):
        xpos = self.previousmove[0]
        ypos = self.previousmove[1]
        if (promotion_value == 0):
            self.board[xpos][ypos] = queen.Queen(self.board[xpos][ypos].white, True)
        elif (promotion_value == 1):
            self.board[xpos][ypos] = knight.Knight(self.board[xpos][ypos].white, True)
        elif (promotion_value == 2):
            self.board[xpos][ypos] = rook.Rook(self.board[xpos][ypos].white, True)
        elif (promotion_value == 3):
            self.board[xpos][ypos] = bishop.Bishop(self.board[xpos][ypos].white, True)
        self.pawn_promotion = False
            
    
    def start_turn(self):
        #generate all moves at the start of the turn
        #TODO: generate the moves for current players king last so that
        #we can check if the king would be put in danger
        bk = []
        wk = []
        whitemoves = []
        blackmoves = []
        for x in range(8):
            for y in range(8):
                if self.board[x][y] != None:
                    if(not isinstance(self.board[x][y], king.King)):
                        p_moves = self.board[x][y].generate_moves(x,y, self.board)
                        if (self.board[x][y].white):
                            for m in p_moves:
                                if not m in whitemoves:
                                    whitemoves.append(m)
                        else:
                            for m in p_moves:
                                if not m in blackmoves:
                                    blackmoves.append(m)
                    else:
                        if self.board[x][y].white:
                            wk = [self.board[x][y],x,y]
                        else:
                            bk = [self.board[x][y],x,y]
        if (self.white):
            p_moves = bk[0].generate_moves(bk[1],bk[2],self.board,[])
            for m in p_moves:
                if not x in blackmoves:
                    blackmoves.append(x)
            wk[0].generate_moves(wk[1],wk[2],self.board,blackmoves)
        else:
            p_moves = wk[0].generate_moves(wk[1],wk[2],self.board,[]) 
            for m in p_moves:
                if not x in whitemoves:
                    whitemoves.append(x)
            bk[0].generate_moves(bk[1],bk[2],self.board,whitemoves)
        
        #if a player is an AI then generate a move based on the difficulty
        if (self.players[self.currentp] == 1):
            ai = aiplayer.AI(self.players[self.currentp+2])
            move = ai.decide_move(self.board, self.white)
            self.currentpiece = [move[0],move[1]]
            self.moves = self.board[move[0]][move[1]].moves
            if(self.play_move(move[2],move[3])):
                self.aimove = True
                
    def save_state(self):
        saved_state = int(time.mktime(time.localtime()))
        file_name = f'{saved_state}.txt'
        with open(f'{file_name}','w') as f:
            if (self.white):
                f.writelines('True\n')
            else:
                f.writelines('False\n')
            for x in range(8):
                for y in range(8):
                        if(isinstance(self.board[x][y], pawn.Pawn)):
                            if (self.board[x][y].white == True):
                                f.writelines('wpawn\n')
                            if (self.board[x][y].white == False):
                                f.writelines('bpawn\n')
                        elif(isinstance(self.board[x][y], rook.Rook)):
                            if (self.board[x][y].white == True):
                                f.writelines('wrook\n')
                            if (self.board[x][y].white == False):
                                f.writelines('brook\n')
                        elif(isinstance(self.board[x][y], bishop.Bishop)):
                            if (self.board[x][y].white == True):
                                f.writelines('wbishop\n')
                            if (self.board[x][y].white == False):
                                f.writelines('bbishop\n')
                        elif(isinstance(self.board[x][y], knight.Knight)):
                            if (self.board[x][y].white == True):
                                f.writelines('wknight\n')
                            if (self.board[x][y].white == False):
                                f.writelines('bknight\n')
                        elif(isinstance(self.board[x][y], queen.Queen)):
                            if (self.board[x][y].white == True):
                                f.writelines('wqueen\n')
                            if (self.board[x][y].white == False):
                                f.writelines('bqueen\n')
                        elif(isinstance(self.board[x][y], king.King)):
                            if (self.board[x][y].white == True):
                                f.writelines('wking\n')
                            if (self.board[x][y].white == False):
                                f.writelines('bking\n')
                        else:
                            f.writelines('None\n')
                        if (self.board[x][y] != None):
                            if (self.board[x][y].made_first_move):
                                f.writelines('True\n')
                            else:
                                f.writelines('False\n')
            f.close()
            
            
    def load_state(self, fp):
        root = tk.Tk()
        root.withdraw()
        file_path = None
        if fp == None:
            file_path = filedialog.askopenfilename() 
        else:
            file_path = fp
        checking_turn = True
        x = 0
        y = 0
        with open(f'{file_path}', 'r') as f:
            for line in f:
                set_piece = False
                if(checking_turn):
                    if line == 'True\n':
                        self.white = True
                    else:
                        self.white = False
                    checking_turn = False  
                elif line == 'None\n':
                    self.board[x][y] = None
                    set_piece = True
                    
                elif line == 'bpawn\n':
                    self.board[x][y] = pawn.Pawn(False,False)
                elif line == 'wpawn\n':
                    self.board[x][y] = pawn.Pawn(True,False)
                    
                elif line == 'brook\n':
                    self.board[x][y] = rook.Rook(False,False)
                elif line == 'wrook\n':
                    self.board[x][y] = rook.Rook(True,False)
                    
                elif line == 'bknight\n':
                    self.board[x][y] = knight.Knight(False,False)
                elif line == 'wknight\n':
                    self.board[x][y] = knight.Knight(True,False)
                    
                elif line == 'bbishop\n':
                    self.board[x][y] = bishop.Bishop(False,False)
                elif line == 'wbishop\n':
                    self.board[x][y] = bishop.Bishop(True,False)
                    
                elif line == 'bqueen\n':
                    self.board[x][y] = queen.Queen(False,False)
                elif line == 'wqueen\n':
                    self.board[x][y] = queen.Queen(True,False)
                    
                elif line == 'bking\n':
                    self.board[x][y] = king.King(False,False)
                elif line == 'wking\n':
                    self.board[x][y] = king.King(True,False)
                    
                elif line == 'True\n':
                    set_piece = True
                    self.board[x][y].made_first_move = True
                elif line == 'False\n':
                    set_piece = True
                    self.board[x][y].made_first_move = False
                
                if set_piece:
                    y += 1
                    if (y == 8):
                        x += 1
                    y = y%8
        return file_path
        
    def save_match(self, fp):
        saved_state = int(time.mktime(time.localtime()))
        file_name = f'match-{saved_state}.txt'
        print(fp)
        with open(f'{file_name}','w') as f:
            if fp == None:
                f.writelines('Default\n')
            else:
                with open(f'{fp}','r') as initstate:
                    for line in initstate:
                        f.writelines(line)
                    initstate.close()
            for movez in self.move_list:
                f.writelines(f'{movez[0]} {movez[1]} {movez[2]} {movez[3]}\n')