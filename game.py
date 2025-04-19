import pygame, random
pygame.init()

window = pygame.display.set_mode((780, 660))
clock = pygame.time.Clock()

player_img = pygame.image.load("player.png")
player_img = pygame.transform.scale(player_img, (35, 47))
block_img = pygame.image.load("block.png")
block_img = pygame.transform.scale(block_img, (60, 60))
map_img = pygame.image.load("map.png")
enemy_img = pygame.image.load("ballon.png")
enemy_img = pygame.transform.scale(enemy_img, (37, 50))
bomb_img = pygame.image.load("bomb.png")
bomb_img = pygame.transform.scale(bomb_img, (40, 40))
destroyable_block_img = pygame.image.load("destroyable_block.png")
destroyable_block_img = pygame.transform.scale(destroyable_block_img, (60, 60))

player_x, player_y = 60, 60
player_width, player_height = 35, 47

enemy_x, enemy_y = 375, 300
enemy_direction = random.choice([(1,0),(-1,0),(0,1),(0,-1)])
next_enemy_move_time = pygame.time.get_ticks() + 1000

solid_blocks = []
for i in range(4):
    for j in range(5):
        solid_blocks.append(pygame.Rect(120 + j*120, 120 + i*120, 60, 60))

tile_positions = [(x, y) for x in range(60, 661, 60) for y in range(60, 541, 60)]
player_cell = (player_x // 60 * 60, player_y // 60 * 60)
forbidden_cells = set((player_cell[0] + dx*60, player_cell[1] + dy*60) for dx in (-1,0,1) for dy in (-1,0,1))
enemy_cell = ((enemy_x // 60) * 60, (enemy_y // 60) * 60)
valid_destroyable_cells = []
for cell in tile_positions:
    if cell not in forbidden_cells and cell != enemy_cell:
        is_valid = True
        for block in solid_blocks:
            if (block.x, block.y) == cell:
                is_valid = False
                break
        if is_valid:
            valid_destroyable_cells.append(cell)

random.shuffle(valid_destroyable_cells)
destroyable_blocks = [pygame.Rect(x, y, 60, 60) for (x, y) in valid_destroyable_cells[:49]]

bombs = []
explosions = []

running = True
while running:
    current_time = pygame.time.get_ticks()
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bomb_x = (player_x // 60) * 60 + 10
            bomb_y = (player_y // 60) * 60 + 10
            bombs.append({
                "x": bomb_x,
                "y": bomb_y,
                "time": current_time,
                "player_inside": True
            })

    keys = pygame.key.get_pressed()
    dx = dy = 0
    if keys[pygame.K_w] and player_y > 60:
        dy = -3
    if keys[pygame.K_s] and player_y < 540 - player_height:
        dy = 3
    if keys[pygame.K_a] and player_x > 60:
        dx = -3
    if keys[pygame.K_d] and player_x < 660 - player_width:
        dx = 3

    next_player_rect = pygame.Rect(player_x + dx, player_y + dy, player_width, player_height)
    collision = False
    for block in solid_blocks + destroyable_blocks:
        if next_player_rect.colliderect(block):
            collision = True
            break
    for bomb in bombs:
        bomb_rect = pygame.Rect(bomb["x"], bomb["y"], 30, 30)
        if next_player_rect.colliderect(bomb_rect) and not bomb["player_inside"]:
            collision = True
            break
    if not collision:
        player_x += dx
        player_y += dy

    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

    for bomb in bombs:
        bomb_rect = pygame.Rect(bomb["x"], bomb["y"], 30, 30)
        if not player_rect.colliderect(bomb_rect):
            bomb["player_inside"] = False

    if current_time > next_enemy_move_time:
        enemy_direction = random.choice([(1,0),(-1,0),(0,1),(0,-1)])
        next_enemy_move_time = current_time + 1000

    next_enemy_x = enemy_x + enemy_direction[0]*2
    next_enemy_y = enemy_y + enemy_direction[1]*2
    next_enemy_rect = pygame.Rect(next_enemy_x, next_enemy_y, 37, 50)

    enemy_can_move = True
    for block in solid_blocks + destroyable_blocks:
        if next_enemy_rect.colliderect(block):
            enemy_can_move = False
            break
    for bomb in bombs:
        bomb_rect = pygame.Rect(bomb["x"], bomb["y"], 30, 30)
        if next_enemy_rect.colliderect(bomb_rect):
            enemy_can_move = False
            break
    if not enemy_can_move or not (120 <= next_enemy_x <= 660 and 120 <= next_enemy_y <= 540):
        enemy_direction = random.choice([(1,0),(-1,0),(0,1),(0,-1)])
    else:
        enemy_x, enemy_y = next_enemy_x, next_enemy_y

    enemy_rect = pygame.Rect(enemy_x, enemy_y, 37, 50)

    active_bombs = []
    for bomb in bombs:
        if current_time - bomb["time"] < 3000:
            active_bombs.append(bomb)
        else:
            explosions.append((bomb["x"] - 15, bomb["y"] - 15, current_time))
    bombs = active_bombs

    window.fill((0,0,0))
    window.blit(map_img, (0,0))

    for block in solid_blocks:
        window.blit(block_img, (block.x, block.y))
    for block in destroyable_blocks:
        window.blit(destroyable_block_img, (block.x, block.y))
    for bomb in bombs:
        window.blit(bomb_img, (bomb["x"], bomb["y"]))

    new_explosions = []
    player_dead = False

    for exp_x, exp_y, start_time in explosions:
        if current_time - start_time < 500:
            new_explosions.append((exp_x, exp_y, start_time))
            for offset_x, offset_y in [(0,0),(0,-40),(0,40),(-40,0),(40,0)]:
                explosion_rect = pygame.Rect(exp_x + offset_x, exp_y + offset_y, 40, 40)
                pygame.draw.rect(window, (255,165,0), explosion_rect)

                destroyable_blocks = [block for block in destroyable_blocks if not explosion_rect.colliderect(block)]
                if player_rect.colliderect(explosion_rect):
                    player_dead = True

    explosions = new_explosions
    if player_dead:
        running = False

    window.blit(enemy_img, (enemy_rect.x, enemy_rect.y))
    window.blit(player_img, (player_x, player_y))
    pygame.display.flip()

pygame.quit()
