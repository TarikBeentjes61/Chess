from models.Color import Color
from models.ChessEvaluator import ChessEvaluator
import math

class Bob:
    def __init__(self):
        self.piece_values = {
            "Pawn": 10,
            "Rook": 500,
            "Knight": 320,
            "Bishop": 330,
            "Queen": 900,
            "King": 2000
        }
        self.depth = 3
        self.whiteScore = 0
        self.blackScore = 0
        self.color = Color.Black
        self.chessEvaluator = ChessEvaluator()

    def calcMaterial(self, board):
        material = 0
        piece_values = self.piece_values
        for r, row in enumerate(board.pieces):
            for c, piece in enumerate(row):
                if piece is not None:
                    piece_type = piece.get_type()
                    piece_color = piece.color
                    evaluate_table = self.chessEvaluator.pieceSquareTables[(piece_type, piece_color)]

                    #piece value
                    piece_value = piece_values[piece_type]
                    if piece_color == Color.White:
                        material += piece_value
                    else:
                        material -= piece_value

                    #position value
                    positional_eval = evaluate_table[r][c]
                    if piece_color == Color.White:
                        material += positional_eval
                    else:
                        material -= positional_eval

                    #activity value
                    activity_bonus = len(piece.legalMoves)
                    if piece_color == Color.White:
                        material += activity_bonus
                    else:
                        material -= activity_bonus
        return material
    
    def move_score(self, start_row, start_col, end_row, end_col):
        score = 0
        piece = self.pieces[start_row][start_col]
        if piece is None:
            return 0

        captured_piece = self.pieces[end_row][end_col]
        if captured_piece is not None:
            captured_value = self.piece_values.get(captured_piece.get_type(), 0)
            score += captured_value
        evaluate_table = self.chessEvaluator.pieceSquareTables[(piece.getType(), piece.color)]
        positional_eval = evaluate_table[end_row][end_col]
        score+= positional_eval
        return score if piece.color == Color.White else -score

    def alpha_beta(self, board, depth, alpha, beta, color):
        if depth == 0:
            return self.calcMaterial(board)

        if color == Color.White:
            max_eval = -math.inf
            for r, row in enumerate(board.pieces):
                for c, piece in enumerate(row):
                    if piece is not None and piece.color == color:
                        for move in piece.legalMoves:
                            move_coords, move_type = move
                            moveRow, moveCol = move_coords
                            board.move_piece(r, c, moveRow, moveCol, move_type)
                            score = self.alpha_beta(board, depth-1, alpha, beta, Color.Black)
                            board.undo_move()
                            max_eval = max(max_eval, score)
                            alpha = max(alpha, score)

                            if beta <= alpha:
                                break
            return max_eval
        else:
            min_eval = math.inf
            for r, row in enumerate(board.pieces):
                for c, piece in enumerate(row):
                    if piece is not None and piece.color == color:
                        for move in piece.legalMoves:
                            move_coords, move_type = move
                            moveRow, moveCol = move_coords
                            board.move_piece(r, c, moveRow, moveCol, move_type)
                            score = self.alpha_beta(board, depth-1, alpha, beta, Color.White)
                            board.undo_move()
                            min_eval = min(min_eval, score)
                            beta = min(beta, score)

                            if beta <= alpha:
                                break
            return min_eval

    def find_best_move(self, board):
        best_move = None
        alpha = -math.inf
        beta = math.inf
        best_score = math.inf
        for r, row in enumerate(board.pieces):
            for c, piece in enumerate(row):
                if piece is not None and piece.color == self.color:
                    for move in piece.legalMoves:
                        move_coords, move_type = move
                        moveRow, moveCol = move_coords
                        board.move_piece(r, c, moveRow, moveCol, move_type)
                        score = self.alpha_beta(board, self.depth-1, alpha, beta, Color.White)
                        board.undo_move()

                        if score < best_score:
                            best_score = score
                            best_move = (r, c, moveRow, moveCol, move_type)
                        beta = min(beta, best_score)
        return best_move

    def is_square_attacked(self, row, col, attacking_color, board):
        for r, board_row in enumerate(board.pieces):
            for c, piece in enumerate(board_row):
                if piece is not None and piece.color == attacking_color:
                    for move in piece.legalMoves:
                        move_coords, move_type = move
                        moveRow, moveCol = move_coords
                        if moveRow == row and moveCol == col:
                            return True
        return False





