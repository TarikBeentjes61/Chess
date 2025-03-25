from models.Piece import Piece
class Bishop(Piece):
    def calcMoves(self, row, col, board):
        pieces = board.pieces
        legalMoves = []
        oppositeColor = self.color.opposite()

        directions = [
            (-1,-1), #Top left
            (-1, 1), #Top right
            (1, -1), #Bottom left
            (1,1),   #Bottom right
        ]

        for direction in directions:
            newY = row
            newX = col
            while True:
                newY += direction[0]
                newX += direction[1]
                if newY >= 0 and newY < len(pieces) and newX >= 0 and newX < len(pieces):
                    piece = pieces[newY][newX]
                    if piece is None:
                        legalMoves.append(((newY, newX), "attack"))
                    elif piece.color == oppositeColor:
                        legalMoves.append(((newY, newX), "attack"))
                        break
                    else:
                        break
                else:
                    break

        return legalMoves
