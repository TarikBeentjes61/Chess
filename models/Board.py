from models.Piece import Piece
from models.Type import Type
from models.Color import Color
class Board:
    def __init__(self):
        self.pieces = self.baseBoard()
    def baseBoard(self):
        board = []

        board.append([
            Piece(Type.Rook, Color.White), Piece(Type.Knight, Color.White),
            Piece(Type.Bishop, Color.White), Piece(Type.Queen, Color.White),
            Piece(Type.King, Color.White), Piece(Type.Bishop, Color.White),
            Piece(Type.Knight, Color.White), Piece(Type.Rook, Color.White)
        ])

        board.append([Piece(Type.Pawn, Color.White) for _ in range(8)])

        for _ in range(4):
            board.append([Piece(Type.Empty, Color.Empty) for _ in range(8)])

        board.append([Piece(Type.Pawn, Color.Black) for _ in range(8)])

        board.append([
            Piece(Type.Rook, Color.Black), Piece(Type.Knight, Color.Black),
            Piece(Type.Bishop, Color.Black), Piece(Type.Queen, Color.Black),
            Piece(Type.King, Color.Black), Piece(Type.Bishop, Color.Black),
            Piece(Type.Knight, Color.Black), Piece(Type.Rook, Color.Black)
        ])

        return board