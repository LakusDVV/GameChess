import os
import raylibpy as rl
from typing import Optional, TYPE_CHECKING
from src.paths import IMAGES_DIR
from src.dataclass import Move



if TYPE_CHECKING:
    from src.chessboard import ChessBoard

class RenderComponent:
    def __init__(self, texture):
        self.texture = texture


    def draw(self, *, x, y, tile_size):
        rl.draw_texture(
            texture=self.texture,
            pos_x=x * tile_size,
            pos_y=y * tile_size,
            tint= rl.WHITE
        )


class TextureManager:
    def __init__(self):
        self._textures = {}


    def load_textures(self):
        self._load("black_king",    "black_king.png")
        self._load("black_queen",   "black_queen.png")
        self._load("black_rook",    "black_rook.png")
        self._load("black_bishop",  "black_bishop.png")
        self._load("black_knight",  "black_knight.png")
        self._load("black_pawn",    "black_pawn.png")
        self._load("white_king",    "white_king.png")
        self._load("white_queen",   "white_queen.png")
        self._load("white_rook",    "white_rook.png")
        self._load("white_bishop",  "white_bishop.png")
        self._load("white_knight",  "white_knight.png")
        self._load("white_pawn",    "white_pawn.png")
        self._load("highlighting",  "highlighting_texture.png")


    def _load(self, key: str, filename: str):
        path = os.path.join(IMAGES_DIR, filename)

        if not rl.is_window_ready():
            raise RuntimeError("Window not initialized before loading texture")

        texture = rl.load_texture(path)
        assert texture.id != 0, f"Failed to load texture: {path}"
        self._textures[key] = texture


    def get_texture(self, name):
        return self._textures[name]


class Render:
    """
    Class for draw

    """
    def __init__(self, *, chessboard, texture_manager: TextureManager):
        self.rows = 8
        self.cols = 8
        self.tile_size = 70
        self.radius = self.tile_size // 5.5
        width = self.cols * self.tile_size
        height = self.rows * self.tile_size

        rl.init_window(width, height, "Chess")
        rl.set_target_fps(60)

        self._chessboard: ChessBoard = chessboard
        self.texture_manager= texture_manager
        self.light_color = rl.Color(r=240, g=217, b=181, a=255)
        self.dark_color = rl.Color(r=181, g=136, b=99, a=255)
        self.check_color = rl.Color(r=230, g=41, b=55, a=120)
        self.highlighting_color = rl.Color(r=129, g=151, b=105, a=255)

        self.highlighting_list: list[tuple[int, int]] = []
        self.check_data: dict = {
            "has_data": False,
            "data": ()
        }


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
        self.draw_highlighting()
        self.draw_check_king()

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

        figures = self._chessboard.get_figures()

        for fig in figures:
            fig.draw()


    def draw_highlighting(self) -> None:
        chessboard = self._chessboard
        highlighting_texture = self.texture_manager.get_texture("highlighting")

        for nx, ny in self.highlighting_list:

            cx = nx * self.tile_size + self.tile_size // 2
            cy = ny * self.tile_size + self.tile_size // 2
            tx = nx * self.tile_size
            ty = ny * self.tile_size


            if chessboard.is_empty(x=nx, y=ny):
                rl.draw_circle(
                    center_x=cx,
                    center_y=cy,
                    radius=self.radius,
                    color=self.highlighting_color
                )

            else:
                rl.draw_texture(
                    texture=highlighting_texture,
                    pos_x=tx,
                    pos_y=ty,
                    tint=rl.WHITE
                )


    def draw_check_king(self) -> None:
        if self.check_data["has_data"]:
            x, y = self.check_data["data"]
            rl.draw_rectangle(
                pos_x=x * self.tile_size,
                pos_y=y * self.tile_size,
                width=self.tile_size,
                height=self.tile_size,
                color=self.check_color
            )


    def change_check_data(self, new_pos: tuple[int, int]):
        self.check_data["data"] = new_pos
        self.check_data["has_data"] = True


    def clear_check_data(self):
        self.check_data["data"] = ()
        self.check_data["has_data"] = False


    def change_highlighting(self, new_moves: list[Move]):
        moves = []
        for move in new_moves:
            moves.append(move.to_pos)

        self.highlighting_list = moves


    def clear_highlighting(self) -> None:
        self.highlighting_list.clear()

