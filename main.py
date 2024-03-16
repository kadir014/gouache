import platform
from dataclasses import dataclass

import pygame
import pygame.gfxdraw
from pygame import Vector2

from src import tablet


WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
MAX_FPS = 165


pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
title = f"Gouache  -  Python {platform.python_version()}  Pygame-CE {pygame.ver}"
clock = pygame.Clock()
is_running = True

font = pygame.font.Font("assets/ClearSans-Regular.ttf", 18)

@dataclass
class Mouse:
    pos: Vector2
    left: bool = False
    right: bool = False
    middle: bool = False

mouse = Mouse(Vector2())

canvas = pygame.Surface((700, 700)).convert()
canvas.fill((255, 255, 255))

hwnd = pygame.display.get_wm_info()["window"]
tb = tablet.Tablet(hwnd)

is_pen_down = False


def brush_stroke(start: Vector2, end: Vector2, size: float):
    steps = 50
    dir = (end - start)
    step_size = dir.length() / steps

    if dir.length_squared() == 0: steps = 1
    else: dir = dir.normalize()
        
    for s in range(steps):
        pygame.draw.circle(canvas, (0, 0, 0), start + dir * s * step_size, round(size), 0)


while is_running:
    dt = clock.tick(MAX_FPS) / 1000
    pygame.display.set_caption(f"{title}  @{round(clock.get_fps())}FPS")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                is_running = False

            elif event.key == pygame.K_r:
                canvas.fill((255, 255, 255))

        elif event.type == pygame.MOUSEBUTTONDOWN:
            is_pen_down = event.touch

        elif event.type == pygame.MOUSEBUTTONUP:
            is_pen_down = event.touch

    old_mouse_pos = mouse.pos.copy()
    mouse.pos = Vector2(*pygame.mouse.get_pos())

    mouse.left, mouse.right, mouse.middle = pygame.mouse.get_pressed()

    window.fill((200, 200, 200))

    if mouse.left:
        size = 20
        w = tb.pen.pressure * size if is_pen_down else size
        brush_stroke(old_mouse_pos, mouse.pos, w)

    window.blit(canvas, (0, 0))

    if canvas.get_rect().collidepoint(mouse.pos):
        pygame.mouse.set_visible(False)

        if tb.pen.pressure == 0:
            r = 20
        else:
            r = tb.pen.pressure * 20

        pygame.gfxdraw.aacircle(window, round(mouse.pos.x), round(mouse.pos.y), round(r), (0, 255, 30))

        pygame.draw.circle(window, (255, 255, 255), mouse.pos, 3, 0)
        pygame.draw.circle(window, (0, 0, 0), mouse.pos, 3, 1)

    else:
        pygame.mouse.set_visible(True)

    window.blit(font.render(f"Pen pressure: {round(tb.pen.pressure * 100)}%", True, (0, 0, 0)), (715, 10))
    br = 5
    pygame.draw.rect(window, (255, 255, 255), (715, 40, 140, 10), border_radius=br)
    pygame.draw.rect(window, (0, 0, 0), (715, 40, 140 * tb.pen.pressure, 10), border_bottom_left_radius=br, border_top_left_radius=br)

    window.blit(font.render(f"Azimuth: {round(tb.pen.azimuth, 1)}°", True, (0, 0, 0)), (715, 60))
    window.blit(font.render(f"Tilt:    {round(tb.pen.tilt, 1)}°", True, (0, 0, 0)), (715, 90))

    pygame.display.flip()

pygame.quit()
tb.release()