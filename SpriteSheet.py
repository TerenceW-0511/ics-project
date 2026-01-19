import pygame

class SpriteSheet:
    def __init__(self, filename):
        self.sheet = pygame.image.load(filename).convert_alpha()

    def image_at(self, x, y, w, h):
        image = pygame.Surface((w, h), pygame.SRCALPHA)
        image.blit(self.sheet, (0, 0), (x, y, w, h))
        return image

    def load_strip(self, x, y, w, h, count):
        return [
            self.image_at(x + i * w, y, w, h)
            for i in range(count)
        ]
