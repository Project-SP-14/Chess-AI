class Bishop:
    white = True
    made_first_move = False
    moves = []
    def __init__(self, white, first_move):
        self.white = white
        self.made_first_move = first_move
        
    def generate_moves(self, x, y, board):
        self.moves = []
        search_x = x+1
        search_y = y+1
        #check upright diagonal
        while (search_x < 8 and search_y < 8):
            if (board[search_x][search_y] == None):
                self.moves.append([search_x,search_y])
            else:
                if (board[search_x][search_y].white != self.white):
                    self.moves.append([search_x,search_y])
                break
            search_x = search_x + 1
            search_y = search_y + 1
            
            
        search_x = x-1
        search_y = y+1
        #check down right diagonal
        while (search_x > -1 and search_y < 8):
            if (board[search_x][search_y] == None):
                self.moves.append([search_x,search_y])
            else:
                if (board[search_x][search_y].white != self.white):
                    self.moves.append([search_x,search_y])
                break
            search_x = search_x - 1
            search_y = search_y + 1
            
        search_x = x+1
        search_y = y-1  
        #check upleft diagonal
        while (search_x < 8 and search_y > -1):
            if (board[search_x][search_y] == None):
                self.moves.append([search_x,search_y])
            else:
                if (board[search_x][search_y].white != self.white):
                    self.moves.append([search_x,search_y])
                break
            search_x = search_x + 1
            search_y = search_y - 1
            
        search_x = x-1
        search_y = y-1
        #check downleft diagonal
        while (search_x > -1 and search_y > -1):
            if (board[search_x][search_y] == None):
                self.moves.append([search_x,search_y])
            else:
                if (board[search_x][search_y].white != self.white):
                    self.moves.append([search_x,search_y])
                break
            search_x = search_x - 1
            search_y = search_y - 1
            
        return self.moves