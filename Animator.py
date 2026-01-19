class Animator:
    def __init__(self, animations, speed=0.12):
        self.animations = animations
        self.speed = speed

        self.current = None
        self.frame_index = 0
        self.timer = 0
        self.finished = False

    def play(self, name):
        if name != self.current:
            self.current = name
            self.frame_index = 0
            self.timer = 0
            self.finished = False

    def update(self, dt):
        if self.current is None or self.finished:
            return

        anim = self.animations[self.current]
        frames = anim["frames"]
        loop = anim["loop"]

        self.timer += dt
        if self.timer >= self.speed:
            self.timer = 0
            self.frame_index += 1

            if self.frame_index >= len(frames):
                if loop:
                    self.frame_index = 0
                else:
                    self.frame_index = len(frames) - 1
                    self.finished = True

    def get_image(self):
        if self.current is None:
            return None
        return self.animations[self.current]["frames"][self.frame_index]
