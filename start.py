from models.Board import Board
from models.Pawn import Pawn
from models.Piece import Piece
from models.Type import Type
from models.Color import Color
import pygame

mainBoard = Board()

pygame.init()

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS
WHITE = (255, 255, 255)
BLACK = (100, 100, 100)

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Board")
piece_images = {}
for color in ["white", "black"]:
    for piece_type in Type:
        if piece_type != Type.Empty:
            piece_images[(color, piece_type.value)] = pygame.transform.scale(
                pygame.image.load(f"{color}pieces/{piece_type.value}.png").convert_alpha(),
                (SQUARE_SIZE, SQUARE_SIZE)
            )

board_surface = pygame.Surface((WIDTH, HEIGHT))

def draw_board():
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(board_surface, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

draw_board()

def draw_pieces():
    for row in range(len(mainBoard.pieces)):
        for col in range(len(mainBoard.pieces[row])):
            piece = mainBoard.pieces[row][col]
            if piece != None:
                img = piece_images[(piece.color.value.lower(), piece.type())]
                win.blit(img, (col * SQUARE_SIZE, row * SQUARE_SIZE))

running = True
dragging = False
selectedPiece = None
lastX, lastY = 0, 0
clock = pygame.time.Clock()
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            x = pos[0] // SQUARE_SIZE
            y = pos[1] // SQUARE_SIZE
            selectedPiece = mainBoard.pieces[y][x]
            lastX = x
            lastY = y
            mainBoard.checkLegalMoves(y,x)
            if selectedPiece != None:
                dragging = True
                mainBoard.pieces[y][x] = None


        if event.type == pygame.MOUSEBUTTONUP and dragging:
            pos = pygame.mouse.get_pos()
            x = pos[0] // SQUARE_SIZE
            y = pos[1] // SQUARE_SIZE

            if 0 <= x < 8 and 0 <= y < 8 and (x != lastX or y != lastY):
                mainBoard.pieces[y][x] = selectedPiece
            else:
                mainBoard.pieces[lastY][lastX] = selectedPiece
            dragging = False
            selectedPiece = None

    win.blit(board_surface, (0, 0))
    draw_pieces()

    if dragging and selectedPiece:
        pos = pygame.mouse.get_pos()
        img = piece_images[(selectedPiece.color.value.lower(), selectedPiece.type())]
        win.blit(img, (pos[0] - SQUARE_SIZE // 2, pos[1] - SQUARE_SIZE // 2))

    pygame.display.update()

pygame.quit()