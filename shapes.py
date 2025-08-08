import raylibpy as rl

class Pawn:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.texture = rl.load_texture("pawn.jpg")

    def draw(self):
        rl.draw_texture(self.texture, self.x, self.y, rl.WHITE)