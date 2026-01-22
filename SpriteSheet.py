# Import pygame for image loading and surface operations
import pygame

class SpriteSheet:
    def __init__(self, filename):
        # Load the sprite sheet image and convert to alpha format
        self.sheet = pygame.image.load(filename).convert_alpha()

    def image_at(self, x, y, w, h):
        # Create a new transparent surface with the sprite's dimensions
        image = pygame.Surface((w, h), pygame.SRCALPHA)
        # Copy the sprite from the sheet to the new surface
        image.blit(self.sheet, (0, 0), (x, y, w, h))
        return image  # Return the extracted sprite

    def load_strip(self, x, y, w, h, count):
        return [
            self.image_at(x + i * w, y, w, h)  # Extract sprite at current position
            for i in range(count)  # Loop from 0 to count -1
        ]
