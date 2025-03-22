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

        if row < 0 or row > 7 or col < 0 or col > 7:
            return None
        #check forward
        for i in range(1,maxMove+1):
            if board[row+(direction*i)][col] is None:
                setPassant = False if i is 1 else "setPassant"
                legalMoves.append(((row+(direction*i), col), setPassant))
            else:
                break

        #check taking
        for z in [-1, 1]:
            if col-z >= 0 and col+z < len(board):
                if board[row+(direction)][col+z] is not None:
                    if self.checkColor(board[row+(direction)][col+z]):
                        legalMoves.append(((row+(direction), col+z), False))
                        
        #check en passant
        for z in [-1, 1]:
            if col-z >= 0 and col+z < len(board):
                if type(board[row][col+z]) is Pawn and board[row][col+z].passant is True and board[row+(direction)][col+z] is None:
                    if self.checkColor(board[row][col+z]):
                        legalMoves.append(((row+(direction), col+z), True))
        return legalMoves
    
    def checkColor(self, piece):
        if self.color != piece.color:
            return True
        else:
            return False