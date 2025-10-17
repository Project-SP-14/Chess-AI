import random
import pawn, rook, knight, bishop, queen, king

class AI:
    def __init__(self, difficulty):
        self.difficulty = difficulty

    def piece_value(self, piece):  # piece scores
        if isinstance(piece, pawn.Pawn): return 1
        if isinstance(piece, (knight.Knight, bishop.Bishop)): return 3
        if isinstance(piece, rook.Rook): return 5
        if isinstance(piece, queen.Queen): return 9
        if isinstance(piece, king.King): return 100
        return 0

    def is_square_attacked(self, board, color, x, y):  # check if square attacked
        for i in range(8):
            for j in range(8):
                piece = board[i][j]
                if piece != None and piece.white != color:
                    for m in piece.moves:
                        if m[0] == x and m[1] == y:
                            return True
        return False

    def decide_move(self, board, color):
        all_moves = []
        capture_moves = []
        center = [(3,3),(3,4),(4,3),(4,4)]

        for x in range(8):
            for y in range(8):
                piece = board[x][y]
                if piece != None and piece.white == color:
                    for move in piece.moves:
                        new_x = move[0]
                        new_y = move[1]
                        target = board[new_x][new_y]
                        # check captures
                        if target != None and target.white != color:
                            val = self.piece_value(target)
                            if isinstance(target, king.King):  # checkmate move
                                return [x,y,new_x,new_y]
                            # avoid bad trade
                            if self.piece_value(piece) > val + 1:
                                continue
                            # center bonus
                            bonus = 0.5 if (new_x,new_y) in center else 0
                            capture_moves.append([x,y,new_x,new_y,val+bonus])
                        else:
                            bonus = 0.5 if (new_x,new_y) in center else 0
                            all_moves.append([x,y,new_x,new_y,bonus])

        if len(all_moves) == 0 and len(capture_moves) == 0:
            return None

        if self.difficulty == 0:
            if len(all_moves) > 0: return [*random.choice(all_moves)[:4]]
            else: return [*random.choice(capture_moves)[:4]]

        if self.difficulty == 1:
            if len(capture_moves) > 0: return [*random.choice(capture_moves)[:4]]
            else: return [*random.choice(all_moves)[:4]]

        safe_moves = []  # ai logic gets smarter in higher difficulty
        for move in capture_moves + all_moves:
            x2,y2 = move[2],move[3]
            if not self.is_square_attacked(board,color,x2,y2):
                safe_moves.append(move)

        moveset = safe_moves if len(safe_moves)>0 else (capture_moves if len(capture_moves)>0 else all_moves)

        # pick best move by score
        best = moveset[0]
        for mv in moveset:
            if len(mv) == 5 and mv[4] > best[4]: best = mv
        return [best[0],best[1],best[2],best[3]]
