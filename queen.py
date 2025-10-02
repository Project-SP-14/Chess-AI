class Queen:
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
                search_x = 9
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
                search_x = -2
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
                search_x = 9
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
                search_x = -2
                break
            search_x = search_x - 1
            search_y = search_y - 1
            
        search_x = x+1
        while(search_x < 8):
            if (board[search_x][y] == None):
                self.moves.append([search_x,y])
            else:
                #if piece is enemy, add position to list of possible moves
                if (board[search_x][y].white != self.white):
                    self.moves.append([search_x,y])
                search_x = 9
                break
            search_x = search_x + 1

        search_x = x-1    
        #check vertical upward move
        while(search_x > -1):
            if (board[search_x][y] == None):
                self.moves.append([search_x,y])
            else:
                if (board[search_x][y].white != self.white):
                    self.moves.append([search_x,y])
                search_x = -2
                break
            search_x = search_x - 1
            
        search_y = y+1
        #check horizontal move
        while(search_y < 8):
            if (board[x][search_y] == None):
                self.moves.append([x,search_y])
            else:
                #if piece is enemy, add position to list of possible moves
                if (board[x][search_y].white != self.white):
                    self.moves.append([x,search_y])
                search_y = 9
                break
            search_y = search_y + 1
            
        search_y = y-1    
        #check vertical upward move
        while(search_y > -1):
            if (board[x][search_y] == None):
                self.moves.append([x,search_y])
            else:
                if (board[x][search_y].white != self.white):
                    self.moves.append([x,search_y])
                search_y = -2
                break
            search_y = search_y - 1    
        return self.moves