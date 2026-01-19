# player.py
import pygame
from Animator import Animator

class Player:
    def __init__(self, x,y, animations, scale=3):
        self.animations = animations
        self.animator = Animator(animations, speed=0.12)
        self.animator.play("idle")
        self.x = x
        self.y = y
        self.facing_left = False
        self.attack_requested = False
        self.jump_requested = False
        self.scale = scale

    def handle_input(self, keys):
        # Lock non-looping animations
        if self.animator.current in ("attack", "jump") and not self.animator.finished:
            return

        if self.attack_requested:
            self.animator.play("attack")
            self.attack_requested = False
        elif self.jump_requested:
            self.animator.play("jump")
            self.jump_requested = False
        elif keys.get("d", False):
            self.facing_left = False
            self.animator.play("walk")
        elif keys.get("a", False):
            self.facing_left = True
            self.animator.play("walk")
        else:
            self.animator.play("idle")

    def update(self, dt, keys):
        self.handle_input(keys)
        self.animator.update(dt)

    def draw(self, surface):
        frame = self.animator.get_image()
        if frame:
            if self.facing_left:
                frame = pygame.transform.flip(frame, True, False)
            surface.blit(frame, (self.x,self.y))
