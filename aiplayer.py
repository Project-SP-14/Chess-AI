import random

class AI:
    def __init__(self,difficulty):
        self.difficulty = difficulty
        
    def decide_move(self, board, color):
        #difficulty of 0 is easy difficulty
        #just picks a random valid move
        valid_pieces = []
        if (self.difficulty == 0):
            for x in range(8):
                for y in range(8):
                    if (board[x][y] != None and board[x][y].white == color):
                        if(len(board[x][y].moves) > 0):
                            valid_pieces.append([x,y])
        
            rand = random.randrange(0,len(valid_pieces))-1
            x = valid_pieces[rand][0]
            y = valid_pieces[rand][1]
            moves = board[x][y].moves
            rand = random.randrange(0,len(moves))-1
            x2 = moves[rand][0]
            y2 = moves[rand][1]
            return [x,y,x2,y2]