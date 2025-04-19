import pygame
import sys
import Constants

def draw_win_screen():
    Constants.screen.fill(Constants.YELLOW)
    
    # Thông báo chiến thắng
    win_text = Constants.font.render("YOU WIN!", True, Constants.BLACK)
    Constants.screen.blit(win_text, (350, 200))
    
    # Nút Quay lại và Chơi lại
    button_back = pygame.Rect(300, 300, 100, 40)
    button_replay = pygame.Rect(400, 300, 100, 40)
    pygame.draw.rect(Constants.screen, Constants.BLUE, button_back)
    pygame.draw.rect(Constants.screen, Constants.BLUE, button_replay)
    
    back_text = Constants.font.render("Quay lại", True, Constants.BLACK)
    replay_text = Constants.font.render("Chơi lại", True, Constants.BLACK)
    Constants.screen.blit(back_text, (310, 305))
    Constants.screen.blit(replay_text, (410, 305))
    
    return button_back, button_replay

def win_screen():
    while True:
        button_back, button_replay = draw_win_screen()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if button_back.collidepoint(mouse_pos):
                    return "menu"
                elif button_replay.collidepoint(mouse_pos):
                    return "replay"
        
        pygame.display.flip()