import pygame
import random
import math

pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('upc.png')
pygame.display.set_icon(icon)

# Load images
background = pygame.image.load('background.jpg')
player_image = pygame.image.load('astronave.png')
enemy_image = pygame.image.load('alien.png')
bullet_image = pygame.image.load('bala.png')
enemy_image_small = pygame.transform.scale(enemy_image,(16,16))

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.x = 370
        self.rect.y = 480
        self.x_change = 0

        # Dictionary to track key states
        self.keys = {'left': False, 'right': False}

    def update(self):

        # Adjust x_change based on key states
        if self.keys['left']:
            self.x_change = -5
        elif self.keys['right']:
            self.x_change = 5
        else:
            self.x_change = 0
        
        self.rect.x += self.x_change
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > SCREEN_WIDTH - 64:
            self.rect.x = SCREEN_WIDTH - 64

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = enemy_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x_change = 4
        self.y_change = 40

    def update(self):
        self.rect.x += self.x_change
        if self.rect.x <= 0 or self.rect.x >= SCREEN_WIDTH - 64:
            self.x_change = -self.x_change
            self.rect.y += self.y_change

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.y -= 5  # Adjusted speed for better visibility


def init(num_of_enemies):

    # Initialize player
    player = Player()

    # Initialize enemies using sprite group
    all_enemies = pygame.sprite.Group()
    enemies_remaining = num_of_enemies  # Track the number of enemies remaining

    for _ in range(num_of_enemies):
        enemy = Enemy(random.randint(0, SCREEN_WIDTH - 64), random.randint(50, 150))
        all_enemies.add(enemy)

    # Initialize bullets using sprite group
    all_bullets = pygame.sprite.Group()

    # Score variables
    score = 0
    
    selected_option = 0

    running = True
    end_game = False
    win_game = True
    menu = False

    options = ['Resume','Restart', 'Quit']

    return (
        player,
        all_enemies,
        enemies_remaining,
        all_bullets,
        score,
        selected_option,
        running,
        end_game,
        win_game,
        menu,
        options
    )

def draw_menu():
    screen.blit(background, (0, 0))

    # Calculate total height of all options
    total_height = len(options) * 50

    # Calculate starting y-coordinate to center the text vertically
    start_y = (SCREEN_HEIGHT - total_height) // 2 + 25
    
    for i, option in enumerate(options):
        text = menu_font.render(option, True, white if i != selected_option else highlight_color)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, start_y + i * 50))
        screen.blit(text, text_rect)

def show_bullets_left(x, y):
    for i in range(max_bullets - len(all_bullets)):
            screen.blit(bullet_image, (bullet_x + i * 30, bullet_y))

def show_enemies_killed(x, y):
    for i in range(num_of_enemies - len(all_enemies)):
            screen.blit(enemy_image_small, (x - i * 30, y))

def show_game_over(winner=False):
    if winner:
        over_text = over_font.render("YOU WIN!", True, (255, 255, 255))
        over_text_rect = over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    else:
        over_text = over_font.render("GAME OVER", True, (255, 255, 255))
        over_text_rect = over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    screen.blit(over_text, over_text_rect)
    
    sub_text = font.render("Press 'Esc'", True, (255, 255, 255))
    sub_text_rect = sub_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    
    screen.blit(sub_text, sub_text_rect)

# Main game loop
clock = pygame.time.Clock()
FPS = 60

num_of_enemies = 6
max_bullets = 6

menu_font = pygame.font.Font('freesansbold.ttf', 32)
font = pygame.font.Font('freesansbold.ttf', 24)

# Bullets left start position
bullet_x = 10
bullet_y = SCREEN_HEIGHT - 30

# Enemies left start position
enemy_x = SCREEN_WIDTH - 30
enemy_y = SCREEN_HEIGHT - 30 

# Game over font
over_font = pygame.font.Font('freesansbold.ttf', 64)

white = (255, 255, 255)
black = (0, 0, 0)
highlight_color = (255, 0, 0)

player, all_enemies, enemies_remaining, all_bullets, score, selected_option, running, end_game, win_game, menu, options = init(num_of_enemies)

while running:

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.keys['left'] = True
            if event.key == pygame.K_RIGHT:
                player.keys['right'] = True
            if event.key == pygame.K_SPACE and not(end_game) and not(menu):
                if len(all_bullets) < max_bullets:
                    bullet = Bullet(player.rect.x + 16, player.rect.y - 10)
                    all_bullets.add(bullet)
            if event.key ==  pygame.K_ESCAPE:
                menu = not(menu)
            if event.key ==  pygame.K_UP and menu:
                selected_option = (selected_option - 1) % len(options)
            if event.key ==  pygame.K_DOWN and menu:
                selected_option = (selected_option + 1) % len(options)
            if event.key == pygame.K_SPACE and menu:
                if options[selected_option] == 'Restart':
                    player, all_enemies, enemies_remaining, all_bullets, score, selected_option, running, end_game, win_game, menu, options = init(num_of_enemies)
                    menu = False
                if options[selected_option] == 'Quit':
                    running = False
                else:
                    menu = False
                
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.keys['left'] = False
            if event.key == pygame.K_RIGHT:
                player.keys['right'] = False

    if menu:
        draw_menu()
    else:
        # Update player
        player.update()

        # Update enemies
        all_enemies.update()

        # Update bullets
        all_bullets.update()

        # Check collision with bullet
        for bullet in all_bullets:
            collisions = pygame.sprite.spritecollide(bullet, all_enemies, True)
            for _ in collisions:
                enemies_remaining -= 1
                score += 1

        # Render everything
        screen.blit(background, (0, 0))
        player_group = pygame.sprite.Group(player)
        player_group.draw(screen)
        all_enemies.draw(screen)
        all_bullets.draw(screen)
        show_bullets_left(bullet_x, bullet_y)
        show_enemies_killed(enemy_x, enemy_y)
    
        for enemy in all_enemies:
            if enemy.rect.y > SCREEN_HEIGHT - 184 and not(end_game):
                end_game = True
                win_game = False
            if not(win_game):
                enemy.x_change = 0
                enemy.y_change = 0
                    
        if enemies_remaining == 0:
            end_game = True

        if end_game:
            show_game_over(win_game)
            options = ['Restart', 'Quit']
        
    pygame.display.update()

pygame.quit()
