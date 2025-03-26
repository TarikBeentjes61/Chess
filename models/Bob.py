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
            "King": 0
        }
        self.color = Color.Black
        self.depth = 3
        self.chessEvaluator = ChessEvaluator()

    def calcMaterial(self, board):
        material = 0
        for r, row in enumerate(board.pieces):
            for c, piece in enumerate(row):
                if piece is not None:
                    evaluateTable = self.chessEvaluator.pieceSquareTables[(piece.get_type(), piece.color)]
                    material += evaluateTable[r][c]
                    if piece.color == Color.White:
                        material += self.piece_values[piece.get_type()]
                    else:
                        material -= self.piece_values[piece.get_type()]
        return material
    
    def alpha_beta(self, board, depth, alpha, beta, color):
        if depth == 0:
            return self.calcMaterial(board)  # Use evaluation function

        if color == Color.White:
            max_eval = -math.inf
            for r, row in enumerate(board.pieces):
                for c, piece in enumerate(row):
                    if piece is not None and piece.color == color:
                        for move in piece.legalMoves:
                            moveRow, moveCol = move[0]
                            board.move_piece(r, c, moveRow, moveCol, move[1])
                            score = self.alpha_beta(board, depth-1, alpha, beta, Color.Black)
                            board.undo_move()
                            max_eval = max(max_eval, score)
                            alpha = max(alpha, score)

                            if beta <= alpha:  # Stop searching immediately
                                return max_eval
            return max_eval
        else:
            min_eval = math.inf
            for r, row in enumerate(board.pieces):
                for c, piece in enumerate(row):
                    if piece is not None and piece.color == color:
                        for move in piece.legalMoves:
                            moveRow, moveCol = move[0]
                            board.move_piece(r, c, moveRow, moveCol, move[1])
                            score = self.alpha_beta(board, depth-1, alpha, beta, Color.White)
                            board.undo_move()
                            min_eval = min(min_eval, score)
                            beta = min(beta, score)

                            if beta <= alpha:  # Stop searching immediately
                                return min_eval
            return min_eval

    def find_best_move(self, board, depth):
        best_move = None
        best_score = -math.inf
        alpha = -math.inf
        beta = math.inf

        for r, row in enumerate(board.pieces):
            for c, piece in enumerate(row):
                if piece is not None and piece.color == self.color:
                    for move in piece.legalMoves:
                        moveRow, moveCol = move[0]
                        board.move_piece(r, c, moveRow, moveCol, move[1])
                        score = self.alpha_beta(board, depth-1, alpha, beta, self.color.opposite())
                        board.undo_move()
                    
                        if score > best_score:
                            best_score = score
                            best_move = (r, c, moveRow, moveCol, move[1])
                        alpha = max(alpha, best_score)
        return best_move

        

    



