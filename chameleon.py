import pygame
import pygame_gui
import random

# screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


# initialize pygame window and surfaces
pygame.init()
pygame.display.set_caption("Chameleon")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
font = pygame.font.SysFont("Comic Sans MS", 26)
title_font = pygame.font.SysFont("Comic Sans MS", 72)


# load and scale images
forest_img = pygame.image.load("img/forest_bg.jpg").convert()
forest_img = pygame.transform.scale_by(forest_img, 0.6)


def load_scale_img(path):
    scale = 0.6
    img = pygame.image.load(path).convert_alpha()
    img = pygame.transform.scale_by(img, scale)
    return img

twig_img = load_scale_img("img/twig.png")
stripes_img = load_scale_img("img/stripes.png")
mask_img = load_scale_img("img/mask.png")
sad_img = load_scale_img("img/sad.png")
happy_img = load_scale_img("img/happy.png")



background.blit(forest_img, (-10, -10))

# initialize ui elements
manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), theme_path="gui_theme.json")


start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 480), (150, 75)),
                                             text='Start Game',
                                             manager=manager)

red_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((520, 475), (250, 25)), 
                                                    start_value= 88, value_range=(0, 255), 
                                                    manager=manager)

green_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((520, 510), (250, 25)), 
                                                    start_value= 138, value_range=(0, 255), 
                                                    manager=manager)

blue_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((520, 545), (250, 25)), 
                                                    start_value= 5, value_range=(0, 255), 
                                                    manager=manager)


# initialize text
red_label = font.render("R", True, (255, 0, 0))

green_label = font.render("G", True, (0, 255, 0))

blue_label = font.render("B", True, (0, 0, 255))

title_label = title_font.render("RGB Chameleon", True, (255, 255, 0))


# random color
random_red = random.randint(0, 255)
random_green = random.randint(0, 255)
random_blue = random.randint(0, 255)

random_color = (random_red, random_green, random_blue)

# create mask for chameleon color
cham_mask = pygame.Surface(mask_img.get_size(), pygame.SRCALPHA)

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
                if not game_active:
                    print("startgame")
                    game_active = True
                else:
                    print("gamefinished")
                    game_active = False

        manager.process_events(event)

    manager.update(delta_time)

    cham_r = red_slider.get_current_value()
    cham_g = green_slider.get_current_value()
    cham_b = blue_slider.get_current_value()

    chameleon_color = (cham_r,cham_g,cham_b)

    # game loop
    if game_active:
        screen.fill(random_color)
    else:
        screen.blit(background, (0,0))
        screen.blit(title_label, (100, 50))



    # draw color labels
    screen.blit(red_label, (490, 465))
    screen.blit(green_label, (490, 500))
    screen.blit(blue_label, (490, 535))


    screen.blit(twig_img, (-10, 200))

    cham_mask.fill(chameleon_color)
    cham_mask.blit(mask_img, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
    screen.blit(cham_mask, (-10, 200))

    screen.blit(stripes_img, (-10, 200))
    screen.blit(happy_img, (-10, 200))
    
    manager.draw_ui(screen)


    pygame.display.update()



pygame.quit()