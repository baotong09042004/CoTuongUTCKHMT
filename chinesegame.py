import pygame

# Khởi tạo pygame
pygame.init()

# Kích thước cửa sổ
WIDTH, HEIGHT = 750, 850
SQUARE_SIZE = 70
ROWS, COLS = 10, 9
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cờ Tướng")

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 50, 50)
HIGHLIGHT = (0, 255, 0)

# Hình ảnh quân cờ
piece_images = {
    "xe_r": pygame.image.load("chinese game/img/Red/xe_R.png"),
    "xe_b": pygame.image.load("chinese game/img/Black/xe_B.png"),
    "phao_r": pygame.image.load("chinese game/img/Red/phao_R.png"),
    "phao_b": pygame.image.load("chinese game/img/Black/Phao_B.png"),
    "si_r": pygame.image.load("chinese game/img/Red/si_R.png"),
    "si_b": pygame.image.load("chinese game/img/Black/si_B.png"),
    "ma_r": pygame.image.load("chinese game/img/Red/ma_R.png"),
    "ma_b": pygame.image.load("chinese game/img/Black/ma_B.png"),
    "tuong_r": pygame.image.load("chinese game/img/Red/tuong_R.png"),
    "tuong_b": pygame.image.load("chinese game/img/Black/tuong_B.png"),
    "tot_r": pygame.image.load("chinese game/img/Red/tot_R.png"),
    "tot_b": pygame.image.load("chinese game/img/Black/tot_B.png"),
    "king_r": pygame.image.load("chinese game/img/Red/king_R.png"),
    "king_b": pygame.image.load("chinese game/img/Black/king_B.png"),

}


# Lớp quân cờ
class Piece:
    def __init__(self, row, col, color, name):
        self.row = row
        self.col = col
        self.color = color
        self.name = name
        self.x = col * SQUARE_SIZE
        self.y = row * SQUARE_SIZE

    def draw(self, screen):
        if self.name in piece_images:
            img = pygame.transform.scale(piece_images[self.name], (SQUARE_SIZE, SQUARE_SIZE))
            screen.blit(img, (self.x, self.y))

    def get_valid_moves(self, board):
        moves = []
        row, col = self.row, self.col

        if "tot" in self.name:  # Quân tốt
            direction = -1 if self.color == "red" else 1
            new_row = row + direction
            if 0 <= new_row < 10:
                moves.append((new_row, col))
            # Nếu đã qua sông, có thể đi ngang
            if (self.color == "red" and row <= 4) or (self.color == "black" and row >= 5):
                if col - 1 >= 0:
                    moves.append((row, col - 1))
                if col + 1 < 9:
                    moves.append((row, col + 1))

        elif "ma" in self.name:  # Quân mã
            candidates = [(row - 2, col - 1), (row - 2, col + 1),
                        (row + 2, col - 1), (row + 2, col + 1),
                        (row - 1, col - 2), (row - 1, col + 2),
                        (row + 1, col - 2), (row + 1, col + 2)]
            for r, c in candidates:
                if 0 <= r < 10 and 0 <= c < 9:
                    moves.append((r, c))

        elif "xe" in self.name:  # Quân xe
            for i in range(row + 1, 10):
                moves.append((i, col))
                if board.grid[i][col]:  # Nếu gặp quân cờ, dừng lại
                    break
            for i in range(row - 1, -1, -1):
                moves.append((i, col))
                if board.grid[i][col]:
                    break
            for i in range(col + 1, 9):
                moves.append((row, i))
                if board.grid[row][i]:
                    break
            for i in range(col - 1, -1, -1):
                moves.append((row, i))
                if board.grid[row][i]:
                    break

        elif "tuong" in self.name:  # Quân tượng
            candidates = [(row - 2, col - 2), (row - 2, col + 2),
                        (row + 2, col - 2), (row + 2, col + 2)]
            for r, c in candidates:
                if 0 <= r < 10 and 0 <= c < 9:
                    moves.append((r, c))

        elif "si" in self.name:  # Quân sĩ
            candidates = [(row - 1, col - 1), (row - 1, col + 1),
                        (row + 1, col - 1), (row + 1, col + 1)]
            for r, c in candidates:
                if 3 <= r <= 5 and (c in [3, 4, 5]):  # Phạm vi cung
                    moves.append((r, c))

        elif "king" in self.name:  # Quân tướng
            candidates = [(row - 1, col), (row + 1, col),
                        (row, col - 1), (row, col + 1)]
            for r, c in candidates:
                if 3 <= r <= 5 and (c in [3, 4, 5]):  # Phạm vi cung
                    moves.append((r, c))

        elif "phao" in self.name:  # Quân pháo
            # Di chuyển như xe
            for i in range(row + 1, 10):
                moves.append((i, col))
                if board.grid[i][col]: break
            for i in range(row - 1, -1, -1):
                moves.append((i, col))
                if board.grid[i][col]: break
            for i in range(col + 1, 9):
                moves.append((row, i))
                if board.grid[row][i]: break
            for i in range(col - 1, -1, -1):
                moves.append((row, i))
                if board.grid[row][i]: break

        return moves


# Lớp bàn cờ
class Board:
    def __init__(self):
        self.grid = [[None] * COLS for _ in range(ROWS)]
        self.init_pieces()

    def init_pieces(self):
        """ Khởi tạo vị trí quân cờ ban đầu """
        # Xe
        self.grid[0][0] = Piece(0, 0, "red", "xe_r")
        self.grid[0][8] = Piece(0, 8, "red", "xe_r")
        self.grid[9][0] = Piece(9, 0, "black", "xe_b")
        self.grid[9][8] = Piece(9, 8, "black", "xe_b")

        # Mã
        self.grid[0][1] = Piece(0, 1, "red", "ma_r")
        self.grid[0][7] = Piece(0, 7, "red", "ma_r")
        self.grid[9][1] = Piece(9, 1, "black", "ma_b")
        self.grid[9][7] = Piece(9, 7, "black", "ma_b")

        # Tượng
        self.grid[0][2] = Piece(0, 2, "red", "tuong_r")
        self.grid[0][6] = Piece(0, 6, "red", "tuong_r")
        self.grid[9][2] = Piece(9, 2, "black", "tuong_b")
        self.grid[9][6] = Piece(9, 6, "black", "tuong_b")

        # Sĩ
        self.grid[0][3] = Piece(0, 3, "red", "si_r")
        self.grid[0][5] = Piece(0, 5, "red", "si_r")
        self.grid[9][3] = Piece(9, 3, "black", "si_b")
        self.grid[9][5] = Piece(9, 5, "black", "si_b")

        # Tướng
        self.grid[0][4] = Piece(0, 4, "red", "king_r")
        self.grid[9][4] = Piece(9, 4, "black", "king_b")

        # Pháo
        self.grid[2][1] = Piece(2, 1, "red", "phao_r")
        self.grid[2][7] = Piece(2, 7, "red", "phao_r")
        self.grid[7][1] = Piece(7, 1, "black", "phao_b")
        self.grid[7][7] = Piece(7, 7, "black", "phao_b")

        # Tốt
        for i in range(0, 9, 2):
            self.grid[3][i] = Piece(3, i, "red", "tot_r")
            self.grid[6][i] = Piece(6, i, "black", "tot_b")

    def draw(self, screen):
        for row in range(ROWS):
            for col in range(COLS):
                rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(screen, WHITE, rect, 1)

        for row in range(ROWS):
            for col in range(COLS):
                piece = self.grid[row][col]
                if piece:
                    piece.draw(screen)

# Lớp Game
class Game:
    def __init__(self):
        self.board = Board()
        self.selected_piece = None
        self.turn = "red"  # Bắt đầu với quân đỏ

    def draw(self): # Vẽ bàn cờ và quân cờ
        self.board.draw(screen)
        if self.selected_piece:
            moves = self.selected_piece.get_valid_moves(self.board)
            for move in moves:
                pygame.draw.circle(screen, HIGHLIGHT, 
                                   (move[1] * SQUARE_SIZE + SQUARE_SIZE // 2, move[0] * SQUARE_SIZE + SQUARE_SIZE // 2), 
                                   10)

    def select_piece(self, row, col):
        piece = self.board.grid[row][col]
        
        # Chỉ được chọn quân của mình theo lượt chơi
        if piece and piece.color == self.turn:
            self.selected_piece = piece
        elif self.selected_piece:
            self.move_piece(row, col)

    def move_piece(self, row, col):
        if self.selected_piece:
            moves = self.selected_piece.get_valid_moves(self.board)
            if (row, col) in moves:
                old_row, old_col = self.selected_piece.row, self.selected_piece.col
                
                # Nếu có quân cờ đối phương, ăn nó
                if self.board.grid[row][col] and self.board.grid[row][col].color != self.selected_piece.color:
                    self.board.grid[row][col] = None  
                
                # Cập nhật vị trí quân cờ
                self.board.grid[old_row][old_col] = None
                self.selected_piece.row, self.selected_piece.col = row, col
                self.selected_piece.x = col * SQUARE_SIZE  
                self.selected_piece.y = row * SQUARE_SIZE  
                self.board.grid[row][col] = self.selected_piece

                # Chuyển lượt chơi
                self.turn = "black" if self.turn == "red" else "red"

            # Đặt lại quân cờ được chọn
            self.selected_piece = None  

# Chạy game
def main():
    clock = pygame.time.Clock()
    game = Game()
    running = True

    while running:
        screen.fill(BLACK)
        game.draw()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                row, col = y // SQUARE_SIZE, x // SQUARE_SIZE
                game.select_piece(row, col)

        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
