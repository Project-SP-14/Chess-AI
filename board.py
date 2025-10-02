import pawn
import rook
import king
import knight
import bishop
import queen
import aiplayer

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
        self.white = True
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
            self.board[x][y] = self.board[self.currentpiece[0]][self.currentpiece[1]]
            self.board[self.currentpiece[0]][self.currentpiece[1]] = None
            self.board[x][y].made_first_move = True
            self.moves = []
            self.currentpiece = [-1,-1]
            self.white = not self.white
            self.currentp = (self.currentp + 1)%2
            return True
        else:
            print('invalid move')
            self.moves = []
            self.currentpiece = [-1,-1]
            return False
    def start_turn(self):
        #generate all moves at the start of the turn
        #TODO: generate the moves for current players king last so that
        #we can check if the king would be put in danger
        for x in range(8):
            for y in range(8):
                if self.board[x][y] != None:
                    self.board[x][y].generate_moves(x,y, self.board)
        #if a player is an AI then generate a move based on the difficulty
        if (self.players[self.currentp] == 1):
            ai = aiplayer.AI(self.players[self.currentp+2])
            move = ai.decide_move(self.board, self.white)
            self.currentpiece = [move[0],move[1]]
            self.moves = self.board[move[0]][move[1]].moves
            if(self.play_move(move[2],move[3])):
                self.start_turn()