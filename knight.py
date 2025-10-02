class Knight:
    white = True
    made_first_move = False
    moves = []
    def __init__(self, white, first_move):
        self.white = white
        self.made_first_move = first_move
        
        
    def generate_moves(self, x, y, board):
        self.moves = []
        if (x + 2 < 8):
            if (y-1 > -1):
                if(board[x+2][y-1] == None or board[x+2][y-1].white == (not self.white)):
                    self.moves.append([x+2,y-1])
            if (y+1 < 8):
                if(board[x+2][y+1] == None or board[x+2][y+1].white == (not self.white)):
                    self.moves.append([x+2,y+1])
        if (x - 2 > -1):
            if (y-1 > -1):
                if(board[x-2][y-1] == None or board[x-2][y-1].white == (not self.white)):
                    self.moves.append([x-2,y-1])
            if (y+1 < 8):
                if(board[x-2][y+1] == None or board[x-2][y+1].white == (not self.white)):
                    self.moves.append([x-2,y+1])
        if (y + 2 < 8):
            if (x-1 > -1):
                if(board[x-1][y+2] == None or board[x-1][y+2].white == (not self.white)):
                    self.moves.append([x-1,y+2])
            if (x+1 < 8):
                if(board[x+1][y+2] == None or board[x+1][y+2].white == (not self.white)):
                    self.moves.append([x+1,y+2])
        if (y - 2 > -1):
            if (x-1 > -1):
                if(board[x-1][y-2] == None or board[x-1][y-2].white == (not self.white)):
                    self.moves.append([x-1,y-2])
            if (x+1 < 8):
                if(board[x+1][y-2] == None or board[x+1][y-2].white == (not self.white)):
                    self.moves.append([x+1,y-2])
                    
        return self.moves