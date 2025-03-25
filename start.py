import pygame
from models.Board import Board
from models.Pawn import Pawn
from models.Queen import Queen
from models.King import King
from models.Color import Color
from models.Type import Type

class ChessGame:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 800, 800
        self.ROWS, self.COLS = 8, 8
        self.SQUARE_SIZE = self.WIDTH // self.COLS
        self.WHITE = (255, 255, 255)
        self.BLACK = (100, 100, 100)
        self.win = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Chess Board")
        self.clock = pygame.time.Clock()
        self.running = True
        self.dragging = False
        self.selectedPiece = None
        self.selectedRow = None
        self.selectedCol = None
        self.lastX, self.lastY = 0, 0
        self.legalMoves = None
        self.mainBoard = Board()
        self.load_piece_images()
        self.board_surface = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.draw_board()

    def load_piece_images(self):
        self.piece_images = {}
        for color in ["white", "black"]:
            for piece_type in Type:
                if piece_type != Type.Empty:
                    self.piece_images[(color, piece_type.value)] = pygame.transform.scale(
                        pygame.image.load(f"{color}pieces/{piece_type.value}.png").convert_alpha(),
                        (self.SQUARE_SIZE, self.SQUARE_SIZE)
                    )

    def draw_board(self):
        for row in range(self.ROWS):
            for col in range(self.COLS):
                color = self.WHITE if (row + col) % 2 == 0 else self.BLACK
                pygame.draw.rect(self.board_surface, color, (col * self.SQUARE_SIZE, row * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE))

    def draw_pieces(self):
        for row in range(len(self.mainBoard.pieces)):
            for col in range(len(self.mainBoard.pieces[row])):
                piece = self.mainBoard.pieces[row][col]
                if piece:
                    img = self.piece_images[(piece.color.value.lower(), piece.type())]
                    self.win.blit(img, (col * self.SQUARE_SIZE, row * self.SQUARE_SIZE))

    def swap_turns(self):
        for row in self.mainBoard.pieces:
            for piece in row:
                if isinstance(piece, Pawn) and piece.color != self.mainBoard.color:
                    piece.passant = False
        self.mainBoard.color = Color.Black if self.mainBoard.color == Color.White else Color.White
        self.mainBoard.checkCheck()
        self.mainBoard.setLegalMoves()

    def handle_mouse_down(self, pos):
        col, row = pos[0] // self.SQUARE_SIZE, pos[1] // self.SQUARE_SIZE
        self.selectedPiece = self.mainBoard.pieces[row][col]
        self.selectedRow, self.selectedCol = row, col
        self.lastX, self.lastY = col, row
        if self.selectedPiece and self.selectedPiece.color ==self.mainBoard.color:
            self.legalMoves = self.selectedPiece.legalMoves
            self.dragging = True
        else:
            self.selectedPiece = None

    def handle_mouse_drag(self):
        pos = pygame.mouse.get_pos()
        img = self.piece_images[(self.selectedPiece.color.value.lower(), self.selectedPiece.type())]
        self.win.blit(img, (pos[0] - self.SQUARE_SIZE // 2, pos[1] - self.SQUARE_SIZE // 2))

    def handle_mouse_up(self, pos):
        if not self.dragging:
            return

        col, row = pos[0] // self.SQUARE_SIZE, pos[1] // self.SQUARE_SIZE
        target = (row, col)
        selectedMove, flag = None, None

        for move, flag_ in self.legalMoves:
            if move == target:
                selectedMove, flag = move, flag_
                break

        if selectedMove and (col != self.lastX or row != self.lastY):
            self.move_piece(row, col, flag)
        else:
            self.mainBoard.pieces[self.lastY][self.lastX] = self.selectedPiece

        self.dragging = False
        self.selectedPiece = None

    def move_piece(self, row, col, flag):
        if isinstance(self.selectedPiece, King):
            if flag == "castleQueen":
                rook = self.mainBoard.pieces[row][0]
                self.mainBoard.pieces[row][col+1] = rook
                self.mainBoard.pieces[row][0] = None
            elif flag== "castleKing":
                rook = self.mainBoard.pieces[row][7]
                self.mainBoard.pieces[row][col-1] = rook
                self.mainBoard.pieces[row][7] = None

        if isinstance(self.selectedPiece, Pawn):
            if self.selectedPiece.passant:
                self.selectedPiece.passant = False
            if flag == "setPassant":
                self.selectedPiece.passant = True
            if flag == "passant":
                capturedRow = row - 1 if self.selectedPiece.color == Color.Black else row + 1
                self.mainBoard.pieces[capturedRow][col] = None
            if row == 0 or row == 7:
                self.selectedPiece = Queen(self.selectedPiece.color)

        self.mainBoard.pieces[row][col] = self.selectedPiece
        self.mainBoard.pieces[self.selectedRow][self.selectedCol] = None
        self.swap_turns()
        

    def highlight_moves(self):
        if self.legalMoves:
            for move in self.legalMoves:
                move_row, move_col = move[0]
                pygame.draw.circle(self.win, (0, 255, 0),
                                   (move_col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2,
                                    move_row * self.SQUARE_SIZE + self.SQUARE_SIZE // 2),
                                   self.SQUARE_SIZE // 4)

    def highlight_attacked_squares(self):
        attackedSquares = self.mainBoard.getAttackedSquares(self.mainBoard.color)
        for move in attackedSquares:
            move_row, move_col = move[0]
            pygame.draw.circle(self.win, (155, 155, 0),
                               (move_col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2,
                                move_row * self.SQUARE_SIZE + self.SQUARE_SIZE // 2),
                               self.SQUARE_SIZE // 4)
    def highlight_check(self):
        kingPos = self.mainBoard.findKing()
        move_row, move_col = kingPos
        pygame.draw.circle(self.win, (255, 0, 0),
                            (move_col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2,
                            move_row * self.SQUARE_SIZE + self.SQUARE_SIZE // 2),
                            self.SQUARE_SIZE // 4)

    def run(self):
        while self.running:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_down(pygame.mouse.get_pos())
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.handle_mouse_up(pygame.mouse.get_pos())

            self.win.blit(self.board_surface, (0, 0))
            #self.highlight_attacked_squares()
            if self.mainBoard.check:
                self.highlight_check()
            self.draw_pieces()
            if self.selectedPiece:
                self.highlight_moves()
            if self.dragging and self.selectedPiece:
                self.handle_mouse_drag()
            pygame.display.update()

        pygame.quit()

if __name__ == "__main__":
    ChessGame().run()
