import pygame
import time
import random

pygame.init()
running = True
clock = pygame.time.Clock()
screen = pygame.display.set_mode((780, 660))
player_x, player_y = 60, 60
player_image = pygame.image.load("player.png") 
player_image = pygame.transform.scale(player_image, (55, 55))
block_image = pygame.image.load("block.png")
block_image = pygame.transform.scale(block_image, (60, 60))
bomb_image = pygame.image.load("bomb.png")
bomb_image = pygame.transform.scale(bomb_image, (30, 30))

enemy_x, enemy_y = 390, 330 
enemy_speed = 2
enemy_direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
change_direction_time = pygame.time.get_ticks() + 1000

bombs = []
bomb_duration = 3000
explosions = []
explosion_duration = 500
map = pygame.image.load("map.png")
blocks = []
destructible_blocks = []


for i in range(4):
    for j in range(5):
        block = pygame.Rect(120 + (j * 120), 120 + (120 * i), 60, 60)
        blocks.append(block)


possible_positions = [(x, y) for x in range(120, 661, 60) for y in range(120, 541, 60)
                      if (x, y) != (60, 60) and not any(block.collidepoint(x, y) for block in blocks)]
random.shuffle(possible_positions)

destructible_blocks = [pygame.Rect(x, y, 60, 60) for x, y in possible_positions[:50]] 

while running:
    screen.fill((0, 0, 0))
    screen.blit(map, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bombs.append((player_x + 13, player_y + 13, pygame.time.get_ticks()))
    
    pressed = pygame.key.get_pressed()
    player_rect = pygame.Rect(player_x, player_y, 55, 55)
    
    if pressed[pygame.K_w] and player_y > 60:
        player_y -= 5
        player_rect.y = player_y
        for block in blocks + destructible_blocks:
            if player_rect.colliderect(block):
                player_y += 5
                break
    
    if pressed[pygame.K_s] and player_y < 545:
        player_y += 5
        player_rect.y = player_y
        for block in blocks + destructible_blocks:
            if player_rect.colliderect(block):
                player_y -= 5
                break
    
    if pressed[pygame.K_a] and player_x > 60:
        player_x -= 5
        player_rect.x = player_x
        for block in blocks + destructible_blocks:
            if player_rect.colliderect(block):
                player_x += 5
                break
    
    if pressed[pygame.K_d] and player_x < 665:
        player_x += 5
        player_rect.x = player_x
        for block in blocks + destructible_blocks:
            if player_rect.colliderect(block):
                player_x -= 5
                break
    
    current_time = pygame.time.get_ticks()
    new_bombs = []
    
    for x, y, t in bombs:
        if current_time - t < bomb_duration:
            new_bombs.append((x, y, t))
            screen.blit(bomb_image, (x, y))
        else:
            explosions.append((x - 15, y - 15, current_time))
    bombs = new_bombs
    
    new_explosions = []
    player_in_explosion = False 
    
    for x, y, t in explosions:
        if current_time - t < explosion_duration:
            new_explosions.append((x, y, t))
            pygame.draw.rect(screen, (255, 165, 0), (x, y, 40, 40))  
            pygame.draw.rect(screen, (255, 165, 0), (x, y - 40, 40, 40))
            pygame.draw.rect(screen, (255, 165, 0), (x, y + 40, 40, 40))
            pygame.draw.rect(screen, (255, 165, 0), (x - 40, y, 40, 40))
            pygame.draw.rect(screen, (255, 165, 0), (x + 40, y, 40, 40))
            
            explosion_rects = [
                pygame.Rect(x, y, 40, 40), 
                pygame.Rect(x, y - 40, 40, 40), 
                pygame.Rect(x, y + 40, 40, 40),  
                pygame.Rect(x - 40, y, 40, 40),  
                pygame.Rect(x + 40, y, 40, 40)  
            ]
            for explosion_rect in explosion_rects:
                destructible_blocks = [block for block in destructible_blocks if not block.colliderect(explosion_rect)]
                if player_rect.colliderect(explosion_rect):
                    player_in_explosion = True
    
    explosions = new_explosions
    
    if player_in_explosion:
        running = False 
    
    for block in blocks:
        screen.blit(block_image, (block.x, block.y))
    
    for block in destructible_blocks:
        pygame.draw.rect(screen, (50, 50, 50), block)
    
    if current_time > change_direction_time:
        enemy_direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        change_direction_time = current_time + 1000
    
    enemy_rect = pygame.Rect(enemy_x, enemy_y, 20, 20)
    new_enemy_x = enemy_x + enemy_direction[0] * enemy_speed
    new_enemy_y = enemy_y + enemy_direction[1] * enemy_speed
    new_enemy_rect = pygame.Rect(new_enemy_x, new_enemy_y, 20, 20)
    
    if (120 <= new_enemy_x <= 660 and 120 <= new_enemy_y <= 540 and
        not any(new_enemy_rect.colliderect(block) for block in blocks + destructible_blocks)):
        enemy_x = new_enemy_x
        enemy_y = new_enemy_y
    else:
        enemy_direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
    
    if player_rect.colliderect(enemy_rect):
        running = False
    
    pygame.draw.rect(screen, (255, 0, 0), (enemy_x, enemy_y, 20, 20))
    screen.blit(player_image, (player_x, player_y))
    
    pygame.display.flip()
    clock.tick(60)
