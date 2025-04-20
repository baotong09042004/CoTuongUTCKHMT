import sys
import pygame
import ChessChineseEngine
import AIEngine
import Constants
import time
import Win
WIDTH = Constants.WIDTH
HEIGHT = Constants.HEIGHT
WIDTH_BOARD = Constants.WIDTH_BOARD  # chiều rộng của bàn cờ
HEIGHT_BOARD = Constants.HEIGHT_BOARD  # chiều cao của bàn cờ

SQ_SIZE = Constants.SQ_SIZE  # kich cỡ của một ô vuông trong bàn cờ

PIECE_IMAGES = {}

# Khởi tạo các hình ảnh
canmove = pygame.transform.smoothscale(pygame.image.load("assets/img/CanMove.png"), (15, 15)) # ảnh đường đi của quân cờ
board_img = pygame.transform.smoothscale(pygame.image.load("assets/img/banco.png"), (WIDTH_BOARD, HEIGHT_BOARD))

pieces1 = ["r_king", "r_guard", "r_elephant", "r_rook", "r_horse", "r_cannon", "r_pawn"]
pieces2 = ["b_king", "b_guard", "b_elephant", "b_rook", "b_horse", "b_cannon", "b_pawn"]
for pi in pieces1:
    PIECE_IMAGES[pi] = pygame.transform.smoothscale(pygame.image.load("assets/img/Red/" + pi + ".png"), (SQ_SIZE, SQ_SIZE))
for pi in pieces2:
    PIECE_IMAGES[pi] = pygame.transform.smoothscale(pygame.image.load("assets/img/Black/" + pi + ".png"), (SQ_SIZE, SQ_SIZE))

#     Vẽ bàn cờ
def draw_Board(screen):
    screen.blit(board_img, (0, 0))
    
#     Vẽ Quân cờ lên bàn cờ
def draw_Pieces(screen, board):
    for r in range(Constants.ROWS):
        for c in range(Constants.COLS):
            piece = board[r][c]
            if piece != "--":
                screen.blit(PIECE_IMAGES[piece], (c * SQ_SIZE, r * SQ_SIZE))


def highlightSquares(screen, gs, validMoves, sqSelected):
    """
    Hàm này vẽ highlight cho các ô đã chọn và các nước đi hợp lệ.
    
    Tham số:
    - screen: Màn hình pygame để vẽ lên
    - gs: Trạng thái hiện tại của trò chơi
    - validMoves: Danh sách các nước đi hợp lệ
    - sqSelected: Ô đã chọn (r, c)
    """
    if sqSelected != ():  # nếu có ô nào được chọn
        r, c = sqSelected
        piece = gs.board[r][c]
        if piece != "--":  # nếu ô được chọn có quân cờ
            # Vẽ highlight cho ô được chọn
            s = pygame.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)  # độ trong suốt
            s.fill(pygame.Color("blue"))
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
            
            # Tìm vị trí của tướng đối phương
            enemy_king_pos = gs.blackKingLocation if gs.redToMove else gs.redKingLocation
            enemy_king = 'b_king' if gs.redToMove else 'r_king'
            
            # Vẽ các ô highlight cho các nước đi hợp lệ
            move_count = 0
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    move_count += 1
                    # Xác định màu highlight dựa trên loại nước đi
                    highlight_color = "green"  # Màu mặc định cho nước đi hợp lệ
                    alpha_value = 150  # Độ trong suốt mặc định
                    
                    # Nếu nước đi ăn quân
                    if move.pieceCaptured != "--":
                        # Nếu ăn tướng đối phương, hiển thị màu đỏ đậm
                        if move.pieceCaptured == enemy_king:
                            highlight_color = "red"
                            alpha_value = 180
                        # Nếu ăn quân khác, hiển thị màu cam
                        else:
                            highlight_color = "orange"
                            alpha_value = 170
                    # Nếu nước đi chiếu tướng (kiểm tra đặc biệt)
                    elif (move.endRow == enemy_king_pos[0] and move.endCol == enemy_king_pos[1]):
                        highlight_color = "purple"
                        alpha_value = 180
                    
                    # Tạo surface để highlight ô đích với màu được chọn
                    s = pygame.Surface((SQ_SIZE, SQ_SIZE))
                    s.set_alpha(alpha_value)
                    s.fill(pygame.Color(highlight_color))
                    screen.blit(s, (move.endCol * SQ_SIZE, move.endRow * SQ_SIZE))
                    
                    # Vẽ chấm tròn ở chính giữa ô
                    screen.blit(canmove, (move.endCol * SQ_SIZE + (SQ_SIZE - 15) // 2, 
                                          move.endRow * SQ_SIZE + (SQ_SIZE - 15) // 2))
            
            # Debug: In ra số lượng nước đi được highlight
            print(f"Highlighted {move_count} valid moves for {piece} at ({r}, {c})")

def drawGameState(screen, gs, validMoves, sqSelected):
    draw_Board(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    draw_Pieces(screen, gs.board)
    
    
    

def game_screen(play_with_ai=False):
    screen = Constants.screen
    screen.fill(Constants.BLACK)
    clock = pygame.time.Clock()
    
    # Khởi tạo game state
    gs = ChessChineseEngine.GameState()
    validMoves = gs.getValidMoves()  # Lấy các nước đi hợp lệ ban đầu
    moveMade = False
    running = True
    sqSelected = ()
    playerClicks = []
    gameOver = False
    
    # Xác định người chơi
    playerOne = True  # Người chơi quân đỏ
    playerTwo = not play_with_ai  # True nếu là người, False nếu là AI
    
    # Thêm biến để kiểm soát thời gian AI
    ai_thinking = False
    ai_move_time = 0
    
    while running:
        humanTurn = (gs.redToMove and playerOne) or (not gs.redToMove and playerTwo)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            
            elif event.type == pygame.MOUSEBUTTONDOWN and not gameOver:
                if humanTurn:  # Chỉ cho phép click khi đến lượt người chơi
                    location = pygame.mouse.get_pos()
                    col = int(location[0] // Constants.SQ_SIZE)
                    row = int(location[1] // Constants.SQ_SIZE)
                    
                    if 0 <= row < Constants.ROWS and 0 <= col < Constants.COLS:
                        # Nếu click vào ô đã chọn, hủy chọn
                        if sqSelected == (row, col):
                            sqSelected = ()
                            playerClicks = []
                        else:
                            sqSelected = (row, col)
                            playerClicks.append(sqSelected)
                            
                            # Xử lý click thứ hai
                            if len(playerClicks) == 2:
                                move = ChessChineseEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                                print(f"Try move: {move.getChessNotation()}")  # Debug
                                
                                # Kiểm tra nước đi hợp lệ
                                for validMove in validMoves:
                                    if move == validMove:
                                        print("Valid move found")  # Debug
                                        gs.makeMove(validMove)
                                        moveMade = True
                                        sqSelected = ()
                                        playerClicks = []
                                        break
                                
                                if not moveMade:
                                    print("Invalid move")  # Debug
                                    playerClicks = [sqSelected]
        
        # AI move
        if not gameOver and not humanTurn and play_with_ai:
            if not ai_thinking:
                ai_thinking = True
                ai_move_time = time.time()
            elif time.time() - ai_move_time > 0.5:  # Đợi 0.5 giây trước khi AI đi
                ai_move = AIEngine.findBestMove(gs, validMoves)
                if ai_move:
                    gs.makeMove(ai_move)
                    moveMade = True
                ai_thinking = False
        
        # Cập nhật danh sách nước đi hợp lệ nếu có nước đi mới
        if moveMade:
            validMoves = gs.getValidMoves()
            print(f"Number of valid moves: {len(validMoves)}")  # Debug
            moveMade = False
        
        drawGameState(screen, gs, validMoves, sqSelected)
        
        # Kiểm tra kết thúc game
        if gs.checkMate:
            gameOver = True
            if gs.redToMove:
                Win.win_screen(screen, "Đen thắng!")
            else:
                Win.win_screen(screen, "Đỏ thắng!")
        elif gs.staleMate:
            gameOver = True
            Win.win_screen(screen, "Hòa cờ!")
        
        clock.tick(60)
        pygame.display.flip() 
        
def drawText(screen, text):
    font = pygame.font.SysFont("Helvitca", 32, True, False)
    textObject = font.render(text, 0, pygame.Color("Black"))
    textLocation = pygame.Rect(0, 0, WIDTH, HEIGHT).move(
        WIDTH / 2 - textObject.get_width() / 2, HEIGHT / 2 - textObject.get_height() / 2
    )
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, pygame.Color("Black"))
    screen.blit(textObject, textLocation.move(2, 2))
            
