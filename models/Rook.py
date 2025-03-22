from models.Piece import Piece
from models.Color import Color

class Rook(Piece):
    def calcMoves(self, row,col, board):
        legalMoves = []

        for y in range(col, 7):
            square = board[y][col]
            if square is not None or square.color != self.color:
                legalMoves.append(square)
        


        return legalMoves
