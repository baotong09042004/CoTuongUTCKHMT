import os
import pygame
import sys
pygame.init()

# Kích thước cửa sổ
WIDTH=1100 # chiều rộng
HEIGHT=770 # chiều cao
# Kích thước bàn cờ
WIDTH_BOARD= 693 # chiều rộng bàn cờ
HEIGHT_BOARD= 770 # chiều cao bàn cờ
MARGIN= 38.5 # khoảng cách lề trái & trên 
ROWS, COLS = 10, 9 # số hàng và cột của bàn cờ
SQ_SIZE=(HEIGHT_BOARD - 2 * MARGIN) // (ROWS-1) # kích thước ô vuông của bàn cờ
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cờ Tướng Offline")

# Màu sắc
WHITE = (255, 255, 255)
YELLOW = (255, 255, 204)
BLACK = (0, 0, 0)
BLUE = (0, 191, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)  # Màu xanh lá cho các nước đi hợp lệ
HIGHLIGHT = (0, 255, 0, 100)  # Màu xanh lá nhạt cho ô được chọn

# Đường dẫn tuyệt đối tới file Constants.py
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Đi lên 2 cấp để tới thư mục "chinese game"
BASE_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))

# Đường dẫn tới thư mục assets/font
ASSETS_PATH = os.path.join(BASE_DIR, 'assets')
FONT_PATH = os.path.join(ASSETS_PATH, 'font', 'Roboto-Regular.ttf')
font = pygame.font.Font(FONT_PATH, 36)
