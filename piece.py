class Piece:
    def __init__(self, white, first_move):
        self.white = white
        self.made_first_move = first_move
        self.moves = []

    def generate_moves(self, x, y, board):
        return []
