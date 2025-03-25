from models.Piece import Piece
from models.Rook import Rook
class King(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.hasMoved = False  
    def calcMoves(self, row, col, board):
        pieces = board.pieces
        legalMoves = []
        oppositeColor = self.color.opposite()

        for r in range(-1, 2):
            for c in range(-1, 2):
                newY = row+r
                newX = col+c
                if newY >= 0 and newY < len(pieces) and newX >= 0 and newX < len(pieces):
                    piece = pieces[newY][newX]

                    if piece == None or piece.color == oppositeColor:
                        legalMoves.append(((newY, newX), "attack"))

        if not self.hasMoved and board.check is False:
            if self.checkQueenSideCastle(row, pieces):
                legalMoves.append(((row, col-2), "castleQueen"))
            if self.checkKingSideCastle(row, pieces):
                legalMoves.append(((row, col+2), "castleKing"))
        return legalMoves
    
    def checkQueenSideCastle(self, row, board):
        rook = board[row][0]
        if isinstance(rook, Rook) and rook.color == self.color and not rook.hasMoved:
                for x in [1,2,3]:
                    if board[row][x] is not None:
                        return False
                return True
        return False
    def checkKingSideCastle(self, row, board):
        rook = board[row][7]
        if isinstance(rook, Rook) and rook.color == self.color and not rook.hasMoved:
                for x in [5,6]:
                    if board[row][x] is not None:
                        return False
                    else:
                        return True
        return False