import pygame, random
pygame.init()

window = pygame.display.set_mode((780, 660))
clock = pygame.time.Clock()

def main_menu(window, game_settings):
    pygame.font.init()
    font = pygame.font.SysFont("Arial", 50)
    small_font = pygame.font.SysFont("Arial", 30)

    title_text = font.render("Bomberman", True, (255, 255, 255))
    start_text = small_font.render("Start Game", True, (0, 0, 0))
    settings_text = small_font.render("Settings", True, (0, 0, 0))
    quit_text = small_font.render("Quit", True, (0, 0, 0))

    start_button = pygame.Rect(300, 280, 180, 50)
    settings_button = pygame.Rect(300, 350, 180, 50)
    quit_button = pygame.Rect(300, 420, 180, 50)

    menu_running = True
    while menu_running:
        window.fill((0, 0, 128))
        window.blit(title_text, (240, 150))

        pygame.draw.rect(window, (255, 255, 255), start_button)
        pygame.draw.rect(window, (255, 255, 255), settings_button)
        pygame.draw.rect(window, (255, 255, 255), quit_button)
        window.blit(start_text, (start_button.x + 30, start_button.y + 10))
        window.blit(settings_text, (settings_button.x + 30, settings_button.y + 10))
        window.blit(quit_text, (quit_button.x + 60, quit_button.y + 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_button.collidepoint(mouse_pos):
                    menu_running = False
                elif settings_button.collidepoint(mouse_pos):
                    settings_menu(window, game_settings)
                elif quit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    menu_running = False

def settings_menu(window, game_settings):
    font = pygame.font.SysFont("Arial", 40)
    small_font = pygame.font.SysFont("Arial", 28)

    title = font.render("Control Settings", True, (255, 255, 255))

    control_keys = [
        ("Move Up", "up"),
        ("Move Down", "down"),
        ("Move Left", "left"),
        ("Move Right", "right"),
        ("Place Bomb", "bomb")
    ]

    buttons = [pygame.Rect(200, 180 + i * 70, 380, 50) for i in range(len(control_keys))]
    back_button = pygame.Rect(200, 550, 380, 50)

    waiting_for_key = None

    running = True
    while running:
        window.fill((0, 0, 64))
        window.blit(title, (200, 100))

        for i, (label, action) in enumerate(control_keys):
            pygame.draw.rect(window, (255, 255, 255), buttons[i])
            key_name = pygame.key.name(game_settings["controls"][action]).upper()
            text = small_font.render(f"{label}: {key_name}", True, (0, 0, 0))
            window.blit(text, (buttons[i].x + 10, buttons[i].y + 10))

        pygame.draw.rect(window, (200, 200, 200), back_button)
        back_text = small_font.render("Back", True, (0, 0, 0))
        window.blit(back_text, (back_button.x + 140, back_button.y + 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if waiting_for_key:
                if event.type == pygame.KEYDOWN:
                    game_settings["controls"][waiting_for_key] = event.key
                    waiting_for_key = None
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for i, btn in enumerate(buttons):
                        if btn.collidepoint(pos):
                            waiting_for_key = control_keys[i][1]
                    if back_button.collidepoint(pos):
                        running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False

def pause_menu(window, game_settings):
    font = pygame.font.SysFont("Arial", 50)
    small_font = pygame.font.SysFont("Arial", 30)
    paused = True

    title_text = font.render("Pause", True, (255, 255, 255))

    resume_button = pygame.Rect(270, 240, 240, 50)
    settings_button = pygame.Rect(270, 310, 240, 50)
    menu_button = pygame.Rect(270, 380, 240, 50)

    resume_text = small_font.render("Continue", True, (0, 0, 0))
    settings_text = small_font.render("Settings", True, (0, 0, 0))
    menu_text = small_font.render("Back to menu", True, (0, 0, 0))

    while paused:
        window.fill((30, 30, 30))
        window.blit(title_text, (300, 160))

        pygame.draw.rect(window, (255, 255, 255), resume_button)
        pygame.draw.rect(window, (255, 255, 255), menu_button)
        pygame.draw.rect(window, (255, 255, 255), settings_button)

        window.blit(resume_text, (resume_button.x + 50, resume_button.y + 10))
        window.blit(menu_text, (menu_button.x + 40, menu_button.y + 10))
        window.blit(settings_text, (settings_button.x + 55, settings_button.y + 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if resume_button.collidepoint(mouse_pos):
                    paused = False
                elif menu_button.collidepoint(mouse_pos):
                    return True
                elif settings_button.collidepoint(mouse_pos):
                    settings_menu(window, game_settings)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False
                elif event.key == pygame.K_m:
                    return True
    return False

def run_game(game_settings):
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
    explosion_img = pygame.image.load("explosion.png")
    explosion_img = pygame.transform.scale(explosion_img, (180, 180))

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
    can_place_bomb = True
    bomb_cooldown_time = 0 

    running = True
    while running:
        current_time = pygame.time.get_ticks()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == game_settings["controls"]["bomb"]:
                    if can_place_bomb and len(bombs) == 0 and current_time >= bomb_cooldown_time:
                        bomb_x = (player_x // 60) * 60 + 10
                        bomb_y = (player_y // 60) * 60 + 10
                        bombs.append({"x": bomb_x, "y": bomb_y, "time": current_time, "player_inside": True})
                        can_place_bomb = False 
                if event.key == pygame.K_ESCAPE:
                    if pause_menu(window, game_settings):
                        return

        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[game_settings["controls"]["up"]] and player_y > 60:
            dy = -3
        if keys[game_settings["controls"]["down"]] and player_y < 540 - player_height:
            dy = 3
        if keys[game_settings["controls"]["left"]] and player_x > 60:
            dx = -3
        if keys[game_settings["controls"]["right"]] and player_x < 660 - player_width:
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
                explosions.append((bomb["x"]-70 , bomb["y"]-70, current_time))
                can_place_bomb = True  
                bomb_cooldown_time = current_time + 100

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
                window.blit(explosion_img, (exp_x, exp_y))

                for offset_x, offset_y in [(0,0),(0,-40),(0,40),(-40,0),(40,0)]:
                    explosion_rect = pygame.Rect(exp_x + 50 + offset_x, exp_y + 50 + offset_y, 40, 40)
                    destroyable_blocks = [block for block in destroyable_blocks if not explosion_rect.colliderect(block)]
                    if player_rect.colliderect(explosion_rect):
                        player_dead = True

        explosions = new_explosions
        if player_dead:
            return

        window.blit(enemy_img, (enemy_rect.x, enemy_rect.y))
        window.blit(player_img, (player_x, player_y))
        pygame.display.flip()

while True:
    game_settings = {
        "controls": {
            "up": pygame.K_w,
            "down": pygame.K_s,
            "left": pygame.K_a,
            "right": pygame.K_d,
            "bomb": pygame.K_SPACE
        }
    }
    main_menu(window, game_settings)
    run_game(game_settings)
