import pgzrun
import pygame
from SpriteSheet import SpriteSheet
from player import Player  

WIDTH = 800
HEIGHT = 450
rect = Rect(100, 400,50,50)
rect2 = Rect(40, 400,50, 50)
target_speed = 5
velo_x = 0
velocity_up = 0
gravity = 0.5
ground = 385
on_ground = True
sheet = SpriteSheet("images/AnimationSheet_Character.png")
scale = 2

def scale_frames(frames, scale):
    return [
        pygame.transform.scale(f, (f.get_width() * scale, f.get_height() * scale))
        for f in frames
    ]

# Load and scale frames
idle = scale_frames(sheet.load_strip(0, 0, 32, 32, 2), scale)
walk = scale_frames(sheet.load_strip(0, 96, 32, 32, 8), scale)
attack = scale_frames(sheet.load_strip(0, 256, 32, 32, 8), scale)
jump = scale_frames(sheet.load_strip(0, 160, 32, 32, 8), scale)

animations = {
    "idle": {"frames": idle, "loop": True},
    "walk": {"frames": walk, "loop": True},
    "attack": {"frames": attack, "loop": False},
    "jump": {"frames": jump, "loop": False},
}

player = Player(384, 284, animations)

keys_pressed = {"a": False, "d": False}

def draw():
    screen.fill(("grey"))
    player.draw(screen)
    screen.draw.filled_rect(rect2, "red")

    screen.draw.text("x "+str(rect.x), (20, 100))
    screen.draw.text("y "+str(rect.y), (20, 80))
    screen.draw.text("jump "+str(on_ground), (20, 60))
    screen.draw.text("velo x "+str(velo_x), (20, 120))

def update(dt):
    player.update(dt, keys_pressed)
    player.x = rect.x
    player.y = rect.y
    global velo_x
    global velocity_up
    global on_ground
    collision()
    move()
    jump()
    rect.x += velo_x
    rect.y += velocity_up
    velocity_up += gravity

    if rect.y > ground:
        velocity_up = 0
        rect.y = ground
def move():
    global velo_x
    velo_x = 0
    if keyboard.a:
        velo_x = -target_speed
    if keyboard.d:
        velo_x = target_speed
def jump():
    global velocity_up
    global on_ground

    if keyboard.w and on_ground:
        velocity_up = -15
        on_ground = False
    ground_check()
    rect.y += velocity_up
    velocity_up += gravity

def ground_check():
    global on_ground
    if rect.y >= ground:
        on_ground = True
    else:
        on_ground = False
    
def collision():
    if rect.colliderect(rect2):
        rect.x = 90

def on_key_down(key):
    if key == keys.A:
        keys_pressed["a"] = True
    elif key == keys.D:
        keys_pressed["d"] = True
    elif key == keys.W:
        player.jump_requested = True
    elif key == keys.SPACE:
        player.attack_requested = True

def on_key_up(key):
    if key == keys.A:
        keys_pressed["a"] = False
    elif key == keys.D:
        keys_pressed["d"] = False

def scale_frames(frames, scale):
    return [
        pygame.transform.scale(f, (f.get_width() * scale, f.get_height() * scale))
        for f in frames
    ]

pgzrun.go()
