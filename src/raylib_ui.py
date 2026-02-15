import raylibpy as rl
from src.render import Render, TextureManager
from src.chess_core.game import Game


class Game_UI:
    def __init__(self):
        self.chess_game = Game()

        self.rows = 8
        self.cols = 8
        self.tile_size = 70
        width = self.cols * self.tile_size
        height = self.rows * self.tile_size

        rl.init_window(width, height, "Chess")
        rl.set_target_fps(60)

        self.texture_manager = TextureManager()

        self.render = Render(chessboard=self.chessboard, texture_manager=self.texture_manager)
        self.texture_manager.load_textures()



    def run(self):
        while not rl.window_should_close():
            self.render.draw()
            self.update()

        rl.close_window()