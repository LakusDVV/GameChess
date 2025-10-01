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

class Game:
    def __init__(self, rows=8, cols=8, tile_size=70):
        self.rows = rows
        self.cols = cols
        self.tile_size = tile_size
        self.chessboard = Chessboard()
        self.old_x, self.old_y = None, None
        self.mouse_first_right_click = False
        self.ri = {"status": 0, }
        self.chessboard_chess_cords_to_array = None
        self.initialize_convert_board()
        self.motion = True
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
        mouse_y = rl.get_mouse_y()

        if rl.is_mouse_button_pressed(rl.MOUSE_LEFT_BUTTON):
            self.ri = self.mouse_right_button(mouse_x, mouse_y)
            if self.ri["status"] == MoveStatus.MOVED:
                print("Second click, move is successful")
            elif self.ri["status"] == MoveStatus.ERROR:
                print("Error")
            elif self.ri["status"] == MoveStatus.SELECTED:
                print("First click: piece selected")
            elif self.ri["status"] == MoveStatus.WRONG_TURN:
                print("First click: wrong turn")
            elif self.ri["status"] == MoveStatus.EMPTY:
                print("Clicked empty cell")
            self.print_chessboard()


    def draw(self):
        rl.begin_drawing()
        rl.clear_background(rl.RAYWHITE)

        self.chessboard.draw()

        # если выбрана фигура — подсветить доступные ходы
        if self.mouse_first_right_click:
            if self.ri["status"] in (MoveStatus.SELECTED, MoveStatus.WRONG_TURN):
                for x, y in self.ri["available_moves"]:
                    rl.draw_circle(
                        (x + 1) * self.tile_size - self.tile_size / 2,
                        (y + 1) * self.tile_size - self.tile_size / 2,
                        12, self.ri["color"]
                    )

        rl.end_drawing()


    def creating_figures(self):
        # Загружаем текстуры
        black_king_texture = rl.load_texture("images/black_king.png")
        white_king_texture = rl.load_texture("images/white_king.png")
        black_pawn_texture = rl.load_texture("images/black_pawn.png")
        white_pawn_texture = rl.load_texture("images/white_pawn.png")

        # Создаем фигуры
        black_king = s.King(
            color="black",
            texture=black_king_texture,
            board=self.chessboard
        )

        if self.chessboard.redact_board_add(element=black_king, cord=self.convert_board("e8")):
            print("Фигура установлена")
        else:
            print("Клетка занята")

        white_king = s.King(
            color="white",
            texture=white_king_texture,
            cord=self.convert_board("e1"),
            board=self.chessboard
        )

        if self.chessboard.redact_board_add(element=white_king, cord=self.convert_board("e1")):
            print("Фигура установлена")
        else:
            print("Клетка занята")

        for i in range(self.rows):
            x = s.Pawn(
                color="white",
                texture=white_pawn_texture,
                cord=(6, i),
                board=self.chessboard
            )
            if self.chessboard.redact_board_add(element=x, cord=(i, 6)):
                print("Фигура установлена")
            else:
                print("Клетка занята")
        for i in range(self.rows):
            x = s.Pawn(
                color="black",
                texture=black_pawn_texture,
                cord=(i, 1),
                board=self.chessboard
            )
            if self.chessboard.redact_board_add(element=x, cord=(i, 1)):
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

    def _handle_first_click(self, piece, x, y):
        if piece == 0:
            return self._make_response(MoveStatus.EMPTY, None, rl.RED)

        if self.motion != self.color_motion[piece.color]:
            return self._make_response(MoveStatus.WRONG_TURN, piece.draw_move(), rl.BLUE)

        # Всё ок — выбираем фигуру
        self.mouse_first_right_click = True
        self.old_x, self.old_y = x, y
        return self._make_response(MoveStatus.SELECTED, piece.draw_move(), rl.GREEN)

    def _handle_second_click(self, new_x, new_y):
        if (new_x, new_y) not in self.ri["available_moves"]:
            return self._make_response(MoveStatus.ERROR, None, rl.RED)

        success = self.chessboard.redact_board_move(
            old_cord=(self.old_x, self.old_y),
            new_cord=(new_x, new_y)
        )

        if success:
            self.mouse_first_right_click = False
            self.motion = not self.motion
            return self._make_response(MoveStatus.MOVED, None, rl.RED)

        return self._make_response(MoveStatus.ERROR, None, rl.RED)

    def _make_response(self, status, moves, color):
        return {
            "status": status,
            "available_moves": moves,
            "color": color,
        }

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

if __name__ == "game":
    game = Game()
    game.run()