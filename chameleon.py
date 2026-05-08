import pygame
import pygame_gui
import random
import math

# screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


# initialize pygame window and surfaces
pygame.init()
pygame.display.set_caption("Chameleon")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


# define fonts
font = pygame.font.SysFont("Comic Sans MS", 26)
font_small = pygame.font.SysFont("Comic Sans MS", 22)
font_big = pygame.font.SysFont("Comic Sans MS", 40)
title_font = pygame.font.SysFont("Comic Sans MS", 72)


# load and scale images
forest_img = pygame.image.load("img/forest_bg.jpg").convert()
forest_img = pygame.transform.scale_by(forest_img, 0.6)

background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
background.blit(forest_img, (-10, -10))


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
lose_img = load_scale_img("img/lose.png")

# create mask for chameleon color
cham_mask = pygame.Surface(mask_img.get_size(), pygame.SRCALPHA)


# load sounds
pygame.mixer.init()

click_sfx = pygame.mixer.Sound("sfx/switch.wav")
ticking_sfx = pygame.mixer.Sound("sfx/ticking.ogg")



# initialize ui elements
manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), theme_path="gui_theme.json")


start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 480), (150, 75)),
                                             text='Play',
                                             manager=manager)

back_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((90, 480), (150, 75)),
                                             text='Back',
                                             manager=manager)
back_button.hide()

red_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((520, 475), (250, 25)), 
                                                    start_value= 88, value_range=(0, 255), 
                                                    manager=manager)

green_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((520, 510), (250, 25)), 
                                                    start_value= 138, value_range=(0, 255), 
                                                    manager=manager)

blue_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((520, 545), (250, 25)), 
                                                    start_value= 5, value_range=(0, 255), 
                                                    manager=manager)


# initialize static text
red_label = font.render("R", True, (255, 0, 0))
green_label = font.render("G", True, (0, 255, 0))
blue_label = font.render("B", True, (0, 0, 255))
title_label = title_font.render("RGB Chameleon", True, (255, 255, 0))
instruction_label = font_small.render("Use the sliders to blend into your surroundings\nbefore the timer runs out!", True, (255, 255, 255))


# random color
def randomize_color():
    random_red = random.randint(0, 255)
    random_green = random.randint(0, 255)
    random_blue = random.randint(0, 255)

    random_color = (random_red, random_green, random_blue)
    return random_color

# negative color for ui text while game is running
def negative_color(r, g, b):
    return (255-r, 255-g, 255-b)

screen_color = (0,0,0)
text_color = (255, 255, 255)


# countdown timer
def set_countdown(time_offset) -> int:
    current_time = pygame.time.get_ticks()
    return current_time + time_offset

def countdown_time_left(time) -> int:
    return time - pygame.time.get_ticks()
    
target_time = 0


# calculate score
score = 0
def calculate_score(rand_r, rand_g, rand_b, r, g, b):
    delta_r = abs(rand_r - r)
    delta_g = abs(rand_g - g)
    delta_b = abs(rand_b - b)
    return max(math.ceil((300 - (delta_r + delta_g + delta_b)) / 3), 0)

clock = pygame.time.Clock()
running = True
game_active = False
timer_running = False

while running:
    delta_time = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame_gui.UI_BUTTON_PRESSED:

            if event.ui_element == start_button:
                click_sfx.set_volume(0.5)
                click_sfx.play()
                ticking_sfx.set_volume(0.5)
                ticking_sfx.play()
                target_time = set_countdown(10000)
                timer_running = True
                screen_color = randomize_color()
                text_color = negative_color(screen_color[0], screen_color[1], screen_color[2])
                game_active = True

            if event.ui_element == back_button:
                click_sfx.set_volume(0.5)
                click_sfx.play()
                game_active = False
                
        
        manager.process_events(event)

    manager.update(delta_time)

    cham_r = red_slider.get_current_value()
    cham_g = green_slider.get_current_value()
    cham_b = blue_slider.get_current_value()

    chameleon_color = (cham_r,cham_g,cham_b)

    # GAME LOOP

    # render only in active game
    if game_active:
        screen.fill(screen_color)
        time_left = 0.0

        if timer_running:
            time_left = round((countdown_time_left(target_time) / 1000.0), 1)
            start_button.hide()
            back_button.hide()
            score = calculate_score(screen_color[0], screen_color[1],
                                screen_color[2], cham_r, cham_g, cham_b)
            
        else:
            ticking_sfx.stop()
            start_button.show()
            back_button.show()
            score_label = font_big.render(f"You've got {score} points!", True, text_color)
            screen.blit(score_label, (200, 80))

        time_label = font_big.render(f"Time: {time_left}", True, text_color)
        screen.blit(time_label,(220, 10))
        if countdown_time_left(target_time) <= 0:
            timer_running = False

    # render only in main menu
    else:
        back_button.hide()
        screen.blit(background, (0,0))
        screen.blit(title_label, (100, 10))
        screen.blit(instruction_label, (110, 110))


    # draw color labels
    screen.blit(red_label, (490, 465))
    screen.blit(green_label, (490, 500))
    screen.blit(blue_label, (490, 535))

    # render chameleon
    screen.blit(twig_img, (-10, 200))

    # render user color
    cham_mask.fill(chameleon_color)
    cham_mask.blit(mask_img, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
    screen.blit(cham_mask, (-10, 200))

    screen.blit(stripes_img, (-10, 200))

    # chameleon mood
    if not game_active:
        screen.blit(happy_img, (-10, 200))
    elif game_active and timer_running:
        screen.blit(sad_img, (-10, 200))
    elif game_active and not timer_running:
        if score > 60:
            screen.blit(happy_img, (-10, 200))
        else:
            screen.blit(lose_img, (-10, 200))
    
    manager.draw_ui(screen)


    pygame.display.update()



pygame.quit()