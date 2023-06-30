import pygame
from pygame import mixer
from fighter import Fighter
from background import Background
from data import *

mixer.init()
pygame.init()


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(GAME_NAME)


# set framerate
clock = pygame.time.Clock()
FPS = 60
last_count_update = pygame.time.get_ticks()


# load music and sounds
pygame.mixer.music.load("./assets/audio/bg.ogg")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1, 0.0, 5000)

# load spritesheets
boxer_sheet = pygame.image.load("./assets/images/boxer/boxer.png").convert_alpha()
omen_sheet = pygame.image.load("./assets/images/omen/omen.png").convert_alpha()
skull_sheet = pygame.image.load("./assets/images/omen/skull.png").convert_alpha()

# load icons
victory_img = pygame.image.load("./assets/images/icons/victory.png").convert_alpha()
icon = pygame.image.load("./assets/images/icons/icon.png").convert_alpha()
pygame.display.set_icon(icon)

# define font
menu_font_big = pygame.font.Font("./assets/fonts/turok.ttf", 75)
menu_font_small = pygame.font.Font("./assets/fonts/turok.ttf", 50)
count_font = pygame.font.Font("./assets/fonts/turok.ttf", 80)
score_font = pygame.font.Font("./assets/fonts/turok.ttf", 30)


# function for drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def draw_menu():
    if PAUSE_MENU:
        name_len = GAME_NAME.__len__()
        background_sprites.draw(screen)
        background_sprites.update()
        name_pos_x = SCREEN_WIDTH - ((name_len * 30) * 2)
        draw_text("PAUSE MENU !!!", menu_font_big, RED, name_pos_x, 60)
        draw_text("Press Enter to Resume", menu_font_small, GREEN, 250, 330)
    elif END_MENU:
        screen.fill((0, 0, 0))
        name_len = GAME_NAME.__len__()
        name_pos_x = SCREEN_WIDTH - ((name_len * 30) * 2)
        BOXER_DATA[1] = 3
        player.menu_character(screen)
        draw_text(
            "GAME OVER" if player.health == 0 else "Victory",
            menu_font_big,
            RED,
            340 if player.health == 0 else 400,
            60,
        )
    else:
        name_len = GAME_NAME.__len__()
        name_pos_x = SCREEN_WIDTH - ((name_len * 30) * 2)
        screen.fill((0, 0, 0))
        BOXER_DATA[1] = 3
        draw_text(GAME_NAME, menu_font_big, WHITE, name_pos_x, 60)
        draw_text("Press Enter to start", menu_font_small, RED, 250, 440)
        player.menu_character(screen)
    clock.tick(45)


# function for drawing fighter health bars
def draw_health_bar(health, x, y):
    ratio = health / 200
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 14))
    pygame.draw.rect(screen, RED, (x, y, 400, 12))
    pygame.draw.rect(screen, GREEN, (x, y, 400 * ratio, 12))


# create two instances of fighters
player = Fighter(1, 200, 310, False, BOXER_DATA, boxer_sheet, BOXER_ANIMATION_STEPS)
enemy = Fighter(2, 700, 310, True, OMEN_DATA, omen_sheet, OMEN_ANIMATION_STEPS)

background_sprites = pygame.sprite.Group()
background = Background()
background_sprites.add(background)


# game loop
run = True
while run:
    clock.tick(FPS)

    if MENU == True:
        # draw background
        draw_menu()
        key = pygame.key.get_pressed()
        if key[pygame.K_RETURN]:
            MENU = False
            round_over = False
        if END_MENU:
            if key[pygame.K_RETURN]:
                run = False
    else:
        background_sprites.draw(screen)
        background_sprites.update()

        # show player stats
        draw_health_bar(player.health, 20, 20)
        draw_health_bar(enemy.health, 580, 20)
        draw_text("Santhosh", score_font, WHITE, 20, 30)
        draw_text("Demon", score_font, WHITE, 910, 30)

        # update countdown
        if intro_count <= 0:
            # move fighters
            player.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, enemy, round_over)
            enemy.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, player, round_over)
            enemy.ai(player, round_over)
        else:
            # display count timer
            draw_text(
                str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3
            )
            # update count timer
            if (pygame.time.get_ticks() - last_count_update) >= 1000:
                intro_count -= 1
                last_count_update = pygame.time.get_ticks()

        # update fighters
        player.update(enemy)
        enemy.update(player)

        # draw fighters
        enemy.draw(screen)
        player.draw(screen)
        enemy.load_ranged_attack(screen, player, skull_sheet)

        if player.health == 0 or enemy.health == 0:
            round_over = True
            END_MENU = True

        if round_over == True:
            MENU = True
            END_MENU = True
            PAUSE_MENU = False

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    key = pygame.key.get_pressed()
    if key[pygame.K_ESCAPE]:
        MENU = True
        PAUSE_MENU = True

    # update display
    pygame.display.flip()

# exit pygame
pygame.quit()
