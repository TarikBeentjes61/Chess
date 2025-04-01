from chess.Piece import Piece
class Queen(Piece):
    def calcMoves(self, row, col, board):
        pieces = board.pieces
        legalMoves = []
        oppositeColor = self.color.opposite()

        #Diagonal lines
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
                
        #Straight lines
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