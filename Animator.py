class Animator:
   
    def __init__(self, animations, speed=0.12):
        self.animations = animations  # Store all animations
        self.speed = speed  # delay between animations
        self.current = None  # Name of current animation
        self.frame_index = 0  # Current frame number in the animation
        self.timer = 0  # when to advance to next frame
        self.finished = False  # Flag indicating if animation has completed

    def play(self, name):
        if name != self.current:  # Only switch if it's a different animation
            self.current = name  # Set new animation as current
            self.frame_index = 0  # Reset to first frame
            self.timer = 0  # Reset timer
            self.finished = False  # Mark as not finished

    def update(self, dt):
        # Don't update if no animation is playing or animation has finished
        if self.current is None or self.finished:
            return

        # Get current animation data
        anim = self.animations[self.current]  # Get animation dictionary
        frames = anim["frames"]  # List of sprite frames
        loop = anim["loop"]  # Whether animation should loop or play once
        self.timer += dt  # Add time to timer
        
        # Check if enough time has passed to advance to next frame
        if self.timer >= self.speed:
            self.timer = 0  # Reset timer for next frame
            self.frame_index += 1  # Move to next frame

            # Check if at end of animation
            if self.frame_index >= len(frames):
                if loop:  # If animation loops
                    self.frame_index = 0  # Go back to first frame
                else:  # If animation plays once
                    self.frame_index = len(frames) - 1  # Stay on last frame
                    self.finished = True  # Mark animation as finished

    def get_image(self):
        if self.current is None:  # If no animation is playing
            return None  # Return nothing
        # Return the sprite surface at current index of frame
        return self.animations[self.current]["frames"][self.frame_index]
