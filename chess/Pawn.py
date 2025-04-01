from chess.Piece import Piece
from chess.Color import Color

class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.passant = False

    def calcMoves(self, row, col, board):
        pieces = board.pieces
        legalMoves = []
        direction = -1 if self.color == Color.White else 1
        start_row = 6 if self.color == Color.White else 1
        maxMove = 2 if row == start_row else 1

        #check foward
        for i in range(1, maxMove + 1):
            newRow = row + (direction * i)

            if 0 <= newRow < len(pieces):
                if pieces[newRow][col] is None:
                    flag = False if i == 1 else "setPassant"
                    if newRow == 0 or newRow == 7:
                        flag = "promotion"
                    legalMoves.append(((newRow, col), flag))
                else:
                    break
            else:
                break

        #check taking
        for z in [-1, 1]:
            newCol = col + z
            newRow = row + direction

            if 0 <= newCol < len(pieces[0]) and 0 <= newRow < len(pieces):
                if pieces[newRow][newCol] is not None:
                    if self.color != pieces[newRow][newCol].color:
                        legalMoves.append(((newRow, newCol), "attack"))

        #check en passant
        for z in [-1, 1]:
            newCol = col + z
            if 0 <= newCol < len(pieces[0]):
                if isinstance(pieces[row][newCol], Pawn) and pieces[row][newCol].passant:
                    if pieces[row + direction][newCol] is None:
                        legalMoves.append(((row + direction, newCol), "passant"))

        return legalMoves