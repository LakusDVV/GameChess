import copy

import raylibpy as rl
import shapes as s
from board import Chessboard
from enum import Enum


class TextureManager:
    def __init__(self):
        self.textures = {
            "black_king_texture"    :   rl.load_texture("images/black_king.png"),
            "black_queen_texture"   :   rl.load_texture("images/black_queen.png"),
            "black_rook_texture"    :   rl.load_texture("images/black_rook.png"),
            "black_bishop_texture"  :   rl.load_texture("images/black_bishop.png"),
            "black_knight_texture"  :   rl.load_texture("images/black_knight.png"),
            "black_pawn_texture"    :   rl.load_texture("images/black_pawn.png"),
            "white_king_texture"    :   rl.load_texture("images/white_king.png"),
            "white_queen_texture"   :   rl.load_texture("images/white_queen.png"),
            "white_rook_texture"    :   rl.load_texture("images/white_rook.png"),
            "white_bishop_texture"  :   rl.load_texture("images/white_bishop.png"),
            "white_knight_texture"  :   rl.load_texture("images/white_knight.png"),
            "white_pawn_texture"    :   rl.load_texture("images/white_pawn.png"),
            "highlighting_texture"  :   rl.load_texture("images/highlighting_texture.png")
        }

    def get_texture(self, name):
        return self.textures[name]

class MoveStatus(Enum):
    EMPTY = 0         # кликнули по пустой клетке
    MOVED = 1         # успешный ход
    SELECTED = 2      # выбрана фигура (правильный цвет)
    WRONG_TURN = 3    # фигура не того цвета
    ERROR = 4         # ошибка (невалидный ход и т.п.)


def _make_response(status, moves, color):
    return {
        "status": status,
        "moves": moves,
        "color": color,
    }


def get_tile_color(x, y):
    light_color = rl.Color(240, 217, 181, 255)
    dark_color = rl.Color(181, 136, 99, 255)
    return dark_color if (x + y) % 2 == 0 else light_color


def draw_highlight(TM, x, y, tile_size, piece=None):
    cx = x * tile_size + tile_size // 2
    cy = y * tile_size + tile_size // 2
    left = x * tile_size
    top = y * tile_size

    if piece is None:
        # ✅ Подсветка пустой клетки — маленький кружок
        rl.draw_circle(cx, cy, tile_size // 5.5, rl.Color(129, 151, 105, 255)) # rgb(129, 151, 105)
    else:
        rl.draw_texture(TM.get_texture("highlighting_texture"), x * tile_size, y *  tile_size, rl.WHITE)


class Game:
    def __init__(self, rows=8, cols=8, tile_size=70):
        self.rows = rows
        self.cols = cols
        self.tile_size = tile_size
        width = self.cols * self.tile_size
        height = self.rows * self.tile_size

        rl.init_window(width, height, "Chess")
        rl.set_target_fps(60)


        self.chessboard = Chessboard()
        self.TM = TextureManager()
        self.old_x, self.old_y = None, None
        self.mouse_first_right_click = False
        self.ri = {"status": 0, "moves": []}
        self.chessboard_chess_cords_to_array = None
        self.initialize_convert_board()
        self.motion = "white"   # белые начинают партию
        self.color_motion = {"black": 0, "white": 1}



        self.white_king = None
        self.black_king = None
        self.creating_figures()

        self._dick = {
            MoveStatus.MOVED: "Second click, move is successful",
            MoveStatus.ERROR: "Error",
            MoveStatus.SELECTED: "First click: piece selected",
            MoveStatus.WRONG_TURN: "First click: wrong turn",
            MoveStatus.EMPTY: "Clicked empty cell"

        }

    def run(self):
        while not rl.window_should_close():
            self.update()
            self.draw()
        rl.close_window()


    def update(self):
        mouse_x = rl.get_mouse_x()
        mouse_y = rl.get_mouse_y()



        if rl.is_mouse_button_pressed(rl.MOUSE_LEFT_BUTTON):
            self.ri = self.mouse_right_button(mouse_x, mouse_y)

            print(self._dick[self.ri["status"]])

            self.print_chessboard()


    def draw(self):
        rl.begin_drawing()
        rl.clear_background(rl.RAYWHITE)

        # 1. Рисуем доску (только клетки, без фигур)
        self.chessboard.draw_tiles()

        # 2. Подсветка доступных ходов
        if self.mouse_first_right_click:
            if self.ri["status"] in (MoveStatus.SELECTED, MoveStatus.WRONG_TURN):
                for (x, y) in self.ri["moves"]:

                    piece = self.chessboard.get_chessboard()[y][x]
                    draw_highlight(TM=self.TM, x=x, y=y, tile_size=self.tile_size, piece=piece if piece != 0 else None)

        wx, wy = self.chessboard.find_king(color="white")
        if self.chessboard.get_chessboard()[wy][wx].is_in_check(figures=self.chessboard.figures):
            x, y = self.chessboard.find_king(color="white")
            color = rl.Color(230, 41, 55, 120)
            rl.draw_rectangle(x * self.tile_size, y * self.tile_size,
                              self.tile_size, self.tile_size, color)

        bx, by = self.chessboard.find_king(color="black")
        if self.chessboard.get_chessboard()[by][bx].is_in_check(figures=self.chessboard.figures):
            x, y = self.chessboard.find_king(color="black")
            color = rl.Color(230, 41, 55, 120)
            rl.draw_rectangle(x * self.tile_size, y * self.tile_size,
                              self.tile_size, self.tile_size, color)



        # 3. Рисуем фигуры поверх подсветки
        self.chessboard.draw_pieces()

        rl.end_drawing()


    # function for load textures black and white figures and added it on chessboard
    def creating_figures(self):
        """
        casus functions creating_black_figures and creating_white_figures

        Returns:
            None

        """

        # Загружаем текстуры
        self.creating_white_figures()
        self.creating_black_figures()

    # function for load textures black figures and added it on chessboard
    def creating_black_figures(self):
        black_king_texture   = self.TM.get_texture("black_king_texture")
        black_queen_texture  = self.TM.get_texture("black_queen_texture")
        black_rook_texture   = self.TM.get_texture("black_rook_texture")
        black_bishop_texture = self.TM.get_texture("black_bishop_texture")
        black_knight_texture = self.TM.get_texture("black_knight_texture")
        black_pawn_texture   = self.TM.get_texture("black_pawn_texture")

        black_king = s.King(
            color="black",
            texture=black_king_texture,
            board=self.chessboard
        )
        if self.chessboard.redact_board_add(element=black_king, cord=self.convert_board("e8")):
            print("Фигура установлена")
        else: print("Клетка занята")


        black_queen = s.Queen(
            color="black",
            texture=black_queen_texture,
            board=self.chessboard
        )
        if self.chessboard.redact_board_add(element=black_queen, cord=self.convert_board("d8")):
            print("Фигура установлена")
        else: print("Клетка занята")


        black_bishop = s.Bishop(
            color="black",
            texture=black_bishop_texture,
            board=self.chessboard
        )
        copy_black_bishop = copy.deepcopy(black_bishop)
        if self.chessboard.redact_board_add(element=black_bishop, cord=self.convert_board("c8")):
            print("Фигура установлена")
        else: print("Клетка занята")
        if self.chessboard.redact_board_add(element=copy_black_bishop, cord=self.convert_board("f8")):
            print("Фигура установлена")
        else: print("Клетка занята")


        black_knight = s.Knight(
            color="black",
            texture=black_knight_texture,
            board=self.chessboard
        )
        copy_black_knight = copy.deepcopy(black_knight)
        if self.chessboard.redact_board_add(element=black_knight, cord=self.convert_board("b8")):
            print("Фигура установлена")
        else: print("Клетка занята")
        if self.chessboard.redact_board_add(element=copy_black_knight, cord=self.convert_board("g8")):
            print("Фигура установлена")
        else: print("Клетка занята")


        black_rook = s.Rook(
            color="black",
            texture=black_rook_texture,
            board=self.chessboard
        )
        copy_black_rook = copy.deepcopy(black_rook)
        if self.chessboard.redact_board_add(element=black_rook, cord=self.convert_board("a8")):
            print("Фигура установлена")
        else: print("Клетка занята")
        if self.chessboard.redact_board_add(element=copy_black_rook, cord=self.convert_board("h8")):
            print("Фигура установлена")
        else: print("Клетка занята")


        # for i in range(self.rows):
        #     x = s.Pawn(
        #         color="black",
        #         texture=black_pawn_texture,
        #         cord=(i, 1),
        #         board=self.chessboard
        #     )
        #     if self.chessboard.redact_board_add(element=x, cord=(i, 1)):
        #         print("Фигура установлена")
        #     else: print("Клетка занята")

    # function for load textures white figures and added it on chessboard
    def creating_white_figures(self):
        white_king_texture   = self.TM.get_texture("white_king_texture")
        white_queen_texture  = self.TM.get_texture("white_queen_texture")
        white_rook_texture   = self.TM.get_texture("white_rook_texture")
        white_bishop_texture = self.TM.get_texture("white_bishop_texture")
        white_knight_texture = self.TM.get_texture("white_knight_texture")
        white_pawn_texture   = self.TM.get_texture("white_pawn_texture")

        white_king = s.King(
            color="white",
            texture=white_king_texture,
            board=self.chessboard
        )
        if self.chessboard.redact_board_add(element=white_king, cord=self.convert_board("e1")):
            print("Фигура установлена")
        else: print("Клетка занята")


        white_queen = s.Queen(
            color="white",
            texture=white_queen_texture,
            board=self.chessboard
        )
        if self.chessboard.redact_board_add(element=white_queen, cord=self.convert_board("d1")):
            print("Фигура установлена")
        else: print("Клетка занята")


        white_bishop = s.Bishop(
            color="white",
            texture=white_bishop_texture,
            board=self.chessboard
        )
        copy_white_bishop = copy.deepcopy(white_bishop)
        if self.chessboard.redact_board_add(element=white_bishop, cord=self.convert_board("c1")):
            print("Фигура установлена")
        else:
            print("Клетка занята")

        if self.chessboard.redact_board_add(element=copy_white_bishop, cord=self.convert_board("f1")):
            print("Фигура установлена")
        else:
            print("Клетка занята")


        white_knight = s.Knight(
            color="white",
            texture=white_knight_texture,
            board=self.chessboard
        )
        copy_white_knight = copy.deepcopy(white_knight)
        if self.chessboard.redact_board_add(element=white_knight, cord=self.convert_board("b1")):
            print("Фигура установлена")
        else: print("Клетка занята")
        if self.chessboard.redact_board_add(element=copy_white_knight, cord=self.convert_board("g1")):
            print("Фигура установлена")
        else: print("Клетка занята")

        white_rook = s.Rook(
            color="white",
            texture=white_rook_texture,
            board=self.chessboard
        )
        copy_white_rook = copy.deepcopy(white_rook)
        if self.chessboard.redact_board_add(element=white_rook, cord=self.convert_board("a1")):
            print("Фигура установлена")
        else: print("Клетка занята")
        if self.chessboard.redact_board_add(element=copy_white_rook, cord=self.convert_board("h1")):
            print("Фигура установлена")
        else: print("Клетка занята")

        # for i in range(self.rows):
        #     x = s.Pawn(
        #         color="white",
        #         texture=white_pawn_texture,
        #         cord=(i, 6),
        #         board=self.chessboard
        #     )
        #     if self.chessboard.redact_board_add(element=x, cord=(i, 6)):
        #         print("Фигура установлена")
        #     else:
        #         print("Клетка занята")


    def mouse_right_button(self, mouse_x, mouse_y):
        new_x = mouse_x // self.tile_size
        new_y = mouse_y // self.tile_size
        board = self.chessboard.get_chessboard()
        piece = board[new_y][new_x]

        # Первый клик: выбор фигуры
        if not self.mouse_first_right_click:
            return self._handle_first_click(piece, new_x, new_y)

        # Второй клик: попытка сделать ход
        return self._handle_second_click(new_x, new_y)


    def _handle_first_click(self, piece, x, y):

        if piece == 0:
            return _make_response(MoveStatus.EMPTY, None, rl.RED)


        if piece.color != self.motion:  # ❌ не тот цвет хода
            return _make_response(MoveStatus.WRONG_TURN, piece.draw_move(), rl.BLUE)

        # Всё ок — выбираем фигуру
        self.mouse_first_right_click = True
        self.old_x, self.old_y = x, y

        dm = piece.draw_move()
        war_moves: list = []

        for (new_x, new_y) in dm:
            if self.chessboard.redact_board_move(simulate=True, old_cord=(self.old_x, self.old_y), new_cord=(new_x, new_y)):
                war_moves.append((new_x, new_y))


        return _make_response(MoveStatus.SELECTED, war_moves, rl.GREEN)


    def _handle_second_click(self, new_x, new_y):
        moves = self.ri.get("moves") or []
        board = self.chessboard.get_chessboard()
        target = board[new_y][new_x]

        # 🔄 Если нажали на ту же клетку → отменяем выбор
        if (new_x, new_y) == (self.old_x, self.old_y):
            self.mouse_first_right_click = False
            return _make_response(MoveStatus.EMPTY, None, rl.RED)

        # 🎯 Если кликнули на свою другую фигуру → переназначаем выбор
        if target != 0 and target.color == self.motion:
            return self._handle_first_click(target, new_x, new_y)

        # ❌ Если клетка не входит в доступные ходы → снимаем выбор
        if (new_x, new_y) not in moves:
            self.mouse_first_right_click = False
            return _make_response(MoveStatus.EMPTY, None, rl.RED)

        # ✅ Если всё ок → делаем ход
        if (new_x, new_y) != (self.old_x, self.old_y):
            success = self.chessboard.redact_board_move(
                old_cord=(self.old_x, self.old_y),
                new_cord=(new_x, new_y)
            )
        else:
            success = False

        if success:
            self.mouse_first_right_click = False
            # переключаем ход
            self.motion = "black" if self.motion == "white" else "white"
            return _make_response(MoveStatus.MOVED, None, rl.RED)


        self.mouse_first_right_click = False
        return _make_response(MoveStatus.ERROR, None, rl.RED)


    def initialize_convert_board(self):
        y = [str(i) for i in range(self.cols - 1, -1, -1)]
        # self.y = [str(i) for i in range(self.line)]
        x = ["a", "b", "c", "d", "e", "f", "g", "h"]

        self.chessboard_chess_cords_to_array = {
            str(cord_y): {
                cord_x: (int(index_x), int(index_y))
                for index_x, cord_x in enumerate(x)
            }
            for index_y, cord_y in enumerate(y)
        }


    def convert_board(self, chess_cord: str) -> (int, int):
        x, y = chess_cord
        y = str(int(y) - 1)
        return self.chessboard_chess_cords_to_array[y][x]


    def print_chessboard(self):
        for i in self.chessboard.get_chessboard():
            for j in i:
                if j:
                    print(f"{j}", end=" ")
                else:
                    print(f"{j}", end=" ")
            print()
        print()

