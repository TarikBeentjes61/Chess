from chess.Piece import Piece
from chess.Color import Color

class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.hasMoved = False  
    def calcMoves(self, row, col, board):
        pieces = board.pieces
        legalMoves = []
        oppositeColor = self.color.opposite()

        #Up
        for row_ in range(row - 1, -1, -1):
            piece = pieces[row_][col]
            if piece is None:
                legalMoves.append(((row_, col), "attack"))
            elif piece.color == oppositeColor:
                legalMoves.append(((row_, col), "attack"))
                break
            else:
                break

        #Down
        for row_ in range(row + 1, 8):  
            piece = pieces[row_][col]
            if piece is None:
                legalMoves.append(((row_, col), "attack"))
            elif piece.color == oppositeColor:
                legalMoves.append(((row_, col), "attack"))
                break
            else:
                break

        #Left
        for col_ in range(col - 1, -1, -1):
            piece = pieces[row][col_]
            if piece is None:
                legalMoves.append(((row, col_), "attack"))
            elif piece.color == oppositeColor:
                legalMoves.append(((row, col_), "attack"))
                break
            else:
                break

        #Right
        for col_ in range(col + 1, 8):
            piece = pieces[row][col_]
            if piece is None:
                legalMoves.append(((row, col_), "attack"))
            elif piece.color == oppositeColor:
                legalMoves.append(((row, col_), "attack"))
                break
            else:
                break

        return legalMoves
