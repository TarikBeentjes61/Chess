import pygame
import pygame.gfxdraw
import threading
from models.Board import Board
from models.Type import Type
from models.Bob import Bob
from models.Color import Color

class ChessGame:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 800, 800
        self.ROWS, self.COLS = 8, 8
        self.SQUARE_SIZE = self.WIDTH // self.COLS
        self.LIGHT = (235, 217, 186)
        self.DARK = (181, 136, 99)
        self.RED = (155, 0, 0, 135)
        self.GREEN = (0, 125, 0, 105)
        self.win = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Chess Board")
        self.clock = pygame.time.Clock()
        self.running = True
        self.dragging = False
        self.lastX, self.lastY = 0, 0
        self.bob = Bob()
        self.bob_calculating = False
        self.bob_thread = None  
        self.lock = threading.Lock()
        self.mainBoard = Board()
        self.load_piece_images()
        self.board_surface = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.draw_board()

    def load_piece_images(self):
        self.piece_images = {}
        for color in ["white", "black"]:
            for piece_type in Type:
                if piece_type != Type.Empty:
                    self.piece_images[(color, piece_type.value)] = pygame.transform.smoothscale(
                        pygame.image.load(f"{color}pieces/{piece_type.value}.png").convert_alpha(),
                        (self.SQUARE_SIZE, self.SQUARE_SIZE)
                    )

    def draw_board(self):
        for row in range(self.ROWS):
            for col in range(self.COLS):
                color = self.LIGHT if (row + col) % 2 == 0 else self.DARK
                pygame.draw.rect(self.board_surface, color, (col * self.SQUARE_SIZE, row * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE))

    def draw_pieces(self):
        for row in range(len(self.mainBoard.pieces)):
            for col in range(len(self.mainBoard.pieces[row])):
                piece = self.mainBoard.pieces[row][col]
                if piece:
                    img = self.piece_images[(piece.color.value.lower(), piece.get_type())]
                    self.win.blit(img, (col * self.SQUARE_SIZE, row * self.SQUARE_SIZE))

    def handle_mouse_down(self, pos):
        col, row = pos[0] // self.SQUARE_SIZE, pos[1] // self.SQUARE_SIZE
        if self.mainBoard.pieces[row][col] is not None and self.mainBoard.pieces[row][col].color == self.mainBoard.color:
            self.mainBoard.selectedPiece = self.mainBoard.pieces[row][col]
        else:
            return
        self.lastX, self.lastY = col, row
        if self.mainBoard.selectedPiece and self.mainBoard.selectedPiece.color == self.mainBoard.color:
            self.dragging = True
        else:
            self.selectedPiece = None

    def handle_mouse_drag(self):
        pos = pygame.mouse.get_pos()
        img = self.piece_images[(self.mainBoard.selectedPiece.color.value.lower(), self.mainBoard.selectedPiece.get_type())]
        self.win.blit(img, (pos[0] - self.SQUARE_SIZE // 2, pos[1] - self.SQUARE_SIZE // 2))

    def handle_mouse_up(self, pos):
        if not self.dragging:
            return

        col, row = pos[0] // self.SQUARE_SIZE, pos[1] // self.SQUARE_SIZE
        target = (row, col)
        selectedMove, flag = None, None

        for move, flag_ in self.mainBoard.selectedPiece.legalMoves:
            if move == target:
                selectedMove, flag = move, flag_
                break

        if selectedMove and (col != self.lastX or row != self.lastY):
            self.mainBoard.move_piece(self.lastY, self.lastX, row, col, flag)
            self.mainBoard.swap_turns()
        else:
            self.mainBoard.pieces[self.lastY][self.lastX] = self.mainBoard.selectedPiece

        self.dragging = False
        self.selectedPiece = None

    def highlight_moves(self):
        if self.mainBoard.selectedPiece.legalMoves:
            for move in self.mainBoard.selectedPiece.legalMoves:
                move_row, move_col = move[0]
                pygame.gfxdraw.aacircle(
                    self.win, 
                    move_col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2,
                    move_row * self.SQUARE_SIZE + self.SQUARE_SIZE // 2,
                    self.SQUARE_SIZE // 6,
                    self.GREEN)
                pygame.gfxdraw.filled_circle(
                    self.win, 
                    move_col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2,
                    move_row * self.SQUARE_SIZE + self.SQUARE_SIZE // 2,
                    self.SQUARE_SIZE // 6,
                    self.GREEN)

    def highlight_check(self):
        kingPos = self.mainBoard.findKing()
        move_row, move_col = kingPos
        pygame.gfxdraw.aacircle(
            self.win, 
            move_col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2,
            move_row * self.SQUARE_SIZE + self.SQUARE_SIZE // 2,
            self.SQUARE_SIZE // 2,
            self.RED)
        pygame.gfxdraw.filled_circle(
            self.win, 
            move_col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2,
            move_row * self.SQUARE_SIZE + self.SQUARE_SIZE // 2,
            self.SQUARE_SIZE // 2,
            self.RED)

    def calculate_bob_move(self):
        with self.lock:
            self.bob_calculating = True
            best_move = self.bob.find_best_move(self.mainBoard, 4)
            if best_move:
                start_row, start_col, end_row, end_col, flag = best_move
                self.mainBoard.move_piece(start_row, start_col, end_row, end_col, flag)
                self.mainBoard.swap_turns()
            self.bob_calculating = False
        
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_down(pygame.mouse.get_pos())
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.handle_mouse_up(pygame.mouse.get_pos())

            if self.mainBoard.color == Color.Black and not self.bob_calculating:
                if self.bob_thread is None or not self.bob_thread.is_alive():
                    self.bob_thread = threading.Thread(target=self.calculate_bob_move)
                    self.bob_thread.start()

            self.win.blit(self.board_surface, (0, 0))
            if self.mainBoard.check:
                self.highlight_check()
            self.draw_pieces()
            if self.mainBoard.selectedPiece:
                self.highlight_moves()
            if self.dragging and self.mainBoard.selectedPiece:
                self.handle_mouse_drag()

            pygame.display.update()

        pygame.quit()

if __name__ == "__main__":
    ChessGame().run()
