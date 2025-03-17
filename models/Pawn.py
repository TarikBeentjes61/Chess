from models.Piece import Piece
from models.Color import Color

class Pawn(Piece):
    def calcMoves(self, row,col, board):
        legalMoves = []
        direction = -1 if self.color == Color.White else 1
        start_row = 6 if self.color == Color.White else 1
        maxMove = 2 if row == start_row else 1

        for i in range(1,maxMove+1):
            if board[row+(direction*i)][col] == None:
                legalMoves.append((row+(direction*i), col))

        if board[row+(direction*i)][col-1] != None:
            legalMoves.append((row+(direction*i), col-1))
        if board[row+(direction*i)][col+1] != None:
            legalMoves.append((row+(direction*i), col+1))
        print(legalMoves)
        return legalMoves