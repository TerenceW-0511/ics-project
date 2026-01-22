# Import libraries
import pgzrun  # Pygame Zero 
import pygame  # Main pygame library 
from SpriteSheet import SpriteSheet  # Custom sprite sheet loader
from player import Player  # Custom player class
import random  # For random number generation 
from text import scenes  # Import story/dialog scenes

#game window
WIDTH = 800  # Game window width in pixels
HEIGHT = 450  # Game window height in pixels

# Cutscene at the start of the game
backgrounds = ["1", "2", "3", "4", "5", "6"]  # List of background image filenames
scaled_bg = []  # Will store scaled background images
current_bg = 0  # Index of displayed background
scene = 0  # Current scene index for story
dialog_surface = pygame.Surface((WIDTH - 80, 120), pygame.SRCALPHA)# Create transparent surface for dialog box
dialog_surface.fill((35, 35, 35, 180)) # Fill with dark gray color 

# Load and scale images
for n in backgrounds:  # Loop through each background filename
    img = pygame.image.load("images/" + n + ".png")  # Load image from file
    img = pygame.transform.scale(img, (WIDTH, HEIGHT))  # Scale to window size
    scaled_bg.append(img)  # Add scaled image to list

# Game state variables
game_started = False  # Flag to track if gameplay has begun
minigame = False  # Flag to track if minigame is active
score = 0  # Player's score in the minigame

# Wack a mole
# Define the position of each hole in minigame 
holes = [
    (WIDTH//2 - 200, HEIGHT//2 - 100),  # Top left hole
    (WIDTH//2,       HEIGHT//2 - 100),  # Top center hole
    (WIDTH//2 + 200, HEIGHT//2 - 100),  # Top right hole
    (WIDTH//2 - 200, HEIGHT//2 + 50),   # Bottom left hole
    (WIDTH//2,       HEIGHT//2 + 50),   # Bottom center hole
    (WIDTH//2 + 200, HEIGHT//2 + 50),   # Bottom right hole
]
# Mole dictionary for: position, active status, and timer countdown
mole = {"pos": random.choice(holes), "active": True, "timer": 60}

# Player variables
rect = Rect(350, 185, 64, 64)  # Player hitbox
target_speed = 5  # Maximum movement speed
velo_x = 0  # Current horizontal velocity

# Lighting in stage 4
VISION = 60  # Radius of light circle around player in dark areas
darkness = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA) # Create surface for darkness later

# Other game variables
stage = 1  # Current game stage/level
extra_platform = pygame.Rect((WIDTH//2)-100, 250, 200, 10) # Extra platform that appears after puzzle is solved
velocity_up = 0  # Vertical velocity
gravity = 0.8  # Gravity applied each frame
puzzle_solved = False  # Flag for whether player has completed puzzle
on_ground = True  # Flag for whether player is standing on a platform

# Main background
bg_img = pygame.image.load("images/brickwall.png")  # Load brick wall image
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))  # Scale to window size

# Player sprite
sheet = SpriteSheet("images/AnimationSheet_Character.png")  # Load sprite sheet
scale = 2  # Scale player sprite

# Exit button for wack a mole minigame
img = pygame.image.load("images/exit.png")  # Load exit image
img_scaled = pygame.transform.scale(img, (50, 50))  # Scale to 50x50 pixels
pygame.image.save(img_scaled, "images/exit_small.png")  # Save scaled version
exit = Actor('exit_small')  # Create Actor for exit button
exit_box = Rect(740, 0, 50, 50)  # Hitbox for exit button
exit.pos = 780, 20  # Position exit button on screen

# Light fragment for stage 2
img = pygame.image.load("images/light_frag.png")  # Load light fragment image
img_scaled = pygame.transform.scale(img, (50, 50))  # Scale to 50x50 pixels
pygame.image.save(img_scaled, "images/light_small.png")  # Save scaled version
light_frag = Actor('light_small')  # Create Actor for light fragment
light_frag.pos = 720, 50  # Position light fragment on screen
light_box = pygame.Rect(720, 50, 50, 50)  # Hitbox for light fragment
light = False  # Flag if player has collected light fragment

# Wall for stage 4
maze_rect = pygame.Rect(200, 0, 10, 240)  # Vertical wall in maze area

# Door for stage 4
img = pygame.image.load("images/door.png")  # Load door image
img_scaled = pygame.transform.scale(img, (100, 150))  # Scale to 100x150 pixels
pygame.image.save(img_scaled, "images/door_small.png")  # Save scaled version
door = Actor('door_small')  # Create Actor for door
door.pos = 700, 45  # Position door on screen
door_box = pygame.Rect(660, 50, 70, 50)  # Hitbox for door interaction

# Dinosaur npc in stage 2
dino = Actor('dino')  # Create Actor for dinosaur NPC
dino.pos = 80, 320  # Position dinosaur on screen
dino_rect = pygame.Rect(80, 320, 100, 100)  # Hitbox for dinosaur interaction
bounding_wall = pygame.Rect(-27, 0, 10, 800)  # Left boundary wall for stage 2

# Platforms for stage 4
wall_rects3 = [
    pygame.Rect(-100, 400, 1100, 100),  # Ground/floor
    pygame.Rect(600, 100, 200, 10),      # Top right platform
    pygame.Rect(500, 240, 440, 10),      # Mid right platform
    pygame.Rect(0, 320, 740, 10),        # Lower platform
    pygame.Rect(0, 240, 400, 10)         # Mid left platform
]

# Platforms for stage 2
wall_rects2 = [
    pygame.Rect(-100, 400, 1100, 100),  # Ground/floor
    pygame.Rect(600, 100, 200, 10)       # Top right platform
]

# Platforms for stage 1
wall_rects = [
    pygame.Rect(-100, 400, 1100, 100),      # Ground/floor
    pygame.Rect(0, 100, 200, 10),           # Top left platform
    pygame.Rect(600, 100, 200, 10),         # Top right platform
    pygame.Rect((WIDTH//2)-100, 250, 200, 10)  # Center platform
]

# Scale sprite
def scale_frames(frames, scale):
    scaled_frames = []
    for f in frames:
        scaled_frame = pygame.transform.scale(f, (f.get_width() * scale, f.get_height() * scale))
        scaled_frames.append(scaled_frame)
    return scaled_frames

# Load idle animation 
idle = scale_frames(sheet.load_strip(0, 0, 32, 32, 2), scale)
# Load walk animation
walk = scale_frames(sheet.load_strip(0, 96, 32, 32, 8), scale)
# Load attack animation 
attack = scale_frames(sheet.load_strip(0, 256, 32, 32, 8), scale)
# Load jump animation
jump = scale_frames(sheet.load_strip(0, 160, 32, 32, 8), scale)

# Store all animations with their frames and loop settings
animations = {
    "idle": {"frames": idle, "loop": True},      # Idle loops continuously
    "walk": {"frames": walk, "loop": True},      # Walk loops continuously
    "attack": {"frames": attack, "loop": False}, # Attack plays once
    "jump": {"frames": jump, "loop": False},     # Jump plays once
}

# Create player object with animations
player = Player(384, 284, animations)  # Create player at position (384, 284)
keys_pressed = {"a": False, "d": False}  # Track which movement keys are held

def draw():
    global minigame  # Access minigame state variable
    
    # Draw cutscenes
    if not game_started:  # If still in story
        screen.blit(scaled_bg[current_bg], (0, 0))  # Draw current background
        screen.blit(dialog_surface, (40, HEIGHT - 160))  # Draw dialog box

        # Draw current scene text inside dialog box
        screen.draw.text(
            scenes[scene],  # Text from current scene
            (60, HEIGHT - 140),  # Position inside dialog box
            width=WIDTH - 120,  # Maximum text width
            fontsize=24,  # Font size
            color=(230, 230, 230)  # Light gray color
        )

        # Draw "SPACE"
        screen.draw.text(
            "SPACE",
            (WIDTH - 90, HEIGHT - 60),
            fontsize=16,
            color=(150, 150, 150)
        )
    
    # Stage 1
    elif stage == 1:
        screen.clear()  # Clear screen
        screen.blit(bg_img, (0, 0))  # Draw brick wall background
        player.draw(screen)  # Draw player character
        create_platforms(1)  # Draw stage 1 platforms
        createskibidi()  # Draw debug info
    
    # STAGE 2 
    elif stage == 2:
        screen.clear()  # Clear screen
        screen.blit(bg_img, (0, 0))  # Draw brick wall background
        player.draw(screen)  # Draw player character
        create_platforms(2)  # Draw stage 2 platforms
        dino.draw()  # Draw dinosaur NPC
        createskibidi()  # Draw debug info
        # Draw interaction text
        screen.draw.text("press Space to interact".capitalize(), (30, 200), color="white")
        # If puzzle completed, draw the light fragment
        if puzzle_solved:
            light_frag.draw()
    
    # STAGE 3
    elif stage == 3 and puzzle_solved == False:  # Only if puzzle not yet solved
        minigame = True  # Enable minigame mode
        screen.fill("grey")  # Gray background for minigame
        
        if minigame:  # If minigame is active
            # Draw all holes as brown circles
            for x, y in holes:
                screen.draw.filled_circle((x, y), 40, "brown")
            
            # If mole is currently visible
            if mole["active"]:
                x, y = mole["pos"]  # Get mole position
                screen.draw.filled_circle((x, y), 30, "green")  # Draw mole as green circle
                # Display current score
                screen.draw.text("Score" + str(score), (10, 10), fontsize=30, color="white")
            
            # If player has scored enough points, show exit button
            if score > 10:
                exit.draw()  # Draw exit button
        
        createskibidi()  # Draw debug info
    
    # STAGE 4 - DARK MAZE AREA
    elif stage == 4:
        screen.clear()  # Clear screen
        screen.blit(bg_img, (0, 0))  # Draw brick wall background
        screen.draw.filled_rect(maze_rect, "#676b6f")  # Draw wall to block player
        create_platforms(4)  # Draw stage 4 platforms
        door.draw()  # Draw exit door
        player.draw(screen)  # Draw player character
        darkness.fill((0, 0, 0, 220))  # Fill with almost opaque black

        # If player has light fragment, create vision circle
        if light:
            pygame.draw.circle(
                darkness,  # Draw on darkness surface
                (0, 0, 0, 0),  # Fully transparent black (creates hole)
                (player.x + 25, player.y + 25),  # Center on player
                VISION  # Radius of vision circle
)

        screen.blit(darkness, (0, 0))  # Apply darkness overlay to screen
        createskibidi()  # Draw debug info
    
    # Stage 5 / end screen
    elif stage == 5:
        screen.clear()  # Clear screen
        draw_end_screen()  # Draw victory screen

def update(dt):
    global velo_x, stage, velocity_up, on_ground, light  # Access global variables
    
    # Update player animation and state
    player.update(dt, keys_pressed)
    # Sync player position with rectangle hitbox
    player.x = rect.x
    player.y = rect.y
    
    platform = []  # Initialize platform list

    # Handle player movement if game has started
    if game_started:
        move()

    jump()  # Handle jump input
    
    # Apply movement and gravity 
    if stage != 3: # If minigame is not active
        rect.x += velo_x  # Apply horizontal velocity
        rect.y += velocity_up  # Apply vertical velocity
        velocity_up += gravity  # Apply gravity to vertical velocity
    
    # Stage 1 to Stage 2
    if stage == 1 and rect.right < 0:
        stage = 2  # Change to stage 2
        rect.left = WIDTH  # Appear on right side of screen
    
    # Stage 2 to Stage 1
    elif stage == 2 and rect.left > WIDTH:
        stage = 1  # Change to stage 1
        rect.right = 0  # Appear on left side of screen
    
    # Stage 1 to Stage 4
    elif stage == 1 and rect.left > WIDTH:
        stage = 4  # Change to stage 4
        rect.x = -40  # Appear on left side
    
    # Stage 4 to Stage 1
    elif stage == 4 and rect.right < 0:
        stage = 1  # Change to stage 1
        rect.left = WIDTH  # Appear on right side
    
    # Collision with hitboxes
    if stage == 2:
        # Interact with dinosaur to start minigame
        if rect.colliderect(dino_rect) and keyboard.space:
            stage = 3  # Go to minigame
        # Collect light fragment
        elif rect.colliderect(light_box) and keyboard.space:
            light = True  # Mark light as collected
    if stage == 4:
        # Interact with door to finish game
        if rect.colliderect(door_box) and keyboard.space:
            stage = 5  # Go to end screen

    if rect.colliderect(maze_rect) and stage == 4:
        if velo_x > 0:  # Moving right
            rect.right = maze_rect.left  # Stop at left wall
        elif velo_x < 0:  # Moving left
            rect.left = maze_rect.right  # Stop at right wall
    
    # Prevent player from going too far right in stage 4
    if rect.left > WIDTH and stage == 4:
        rect.x = WIDTH  

    # Chooses which platforms are used in a stage 
    if stage == 2:
        platform = wall_rects2  # Use stage 2 platforms
    elif stage == 1:
        platform = wall_rects  # Use stage 1 platforms
    elif stage == 4:
        platform = wall_rects3  # Use stage 4 platforms

    # Push player right if they hit the left wall in stage 2
    while stage == 2 and rect.colliderect(bounding_wall):
        rect.left += 1  # Move player right by 1 pixel
    
    # Platform collision
    for plat in platform:  # Check each platform
        if rect.colliderect(plat):  # If player collides with platform
            # Landing on top of platform
            if velocity_up > 0 and rect.bottom >= plat.top:
                rect.bottom = plat.top  # Place player on platform
                velocity_up = 0  # Stop vertical movement
                on_ground = True  # Mark player as grounded
            # Hitting bottom of platform
            elif velocity_up < 0 and rect.top <= plat.bottom:
                rect.top = plat.bottom  # Stop at platform bottom
                velocity_up = 0  # Stop vertical movement
    
    # Extra platform after minigame is complete
    if stage == 2 and puzzle_solved:
        wall_rects2.append(extra_platform)  # Add platform to stage 2

    # whack a mole timer
    if minigame:  # If minigame is active
        if mole["active"]:  # If mole is visible
            mole["timer"] -= 1  # Countdown timer
            if mole["timer"] <= 0:  # Timer expired
                spawn_mole()  # Spawn new mole in different hole

# Mouse clicking during minigane
def on_mouse_down(pos):
    global score, minigame, puzzle_solved, stage  # Access global variables
    if minigame and mole["active"]:  # If in minigame and mole is visible
        x, y = mole["pos"]  # Get mole position
        # Calculate distance from click to mole center
        if ((pos[0]-x)**2 + (pos[1]-y)**2)**0.5 <= 30:  # If within mole radius
            score += 1  # Increment score
            spawn_mole()  # Spawn new mole
    if minigame and score > 10 and exit_box.collidepoint(pos):  # Click exit after winning
        minigame = False  # Disable minigame
        puzzle_solved = True  # Mark puzzle as complete
        stage = 2  # Return to stage 2
        rect.y = 336  # Set player Y position
        rect.x = 146  # Set player X position

# Function to spawn a mole in a hole
def spawn_mole():
    mole["pos"] = random.choice(holes)  # Choose random hole position
    mole["active"] = True  # Make mole visible
    mole["timer"] = 60  # Reset countdown timer to 60 frames

# Function to move the player
def move():
    global velo_x  # Access horizontal velocity variable
    velo_x = 0  # Reset velocity to zero
    if keyboard.a:  # If A key is pressed
        velo_x = -target_speed  # Move left
    if keyboard.d:  # If D key is pressed
        velo_x = target_speed  # Move right

# Function to make the player jump
def jump():
    global velocity_up  # Access vertical velocity
    global on_ground  # Access ground state

    if keyboard.w and on_ground:  # If W pressed and player is on ground
        velocity_up = -17  # Apply horizontal velocity 
        on_ground = False  # Mark player as airborne

# Function to toggle animations and next cutscene
def on_key_down(key):
    global scene, current_bg, stage, game_started  # use global variables
    
    if not game_started and key == keys.SPACE:  # If in intro and space pressed
        scene += 1  # Advance to next scene
        current_bg += 1  # Change background

        if scene >= len(scenes):  # If all scenes shown
            stage = 1  # Start at stage 1
            game_started = True  # Begin gameplay
            scene = len(scenes) - 1  # Lock scene to last one
            current_bg = len(scaled_bg) - 1  # Lock background to last one
        else:
            current_bg %= len(scaled_bg)  # Wrap background index

    if key == keys.A:  # A key pressed
        keys_pressed["a"] = True  # Mark as pressed
    elif key == keys.D:  # D key pressed
        keys_pressed["d"] = True  # Mark as pressed
    elif key == keys.W:  # W key pressed
        player.jump_ani = True  # set jump animation to true
    elif key == keys.SPACE:  # Space key pressed
        player.attack_ani = True  # set attack animation to true

# Prebuilt function to end animation
def on_key_up(key):
    if key == keys.A:  # A key released
        keys_pressed["a"] = False  # Mark as not pressed
    elif key == keys.D:  # D key released
        keys_pressed["d"] = False  # Mark as not pressed

# Function to display the ending screen
def draw_end_screen():
    """Draw the victory screen"""
    screen.fill("black")  # Black background

    # Draw end message in center of screen
    screen.draw.text(
        "YOU ESCAPED!",
        center=(WIDTH // 2, HEIGHT // 2 - 40),  # Centered position
        fontsize=64,  # Large font
        color="white"  # White text
    )

# Function to create platfroms in each stage
def create_platforms(stage):
    """
    Draw platforms for the specified stage
    Args:
        stage: Stage number (1, 2, or 4)
    """
    if stage == 1:  # Stage 1 platforms
        platform = wall_rects
    elif stage == 2:  # Stage 2 platforms
        platform = wall_rects2
    elif stage == 4:  # Stage 4 platforms
        platform = wall_rects3
    
    # Draw each platform as a filled rectangle
    for i in range(len(platform)):
        screen.draw.filled_rect(platform[i], "#676b6f")  # Gray color

# Display debugging info
def createskibidi(): 
    """Draw debug information on screen"""
    # Display whether light fragment is collected
    screen.draw.text("light fragment aquired " + str(light), (20, 40))
    # Display player X position
    screen.draw.text("x " + str(rect.x), (20, 100))
    # Display player Y position
    screen.draw.text("y " + str(rect.y), (20, 80))
    # Display whether player is on ground
    screen.draw.text("jump " + str(on_ground), (20, 60))
    # Display horizontal velocity
    screen.draw.text("velo x " + str(velo_x), (20, 120))
    # Display current stage
    screen.draw.text("stage" + str(stage), (20, 140))
    # Display minigame state
    screen.draw.text("minigame" + str(minigame), (20, 160))

pgzrun.go()  # Run the game
