from models.Piece import Piece
class King(Piece):
    def calcMoves(self, row, col, board):
        legalMoves = []
        oppositeColor = self.color.opposite()

        for r in range(-1, 2):
            for c in range(-1, 2):
                newY = row+r
                newX = col+c
                if newY >= 0 and newY < len(board) and newX >= 0 and newX < len(board):
                    piece = board[newY][newX]

                    if piece == None or piece.color == oppositeColor:
                        legalMoves.append(((newY, newX), False))

        return legalMoves