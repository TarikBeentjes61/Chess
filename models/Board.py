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
        self.check = False
        self.color = Color.White
        self.setLegalMoves()

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
    def setLegalMoves(self):
        self.checkCheck()
        for r, row in enumerate(self.pieces):
            for c, piece in enumerate(row):
                if piece is not None:
                    piece.legalMoves = self.getValidMoves(r, c)
    def getValidMoves(self, row, col):
        validMoves = []
        piece = self.pieces[row][col]

        if piece is not None:
            legalMoves = piece.calcMoves(row, col, self)

            for move, flag in legalMoves:
                temp_piece = self.pieces[move[0]][move[1]]
                self.pieces[move[0]][move[1]] = piece
                self.pieces[row][col] = None


                #make sure king is safe
                original_check = self.check
                self.checkCheck() 

                if not self.check:  
                    validMoves.append((move, flag))

                #remove temp
                self.pieces[row][col] = piece
                self.pieces[move[0]][move[1]] = temp_piece
                self.check = original_check

        return validMoves
    def getAttackedSquares(self, color):
        attackedSquares = set()
        for r, row in enumerate(self.pieces):
            for c, piece in enumerate(row):
                if piece is not None and piece.color == color:
                    moves = piece.calcMoves(r, c, self)
                    for move in moves:
                        if move[1] == 'attack': 
                            attackedSquares.add(move)

        return attackedSquares
    
    def findKing(self):
        for r, row in enumerate(self.pieces):
              for c, piece in enumerate(row):
                  if isinstance(piece, King) and piece.color == self.color:
                      return (r,c)
        return None
    
    def checkCheck(self):
        kingPos = self.findKing()
        if not kingPos:
            return  

        attackedSquares = self.getAttackedSquares(self.color.opposite())

        self.check = False
        for pos in attackedSquares:
            if kingPos == pos[0]:  
                self.check = True
                return  

    def checkCheckmate(self):
        pass
