from models.Piece import Piece
from models.Color import Color

class Rook(Piece):
    def calcMoves(self, row, col, board):
        legalMoves = []
        oppositeColor = self.color.opposite()

        # Up
        for row_ in range(row - 1, -1, -1):
            piece = board[row_][col]
            if piece is None:
                legalMoves.append(((row_, col), False))
            elif piece.color == oppositeColor:
                legalMoves.append(((row_, col), False))
                break
            else:
                break

        # Down
        for row_ in range(row + 1, 8):  
            piece = board[row_][col]
            if piece is None:
                legalMoves.append(((row_, col), False))
            elif piece.color == oppositeColor:
                legalMoves.append(((row_, col), False))
                break
            else:
                break

        # Left
        for col_ in range(col - 1, -1, -1):
            piece = board[row][col_]
            if piece is None:
                legalMoves.append(((row, col_), False))
            elif piece.color == oppositeColor:
                legalMoves.append(((row, col_), False))
                break
            else:
                break

        # Right
        for col_ in range(col + 1, 8):
            piece = board[row][col_]
            if piece is None:
                legalMoves.append(((row, col_), False))
            elif piece.color == oppositeColor:
                legalMoves.append(((row, col_), False))
                break
            else:
                break

        return legalMoves
