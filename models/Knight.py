from models.Piece import Piece
class Knight(Piece):
    def calcMoves(self, row, col, board):
        pieces = board.pieces
        legalMoves = []
        oppositeColor = self.color.opposite()
        moves = [
            (-2, -1), (-2, 1),  #Up
            (2, -1),  (2, 1),    #Down
            (-1, -2), (-1, 2),  #Left
            (1, -2),  (1, 2)     #Right
        ]

        for y,x in moves:
            newY = row+y
            newX = col+x

            if newY >= 0 and newY < len(pieces) and newX >= 0 and newX < len(pieces):
                piece = pieces[newY][newX]
                if piece is None or piece.color == oppositeColor:
                    legalMoves.append(((newY, newX), "attack"))

        return legalMoves