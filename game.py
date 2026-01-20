import pgzrun
import pygame
from SpriteSheet import SpriteSheet
from player import Player  
import random

WIDTH = 800
HEIGHT = 450
minigame = False
score = 0
holes = [
    (WIDTH//2 - 200, HEIGHT//2 - 100),
    (WIDTH//2,       HEIGHT//2 - 100),
    (WIDTH//2 + 200, HEIGHT//2 - 100),
    (WIDTH//2 - 200, HEIGHT//2 + 50),
    (WIDTH//2,       HEIGHT//2 + 50),
    (WIDTH//2 + 200, HEIGHT//2 + 50),
]
mole = {"pos": random.choice(holes), "active": True, "timer": 60}  # frames
rect = Rect(350, 185,64,64)
target_speed = 5
velo_x = 0

stage = 1
extra_platform = pygame.Rect((WIDTH//2)-100,250,200,10)
velocity_up = 0
gravity = 0.8
puzzle_solved = False
ground = 331
on_ground = True
sheet = SpriteSheet("images/AnimationSheet_Character.png")
scale = 2
img = pygame.image.load("images/exit.png")
img_scaled = pygame.transform.scale(img, (50, 50))
pygame.image.save(img_scaled, "images/exit_small.png")
exit = Actor('exit_small')
exit_box = Rect(740, 0, 50, 50)
exit.pos = 780, 20
torch_rect = pygame.Rect(720, 50, 50, 50)
dino = Actor('dino')
dino.pos = 80, 320
dino_rect = pygame.Rect(80, 320, 100, 100)
bounding_wall = pygame.Rect(-27, 0, 10, 800)
wall_rects2 = [pygame.Rect(-100, 400,900, 100),pygame.Rect(600, 100, 200, 10)]
wall_rects = [pygame.Rect(-100, 400,900, 100), pygame.Rect(0, 100, 200, 10),pygame.Rect(600, 100, 200, 10) ,pygame.Rect((WIDTH//2)-100,250,200,10)]
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
    global minigame
    if stage == 1:
        screen.clear()
        screen.fill(("grey"))
        player.draw(screen)
        create_platfroms(1)
        createskibidi()
    elif stage == 2:
        screen.clear()
        screen.fill(("grey"))
        player.draw(screen)
        create_platfroms(2)
        dino.draw()
        createskibidi()
        screen.draw.text("press Space".capitalize(), (30, 200), color = "black")
        if puzzle_solved == True:
            screen.draw.filled_rect(torch_rect,"red")
    elif stage == 3 and puzzle_solved == False:
        minigame = True
        screen.fill("grey")
        if minigame:
            for x, y in holes:
                screen.draw.filled_circle((x, y), 40, "brown")
            if mole["active"]:
                x, y = mole["pos"]
                screen.draw.filled_circle((x, y), 30, "green")
                screen.draw.text("Score"+ str(score), (10, 10), fontsize=30, color="white")
            if score > 10:
                exit.draw()
                screen.draw.filled_rect(exit_box,"red")
        createskibidi()

def update(dt):
    player.update(dt, keys_pressed)
    player.x = rect.x
    player.y = rect.y
    global velo_x
    global velocity_up
    global on_ground
    global stage
    platform = []
    
    move()
    jump()
    if stage != 3:
        rect.x += velo_x
        rect.y += velocity_up
        velocity_up += gravity
    if rect.x < -60:
        stage = 2
        rect.x = 795
    elif rect.colliderect(dino_rect) and keyboard.space:
        stage = 3

    if stage == 2:
        platform = wall_rects2
    elif stage == 1:
        platform = wall_rects
        
    while stage == 2 and rect.colliderect(bounding_wall):
        rect.left += 1
    
    for plat in platform:
        if rect.colliderect(plat):
            if velocity_up > 0 and rect.bottom >= plat.top:
                rect.bottom = plat.top
                velocity_up = 0
                on_ground = True
            elif velocity_up < 0 and rect.top <= plat.bottom:
                rect.top = plat.bottom
                velocity_up = 0
    
    if stage == 2 and puzzle_solved == True:
        wall_rects2.append(extra_platform)

    if minigame:
        if mole["active"]:
            mole["timer"] -= 1
            if mole["timer"] <= 0:
                spawn_mole()

def on_mouse_down(pos):
    global score, minigame, puzzle_solved,stage
    if minigame and mole["active"]:
        x, y = mole["pos"]
        if ((pos[0]-x)**2 + (pos[1]-y)**2)**0.5 <= 30:
            score += 1
            spawn_mole()
    if minigame and score > 10 and exit_box.collidepoint(pos):
        minigame = False
        puzzle_solved = True
        stage = 2
        rect.y = 336
        rect.x = 146
def spawn_mole():
    """Place a mole in a random hole and reset timer"""
    mole["pos"] = random.choice(holes)
    mole["active"] = True
    mole["timer"] = 60 
            
        
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
        velocity_up = -17
        on_ground = False

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
def create_platfroms(stage): 
    if stage == 1: 
        platform = wall_rects 
    elif stage == 2: 
        platform = wall_rects2 
    for i in range(len(platform)): 
        screen.draw.filled_rect(platform[i], "green")
    
def createskibidi():
    screen.draw.text("x "+str(rect.x), (20, 100))
    screen.draw.text("y "+str(rect.y), (20, 80))
    screen.draw.text("jump "+str(on_ground), (20, 60))
    screen.draw.text("velo x "+str(velo_x), (20, 120))
    screen.draw.text("stage"+str(stage), (20, 140))
    screen.draw.text("minigame"+str(minigame), (20, 160))
pgzrun.go()
