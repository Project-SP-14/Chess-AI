import copy
import random

import pawn, rook, knight, bishop, queen, king

class AI:

    def __init__(self, difficulty):
        self.difficulty = difficulty

    # piece scores
    def piece_value(self, piece):
        if isinstance(piece, pawn.Pawn): return 1
        if isinstance(piece, (knight.Knight, bishop.Bishop)): return 3
        if isinstance(piece, rook.Rook): return 5
        if isinstance(piece, queen.Queen): return 9
        if isinstance(piece, king.King): return 100
        return 0

    # simulate a move on a copied board
    def simulate_move(self, board, x1, y1, x2, y2):
        new_board = copy.deepcopy(board)

        piece = new_board[x1][y1]
        new_board[x1][y1] = None
        new_board[x2][y2] = piece

        # regenerate moves for all pieces
        for i in range(8):
            for j in range(8):
                if new_board[i][j] != None:
                    if not isinstance(new_board[i][j], king.King):
                        new_board[i][j].generate_moves(i, j, new_board)
                    else:
                        new_board[i][j].generate_moves(i, j, new_board, [])

        return new_board

    # evaluate board for the chosen color
    def evaluate_board(self, board, color):
        score = 0
        center = [(3,3),(3,4),(4,3),(4,4)]

        for x in range(8):
            for y in range(8):
                piece = board[x][y]
                if piece != None:
                    v = self.piece_value(piece)
                    if piece.white:
                        score += v
                    else:
                        score -= v
                    if (x,y) in center:
                        if piece.white:
                            score += 0.3
                        else:
                            score -= 0.3
        return score

    # get all moves for a color
    def get_all_moves(self, board, color):
        moves = []
        for x in range(8):
            for y in range(8):
                piece = board[x][y]
                if piece != None and piece.white == color:
                    for m in piece.moves:
                        moves.append([x, y, m[0], m[1]])
        return moves

    # minimax
    def minimax(self, board, depth, maximizing, color):
        if depth == 0:
            return self.evaluate_board(board, color)

        moves = self.get_all_moves(board, maximizing)
        if len(moves) == 0:
            return self.evaluate_board(board, color)

        if maximizing:
            best = -9999
            for m in moves:
                new_b = self.simulate_move(board, m[0],m[1],m[2],m[3])
                val = self.minimax(new_b, depth-1, False, color)
                if val > best:
                    best = val
            return best
        else:
            best = 9999
            for m in moves:
                new_b = self.simulate_move(board, m[0],m[1],m[2],m[3])
                val = self.minimax(new_b, depth-1, True, color)
                if val < best:
                    best = val
            return best

    # alphabeta pruning
    def alphabeta(self, board, depth, alpha, beta, maximizing, color):
        if depth == 0:
            return self.evaluate_board(board, color)

        moves = self.get_all_moves(board, maximizing)
        if len(moves) == 0:
            return self.evaluate_board(board, color)

        if maximizing:
            best = -9999
            for m in moves:
                new_b = self.simulate_move(board, m[0],m[1],m[2],m[3])
                val = self.alphabeta(new_b, depth-1, alpha, beta, False, color)
                if val > best:
                    best = val
                if best >= beta:
                    break
                alpha = max(alpha, best)
            return best
        else:
            best = 9999
            for m in moves:
                new_b = self.simulate_move(board, m[0],m[1],m[2],m[3])
                val = self.alphabeta(new_b, depth-1, alpha, beta, True, color)
                if val < best:
                    best = val
                if alpha >= best:
                    break
                beta = min(beta, best)
            return best

    # main function called by board
    def decide_move(self, board, color):
        # difficulty 0 -> random
        if self.difficulty == 0:
            mv = self.get_all_moves(board, color)
            return random.choice(mv) if mv else None

        moves = self.get_all_moves(board, color)
        if len(moves) == 0:
            return None

        best_move = [0,0,0,0]  
        best_score = 0
        if color:
            best_score = -9999
        else:
            best_score = 9999

        # difficulty 1 - minimax depth 2
        if self.difficulty == 1:
            depth = 2
            for m in moves:
                new_b = self.simulate_move(board, m[0],m[1],m[2],m[3])
                val = self.minimax(new_b, depth-1, False, color)
                if val > best_score:
                    best_score = val
                    best_move = m

        # difficulty 2 - alphabeta depth 4
        elif self.difficulty == 2:
            depth = 4
            alpha = -9999
            beta = 9999
            for m in moves:
                new_b = self.simulate_move(board, m[0],m[1],m[2],m[3])
                val = self.alphabeta(new_b, depth, alpha, beta, not color, color)
                if color:
                    if val > best_score:
                        best_score = val
                        best_move = m
                        alpha = val
                else:
                    if val < best_score:
                        best_score = val
                        best_move = m
                        beta = val

        return best_move
