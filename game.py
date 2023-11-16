import pygame
import random
import math

pygame.init()

screen = pygame.display.set_mode((800,600))

background = pygame.image.load('background.jpg')

running = True

pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('upc.png')
pygame.display.set_icon(icon)

playerImg = pygame.image.load('astronave.png')
playerX = 370
playerY = 480
playerX_change = 0

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(4) 
    enemyY_change.append(40)

bulletImg = pygame.image.load('bala.png')
bulletX = 0
bulletY = playerY
bulletX_change = 0
bulletY_change = 20
bullet_state = "ready"

score = 0
font = pygame.font.Font('freesansbold.ttf',32)
textX = 10
textY = 10

over_font = pygame.font.Font('freesansbold.ttf',64)

def show_score(x,y):
    sc = font.render("Score: " + str(score), True, (255,255,255))
    screen.blit(sc, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255,255,255))
    screen.blit(over_text, (200,250))
    
def player(x,y):  
    screen.blit(playerImg, (x, y))

def enemy(x,y,i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX-bulletX,2) + math.pow(enemyY-bulletY,2)) 
    if distance < 40:
        return True
    else:
        return False
    
while running:

    #screen.fill((0,0,0))
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX,bulletY)
                
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
                
    playerX += playerX_change

    if playerX < 0:
        playerX = 0
    elif playerX > 736:
        playerX = 736

    for i in range(num_of_enemies):

        if enemyY[i] > 400:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score += 1
            print(score)
            enemyX[i] = random.randint(0,735) 
            enemyY[i] = random.randint(50,150)

        enemy(enemyX[i],enemyY[i],i)


    if bulletY <=0:
        bulletY = 480
        bullet_state = "ready"
        
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    
    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()

pygame.quit()
exit()
