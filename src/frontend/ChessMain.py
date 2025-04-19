import sys
import pygame
import ChessEngine
import AIEngine
import Constants
import time

WIDTH = Constants.WIDTH
HEIGHT = Constants.HEIGHT
WIDTH_BOARD = Constants.WIDTH_BOARD  # chiều rộng của bàn cờ
HEIGHT_BOARD = Constants.HEIGHT_BOARD  # chiều cao của bàn cờ
# MOVE_LOG_W = Constants.MOVE_LOG_W # chiều rộng của bảng lịch sử nước đi
# MOVE_LOG_H = Constants.MOVE_LOG_H # chiều cao của bảng lịch sử nước đi
# DIMENSION = Constants.DIMENSION  # chiều của bàn cờ là 8x8
SQ_SIZE = Constants.SQ_SIZE  # kich cỡ của một ô vuông trong bàn cờ
# MAX_FPS = Constants.MAX_FPS  # for animation
PIECE_IMAGES = {}
gs = ChessEngine.GameState()  # Khởi tạo trạng thái game
board = gs.board  # Lấy bàn cờ từ trạng thái game
validMoves = []  # Danh sách các nước đi hợp lệ
sqSelected = ()  # Ô được chọn (row, col)
playerClicks = []  # Danh sách các ô đã click [(row, col), (row, col)]

"""
khởi tạo một từ điển hình ảnh toàn cục. sẽ được gọi một lần duy nhât trong main
"""
board_img = pygame.transform.smoothscale(pygame.image.load("assets/img/banco.png"), (WIDTH_BOARD, HEIGHT_BOARD))

pieces1 = ["r_king", "r_guard", "r_elephant", "r_rook", "r_horse", "r_cannon", "r_pawn"]
pieces2 = ["b_king", "b_guard", "b_elephant", "b_rook", "b_horse", "b_cannon", "b_pawn"]
for pi in pieces1:
    PIECE_IMAGES[pi] = pygame.transform.smoothscale(pygame.image.load("assets/img/Red/" + pi + ".png"), (SQ_SIZE, SQ_SIZE))
for pi in pieces2:
    PIECE_IMAGES[pi] = pygame.transform.smoothscale(pygame.image.load("assets/img/Black/" + pi + ".png"), (SQ_SIZE, SQ_SIZE))

def draw_board():
    Constants.screen.blit(board_img, (0, 0))
    if sqSelected != ():
        r, c = sqSelected
        # Vẽ ô được chọn
        s = pygame.Surface((SQ_SIZE, SQ_SIZE))
        s.set_alpha(100)
        s.fill(Constants.BLUE)
        Constants.screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
        # Vẽ các nước đi hợp lệ
        s.fill(Constants.GREEN)
        for move in validMoves:
            if move.startRow == r and move.startCol == c:
                Constants.screen.blit(s, (move.endCol * SQ_SIZE, move.endRow * SQ_SIZE))

def draw_pieces():
    for r in range(Constants.ROWS):
        for c in range(Constants.COLS):
            piece = board[r][c]
            if piece != "--":
                Constants.screen.blit(PIECE_IMAGES[piece], (c * SQ_SIZE, r * SQ_SIZE))

def game_screen():
    global sqSelected, playerClicks, validMoves, gs, board
    while True:
        Constants.screen.fill(Constants.YELLOW)
        draw_board()
        draw_pieces()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()
                col = int(location[0] // SQ_SIZE)  # Chuyển đổi thành số nguyên
                row = int(location[1] // SQ_SIZE)  # Chuyển đổi thành số nguyên
                
                # Kiểm tra xem vị trí có nằm trong bàn cờ không
                if 0 <= row < Constants.ROWS and 0 <= col < Constants.COLS:
                    if sqSelected == (row, col):  # Click vào ô đã chọn
                        sqSelected = ()
                        playerClicks = []
                        validMoves = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)
                        
                        if len(playerClicks) == 1:  # Chọn quân cờ
                            validMoves = gs.getValidMoves()
                            # Lọc các nước đi hợp lệ cho quân cờ được chọn
                            validMoves = [move for move in validMoves if move.startRow == row and move.startCol == col]
                        elif len(playerClicks) == 2:  # Di chuyển quân cờ
                            move = ChessEngine.Move(playerClicks[0], playerClicks[1], board)
                            if move in validMoves:
                                gs.makeMove(move)
                                sqSelected = ()
                                playerClicks = []
                                validMoves = []
                            else:
                                playerClicks = [playerClicks[1]]
                                validMoves = gs.getValidMoves()
                                validMoves = [move for move in validMoves if move.startRow == row and move.startCol == col]
        
        pygame.display.flip()