from models.Bishop import Bishop
from models.Pawn import Pawn
from models.Knight import Knight
from models.King import King
from models.Rook import Rook
from models.Queen import Queen
from models.Color import Color
from models.Bob import Bob
class Board:
    def __init__(self):
        self.pieces = self.baseBoard()
        self.board_state_before_move = None
        self.move_history = []
        self.selectedPiece = None
        self.check = False
        self.color = Color.White
        self.bob = Bob()
        self.moveCount = 0
        self.setLegalMoves()
        self.count = 0
    def baseBoard(self):
            board = []
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
    
    def move_piece(self, start_row, start_col, end_row, end_col, flag):
            piece = self.pieces[start_row][start_col]
            self.selectedPiece = piece

            if piece is None:
                return

            captured_piece = self.pieces[end_row][end_col]

            if isinstance(piece, Rook):
                piece.hasMoved = True

            if isinstance(piece, King):
                if flag == "castleQueen":
                    rook = self.pieces[end_row][0]
                    if isinstance(rook, Rook): 
                        self.pieces[end_row][end_col+1] = rook
                        self.pieces[end_row][0] = None 
                        rook.hasMoved = True
                elif flag == "castleKing":
                    rook = self.pieces[end_row][7] 
                    if isinstance(rook, Rook): 
                        self.pieces[end_row][end_col-1] = rook  
                        self.pieces[end_row][7] = None 
                        rook.hasMoved = True
                        piece.castled = True
                piece.hasMoved = True

            if isinstance(piece, Pawn):
                if piece.passant:
                    piece.passant = False
                if flag == "setPassant":
                    piece.passant = True
                if flag == "passant":
                    capturedRow = end_row - 1 if piece.color == Color.Black else end_row + 1
                    captured_piece = self.pieces[capturedRow][end_col]
                    self.pieces[capturedRow][end_col] = None
                if flag == "promotion":
                    piece = Queen(piece.color)

            self.pieces[start_row][start_col] = None
            self.pieces[end_row][end_col] = piece

            self.move_history.append((piece, start_row, start_col, end_row, end_col, captured_piece, flag))

    def undo_move(self):
        if not self.move_history:
            return
        
        last_move = self.move_history.pop()

        if not last_move:
            return
        
        piece, start_row, start_col, end_row, end_col, captured_piece, flag = last_move

        self.pieces[start_row][start_col] = piece
        self.pieces[end_row][end_col] = captured_piece

        if isinstance(piece, King):
            if flag == "castleQueen":
                if start_row == 0 or start_row == 7:
                    self.pieces[start_row][start_col] = piece
                    self.pieces[end_row][end_col+1] = None
                    self.pieces[start_row][0] = Rook(piece.color)
                    piece.castled = False
            elif flag == "castleKing":
                if start_row == 0 or start_row == 7:
                    self.pieces[start_row][start_col] = piece
                    self.pieces[end_row][end_col-1] = None
                    self.pieces[start_row][7] = Rook(piece.color)
                    piece.castled = False
            piece.hasMoved = False
        if isinstance(piece, Rook):
            piece.hasMoved = False
        if flag == "passant":
            capturedRow = end_row - 1 if piece.color == Color.Black else end_row + 1
            if captured_piece: 
                self.pieces[capturedRow][end_col] = captured_piece

        if flag == "promotion":
            if captured_piece is not None:
                self.pieces[end_row][end_col] = captured_piece

            self.pieces[start_row][start_col] = Pawn(piece.color)
        
    def swap_turns(self):
        self.move_history = []
        for row in self.pieces:
            for piece in row:
                if isinstance(piece, Pawn):
                    piece.passant = False
        self.color = Color.Black if self.color == Color.White else Color.White
        self.checkCheck()
        self.setLegalMoves()
        self.selectedPiece = None

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