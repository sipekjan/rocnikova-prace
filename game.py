import pygame, random
import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
pygame.init()
window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
pygame.mixer.music.load(resource_path("music.mp3"))
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.2)

background_img = pygame.image.load(resource_path("background.png"))
background_img = pygame.transform.scale(background_img, window.get_size())

def center_rect(w, h, bw, bh):
    return pygame.Rect((w - bw) // 2, (h - bh) // 2, bw, bh)

def main_menu(window, game_settings, background_img):
    pygame.font.init()
    font = pygame.font.Font(resource_path("font.TTF"), 50)
    small_font = pygame.font.Font(resource_path("font.TTF"), 30)

    w, h = window.get_size()

    title_text = font.render("Bomberman", True, (255, 255, 255))
    start_text = small_font.render("Start Game", True, (0, 0, 0))
    settings_text = small_font.render("Settings", True, (0, 0, 0))
    quit_text = small_font.render("Quit", True, (0, 0, 0))

    button_width, button_height = 240, 60
    start_button = center_rect(w, h, button_width, button_height)
    start_button.y -= 90
    settings_button = center_rect(w, h, button_width, button_height)
    settings_button.y -= 15
    quit_button = center_rect(w, h, button_width, button_height)
    quit_button.y += 60

    menu_running = True
    while menu_running:
        window.blit(background_img, (0, 0))
        window.blit(title_text, (w//2 - title_text.get_width()//2, h//4))

        for rect, text in [(start_button, start_text), (settings_button, settings_text), (quit_button, quit_text)]:
            window.blit(text, (rect.centerx - text.get_width()//2, rect.centery - text.get_height()//2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_button.collidepoint(mouse_pos):
                    menu_running = False
                elif settings_button.collidepoint(mouse_pos):
                    settings_menu(window, game_settings, background_img)
                elif quit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    menu_running = False

def settings_menu(window, game_settings, background_img):
    font = pygame.font.Font(resource_path("font.TTF"), 40)
    small_font = pygame.font.Font(resource_path("font.TTF"), 28)

    w, h = window.get_size()

    title = font.render("Settings", True, (255, 255, 255))

    control_keys = [
        ("Move Up", "up"),
        ("Move Down", "down"),
        ("Move Left", "left"),
        ("Move Right", "right"),
        ("Place Bomb", "bomb")
    ]

    buttons = []
    button_width, button_height = 380, 50
    start_y = h//2 - (len(control_keys) * 70)//2 - 100

    for i in range(len(control_keys)):
        btn = center_rect(w, h, button_width, button_height)
        btn.y = start_y + i * 70
        buttons.append(btn)

    back_button = center_rect(w, h, button_width, button_height)
    back_button.y = h - 100

    volume_bar = pygame.Rect(w//2 - 150, h - 250, 300, 8)
    dragging_volume = False

    waiting_for_key = None

    running = True
    while running:
        window.blit(background_img, (0, 0))
        window.blit(title, (w//2 - title.get_width()//2, 50))

        volume_handle_x = volume_bar.x + int(pygame.mixer.music.get_volume() * volume_bar.width)

        for i, (label, action) in enumerate(control_keys):
            key_name = pygame.key.name(game_settings["controls"][action]).upper()
            text = small_font.render(f"{label}: {key_name}", True, (0, 0, 0))
            window.blit(text, (buttons[i].centerx - text.get_width()//2, buttons[i].centery - text.get_height()//2))

        back_text = font.render("Back", True, (255, 255, 255))
        window.blit(back_text, (back_button.centerx - back_text.get_width()//2, back_button.centery - back_text.get_height()//2))

        volume_text = small_font.render("Music Volume", True, (255, 255, 255))
        window.blit(volume_text, (w//2 - volume_text.get_width()//2, volume_bar.y - 30))
        pygame.draw.rect(window, (180, 180, 180), volume_bar)
        pygame.draw.circle(window, (255, 255, 255), (volume_handle_x, volume_bar.centery), 10)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if waiting_for_key:
                if event.type == pygame.KEYDOWN:
                    game_settings["controls"][waiting_for_key] = event.key
                    waiting_for_key = None
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if pygame.Rect(volume_handle_x-10, volume_bar.centery-10, 20, 20).collidepoint(pos):
                        dragging_volume = True
                    elif volume_bar.collidepoint(pos):
                        new_volume = (pos[0] - volume_bar.x) / volume_bar.width
                        pygame.mixer.music.set_volume(max(0, min(1, new_volume)))

                    for i, btn in enumerate(buttons):
                        if btn.collidepoint(pos):
                            waiting_for_key = control_keys[i][1]
                    if back_button.collidepoint(pos):
                        running = False

                if event.type == pygame.MOUSEBUTTONUP:
                    dragging_volume = False

                if event.type == pygame.MOUSEMOTION and dragging_volume:
                    new_volume = (event.pos[0] - volume_bar.x) / volume_bar.width
                    pygame.mixer.music.set_volume(max(0, min(1, new_volume)))

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False


def death_menu(window, background_img):
    font = pygame.font.Font(resource_path("font.TTF"), 50)
    small_font = pygame.font.Font(resource_path("font.TTF"), 30)

    w, h = window.get_size()

    retry_button = center_rect(w, h, 240, 50)
    menu_button = center_rect(w, h, 240, 50)

    retry_button.y -= 40
    menu_button.y += 40

    title_text = font.render("You Died!", True, (255, 0, 0))
    retry_text = small_font.render("Retry", True, (0, 0, 0))
    menu_text = small_font.render("Back to Menu", True, (0, 0, 0))

    while True:
        window.blit(background_img, (0, 0))
        window.blit(title_text, (w//2 - title_text.get_width()//2, h//4))

        for rect, text in [(retry_button, retry_text), (menu_button, menu_text)]:
            window.blit(text, (rect.centerx - text.get_width()//2, rect.centery - text.get_height()//2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if retry_button.collidepoint(pos):
                    return "retry"
                elif menu_button.collidepoint(pos):
                    return "menu"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "retry"
                elif event.key == pygame.K_m:
                    return "menu"

def pause_menu(window, game_settings, background_img):
    font = pygame.font.Font(resource_path("font.TTF"), 50)
    small_font = pygame.font.Font(resource_path("font.TTF"), 30)

    w, h = window.get_size()

    paused = True

    title_text = font.render("Pause", True, (255, 255, 255))

    resume_button = center_rect(w, h, 240, 50)
    settings_button = center_rect(w, h, 240, 50)
    menu_button = center_rect(w, h, 240, 50)

    resume_button.y -= 70
    settings_button.y = h//2 - 25
    menu_button.y += 70

    resume_text = small_font.render("Continue", True, (0, 0, 0))
    settings_text = small_font.render("Settings", True, (0, 0, 0))
    menu_text = small_font.render("Back to menu", True, (0, 0, 0))

    while paused:
        window.blit(background_img, (0, 0))
        window.blit(title_text, (w//2 - title_text.get_width()//2, h//4))

        for rect, text in [(resume_button, resume_text), (settings_button, settings_text), (menu_button, menu_text)]:
            window.blit(text, (rect.centerx - text.get_width()//2, rect.centery - text.get_height()//2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if resume_button.collidepoint(mouse_pos):
                    paused = False
                elif menu_button.collidepoint(mouse_pos):
                    return True
                elif settings_button.collidepoint(mouse_pos):
                    settings_menu(window, game_settings, background_img)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False
                elif event.key == pygame.K_m:
                    return True
    return False
def level_complete_menu(window, background_img, score):
    font = pygame.font.Font(resource_path("font.TTF"), 50)
    small_font = pygame.font.Font(resource_path("font.TTF"), 30)

    w, h = window.get_size()

    retry_button = center_rect(w, h, 240, 50)
    next_button = center_rect(w, h, 240, 50)

    retry_button.y += 40
    next_button.y += 120

    title_text = font.render("Level Complete!", True, (0, 255, 0))
    score_text = small_font.render(f"Score: {score}", True, (255, 255, 255))
    retry_text = small_font.render("Retry", True, (0, 0, 0))
    next_text = small_font.render("Next Level", True, (0, 0, 0))

    while True:
        window.blit(background_img, (0, 0))
        window.blit(title_text, (w//2 - title_text.get_width()//2, h//4))
        window.blit(score_text, (w//2 - score_text.get_width()//2, h//4 + 70))

        for rect, text in [(retry_button, retry_text), (next_button, next_text)]:
            window.blit(text, (rect.centerx - text.get_width()//2, rect.centery - text.get_height()//2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if retry_button.collidepoint(pos):
                    return "retry"
                elif next_button.collidepoint(pos):
                    return "next"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "retry"
                elif event.key == pygame.K_n:
                    return "next"


def run_game(game_settings, background_img):
    player_img = pygame.image.load(resource_path("player.png"))
    player_img = pygame.transform.scale(player_img, (35, 47))
    block_img = pygame.image.load(resource_path("block.png"))
    block_img = pygame.transform.scale(block_img, (60, 60))
    map_img = pygame.image.load(resource_path("map.png"))
    enemy_img = pygame.image.load(resource_path("ballon.png"))
    enemy_img = pygame.transform.scale(enemy_img, (37, 50))
    bomb_img = pygame.image.load(resource_path("bomb.png"))
    bomb_img = pygame.transform.scale(bomb_img, (40, 40))
    destroyable_block_img = pygame.image.load(resource_path("destroyable_block.png"))
    destroyable_block_img = pygame.transform.scale(destroyable_block_img, (60, 60))
    explosion_img = pygame.image.load(resource_path("explosion.png"))
    explosion_img = pygame.transform.scale(explosion_img, (180, 180))
    door_img = pygame.image.load(resource_path("door.png"))
    door_img = pygame.transform.scale(door_img, (60, 60))

    map_width = 780
    map_height = 660
    window_width, window_height = window.get_size()
    offset_x = (window_width - map_width) // 2
    offset_y = (window_height - map_height) // 2

    score = 0
    start_time = pygame.time.get_ticks()
    font = pygame.font.Font(resource_path("font.TTF"), 28)

    player_x, player_y = 60, 60
    player_width, player_height = 35, 47

    enemy_x, enemy_y = 375, 300
    enemy_direction = random.choice([(1,0), (-1,0), (0,1), (0,-1)])
    next_enemy_move_time = pygame.time.get_ticks() + 1000
    enemy_dead = False

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
            if all((block.x, block.y) != cell for block in solid_blocks):
                valid_destroyable_cells.append(cell)

    random.shuffle(valid_destroyable_cells)
    destroyable_blocks = [pygame.Rect(x, y, 60, 60) for (x, y) in valid_destroyable_cells[:49]]

    door_block = random.choice(destroyable_blocks)
    door_position = (door_block.x, door_block.y)
    door_visible = False

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
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == game_settings["controls"]["bomb"]:
                    if can_place_bomb and len(bombs) == 0 and current_time >= bomb_cooldown_time:
                        bomb_x = (player_x // 60) * 60 + 10
                        bomb_y = (player_y // 60) * 60 + 10
                        bombs.append({"x": bomb_x, "y": bomb_y, "time": current_time, "player_inside": True})
                        can_place_bomb = False
                if event.key == pygame.K_ESCAPE:
                    if pause_menu(window, game_settings, background_img):
                        return "menu"

        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[game_settings["controls"]["up"]] and player_y > 60:
            dy = -3
        if keys[game_settings["controls"]["down"]] and player_y < 598 - player_height:
            dy = 3
        if keys[game_settings["controls"]["left"]] and player_x > 60:
            dx = -3
        if keys[game_settings["controls"]["right"]] and player_x < 720 - player_width:
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

        if not enemy_dead:
            if current_time > next_enemy_move_time:
                enemy_direction = random.choice([(1,0), (-1,0), (0,1), (0,-1)])
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
                enemy_direction = random.choice([(1,0), (-1,0), (0,1), (0,-1)])
            else:
                enemy_x, enemy_y = next_enemy_x, next_enemy_y

            enemy_rect = pygame.Rect(enemy_x, enemy_y, 37, 50)
        else:
            enemy_rect = pygame.Rect(-100, -100, 0, 0)

        active_bombs = []
        for bomb in bombs:
            if current_time - bomb["time"] < 3000:
                active_bombs.append(bomb)
            else:
                explosions.append((bomb["x"]-68, bomb["y"]-70, current_time))
                can_place_bomb = True
                bomb_cooldown_time = current_time + 100
        bombs = active_bombs

        window.blit(background_img, (0, 0))

        top_bar_height = 60


        score_text = font.render(f"Score: {score}", True, (0, 0, 0))

        window.blit(score_text, (offset_x + 10, offset_y - top_bar_height + 15))

        window.blit(map_img, (offset_x, offset_y))

        for block in solid_blocks:
            window.blit(block_img, (block.x + offset_x, block.y + offset_y))
        for block in destroyable_blocks:
            window.blit(destroyable_block_img, (block.x + offset_x, block.y + offset_y))
        for bomb in bombs:
            window.blit(bomb_img, (bomb["x"] + offset_x, bomb["y"] + offset_y))

        new_explosions = []
        player_dead = False

        for exp_x, exp_y, start_time in explosions:
            if current_time - start_time < 500:
                new_explosions.append((exp_x, exp_y, start_time))
                window.blit(explosion_img, (exp_x + offset_x, exp_y + offset_y))

                for offset_dx, offset_dy in [(0,0), (0,-40), (0,40), (-40,0), (40,0)]:
                    explosion_rect = pygame.Rect(exp_x + 66 + offset_dx, exp_y + 66 + offset_dy, 38, 28)

                    remaining_blocks = []
                    for block in destroyable_blocks:
                        if explosion_rect.colliderect(block):
                            score += 5  
                        else:
                            remaining_blocks.append(block)
                    destroyable_blocks = remaining_blocks

                    if explosion_rect.colliderect(pygame.Rect(door_position[0], door_position[1], 60, 60)):
                        door_visible = True

                    if player_rect.colliderect(explosion_rect):
                        player_dead = True
                    if enemy_rect.colliderect(explosion_rect):
                        enemy_dead = True
                        score += 100

        explosions = new_explosions

        if door_visible:
            window.blit(door_img, (door_position[0] + offset_x, door_position[1] + offset_y))
            door_rect = pygame.Rect(door_position[0], door_position[1], 60, 60)
            if player_rect.colliderect(door_rect):
                return level_complete_menu(window, background_img, score)

        if player_rect.colliderect(enemy_rect):
            player_dead = True

        if player_dead:
            result = death_menu(window, background_img)
            return result

        if not enemy_dead:
            window.blit(enemy_img, (enemy_x + offset_x, enemy_y + offset_y))
        window.blit(player_img, (player_x + offset_x, player_y + offset_y))

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
    main_menu(window, game_settings, background_img)

    while True:
        result = run_game(game_settings, background_img)
        if result == "menu":
            break
        elif result == "retry":
            continue
        elif result == "next":

            continue