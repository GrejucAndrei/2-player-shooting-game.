
import pygame
import os # Helps with paths no matter what operating system the user has
pygame.init()
pygame.font.init() # initializes fonts
pygame.mixer.init() # initializes the sound / sound effects library

WIDTH = 900
HEIGHT = 500

WIN = pygame.display.set_mode((WIDTH, HEIGHT)) # Makes a window with the specified width and height
pygame.display.set_caption("~Sh00ter~") # Sets the window title, caption

HEALTH_FONT = pygame.font.SysFont('constantia', 40)
WINNER_FONT = pygame.font.SysFont('constantia', 100)


CYAN = (153, 187, 255)
DARK_BLUE = (0, 23, 204)
DARK_RED = (127,0,0)
WHITE = (255, 255, 255)

PLAYER_WIDTH, PLAYER_HEIGHT = 45, 85
BULLET_WIDTH, BULLET_HEIGHT = 25, 10

FPS = 60 # Frames per second
VELOCITY = 5

red_bullets = []
blue_bullets = []
MAX_BULLETS = 3 # Max bullets on the screen of one player
BULLET_SPEED = 7

BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Bullet_Fire.mp3"))
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Bullet_Hit.wav"))
VICTORY_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Victory.mp3"))

RED_HIT = pygame.USEREVENT + 1
BLUE_HIT = pygame.USEREVENT + 2

RED_BORDER = pygame.Rect(WIDTH//2 - 2.5, 0, 5,HEIGHT ) # A rectangle positioned in the center of the window that acts like                                          # an unpassable border
BLUE_BORDER = pygame.Rect(WIDTH//2 + 2.5, 0, 5, HEIGHT)

PLAYER_1_IMAGE = pygame.image.load(os.path.join("Assets", "Player_1.png")) # Player 1 image
PLAYER_1 = pygame.transform.scale(PLAYER_1_IMAGE, (PLAYER_WIDTH,PLAYER_HEIGHT)) # Scales down the player

PLAYER_2_IMAGE = pygame.image.load(os.path.join("Assets", "Player_2.png")) # Player 2 image
PLAYER_2 = pygame.transform.scale(PLAYER_2_IMAGE, (PLAYER_WIDTH,PLAYER_HEIGHT))


RIGHT_BULLET_IMAGE = pygame.image.load(os.path.join("Assets", "Red_Bullet.png")) # Bullet going to the right
RIGHT_BULLET = pygame.transform.scale(RIGHT_BULLET_IMAGE, (BULLET_WIDTH,BULLET_HEIGHT))

LEFT_BULLET_IMAGE = pygame.image.load(os.path.join("Assets", "Blue_Bullet.png")) # Bullet going to the left
LEFT_BULLET = pygame.transform.rotate((pygame.transform.scale(LEFT_BULLET_IMAGE, (BULLET_WIDTH, BULLET_HEIGHT))), 180)

BACKGROUND_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "Background_Image.jpg")), (WIDTH, HEIGHT))
pygame.display.set_icon(RIGHT_BULLET_IMAGE)




def red_movement_handler(keys_pressed, red): # Handles movement but also assures that players can't move off the window
                                             # or past the border
    if keys_pressed[pygame.K_a] and red.x - VELOCITY > 0:
        red.x -= VELOCITY
    if keys_pressed[pygame.K_d] and red.x + VELOCITY + red.width < RED_BORDER.x :
        red.x += VELOCITY
    if keys_pressed[pygame.K_w] and red.y + VELOCITY > 0:
        red.y -= VELOCITY
    if keys_pressed[pygame.K_s] and red.y + VELOCITY + red.height < HEIGHT:
        red.y += VELOCITY


def blue_movement_handler(keys_pressed, blue):
    if keys_pressed[pygame.K_LEFT] and blue.x - VELOCITY > BLUE_BORDER.x:
        blue.x -= VELOCITY
    if keys_pressed[pygame.K_RIGHT] and blue.x + VELOCITY + blue.width < WIDTH:
        blue.x += VELOCITY
    if keys_pressed[pygame.K_UP] and blue.y + VELOCITY > 0:
        blue.y -= VELOCITY
    if keys_pressed[pygame.K_DOWN] and blue.y + VELOCITY + blue.height < HEIGHT:
        blue.y += VELOCITY


def bullet_handler(red_bullets, blue_bullets, red, blue):
    for bullet in blue_bullets:
        red_collider = pygame.Rect.colliderect(red, bullet)
        bullet.x -= BULLET_SPEED
        if red_collider == True:
            blue_bullets.remove(bullet)
            pygame.event.post(pygame.event.Event(RED_HIT))
        if bullet.x < 0:
            blue_bullets.remove(bullet)

    for bullet in red_bullets:
        blue_collider = pygame.Rect.colliderect(blue, bullet)
        bullet.x += BULLET_SPEED
        if blue_collider == True:
            pygame.event.post(pygame.event.Event(BLUE_HIT))
            red_bullets.remove(bullet)
        if bullet.x > WIDTH:
            red_bullets.remove(bullet)


def draw_display(red,blue, red_bullets, blue_bullets, red_hp, blue_hp): #
    WIN.blit(BACKGROUND_IMAGE, (0,0))
    pygame.draw.rect(WIN, DARK_RED, RED_BORDER) # Draws the border on the window with a dark blue color
    pygame.draw.rect(WIN, DARK_BLUE, BLUE_BORDER)

    for bullet in red_bullets:
        WIN.blit(RIGHT_BULLET, (bullet.x, bullet.y))
    for bullet in blue_bullets:
        WIN.blit(LEFT_BULLET, (bullet.x, bullet.y))

    red_hp_text = HEALTH_FONT.render("Health : " + str(red_hp), True, DARK_RED)
    blue_hp_text = HEALTH_FONT.render("Health : " + str(blue_hp), True, DARK_BLUE)

    WIN.blit(red_hp_text, (10,10))
    WIN.blit(blue_hp_text, (WIDTH-blue_hp_text.get_width()-10, 10))

    WIN.blit(PLAYER_1, (red.x, red.y))
    WIN.blit(PLAYER_2, (blue.x, blue.y))

    pygame.display.update()  # Updates the display so that the most recent changes get displayed

def draw_winner(text):
        red_text = WINNER_FONT.render(text, True, WHITE)
        WIN.blit(red_text, (WIDTH/2 - red_text.get_width()/2, HEIGHT/2 - red_text.get_height()/2))
        pygame.display.update()
        VICTORY_SOUND.play()
        pygame.time.wait(4000)


def main_loop(): # Main game loop. This will redraw, check for events or collisions etc.
    blue_bullets = []
    red_bullets = []
    red = pygame.Rect(20, 200, PLAYER_WIDTH, PLAYER_HEIGHT)
    blue = pygame.Rect(835, 200, PLAYER_WIDTH, PLAYER_HEIGHT) # Draws an invisible rectangle onto our blue player
    # When we control one of this rectangle, the player assigned to it will also move.

    red_hp = 10
    blue_hp = 10

    run = True #
    clock = pygame.time.Clock()

    while run:
        clock.tick(FPS) # Runs this while loop ONLY 60 times per second.
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Checks if the user quit the window ( Presses X )
                run = False # If the user quit the window then this will break us out of the while loop and close the game
                pygame.quit()  # Closes the game
            if event.type == pygame.KEYDOWN:

                # Red bullets
                if event.key == pygame.K_LCTRL and len(red_bullets) < MAX_BULLETS :
                    bullet_rectangle = pygame.Rect(red.x + red.width - 25, red.y + red.height//2 - 18, BULLET_WIDTH,BULLET_HEIGHT)
                    red_bullets.append(bullet_rectangle)
                    BULLET_FIRE_SOUND.play()

                # Blue bullets
                if event.key == pygame.K_RCTRL and len(blue_bullets) < MAX_BULLETS :
                    bullet_rectangle = pygame.Rect(blue.x - blue.width + 30, blue.y + blue.height//2 - 16, BULLET_WIDTH, BULLET_HEIGHT)
                    blue_bullets.append(bullet_rectangle)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_hp -= 1
                BULLET_HIT_SOUND.play()
            if event.type == BLUE_HIT:
                blue_hp -= 1
                BULLET_HIT_SOUND.play()

        if red_hp <= 0:
            draw_winner("~~ BLUE WINS! ~~")
            break
        if blue_hp <= 0:
            draw_winner("~~ RED WINS! ~~")
            break

        keys_pressed = pygame.key.get_pressed() # Logs all the keys the user presses

        red_movement_handler(keys_pressed, red)
        blue_movement_handler(keys_pressed, blue)
        bullet_handler(red_bullets, blue_bullets, red, blue)

        draw_display(red, blue, red_bullets, blue_bullets, red_hp,blue_hp)

    main_loop()


if __name__ == "__main__": # This makes sure that we will run the game only if it's opened directly, and not imported.
    main_loop()

