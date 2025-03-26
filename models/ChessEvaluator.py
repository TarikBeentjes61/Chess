from models.Color import Color
class ChessEvaluator:
    def __init__(self):
        #Tables based of https://www.chessprogramming.org/Simplified_Evaluation_Function
        self.whitePawnTable = [
            [  0,   0,   0,   0,   0,   0,   0,   0 ],
            [ 50,  50,  50,  50,  50,  50,  50,  50 ],
            [ 10,  10,  20,  30,  30,  20,  10,  10 ],
            [  5,   5,  10,  25,  25,  10,   5,   5 ],
            [  0,   0,   0,  20,  20,   0,   0,   0 ],
            [  5,  -5, -10,   0,   0, -10,  -5,   5 ],
            [  5,  10,  10, -20, -20,  10,  10,   5 ],
            [  0,   0,   0,   0,   0,   0,   0,   0 ]
        ]
        self.blackPawnTable = self.whitePawnTable[::-1]

        self.whiteKnightTable = [
            [-50, -40, -30, -30, -30, -30, -40, -50 ],
            [-40, -20,   0,   0,   0,   0, -20, -40 ],
            [-30,   0,  10,  15,  15,  10,   0, -30 ],
            [-30,   5,  15,  20,  20,  15,   5, -30 ],
            [-30,   0,  15,  20,  20,  15,   0, -30 ],
            [-30,   5,  10,  15,  15,  10,   5, -30 ],
            [-40, -20,   0,   5,   5,   0, -20, -40 ],
            [-50, -40, -30, -30, -30, -30, -40, -50 ]
        ]
        self.blackKnightTable = self.whiteKnightTable[::-1]

        self.whiteBishopTable = [
            [-20, -10, -10, -10, -10, -10, -10, -20 ],
            [-10,   0,   0,   0,   0,   0,   0, -10 ],
            [-10,   0,   5,  10,  10,   5,   0, -10 ],
            [-10,   5,   5,  10,  10,   5,   5, -10 ],
            [-10,   0,  10,  10,  10,  10,   0, -10 ],
            [-10,  10,  10,  10,  10,  10,  10, -10 ],
            [-10,   5,   0,   0,   0,   0,   5, -10 ],
            [-20, -10, -10, -10, -10, -10, -10, -20 ]
        ]
        self.blackBishopTable = self.whiteBishopTable[::-1]

        self.whiteRookTable = [
            [  0,   0,   0,   0,   0,   0,   0,   0 ],
            [  5,  10,  10,  10,  10,  10,  10,   5 ],
            [ -5,   0,   0,   0,   0,   0,   0,  -5 ],
            [ -5,   0,   0,   0,   0,   0,   0,  -5 ],
            [ -5,   0,   0,   0,   0,   0,   0,  -5 ],
            [ -5,   0,   0,   0,   0,   0,   0,  -5 ],
            [ -5,   0,   0,   0,   0,   0,   0,  -5 ],
            [  0,   0,   0,   5,   5,   0,   0,   0 ]
        ]
        self.blackRookTable = self.whiteRookTable[::-1]

        self.whiteQueenTable = [
            [-20, -10, -10,  -5,  -5, -10, -10, -20 ],
            [-10,   0,   0,   0,   0,   0,   0, -10 ],
            [-10,   0,   5,   5,   5,   5,   0, -10 ],
            [ -5,   0,   5,   5,   5,   5,   0,  -5 ],
            [  0,   0,   5,   5,   5,   5,   0,  -5 ],
            [-10,   5,   5,   5,   5,   5,   0, -10 ],
            [-10,   0,   5,   0,   0,   0,   0, -10 ],
            [-20, -10, -10,  -5,  -5, -10, -10, -20 ]
        ]
        self.blackQueenTable = self.whiteQueenTable[::-1]

        self.whiteKingTable = [
            [-30, -40, -40, -50, -50, -40, -40, -30 ],
            [-30, -40, -40, -50, -50, -40, -40, -30 ],
            [-30, -40, -40, -50, -50, -40, -40, -30 ],
            [-30, -40, -40, -50, -50, -40, -40, -30 ],
            [-20, -30, -30, -40, -40, -30, -30, -20 ],
            [-10, -20, -20, -20, -20, -20, -20, -10 ],
            [ 20,  20,   0,   0,   0,   0,  20,  20 ],
            [ 20,  30,  10,   0,   0,  10,  30,  20 ]
        ]
        self.blackKingTable = self.whiteKingTable[::-1]

        self.pieceSquareTables = {
            ('Pawn', Color.White): self.whitePawnTable,
            ('Knight', Color.White): self.whiteKnightTable,
            ('Bishop', Color.White): self.whiteBishopTable,
            ('Rook', Color.White): self.whiteRookTable,
            ('Queen', Color.White): self.whiteQueenTable,
            ('King', Color.White): self.whiteKingTable,
            ('Pawn', Color.Black): self.blackPawnTable,
            ('Knight', Color.Black): self.blackKnightTable,
            ('Bishop', Color.Black): self.blackBishopTable,
            ('Rook', Color.Black): self.blackRookTable,
            ('Queen', Color.Black): self.blackQueenTable,
            ('King', Color.Black): self.blackKingTable
        }
