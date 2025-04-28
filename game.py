import pygame, random
import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def load_map(level_number):
    map_file = resource_path(f"maps/level{level_number}.txt")
    map_data = []
    try:
        with open(map_file, 'r') as f:
            for line in f:
                map_data.append(list(line.strip()))
    except FileNotFoundError:
        print(f"Level {level_number} not found!")
        return None
    return map_data

def available_levels():
    maps_dir = resource_path("maps")
    levels = []
    for file in os.listdir(maps_dir):
        if file.startswith("level") and file.endswith(".txt"):
            level_num = int(file[len("level"): -len(".txt")])
            levels.append(level_num)
    return sorted(levels)
pygame.init()
window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Bomberman")
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
                    selected_level = level_select_menu(window, background_img, game_settings)
                    if selected_level:
                        menu_running = False
                        game_settings["selected_level"] = selected_level
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

def level_select_menu(window, background_img, game_settings):
    font = pygame.font.Font(resource_path("font.TTF"), 50)
    small_font = pygame.font.Font(resource_path("font.TTF"), 30)

    w, h = window.get_size()

    title_text = font.render("Select Level", True, (255, 255, 255))

    levels = available_levels()
    buttons = []
    button_width, button_height = 240, 60
    start_y = h//2 - (len(levels) * (button_height + 20)) // 2

    for i, level_num in enumerate(levels):
        btn = pygame.Rect(w//2 - button_width//2, start_y + i * (button_height + 20), button_width, button_height)
        buttons.append((btn, level_num))

    running = True
    while running:
        window.blit(background_img, (0, 0))
        window.blit(title_text, (w//2 - title_text.get_width()//2, h//4))

        for rect, level_num in buttons:
            text = small_font.render(f"Level {level_num}", True, (0, 0, 0))
            window.blit(text, (rect.centerx - text.get_width()//2, rect.centery - text.get_height()//2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for rect, level_num in buttons:
                    if rect.collidepoint(pos):
                        return level_num

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return None
            
def run_game(game_settings, background_img, level_number):
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

    map_data = load_map(level_number)
    if map_data is None:
        return "menu"

    solid_blocks = []
    destroyable_blocks = []
    enemy_positions = []
    player_position = None
    door_position = None

    for row_idx, row in enumerate(map_data):
        for col_idx, tile in enumerate(row):
            x = col_idx * 60
            y = row_idx * 60
            if tile == '#':
                solid_blocks.append(pygame.Rect(x, y, 60, 60))
            elif tile == 'D':
                destroyable_blocks.append(pygame.Rect(x, y, 60, 60))
            elif tile == 'E':
                enemy_positions.append((x, y))
            elif tile == 'P':
                player_position = (x, y)
            elif tile == 'O':
                door_position = (x, y)

    if not player_position:
        print("No player start position found!")
        return "menu"

    player_rect = pygame.Rect(player_position[0], player_position[1], 35, 47)
    enemies = [{"rect": pygame.Rect(pos[0], pos[1], 37, 50), "dir": random.choice([(2,0), (-2,0), (0,2), (0,-2)]), "next_change": pygame.time.get_ticks() + 1000} for pos in enemy_positions]

    bombs = []
    explosions = []
    can_place_bomb = True
    bomb_cooldown_time = 0

    offset_x = (window.get_width() - len(map_data[0]) * 60) // 2
    offset_y = (window.get_height() - len(map_data) * 60) // 2

    score = 0
    font = pygame.font.Font(resource_path("font.TTF"), 28)

    clock = pygame.time.Clock()
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
                    if can_place_bomb and current_time >= bomb_cooldown_time:
                        bomb_x = (player_rect.centerx // 60) * 60 + 10
                        bomb_y = (player_rect.centery // 60) * 60 + 10
                        bombs.append({"rect": pygame.Rect(bomb_x, bomb_y, 40, 40), "time": current_time, "player_inside": True})
                        can_place_bomb = False
                if event.key == pygame.K_ESCAPE:
                    if pause_menu(window, game_settings, background_img):
                        return "menu"

        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[game_settings["controls"]["up"]]: dy = -3
        if keys[game_settings["controls"]["down"]]: dy = 3
        if keys[game_settings["controls"]["left"]]: dx = -3
        if keys[game_settings["controls"]["right"]]: dx = 3

        next_rect = player_rect.move(dx, dy)
        collision = False
        for block in solid_blocks + destroyable_blocks:
            if next_rect.colliderect(block):
                collision = True
                break
        for bomb in bombs:
            if next_rect.colliderect(bomb["rect"]) and not bomb.get("player_inside", False):
                collision = True
                break
        if not collision:
            player_rect = next_rect

        for bomb in bombs:
            if not player_rect.colliderect(bomb["rect"]):
                bomb["player_inside"] = False

        new_bombs = []
        for bomb in bombs:
            if current_time - bomb["time"] >= 3000:
                bomb_center_x = (bomb["rect"].x // 60) * 60
                bomb_center_y = (bomb["rect"].y // 60) * 60
                explosions.append({"rect": pygame.Rect(bomb_center_x-60, bomb_center_y-60, 60, 60), "time": current_time})

                directions = [(0, -60), (0, 60), (-60, 0), (60, 0)]
                for dx, dy in directions:
                    check_rect = pygame.Rect(bomb_center_x + dx, bomb_center_y + dy, 60, 60)

                    for block in destroyable_blocks[:]:
                        if check_rect.colliderect(block):
                            destroyable_blocks.remove(block)
                            score += 5

                    for enemy in enemies[:]:
                        if check_rect.colliderect(enemy["rect"]):
                            enemies.remove(enemy)
                            score += 100

                    if check_rect.colliderect(player_rect):
                        return death_menu(window, background_img)

                bomb_cooldown_time = current_time + 500
                can_place_bomb = True
            else:
                new_bombs.append(bomb)
        bombs = new_bombs

        new_explosions = []
        for explosion in explosions:
            if current_time - explosion["time"] <= 500:
                new_explosions.append(explosion)

                for block in destroyable_blocks[:]:
                    if explosion["rect"].colliderect(block):
                        destroyable_blocks.remove(block)
                        score += 5

                if door_position and explosion["rect"].colliderect(pygame.Rect(door_position[0], door_position[1], 60, 60)):
                    door_visible = True

                for enemy in enemies[:]:
                    if explosion["rect"].colliderect(enemy["rect"]):
                        enemies.remove(enemy)
                        score += 100

                if explosion["rect"].colliderect(player_rect):
                    return death_menu(window, background_img)
        explosions = new_explosions

        for enemy in enemies:
            if current_time >= enemy["next_change"]:
                enemy["dir"] = random.choice([(2,0), (-2,0), (0,2), (0,-2)])
                enemy["next_change"] = current_time + 1000

            move_x, move_y = enemy["dir"]
            next_enemy = enemy["rect"].move(move_x, move_y)

            collision = False
            for block in solid_blocks + destroyable_blocks:
                if next_enemy.colliderect(block):
                    collision = True
                    break
            for bomb in bombs:
                if next_enemy.colliderect(bomb["rect"]):
                    collision = True
                    break
            if not collision:
                enemy["rect"] = next_enemy
            else:
                enemy["dir"] = random.choice([(2,0), (-2,0), (0,2), (0,-2)])

            if player_rect.colliderect(enemy["rect"]):
                return death_menu(window, background_img)

        window.blit(background_img, (0, 0))
        window.blit(map_img, (offset_x, offset_y))

        for block in solid_blocks:
            window.blit(block_img, (block.x + offset_x, block.y + offset_y))
        for block in destroyable_blocks:
            window.blit(destroyable_block_img, (block.x + offset_x, block.y + offset_y))
        for bomb in bombs:
            window.blit(bomb_img, (bomb["rect"].x + offset_x, bomb["rect"].y + offset_y))
        for explosion in explosions:
            window.blit(explosion_img, (explosion["rect"].x + offset_x, explosion["rect"].y + offset_y))

        if door_position:
            door_rect = pygame.Rect(door_position[0], door_position[1], 60, 60)
            if player_rect.colliderect(door_rect):
                return level_complete_menu(window, background_img, score)
            window.blit(door_img, (door_position[0] + offset_x, door_position[1] + offset_y))

        for enemy in enemies:
            window.blit(enemy_img, (enemy["rect"].x + offset_x, enemy["rect"].y + offset_y))

        window.blit(player_img, (player_rect.x + offset_x, player_rect.y + offset_y))

        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        window.blit(score_text, (offset_x + 10, offset_y - 40))

        pygame.display.flip()

while True:
    game_settings = {
        "controls": {
            "up": pygame.K_w,
            "down": pygame.K_s,
            "left": pygame.K_a,
            "right": pygame.K_d,
            "bomb": pygame.K_SPACE
        },
        "selected_level": 1
    }
    main_menu(window, game_settings, background_img)

    while True:
        result = run_game(game_settings, background_img, game_settings["selected_level"])
        if result == "menu":
            break
        elif result == "retry":
            continue
        elif result == "next":
            next_level = game_settings["selected_level"] + 1
        available = available_levels()
        if next_level in available:
            game_settings["selected_level"] = next_level
            continue
        else:
            break
