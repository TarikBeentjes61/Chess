from models.Board import Board
from models.Bishop import Bishop
from models.Pawn import Pawn
from models.Knight import Knight
from models.King import King
from models.Rook import Rook
from models.Queen import Queen
from models.Color import Color
from models.Type import Type
from models.Color import Color
import pygame

mainBoard = Board()

turn = Color.White
def swapTurns(turn):
    global mainBoard
    for row in mainBoard.pieces:
        for piece in row:
            if isinstance(piece, Pawn) and piece.color != turn:
                piece.passant = False

    return Color.Black if turn == Color.White else Color.White

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
selectedRow = None
selectedCol = None
lastX, lastY = 0, 0
clock = pygame.time.Clock()
legalMoves = None
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            col = pos[0] // SQUARE_SIZE
            row = pos[1] // SQUARE_SIZE
            selectedPiece = mainBoard.pieces[row][col]
            selectedRow = row
            selectedCol = col
            lastX = col
            lastY = row
            if selectedPiece is not None and selectedPiece.color == turn:
                legalMoves = mainBoard.checkLegalMoves(row,col)
                if selectedPiece != None:
                    dragging = True
                    mainBoard.pieces[row][col] = None




        if event.type == pygame.MOUSEBUTTONUP and dragging:
            pos = pygame.mouse.get_pos()
            col = pos[0] // SQUARE_SIZE
            row = pos[1] // SQUARE_SIZE

            target = (row, col)
            isEnPassant = None
            selectedMove = None
            for move, enPassant in legalMoves:
                if move == target:
                    selectedMove = move
                    isEnPassant = enPassant

            #make move
            if 0 <= col < 8 and 0 <= row < 8 and (col != lastX or row != lastY) and selectedMove:
                #special behavior for pawn
                if type(selectedPiece) is Pawn:
                    if selectedPiece.passant:
                        selectedPiece.passant = False

                    if isEnPassant == "setPassant":
                        selectedPiece.passant = True

                    if isEnPassant is True:
                        capturedRow = row -1 if selectedPiece.color == Color.Black else row + 1
                        mainBoard.pieces[capturedRow][col] = None

                    if row == 0:
                        selectedPiece = Queen(Color.White)
                    elif row == 7:
                        selectedPiece = Queen(Color.Black)

                #move the piece
                mainBoard.pieces[row][col] = selectedPiece
                mainBoard.pieces[selectedRow][selectedCol] = None
                turn = swapTurns(turn)
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
    
    if legalMoves is not None:
        for move in legalMoves:
            move_row, move_col = move[0]
            pygame.draw.circle(win, (0, 255, 0),  # Green color
                            (move_col * SQUARE_SIZE + SQUARE_SIZE // 2,  # X position
                                move_row * SQUARE_SIZE + SQUARE_SIZE // 2),  # Y position
                            SQUARE_SIZE // 4)  # Radius of the highlight
    

    pygame.display.update()

pygame.quit()