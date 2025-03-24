from models.Piece import Piece
class Queen(Piece):
    def calcMoves(self, row, col, board):
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
                if newY >= 0 and newY < len(board) and newX >= 0 and newX < len(board):
                    piece = board[newY][newX]
                    if piece is None:
                        legalMoves.append(((newY, newX), False))
                    elif piece.color == oppositeColor:
                        legalMoves.append(((newY, newX), False))
                        break
                    else:
                        break
                else:
                    break
        
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