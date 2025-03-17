from models.Bishop import Bishop
from models.Pawn import Pawn
from models.Knight import Knight
from models.King import King
from models.Rook import Rook
from models.Queen import Queen
from models.Color import Color
class Board:
    def __init__(self):
        self.pieces = self.baseBoard()
    def baseBoard(self):
            board = []

            # Initialize board with specific piece objects
            board.append([
                Rook(Color.Black), Knight(Color.Black), Bishop(Color.Black), Queen(Color.Black),
                King(Color.Black), Bishop(Color.Black), Knight(Color.Black), Rook(Color.Black)
            ])
            board.append([Pawn(Color.Black) for _ in range(8)])

            for _ in range(4):
                board.append([None for _ in range(8)])

            board.append([Pawn(Color.White) for _ in range(8)])
            board.append([
                Rook(Color.White), Knight(Color.White), Bishop(Color.White), Queen(Color.White),
                King(Color.White), Bishop(Color.White), Knight(Color.White), Rook(Color.White)
            ])

            return board
    def checkLegalMoves(self,row,col):
        piece = self.pieces[row][col]
        legalMoves = piece.calcMoves(row, col, self.pieces)
        