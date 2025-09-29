class Pawn:
    white = True
    made_first_move = False
    moves = []
    def __init__(self, white, first_move):
        self.white = white
        self.made_first_move = first_move
    
    def generate_moves(self, x, y, board):
        self.moves = []
        
        
        #if path is clear and king and rook havent moved yet, allow for castling
        if(self.made_first_move):
            if (self.white):
                if (board[7][7].made_first_move == False):
                    print('put something here')
                if (board[7][0].made_first_move == False):
                    print('put something here')
            else:
                if (board[0][7].made_first_move == False):
                    print('put something here')
                if (board[0][0].made_first_move == False):
                    print('put something here') 
        return self.moves