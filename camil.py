import pygame
import random
import math
import sys
import os

pygame.init()

# --------------------
# RESOURCE PATH (IMPORTANT FOR EXE)
# --------------------
def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


# --------------------
# IMAGE INPUT (SCHEDULER / EXE SAFE)
# --------------------
IMAGE = "camil.jpeg"

if len(sys.argv) > 1:
    IMAGE = sys.argv[1]

IMAGE = resource_path(IMAGE)


# --------------------
# CONFIG
# --------------------
screen = pygame.display.set_mode((0, 0), pygame.NOFRAME)
WIDTH, HEIGHT = screen.get_size()

pygame.display.set_caption("Pong Screensaver")
clock = pygame.time.Clock()


# --------------------
# SCALE (KEEP ASPECT RATIO)
# --------------------
def scale_image_keep_aspect(img, max_w, max_h):
    rect = img.get_rect()
    scale = min(max_w / rect.width, max_h / rect.height)

    new_size = (
        int(rect.width * scale),
        int(rect.height * scale)
    )

    return pygame.transform.smoothscale(img, new_size)


# --------------------
# LOAD IMAGE
# --------------------
MAX_SIZE = 250

try:
    camil = pygame.image.load(IMAGE).convert_alpha()
    camil = scale_image_keep_aspect(camil, MAX_SIZE, MAX_SIZE)
except:
    print("Failed to load image:", IMAGE)
    raise SystemExit


IMG_W, IMG_H = camil.get_size()


# --------------------
# GAME OBJECT
# --------------------
class GameObject:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.xtog = False
        self.ytog = False
        self.bounces = 0


obj = GameObject(WIDTH // 2, HEIGHT // 2, 10)

corner_counter = 0
pulse = 0
color_pulse = 0


# --------------------
# MOVEMENT
# --------------------
def handle_input(obj):
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        obj.x -= obj.speed
    if keys[pygame.K_RIGHT]:
        obj.x += obj.speed
    if keys[pygame.K_UP]:
        obj.y -= obj.speed
    if keys[pygame.K_DOWN]:
        obj.y += obj.speed


def update_movement(obj):

    if not obj.xtog:
        obj.x += obj.speed
    else:
        obj.x -= obj.speed

    if not obj.ytog:
        obj.y += obj.speed
    else:
        obj.y -= obj.speed


# --------------------
# BOUNCE LOGIC
# --------------------
def handle_bounce(obj):

    global corner_counter

    if (
        (obj.x >= WIDTH - IMG_W or obj.x <= 0)
        and
        (obj.y >= HEIGHT - IMG_H or obj.y <= 0)
    ):
        corner_counter += 1

    if obj.x >= WIDTH - IMG_W:
        obj.xtog = True

        obj.bounces += 1
    elif obj.x <= 0:
        obj.xtog = False
 
        obj.bounces += 1

    if obj.y >= HEIGHT - IMG_H:
        obj.ytog = True

        obj.bounces += 1
    elif obj.y <= 0:
        obj.ytog = False

        obj.bounces += 1



# --------------------
# DRAW
# --------------------
def draw(screen, img, obj):

    global pulse, color_pulse, corner_counter

    x, y = int(obj.x), int(obj.y)

    # --------------------
    # PULSE (FAST)
    # --------------------
    pulse += 0.05
    breathe = (math.sin(pulse) + 1) / 2
    breathe2 = (math.sin(pulse * 1.3) + 1) / 2

    # --------------------
    # COLOR (SLOW)
    # --------------------
    color_pulse += 0.01

    base1 = math.sin(color_pulse * 0.5) * 0.5 + 1
    base2 = math.sin(color_pulse * 0.7 + 10) * 0.5 + 1

    r = max(0, min(255, int(80 + base1 * 120)))
    g = max(0, min(255, int(60 + (2 - base1) * 120)))
    b = max(0, min(255, int(80 + base2 * 140)))

    color = (r, g, b)

    # --------------------
    # GLOW (STABLE)
    # --------------------
    max_dim = max(IMG_W, IMG_H)

    glow_strength = 5 + int(breathe * 6)
    glow_alpha_base = 10 + int(breathe * 50)

    for i in range(glow_strength, 0, -1):

        size = int(max_dim + i * 6)

        glow = pygame.transform.smoothscale(img, (size, size))

        temp = pygame.Surface((size, size), pygame.SRCALPHA)
        rect = glow.get_rect(center=(size // 2, size // 2))
        temp.blit(glow, rect)

        alpha = max(0, glow_alpha_base - i * 4)
        temp.set_alpha(alpha)

        screen.blit(temp, temp.get_rect(center=(x + IMG_W // 2, y + IMG_H // 2)))

    # main image
    screen.blit(img, (x, y))

    # --------------------
    # TEXT (FADE + COLOR)
    # --------------------
    font = pygame.font.SysFont(None, 36)

    alpha = int(breathe * 255)

    text_surface = font.render(
        f"Corner Hits: {corner_counter}",
        True,
        color
    ).convert_alpha()

    text_surface.set_alpha(alpha)

    screen.blit(text_surface, (20, 20))


# --------------------
# MAIN LOOP
# --------------------
running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            running = False

    handle_input(obj)
    update_movement(obj)
    handle_bounce(obj)

    screen.fill((0, 0, 0))

    draw(screen, camil, obj)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
