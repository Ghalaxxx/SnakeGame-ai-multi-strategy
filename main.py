import pygame
import random
from pygame.math import Vector2

from config import Config, Colors
from astar import AStarPathfinder
from safe_astar_floodfill import SafeAStarFloodFill
from bfs_astar import SafeAStarPathfinder
from longest_safe_path import LongestSafePathFinder
from reviewer import AlgorithmPerformanceTracker

pygame.init()
screen = pygame.display.set_mode((Config.SCREEN_SIZE, Config.SCREEN_SIZE + 80))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)

astar = AStarPathfinder(Config.SCREEN_SIZE // Config.GRID_CELL_SIZE,
                        Config.SCREEN_SIZE // Config.GRID_CELL_SIZE,
                        Config.GRID_CELL_SIZE)
safe_astar = SafeAStarFloodFill(Config.SCREEN_SIZE // Config.GRID_CELL_SIZE,
                                Config.SCREEN_SIZE // Config.GRID_CELL_SIZE,
                                Config.GRID_CELL_SIZE)
bfs_astar = SafeAStarPathfinder(Config.SCREEN_SIZE // Config.GRID_CELL_SIZE,
                                Config.SCREEN_SIZE // Config.GRID_CELL_SIZE,
                                Config.GRID_CELL_SIZE)
longest_pathfinder = LongestSafePathFinder(Config.SCREEN_SIZE // Config.GRID_CELL_SIZE,
                                           Config.SCREEN_SIZE // Config.GRID_CELL_SIZE,
                                           Config.GRID_CELL_SIZE)
tracker = AlgorithmPerformanceTracker()

snake_rect = None
snake_direction = Vector2(0, 0)
snake_parts = []
snake_length = 1
food_rect = None

a_star_path = []
active_path = []

current_mode = "manual"
last_time = 0
running = True
bait = True
score = 0
start_ticks = pygame.time.get_ticks()
flood_area_size = 0
game_over = False
last_summary_text = []
risk_label = "N/A"

def cell_of(rect):
    return (rect.centerx // Config.GRID_CELL_SIZE, rect.centery // Config.GRID_CELL_SIZE)

def reset_game():
    global snake_rect, snake_direction, snake_parts, snake_length, food_rect, bait
    global active_path, score, start_ticks, game_over, flood_area_size, last_summary_text

    snake_rect = pygame.Rect(random.randrange(0, Config.SCREEN_SIZE, Config.GRID_CELL_SIZE),
                             random.randrange(0, Config.SCREEN_SIZE, Config.GRID_CELL_SIZE),
                             Config.SNAKE_PART_SIZE, Config.SNAKE_PART_SIZE)
    snake_direction = Vector2(0, 0)
    snake_parts = []
    snake_length = 1
    bait = True
    active_path.clear()
    score = 0
    start_ticks = pygame.time.get_ticks()
    game_over = False
    flood_area_size = 0
    last_summary_text = []

def build_summary_text():
    summary = tracker.get_summary()
    if not summary:
        return ["No data yet."]
    best_score = max(summary.items(), key=lambda x: x[1]['avg_score'])[0]
    best_speed = min(summary.items(), key=lambda x: x[1]['avg_time'])[0]
    return [
        f"🎯 Best Scorer: {best_score.upper()}",
        f"⚡ Fastest Decision: {best_speed.upper()}"
    ]

def get_risk_level(head, food, obstacles, required_space):
    path = astar.find_path(head, food, obstacles)
    safe_path = safe_astar.find_safe_astar_path(head, food, obstacles, required_space)
    flood_area = safe_astar.bfs_area(food, obstacles)
    space_enough = len(flood_area) >= required_space

    if not path:
        return "panic"
    elif path and safe_path:
        return "safe"
    elif not space_enough:
        return "panic"
    else:
        return "risky"

reset_game()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_over and event.type == pygame.KEYDOWN:
            reset_game()
        if event.type == pygame.KEYDOWN and not game_over:
            key = event.unicode.lower()
            if key == 'a':
                current_mode = "a_star"
            elif key == 's':
                current_mode = "safe_astar"
            elif key == 'b':
                current_mode = "bfs_astar"
            elif key == 'l':
                current_mode = "longest"
            elif key == 'd':
                current_mode = "dynamic"
            elif key == 'm':
                current_mode = "manual"
            elif current_mode == "manual":
                if event.key == pygame.K_UP and not snake_direction[1] > 0:
                    snake_direction = Vector2(0, -Config.SNAKE_MOVE_LENGTH)
                elif event.key == pygame.K_DOWN and not snake_direction[1] < 0:
                    snake_direction = Vector2(0, Config.SNAKE_MOVE_LENGTH)
                elif event.key == pygame.K_LEFT and not snake_direction[0] > 0:
                    snake_direction = Vector2(-Config.SNAKE_MOVE_LENGTH, 0)
                elif event.key == pygame.K_RIGHT and not snake_direction[0] < 0:
                    snake_direction = Vector2(Config.SNAKE_MOVE_LENGTH, 0)

    if game_over:
        screen.fill(Colors.BG)
        text = font.render("GAME OVER - Press any key to restart", True, (0, 0, 0))
        screen.blit(text, (40, Config.SCREEN_SIZE // 2 - 30))
        for i, line in enumerate(last_summary_text):
            summary_render = font.render(line, True, (0, 0, 0))
            screen.blit(summary_render, (40, Config.SCREEN_SIZE // 2 + 10 + i * 25))
        pygame.display.flip()
        continue

    if bait:
        food_rect = pygame.Rect(random.randrange(0, Config.SCREEN_SIZE, Config.GRID_CELL_SIZE),
                                random.randrange(0, Config.SCREEN_SIZE, Config.GRID_CELL_SIZE),
                                Config.FOOD_SIZE, Config.FOOD_SIZE)
        bait = False

    now = pygame.time.get_ticks()
    if now - last_time > Config.DELAY:
        last_time = now

        head = cell_of(snake_rect)
        food = cell_of(food_rect)
        obstacles = {(p.centerx // Config.GRID_CELL_SIZE, p.centery // Config.GRID_CELL_SIZE) for p in snake_parts}
        a_star_path = astar.find_path(head, food, obstacles)

        if current_mode == "a_star":
            active_path = a_star_path
            flood_area_size = 0
            risk_label = "A*"
        elif current_mode == "safe_astar":
            active_path = safe_astar.find_safe_astar_path(head, food, obstacles, required_space=len(snake_parts))
            flood_area_size = len(safe_astar.bfs_area(food, obstacles))
            risk_label = "Safe A*"
        elif current_mode == "bfs_astar":
            active_path = bfs_astar.find_safe_path(head, food, obstacles, len(snake_parts))
            risk_label = "BFS A*"
        elif current_mode == "longest":
            active_path = longest_pathfinder.find_longest_safe_path(head, food, obstacles, len(snake_parts))
            risk_label = "Longest Path"
        elif current_mode == "dynamic":
            risk = get_risk_level(head, food, obstacles, len(snake_parts))
            risk_label = risk.upper()
            if risk == "safe":
                active_path = a_star_path
            elif risk == "risky":
                active_path = safe_astar.find_safe_astar_path(head, food, obstacles, len(snake_parts))
            else:
                active_path = longest_pathfinder.find_longest_safe_path(head, food, obstacles, len(snake_parts))
        else:
            flood_area_size = 0
            risk_label = "Manual"

        if current_mode != "manual" and active_path:
            next_cell = active_path[0]
            dx = next_cell[0] - head[0]
            dy = next_cell[1] - head[1]
            snake_direction = Vector2(dx * Config.SNAKE_MOVE_LENGTH, dy * Config.SNAKE_MOVE_LENGTH)

        snake_rect.move_ip(snake_direction)
        snake_parts.append(snake_rect.copy())
        snake_parts = snake_parts[-snake_length:]

        if (snake_rect.left < 0 or snake_rect.right > Config.SCREEN_SIZE or
            snake_rect.top < 0 or snake_rect.bottom > Config.SCREEN_SIZE or
            len(snake_parts) != len(set(p.center for p in snake_parts))):

            seconds = (pygame.time.get_ticks() - start_ticks) // 1000
            tracker.record(current_mode, score, seconds)
            last_summary_text = build_summary_text()
            best = tracker.get_best_run(current_mode)
            print(f"🎮 GAME OVER [{current_mode.upper()}]")
            print(f"✅ Score: {score}")
            print(f"⏱️ Time Survived: {seconds}s")
            if best:
                print(f"🌟 Best Run ({current_mode.upper()}): Score: {best[0]} | Time: {best[1]}s\n")
            game_over = True

        if snake_rect.center == food_rect.center:
            snake_length += 1
            score += 1
            bait = True

    screen.fill(Colors.BG)
    for i in range(0, Config.SCREEN_SIZE, Config.GRID_CELL_SIZE):
        pygame.draw.line(screen, Colors.GRID, (i, 0), (i, Config.SCREEN_SIZE))
        pygame.draw.line(screen, Colors.GRID, (0, i), (Config.SCREEN_SIZE, i))

    for cell in a_star_path:
        pygame.draw.rect(screen, Colors.PATH_SIMULATION,
                         pygame.Rect(cell[0]*Config.GRID_CELL_SIZE, cell[1]*Config.GRID_CELL_SIZE,
                                     Config.GRID_CELL_SIZE, Config.GRID_CELL_SIZE))

    for cell in active_path:
        pygame.draw.rect(screen, Colors.PATH_MAIN,
                         pygame.Rect(cell[0]*Config.GRID_CELL_SIZE, cell[1]*Config.GRID_CELL_SIZE,
                                     Config.GRID_CELL_SIZE, Config.GRID_CELL_SIZE))

    pygame.draw.rect(screen, Colors.FOOD, food_rect, 0, 10)
    for part in snake_parts:
        pygame.draw.rect(screen, Colors.SNAKE, part, 8, 4)

    pygame.draw.rect(screen, (240, 240, 240), (0, Config.SCREEN_SIZE, Config.SCREEN_SIZE, 80))
    pygame.draw.line(screen, (0, 0, 0), (0, Config.SCREEN_SIZE), (Config.SCREEN_SIZE, Config.SCREEN_SIZE), 2)

    seconds = (pygame.time.get_ticks() - start_ticks) // 1000
    hud_text = f"Mode: {risk_label}    Score: {score}    Time: {seconds}s"
    if current_mode == "safe_astar":
        hud_text += f"    Flood Area: {flood_area_size}"

    screen.blit(font.render(hud_text, True, (0, 0, 0)), (10, Config.SCREEN_SIZE + 10))

    pygame.display.flip()
    clock.tick(Config.FPS)

pygame.quit()
