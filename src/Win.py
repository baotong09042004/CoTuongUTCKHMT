import pygame
import sys
import Constants
import Menu
def draw_win_screen(screen, end_text):
    bg= pygame.Rect(200, 200, 300, 300)
    pygame.draw.rect(screen, Constants.YELLOW, bg)
    
    # Thông báo chiến thắng
    win_text = Constants.font.render(end_text, True, Constants.BLACK)
    screen.blit(win_text, (250, 250))
    # Nút Quay lại và Chơi lại
    button_back = pygame.Rect(260, 410, 150, 35)
    pygame.draw.rect(screen, Constants.RED, button_back)

    back_text = Constants.font.render("Quay lại", True, Constants.BLACK)
    screen.blit(back_text, (button_back.x +10, button_back.y -8))
    
    return button_back

def win_screen(screen, end_text):
    while True:
        button_back= draw_win_screen(screen, end_text)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if button_back.collidepoint(mouse_pos):
                    Menu.menu_screen()
                    return
                
        pygame.display.flip()

