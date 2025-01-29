import pygame
import time

pygame.init()
running = True
clock = pygame.time.Clock()
screen = pygame.display.set_mode ((780,660))
player_x = 60
player_y = 60
player_image = pygame.image.load("player.png")
player_image = pygame.transform.scale(player_image, (55, 55))
block_image = pygame.image.load("block.png")
block_image = pygame.transform.scale(block_image, (60, 60))
bomb_image = pygame.image.load("bomb.png")
bomb_image = pygame.transform.scale(bomb_image, (30, 30))

bombs = []
bomb_duration = 3000
map = pygame.image.load("map.png")
blocks = []
for i in range(4):
    for j in range(5):
        blocks.append(pygame.Rect(120 + (j * 120), 120 + (120 * i), 60, 60))
while running:
    
    screen.fill((0,0,0))
    screen.blit(map, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_w]:
        player_y-=5
        if player_y < 60:
                player_y=61
        player_rect = pygame.Rect(player_x, player_y, 55, 55)
        for block in blocks:
            if player_rect.colliderect(block):
                player_y += 5  
                break
    if pressed[pygame.K_s]:
        player_y+=5
        if player_y > 544:
                player_y=543
        player_rect = pygame.Rect(player_x, player_y, 55, 55)
        for block in blocks:
            if player_rect.colliderect(block):
                player_y -= 5  
                break
    if pressed[pygame.K_a]:
        player_x-=5
        if player_x < 60:
                player_x=61
        player_rect = pygame.Rect(player_x, player_y, 55, 55)
        for block in blocks:
            if player_rect.colliderect(block):
                player_x += 5  
                break
    if pressed[pygame.K_d]:
        player_x+=5
        if player_x > 663:
                player_x=664
        player_rect = pygame.Rect(player_x, player_y, 55, 55)
        for block in blocks:
            if player_rect.colliderect(block):
                player_x -= 5 
                break
    if pressed[pygame.K_SPACE]:
        bombs.append((player_x + 13, player_y + 13, pygame.time.get_ticks()))
        current_time = pygame.time.get_ticks()
        bombs = [(x, y, t) for x, y, t in bombs if current_time - t < 3000]
    for x, y, t in bombs:
        screen.blit(bomb_image, (x, y))

    for block in blocks:
        screen.blit(block_image, (block.x, block.y))

    screen.blit(player_image, (player_x, player_y))
    
  
    pygame.display.flip()
    clock.tick(60)