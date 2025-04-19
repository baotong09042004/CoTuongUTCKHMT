import pygame
import sys
import Constants 
import Button
import Menu

BG = pygame.transform.smoothscale(
    pygame.image.load("assets/img/bgmanhinhchinh.png"),
    (Constants.WIDTH, Constants.HEIGHT),
)

luatChoi = pygame.transform.smoothscale(
    pygame.image.load("assets/img/luatchoi.jpg"),
    (int(Constants.WIDTH * 0.8), int(Constants.HEIGHT * 0.8)),
)
musicon= pygame.image.load("assets/img/musicon.png")
musicoff= pygame.image.load("assets/img/musicoff.png")
tatHuongDan= pygame.image.load("assets/img/daux.png")
def guide_screen():
    Constants.screen.blit(BG, (0, 0))
    Constants.screen.blit(luatChoi, (Constants.WIDTH*0.1, Constants.HEIGHT*0.1))
    
    button_back = Button.Button(
        image=tatHuongDan,
        pos=(Constants.WIDTH * 0.9, Constants.HEIGHT * 0.11),
        text_input="",  # hoặc dòng chữ bạn muốn hiển thị
        font=Constants.font,  # font pygame đã khởi tạo từ trước
        base_color=(255, 255, 255),  # màu cơ bản
        hovering_color=(200, 200, 200),  # màu khi hover
    )
    
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        
        button_back.changeColor(PLAY_MOUSE_POS)
        button_back.update(Constants.screen)
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_back.checkForInput(PLAY_MOUSE_POS):
                    Menu.menu_screen()
        pygame.display.flip()
