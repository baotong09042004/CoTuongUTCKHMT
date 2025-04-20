import pygame
import sys
import Constants 
import Button
import Guide
import GameMain
BG = pygame.transform.smoothscale(
    pygame.image.load("assets/img/bgmanhinhchinh.png"),
    (Constants.WIDTH, Constants.HEIGHT),
)
SCREEN=Constants.screen
AI = None

def draw_menu():
    
    button_play_ai = Button.Button(
            image=None,
            pos=(Constants.WIDTH * 0.5, Constants.HEIGHT * 0.6),
            text_input="Chơi với máy",
            font=Constants.font,  
            base_color="#000000",
            hovering_color="Yellow",
    )
    
    button_play_pvp = Button.Button(
        image=None,  
        pos=(Constants.WIDTH * 0.5, Constants.HEIGHT * 0.45),
        text_input="Hai người chơi",
        font=Constants.font,        
        base_color="#000000",
        hovering_color="Yellow",
    )
    button_guide = Button.Button(
        image=None,  # image=pygame.image.load("assets/menu/PvE.png"),
        pos=(Constants.WIDTH * 0.5, Constants.HEIGHT * 0.75),
        text_input="Luật chơi",
        font=Constants.font,
        base_color="#000000",
        hovering_color="Yellow",
    )
    # Vẽ các nút   

    return button_play_ai, button_play_pvp, button_guide

# Vòng lặp chính cho menu
def menu_screen():
    SCREEN.blit(BG, (0, 0))

    while True:

        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        button_play_ai, button_play_pvp, button_guide = draw_menu()

        for button in [button_play_ai, button_play_pvp, button_guide]:
            button.changeColor(PLAY_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos 
                if button_play_ai.checkForInput(PLAY_MOUSE_POS):
                    GameMain.game_screen(play_with_ai=True)
                elif button_play_pvp.checkForInput(PLAY_MOUSE_POS):
                    GameMain.game_screen(play_with_ai=False)
                elif button_guide.checkForInput(mouse_pos):
                    Guide.guide_screen()
                    
        pygame.display.update()
    