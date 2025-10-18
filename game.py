import copy

import raylibpy as rl
import shapes as s
from board import Chessboard
from enum import Enum


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


class Game:
    def __init__(self, rows=8, cols=8, tile_size=70):
        self.rows = rows
        self.cols = cols
        self.tile_size = tile_size
        self.chessboard = Chessboard()
        self.old_x, self.old_y = None, None
        self.mouse_first_right_click = False
        self.ri = {"status": 0, "moves": []}
        self.chessboard_chess_cords_to_array = None
        self.initialize_convert_board()
        self.motion = "white"   # белые начинают партию
        self.color_motion = {"black": 0, "white": 1}

        width = self.chessboard.cols * self.chessboard.tile_size
        height = self.chessboard.rows * self.chessboard.tile_size
        rl.init_window(width, height, "Chess")
        rl.set_target_fps(60)
        self.white_king = None
        self.black_king = None
        self.creating_figures()


    def run(self):
        while not rl.window_should_close():
            self.update()
            self.draw()
        rl.close_window()


    def update(self):
        mouse_x = rl.get_mouse_x()
        mouse_y = rl.get_mouse_y()\

        _dick = {
            MoveStatus.MOVED: "Second click, move is successful",
            MoveStatus.ERROR: "Error",
            MoveStatus.SELECTED: "First click: piece selected",
            MoveStatus.WRONG_TURN: "First click: wrong turn",
            MoveStatus.EMPTY: "Clicked empty cell"

        }

        if rl.is_mouse_button_pressed(rl.MOUSE_LEFT_BUTTON):
            self.ri = self.mouse_right_button(mouse_x, mouse_y)

            print(_dick[self.ri["status"]])

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
                    self.draw_highlight(x, y, self.tile_size, piece if piece != 0 else None)

        # 3. Рисуем фигуры поверх подсветки
        self.chessboard.draw_pieces()

        rl.end_drawing()


    def creating_figures(self):
        # Загружаем текстуры
        self.creating_white_figures()
        self.creating_black_figures()


    def creating_black_figures(self):
        black_king_texture = rl.load_texture("images/black_king.png")
        black_queen_texture = rl.load_texture("images/black_queen.png")
        black_rook_texture = rl.load_texture("images/black_rook.png")
        black_bishop_texture = rl.load_texture("images/black_bishop.png")
        black_knight_texture = rl.load_texture("images/black_knight.png")
        black_pawn_texture = rl.load_texture("images/black_pawn.png")

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


        for i in range(self.rows):
            x = s.Pawn(
                color="black",
                texture=black_pawn_texture,
                cord=(i, 1),
                board=self.chessboard
            )
            if self.chessboard.redact_board_add(element=x, cord=(i, 1)):
                print("Фигура установлена")
            else: print("Клетка занята")


    def creating_white_figures(self):
        white_king_texture = rl.load_texture("images/white_king.png")
        white_queen_texture = rl.load_texture("images/white_queen.png")
        white_rook_texture = rl.load_texture("images/white_rook.png")
        white_bishop_texture = rl.load_texture("images/white_bishop.png")
        white_knight_texture = rl.load_texture("images/white_knight.png")
        white_pawn_texture = rl.load_texture("images/white_pawn.png")

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

        for i in range(self.rows):
            x = s.Pawn(
                color="white",
                texture=white_pawn_texture,
                cord=(i, 6),
                board=self.chessboard
            )
            if self.chessboard.redact_board_add(element=x, cord=(i, 6)):
                print("Фигура установлена")
            else:
                print("Клетка занята")


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


    def draw_highlight(self, x, y, tile_size, piece=None):
        cx = x * tile_size + tile_size // 2
        cy = y * tile_size + tile_size // 2
        left = x * tile_size
        top = y * tile_size

        if piece is None:
            # ✅ Подсветка пустой клетки — маленький кружок
            rl.draw_circle(cx, cy, tile_size // 5.5, rl.Color(0, 255, 0, 120))
        else:
            # ✅ Подсветка занятой клетки — рамка по краям
            # Рисуем зелёный полупрозрачный квадрат
            rl.draw_rectangle(left, top, tile_size, tile_size, rl.Color(0, 255, 0, 100))

            # Вырезаем центр, закрашивая цветом клетки
            base_color = get_tile_color(x, y)  # например, светлая/тёмная клетка
            rl.draw_circle(cx, cy, tile_size // 1.95, base_color)


    def _handle_first_click(self, piece, x, y):
        if piece == 0:
            return _make_response(MoveStatus.EMPTY, None, rl.RED)

        if piece.color != self.motion:  # ❌ не тот цвет хода
            return _make_response(MoveStatus.WRONG_TURN, piece.draw_move(), rl.BLUE)

        # Всё ок — выбираем фигуру
        self.mouse_first_right_click = True
        self.old_x, self.old_y = x, y
        return _make_response(MoveStatus.SELECTED, piece.draw_move(), rl.GREEN)


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
            self.old_x, self.old_y = new_x, new_y
            return _make_response(MoveStatus.SELECTED, target.draw_move(), rl.GREEN)

        # ❌ Если клетка не входит в доступные ходы → снимаем выбор
        if (new_x, new_y) not in moves:
            self.mouse_first_right_click = False
            return _make_response(MoveStatus.EMPTY, None, rl.RED)

        # ✅ Если всё ок → делаем ход
        success = self.chessboard.redact_board_move(
            old_cord=(self.old_x, self.old_y),
            new_cord=(new_x, new_y)
        )

        if success:
            self.mouse_first_right_click = False
            # переключаем ход
            self.motion = "black" if self.motion == "white" else "white"
            return _make_response(MoveStatus.MOVED, None, rl.RED)

        # ❌ Ошибка хода → снимаем выделение
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


    def implementing_sequence_of_moves(self):
        pass


    def print_chessboard(self):
        for i in self.chessboard.get_chessboard():
            for j in i:
                print(j, end=" ")
            print()
        print()

