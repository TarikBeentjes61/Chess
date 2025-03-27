from models.Color import Color
from models.ChessEvaluator import ChessEvaluator
import math
class Bob:
    def __init__(self):
        self.piece_values = {
            "Pawn": 100,
            "Rook": 500,
            "Knight": 320,
            "Bishop": 330,
            "Queen": 900,
            "King": 2000
        }
        self.color = Color.Black
        self.chessEvaluator = ChessEvaluator()

    def depthDeepening(self, moveCount):
        if moveCount < 10:
            return 3
        elif moveCount < 20:
            return 4
        else:
            return 4
        
    def calcMaterial(self, board):
        material = 0
        piece_values = self.piece_values
        for r, row in enumerate(board.pieces):
            for c, piece in enumerate(row):
                if piece is not None:
                    piece_type = piece.get_type()
                    piece_color = piece.color
                    evaluate_table = self.chessEvaluator.pieceSquareTables[(piece_type, piece_color)]

                    # Material value of the piece
                    piece_value = piece_values[piece_type]
                    positional_eval = evaluate_table[r][c]
                    if piece_color == Color.White:
                        material += piece_value
                        material += positional_eval
                    else:
                        material -= piece_value
                        material -= positional_eval

        return material

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
                                return max_eval
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
                                return min_eval
            return min_eval

    def find_best_move(self, board, depth):
        best_move = None
        alpha = -math.inf
        beta = math.inf

        if self.color == Color.White:
            best_score = -math.inf
            for r, row in enumerate(board.pieces):
                for c, piece in enumerate(row):
                    if piece is not None and piece.color == self.color:
                        for move in piece.legalMoves:
                            move_coords, move_type = move
                            moveRow, moveCol = move_coords
                            board.move_piece(r, c, moveRow, moveCol, move_type)
                            score = self.alpha_beta(board, depth-1, alpha, beta, Color.White)
                            board.undo_move()

                            if score > best_score:
                                best_score = score
                                best_move = (r, c, moveRow, moveCol, move_type)
        else: 
            best_score = math.inf
            for r, row in enumerate(board.pieces):
                for c, piece in enumerate(row):
                    if piece is not None and piece.color == self.color:
                        for move in piece.legalMoves:
                            move_coords, move_type = move
                            moveRow, moveCol = move_coords
                            board.move_piece(r, c, moveRow, moveCol, move_type)
                            score = self.alpha_beta(board, depth-1, alpha, beta, Color.Black)
                            board.undo_move()

                            if score < best_score:
                                best_score = score
                                best_move = (r, c, moveRow, moveCol, move_type)
                                print(best_score)
                                print(best_move)
        print(best_score)
        print(best_move)
        return best_move
    

        

    



