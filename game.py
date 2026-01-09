import pgzrun


WIDTH = 800
HEIGHT = 450
rect = Rect(100, 400,50, 50)
rect2 = Rect(40, 400,50, 50)
target_speed = 10
velo_x = 0
velocity_up = 0
gravity = 1
ground = 400
on_ground = True

def draw():
    screen.fill((255, 255, 255))
    screen.clear()
    screen.draw.filled_rect(rect, "white")
    screen.draw.filled_rect(rect2, "red")
    screen.draw.text("x "+str(rect.x), (20, 100))
    screen.draw.text("y "+str(rect.y), (20, 80))
    screen.draw.text("jump "+str(on_ground), (20, 60))
    screen.draw.text("velo x "+str(velo_x), (20, 120))
def update():
    global velo_x
    global velocity_up
    global on_ground
    collision()
    move()
    jump()
    rect.x += velo_x
    rect.y += velocity_up
    velocity_up += gravity

    if rect.y > 400:
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

# Start the game
pgzrun.go()