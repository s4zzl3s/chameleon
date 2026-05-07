import pygame
import pygame_gui
import random

# screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


# initialize pygame and window
pygame.init()
pygame.display.set_caption("Chameleon")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

# load images
forest_img = pygame.image.load("img/forest_bg.jpg").convert()
forest_img = pygame.transform.scale_by(forest_img, 0.6)


background.blit(forest_img, (-10, -10))

# initialize ui elements
manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), theme_path="gui_theme.json")


start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 475), (100, 50)),
                                             text='Start',
                                             manager=manager)

red_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((300, 275), (200, 25)), 
                                                    start_value= 88, value_range=(0, 255), 
                                                    manager=manager)

green_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((300, 325), (200, 25)), 
                                                    start_value= 138, value_range=(0, 255), 
                                                    manager=manager)

blue_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((300, 375), (200, 25)), 
                                                    start_value= 5, value_range=(0, 255), 
                                                    manager=manager)


# random color
random_red = random.randint(0, 255)
random_green = random.randint(0, 255)
random_blue = random.randint(0, 255)

clock = pygame.time.Clock()
running = True
game_active = False

while running:
    delta_time = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == start_button:
                print("startgame")
                game_active = True




        manager.process_events(event)

    manager.update(delta_time)
    cham_r = red_slider.get_current_value()
    cham_g = green_slider.get_current_value()
    cham_b = blue_slider.get_current_value()

    chameleon_color = (cham_r,cham_g,cham_b)

        
    screen.blit(background, (0,0))
    manager.draw_ui(screen)


    pygame.display.update()



pygame.quit()