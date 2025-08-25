import raylibpy as rl
import shapes as s
from board import Chessboard


class Game:
    def __init__(self, rows=8, cols=8, tile_size=70):
        self.rows = rows
        self.cols = cols
        self.tile_size = tile_size
        self.chessboard = Chessboard()
        self.nx, self.ny = None, None

        self.ri = []
        self.chessboard_chess_cords_to_array = None
        self.initialize_convert_board()

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
            print(mouse_x, mouse_y)
            self.ri = self.mouse_right_button(mouse_x, mouse_y)


    def draw(self):
        rl.begin_drawing()
        rl.clear_background(rl.RAYWHITE)

        self.chessboard.draw()

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
        # self.chessboard.redact_board_add(element=black_king, cord=self.convert_board("e8"))
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
        # self.chessboard.redact_board_add(element=white_king, cord=self.convert_board("e8"))
        if self.chessboard.redact_board_add(element=white_king, cord=self.convert_board("e8")):
            print("Фигура установлена")
        else:
            print("Клетка занята")


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


    def mouse_right_button(self, mouse_x, mouse_y):
        self.t = False
        new_x = mouse_x // self.tile_size
        new_y = mouse_y // self.tile_size

        print(self.nx, self.ny, new_x, new_y)

        if self.nx and self.ny:
            try:
                self.chessboard.get_chessboard()[self.ny][self.nx].move(new_cord=(new_x, new_y))

                for i in self.chessboard.get_chessboard():
                    for j in i:
                        print(j, end=" ")
                    print()
                print()

                self.t = True
            except Exception as e:
                print("Перемещение не удалось", e)
                self.t = False

        if not self.t:
            self.nx = new_x
            self.ny = new_y
            try:

                for i in self.chessboard.get_chessboard():
                    for j in i:
                        print(j, end=" ")
                    print()
                print()
                return self.chessboard.get_chessboard()[new_y][new_x].draw_move()

            except Exception as e:
                print("Перемещение не удалось", e)
                return  []
        else:
            self.nx = None
            self.ny = None
            return []


if __name__ == "game":
    game = Game()
    game.run()