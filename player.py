# player.py
# Import pygame for graphics operations
import pygame
# Import custom Animator class for handling sprite animations
from Animator import Animator

class Player:
    def __init__(self, x, y, animations, scale=3):
        self.animations = animations  # Store animation dictionary
        self.animator = Animator(animations, speed=0.12)  # Create animator with 0.12s per frame
        self.animator.play("idle")  # Start with idle animation
        self.x = x  # Player x position
        self.y = y  # Player y position
        self.facing_left = False  # Direction player is facing (False = right, True = left)
        self.attack_ani = False  # Flag to trigger attack animation
        self.jump_ani = False  # Flag to trigger jump animation
        self.scale = scale  # Sprite scale factor

    def handle_input(self, keys):
        # Lock non looping animations
        if self.animator.current in ("attack", "jump") and not self.animator.finished:
            return  # Exit early, don't process other inputs

        # Check attack  first 
        if self.attack_ani:
            self.animator.play("attack")  # Play attack animation
            self.attack_ani = False  # Reset flag after triggering
        # Check jump  second
        elif self.jump_ani:
            self.animator.play("jump")  # Play jump animation
            self.jump_ani = False  # Reset flag after triggering
        # Check if moving right
        elif keys.get("d", False):
            self.facing_left = False  # Face right
            self.animator.play("walk")  # Play walking animation
        # Check if moving left
        elif keys.get("a", False):
            self.facing_left = True  # Face left
            self.animator.play("walk")  # Play walking animation
        # If no movement keys pressed
        else:
            self.animator.play("idle")  # Play idle animation

    def update(self, dt, keys):

        self.handle_input(keys)  # Update input and animation state
        self.animator.update(dt)  # Update animation frame based on time

    def draw(self, surface):
        frame = self.animator.get_image()  # Get current animation frame
        if frame:  # If there's a valid frame to draw
            if self.facing_left:  # If player is facing left
                frame = pygame.transform.flip(frame, True, False)  # Flip horizontally
            surface.blit(frame, (self.x, self.y))  # Draw the frame at player's position