from models.Piece import Piece
from models.Color import Color

class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.passant = False
    def calcMoves(self, row,col, board):
        legalMoves = []
        direction = -1 if self.color == Color.White else 1
        start_row = 6 if self.color == Color.White else 1
        maxMove = 2 if row == start_row else 1

        #check forward
        for i in range(1,maxMove+1):
            if board[row+(direction*i)][col] is None:
                print(i)
                setPassant = False if i is 1 else "setPassant"
                legalMoves.append(((row+(direction*i), col), setPassant))

        #check taking
        if board[row+(direction*i)][col-1] is not None:
            legalMoves.append(((row+(direction*i), col-1), False))
        if board[row+(direction*i)][col+1] is not None:
            legalMoves.append(((row+(direction*i), col+1), False))

        #check en passant
        if type(board[row][col-1]) is Pawn and board[row][col-1].passant is True and board[row+(direction*i)][col-1] is None:
            legalMoves.append(((row+(direction*i), col-1), True))
        if type(board[row][col+1]) is Pawn and board[row][col+1].passant is True and board[row+(direction*i)][col-+1] is None:
            legalMoves.append(((row+(direction*i), col+1), True))

        print(self.passant)
        return legalMoves