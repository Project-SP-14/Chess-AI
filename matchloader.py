import pawn
import rook
import king
import knight
import bishop
import queen
import board
import copy
import tkinter as tk
from tkinter import filedialog

class MatchLoader:
    def __init__(self):
        self.fp = None
        self.boardlist = []
        self.bpos = 0
        
        
    def load_match(self):
        self.boardlist.append(board.Board(0,0,0,0))
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()
        bpos = 0
        with open(f'{file_path}', 'r') as f:
            x = 0
            y = 0
            checking_turn = True
            for line in f:
                set_piece = False
                if line == 'Default\n':
                    print('default starting state')
                    checking_turn = False
                elif checking_turn:
                    if line == 'True\n':
                        self.boardlist[bpos].white = True
                    else:
                        self.boardlist[bpos].white = False
                    checking_turn = False  
                elif line == 'None\n':
                    self.boardlist[bpos].board[x][y] = None
                    set_piece = True
                    
                elif line == 'bpawn\n':
                    self.boardlist[bpos].board[x][y] = pawn.Pawn(False,False)
                elif line == 'wpawn\n':
                    self.boardlist[bpos].board[x][y] = pawn.Pawn(True,False)
                    
                elif line == 'brook\n':
                    self.boardlist[bpos].board[x][y] = rook.Rook(False,False)
                elif line == 'wrook\n':
                    self.boardlist[bpos].board[x][y] = rook.Rook(True,False)
                    
                elif line == 'bknight\n':
                    self.boardlist[bpos].board[x][y] = knight.Knight(False,False)
                elif line == 'wknight\n':
                    self.boardlist[bpos].board[x][y] = knight.Knight(True,False)
                    
                elif line == 'bbishop\n':
                    self.boardlist[bpos].board[x][y] = bishop.Bishop(False,False)
                elif line == 'wbishop\n':
                    self.boardlist[bpos].board[x][y] = bishop.Bishop(True,False)
                    
                elif line == 'bqueen\n':
                    self.boardlist[bpos].board[x][y] = queen.Queen(False,False)
                elif line == 'wqueen\n':
                    self.boardlist[bpos].board[x][y] = queen.Queen(True,False)
                    
                elif line == 'bking\n':
                    self.boardlist[bpos].board[x][y] = king.King(False,False)
                elif line == 'wking\n':
                    self.boardlist[bpos].board[x][y] = king.King(True,False)
                    
                elif line == 'True\n':
                    set_piece = True
                    self.boardlist[bpos].board[x][y].made_first_move = True
                elif line == 'False\n':
                    set_piece = True
                    self.boardlist[bpos].board[x][y].made_first_move = False
                    
                else:
                    move = line.split()
                    self.boardlist.append(copy.deepcopy(self.boardlist[bpos]))
                    bpos += 1
                    self.boardlist[bpos].start_turn()
                    self.boardlist[bpos].examine(int(move[0]),int(move[1]))
                    self.boardlist[bpos].play_move(int(move[2]),int(move[3]))
                    print(bpos)
                
                if set_piece:
                    y += 1
                    if (y == 8):
                        x += 1
                    y = y%8