class Pawn:
    white = True
    made_first_move = False
    moves = []
    def __init__(self, white, first_move):
        self.white = white
        self.made_first_move = first_move
    
    def generate_moves(self, x, y, board):
        self.moves = []
        if (self.white == True):
            #generate all moves one space in front of the pawn 
            if (x-1 > -1):
                if (board[x-1][y] == None):
                    self.moves.append([x-1, y])
                #check if there are pieces one diagonal to the current piece
                if (y-1 > -1 and board[x-1][y-1] != None and board[x-1][y-1].white == False):
                    self.moves.append([x-1, y-1])
                if (y+1 < 8 and board[x-1][y+1] != None and board[x-1][y+1].white == False):
                    self.moves.append([x-1, y+1])
            #if the pawn hasnt moved yet, check if the space two in front is avalible
            if (self.made_first_move == False and board[x-2][y] == None and board[x-1][y] == None):
                self.moves.append([x-2, y])

        else:
            #generate all moves one space in front of the pawn 
            if (x+1 < 8):
                if (board[x+1][y] == None):
                    self.moves.append([x+1, y])
                #check if there are pieces one diagonal to the current piece
                if (y-1 > -1 and board[x+1][y-1] != None and board[x+1][y-1].white == True):
                    self.moves.append([x+1, y-1])
                if (y+1 < 8 and board[x+1][y+1] != None and board[x+1][y+1].white == True):
                    self.moves.append([x+1, y+1])
            #if the pawn hasnt moved yet, check if the space two in front is avalible
            if (self.made_first_move == False and board[x+2][y] == None and board[x+1][y] == None):
                self.moves.append([x+2, y])
        return self.moves