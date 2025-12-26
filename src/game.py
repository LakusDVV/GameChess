import raylibpy as rl
import shapes
import os

from src.chessboard import ChessBoard
from typing import Optional
from src.enums import MoveResult, PieceColor
from src.paths import IMAGES_DIR
from dataclasses import dataclass






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
        texture = rl.load_texture(path)
        assert texture.id != 0, f"Failed to load texture: {path}"
        self._textures[key] = texture


    def get_texture(self, name):
        return self._textures[name]


class Render:
    """
    Class for draw

    """
    def __init__(self, *, chessboard: ChessBoard, texture_manager: TextureManager):
        self.rows = 8
        self.cols = 8
        self.tile_size = 70
        width = self.cols * self.tile_size
        height = self.rows * self.tile_size

        rl.init_window(width, height, "Chess")
        rl.set_target_fps(60)

        self._chessboard = chessboard
        self.texture_manager= texture_manager
        self.light_color = rl.Color(r=240, g=217, b=181, a=255)
        self.dark_color = rl.Color(r=181, g=136, b=99, a=255)
        self.highlighting_color = rl.Color(r=129, g=151, b=105, a=255)

        self.highlighting: list[tuple[int, int]] = []


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

        figures = self._chessboard.get_figures()

        for fig in figures:
            fig.draw()


    def draw_highlighting(self) -> None:
        chessboard = self._chessboard
        highlighting_texture = self.texture_manager.get_texture("highlighting")

        for nx, ny in self.highlighting:

            if chessboard.is_empty(x=nx, y=ny):
                rl.draw_circle(center_x=nx, center_y=ny, radius=self.tile_size // 5.5, color=self.highlighting_color)
                continue

            rl.draw_texture(texture=highlighting_texture, pos_x=nx, pos_y=ny, tint=rl.WHITE)




# class MoveValidator:
#     def check_move(self, moves: list[Move]) -> list[Move]:
#         right_moves: list[Move] = []
#         for move in moves:






class Game:
    def __init__(self):
        self.rows, self.cols = 8, 8
        self.tile_size = 70

        self.chessboard = ChessBoard()
        self.texture_manager = TextureManager()
        self.texture_manager.load_textures()
        self.render = Render(chessboard=self.chessboard, texture_manager=self.texture_manager)


        self.create_figures()

        self.mouse_first_right_click = False


    def run(self):
        while not rl.window_should_close():
            self.render.draw()

        rl.close_window()


    def update(self):
        mouse_x = rl.get_mouse_x()
        mouse_y = rl.get_mouse_y()

        if rl.is_mouse_button_pressed(rl.MOUSE_LEFT_BUTTON):
            self.mouse_right_button(mouse_x, mouse_y)


    def create_figures(self):
        self.create_white_figures()
        self.create_black_figures()
        self.chessboard.print_board()


    def create_white_figures(self):

        # Create king
        white_king_texture = self.texture_manager.get_texture("white_king")
        x, y = 3, 0
        king = shapes.King(x=x, y=y, texture=white_king_texture, color = PieceColor.WHITE)
        status = self.chessboard.add_figure(x=x, y=y, figure=king)
        view_status_add_figure(status)

        # Create queen
        white_queen_texture = self.texture_manager.get_texture("white_queen")
        x, y = 4, 0
        queen = shapes.Queen(x=x, y=y, texture=white_queen_texture, color = PieceColor.WHITE)
        status = self.chessboard.add_figure(x=x, y=y, figure=queen)
        view_status_add_figure(status)

        # Creates bishops
        white_bishop_texture = self.texture_manager.get_texture("white_bishop")
        x, y = None, 0
        for x in (2, 5):
            bishop = shapes.Bishop(x=x, y=y, texture=white_bishop_texture, color=PieceColor.WHITE)
            status = self.chessboard.add_figure(x=x, y=y, figure=bishop)
            view_status_add_figure(status)

        # Creates knights
        white_knight_texture = self.texture_manager.get_texture("white_knight")
        x, y = None, 0
        for x in (1, 6):
            knight = shapes.Knight(x=x, y=y, texture=white_knight_texture, color=PieceColor.WHITE)
            status = self.chessboard.add_figure(x=x, y=y, figure=knight)
            view_status_add_figure(status)

        # Creates rooks
        white_rook_texture = self.texture_manager.get_texture("white_rook")
        x, y = None, 0
        for x in (0, 7):
            rook = shapes.Rook(x=x, y=y, texture=white_rook_texture, color=PieceColor.WHITE)
            status = self.chessboard.add_figure(x=x, y=y, figure=rook)
            view_status_add_figure(status)

        # Creates pawns
        white_pawn_texture = self.texture_manager.get_texture("white_pawn")
        x, y = None, 1
        for x in range(self.rows):
            pawn = shapes.Pawn(x=x, y=y, texture=white_pawn_texture, color=PieceColor.WHITE)
            status = self.chessboard.add_figure(x=x, y=y, figure=pawn)
            view_status_add_figure(status)


    def create_black_figures(self):

        # Create king
        black_king_texture = self.texture_manager.get_texture("black_king")
        x, y = 3, 7
        king = shapes.King(x=x, y=y, texture=black_king_texture, color = PieceColor.WHITE)
        status = self.chessboard.add_figure(x=x, y=y, figure=king)
        view_status_add_figure(status)

        # Create queen
        black_queen_texture = self.texture_manager.get_texture("black_queen")
        x, y = 4, 7
        queen = shapes.Queen(x=x, y=y, texture=black_queen_texture, color = PieceColor.WHITE)
        status = self.chessboard.add_figure(x=x, y=y, figure=queen)
        view_status_add_figure(status)

        # Creates bishops
        black_bishop_texture = self.texture_manager.get_texture("black_bishop")
        x, y = None, 7
        for x in (2, 5):
            bishop = shapes.Bishop(x=x, y=y, texture=black_bishop_texture, color=PieceColor.WHITE)
            status = self.chessboard.add_figure(x=x, y=y, figure=bishop)
            view_status_add_figure(status)

        # Creates knights
        black_knight_texture = self.texture_manager.get_texture("black_knight")
        x, y = None, 7
        for x in (1, 6):
            knight = shapes.Knight(x=x, y=y, texture=black_knight_texture, color=PieceColor.WHITE)
            status = self.chessboard.add_figure(x=x, y=y, figure=knight)
            view_status_add_figure(status)

        # Creates rooks
        black_rook_texture = self.texture_manager.get_texture("black_rook")
        x, y = None, 7
        for x in (0, 7):
            rook = shapes.Rook(x=x, y=y, texture=black_rook_texture, color=PieceColor.WHITE)
            status = self.chessboard.add_figure(x=x, y=y, figure=rook)
            view_status_add_figure(status)

        # Creates pawns
        black_pawn_texture = self.texture_manager.get_texture("black_pawn")
        x, y = None, 6
        for x in range(self.rows):
            pawn = shapes.Pawn(x=x, y=y, texture=black_pawn_texture, color=PieceColor.WHITE)
            status = self.chessboard.add_figure(x=x, y=y, figure=pawn)
            view_status_add_figure(status)


    def mouse_right_button(self, mouse_x, mouse_y):
        board_x = mouse_x // self.tile_size
        board_y = mouse_y // self.tile_size

        board = self.chessboard.get_board()

        piece = board[board_y][board_x]


        if not self.mouse_first_right_click:
            if piece:
                self._first_click(piece=piece, board_x=board_x, board_y=board_y)


    def _first_click(self, piece, board_x: int, board_y: int):
        pass


    def filter_moves(self, moves: list):
        right_moves: list[Move] = []

        for move in moves:
            mr = MoveRecord(
                piece=move.piece,
                from_pos=move.from_pos,
                to_pos=move.to_pos
            )
            self.chessboard.apply_move(mr)
            king_is_check: bool = self.chessboard.king_is_check(move.piece.color)
            self.chessboard.undo(mr)

            if not king_is_check:
                right_moves.append(move)

        return right_moves



@dataclass
class MoveRecord:
    piece: shapes.Figure
    from_pos: tuple[int, int]
    to_pos: tuple[int, int]

    captured_piece: Optional[shapes.Figure] = None
    captured_pos: Optional[tuple[int, int]] = None

    rook: Optional[shapes.Figure] = None
    rook_from: Optional[tuple[int, int]] = None
    rook_to: Optional[tuple[int, int]] = None


@dataclass
class CastlingRights:
    white_king_side: bool = True
    white_queen_side: bool = True
    black_king_side: bool = True
    black_queen_side: bool = True

    def can_castle_kingside(self, color: PieceColor):
        return (
            self.white_king_side
            if color == PieceColor.WHITE
            else self.black_king_side
        )

    def can_castle_queenside(self, color: PieceColor):
        return (
            self.white_queen_side
            if color == PieceColor.WHITE
            else self.black_queen_side
        )


@dataclass(frozen=True)
class Move:
    piece: shapes.Figure
    from_pos: tuple[int, int]
    to_pos: tuple[int, int]
    special: Optional[str] = None  # "castle_kingside", "castle_queenside", "en_passant", "promotion_pawn", "capture"











def view_status_add_figure(status: MoveResult):
    match status:
        case MoveResult.OK:
            print(f"Figure added")
        case MoveResult.CELL_OCCUPIED:
            print("Cell is not empty")