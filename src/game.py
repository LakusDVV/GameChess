import raylibpy as rl
from chessboard import ChessBoard
import shapes
from src.shapes import PieceColor
from src.enums import MoveResult
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(PROJECT_ROOT, "assets")
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")

class TextureManager:
    def __init__(self):
        self._textures = {}


    def load_textures(self):
        self._textures["black_king"] =      rl.load_texture(os.path.join(IMAGES_DIR, "black_king.png"))
        self._textures["black_queen"]=      rl.load_texture(os.path.join(IMAGES_DIR, "black_queen.png"))
        self._textures["black_rook"] =      rl.load_texture(os.path.join(IMAGES_DIR, "black_rook.png"))
        self._textures["black_bishop"] =    rl.load_texture(os.path.join(IMAGES_DIR, "black_bishop.png"))
        self._textures["black_knight"] =    rl.load_texture(os.path.join(IMAGES_DIR, "black_knight.png"))
        self._textures["black_pawn"] =      rl.load_texture(os.path.join(IMAGES_DIR, "black_pawn.png"))
        self._textures["white_king"] =      rl.load_texture(os.path.join(IMAGES_DIR, "white_king.png"))
        self._textures["white_queen"] =     rl.load_texture(os.path.join(IMAGES_DIR, "white_queen.png"))
        self._textures["white_rook"] =      rl.load_texture(os.path.join(IMAGES_DIR, "white_rook.png"))
        self._textures["white_bishop"] =    rl.load_texture(os.path.join(IMAGES_DIR, "white_bishop.png"))
        self._textures["white_knight"] =    rl.load_texture(os.path.join(IMAGES_DIR, "white_knight.png"))
        self._textures["white_pawn"] =      rl.load_texture(os.path.join(IMAGES_DIR, "white_pawn.png"))
        self._textures["highlighting"] =    rl.load_texture(os.path.join(IMAGES_DIR, "highlighting_texture.png"))



    def get_texture(self, name):
        return self._textures[name]


class Render:
    """
    Class for draw

    """
    def __init__(self, *, chessboard: ChessBoard):
        self.rows = 8
        self.cols = 8
        self.tile_size = 70
        width = self.cols * self.tile_size
        height = self.rows * self.tile_size

        rl.init_window(width, height, "Chess")
        rl.set_target_fps(60)

        self.chessboard = chessboard
        self.light_color = rl.Color(r=240, g=217, b=181, a=255)
        self.dark_color = rl.Color(r=181, g=136, b=99, a=255)


    def get_tile_color(self, x: int, y: int) -> rl.Color:
        """
        Returns the color tile for the tile

        Args:
            x (int): cord x tile
            y (int): cord y tile

        Returns:
            rl.Color: the color tile
        """
        return self.light_color if (x + y) % 2 == 0 else self.dark_color


    def draw(self):
        rl.begin_drawing()
        rl.clear_background(rl.RAYWHITE)

        self.draw_tiles()
        self.draw_figures()

        rl.end_drawing()


    def draw_tiles(self) -> None:
        """
        Draw tiles
        """

        for y in range(self.cols):
            for x in range(self.rows):
                color = self.get_tile_color(x, y)
                rl.draw_rectangle(
                    pos_x= x * self.tile_size,
                    pos_y= y * self.tile_size,
                    width= self.tile_size,
                    height= self.tile_size,
                    color= color
                )


    def draw_figures(self) -> None:

        figures = self.chessboard.get_figures()

        for fig in figures:
            fig.draw()




class Game:
    def __init__(self):
        self.rows = 8

        self.chessboard = ChessBoard()
        self.render = Render(chessboard=self.chessboard)
        self.texture_manager = TextureManager()
        self.texture_manager.load_textures()

        self.create_figures()


    def create_figures(self):
        self.create_white_figures()


    def create_white_figures(self):
        white_pawn_texture = self.texture_manager.get_texture("white_pawn")

        for x in range(self.rows):
            pawn = shapes.Pawn(x=x, y=1, texture=white_pawn_texture, color = PieceColor.WHITE)
            status = self.chessboard.add_figure(x=x, y=1, figure=pawn)

            match status:
                case MoveResult.OK:
                    print(f"Figure added on {x} {1}")

                case MoveResult.CELL_OCCUPIED:
                    print("Cell is not empty")

                case _:
                    print("Unknown status")





    def create_black_figures(self):
        pass


    def run(self):
        while not rl.window_should_close():
            self.render.draw()

        rl.close_window()
