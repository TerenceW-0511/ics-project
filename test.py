from text import scenes
import pgzero
import pygame

WIDTH = 800
HEIGHT = 450

scene = 0

def draw():
    screen.fill((10, 10, 10))

    # Text box
    screen.draw.filled_rect(
        Rect(40, HEIGHT - 160, WIDTH - 80, 120),
        (35, 35, 35)
    )

    screen.draw.text(
        scenes[scene],
        topleft=(60, HEIGHT - 140),
        width=WIDTH - 120,
        fontsize=24,
        color=(230, 230, 230)
    )

    screen.draw.text(
        "SPACE",
        bottomright=(WIDTH - 20, HEIGHT - 10),
        fontsize=16,
        color=(150, 150, 150)
    )

def on_key_down(key):
    global scene
    if key == keys.SPACE:
        scene += 1
        if scene >= len(scenes):
            quit()

def update():
    pass

pgzrun.go()