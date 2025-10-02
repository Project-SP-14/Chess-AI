class King:
    white = True
    made_first_move = False
    moves = []
    def __init__(self, white, first_move):
        self.white = white
        self.made_first_move = first_move
    
    #TODO: add a check to make sure king cant move to a spot 
    #if that position is in the opposite sides valid move list
    def generate_moves(self, x, y, board):
        self.moves = []
        xplus = x + 1 < 8
        xminus = x - 1 > -1
        yplus = y + 1 < 8
        yminus = y - 1 > -1
        if (xplus):
            if (board[x+1][y] == None or board[x+1][y].white == (not self.white)):
                self.moves.append([x+1,y])
            if (yminus):
                if (board[x+1][y-1] == None or board[x+1][y-1].white == (not self.white)):
                    self.moves.append([x+1,y-1])
            if (yplus):
                if (board[x+1][y+1] == None or board[x+1][y+1].white == (not self.white)):
                    self.moves.append([x+1,y+1])
        if (xminus):
            if (board[x-1][y] == None or board[x-1][y].white == (not self.white)):
                self.moves.append([x-1,y])
            if (yminus):
                if (board[x-1][y-1] == None or board[x-1][y-1].white == (not self.white)):
                    self.moves.append([x-1,y-1])
            if (yplus):
                if (board[x-1][y+1] == None or board[x-1][y+1].white == (not self.white)):
                    self.moves.append([x-1,y+1])
        if (yminus):
            if (board[x][y-1] == None or board[x][y-1].white == (not self.white)):
                self.moves.append([x,y-1])
        if (yplus):
            if (board[x][y+1] == None or board[x][y+1].white == (not self.white)):
                self.moves.append([x,y+1])
        
        #if path is clear and king and rook havent moved yet, allow for castling
        if(self.made_first_move == False):
            if (self.white):
                if (board[7][7].made_first_move == False):
                    valid = True
                    if (board[7][5] != None or board[7][6] != None):
                        valid = False
                    if (valid):
                        self.moves.append([7,6])
                if (board[7][0].made_first_move == False):
                    valid = True
                    if (board[7][3] != None or board[7][2] != None or board[7][1] != None):
                        valid = False
                    if (valid):
                        self.moves.append([7,2])
            else:
                if (board[0][7].made_first_move == False):
                    valid = True
                    if (board[0][5] != None or board[0][6] != None):
                        valid = False
                    if (valid):
                        self.moves.append([0,6])
                if (board[0][0].made_first_move == False):
                    valid = True
                    if (board[0][3] != None or board[0][2] != None or board[0][1] != None):
                        valid = False
                    if (valid):
                        self.moves.append([0,2])
        return self.moves