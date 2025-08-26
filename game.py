import raylibpy as rl
import shapes as s
from board import Chessboard


class Game:
    def __init__(self, rows=8, cols=8, tile_size=70):
        self.rows = rows
        self.cols = cols
        self.tile_size = tile_size
        self.chessboard = Chessboard()
        self.old_x, self.old_y = None, None
        self.mouse_first_right_click = False
        self.ri = []
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
            if self.ri[0] == 2:
                if self.ri[1]:
                    print("Second click, move is successful")
                else:
                    print("Error")
            else:
                print("First click")


    def draw(self):
        rl.begin_drawing()
        rl.clear_background(rl.RAYWHITE)

        self.chessboard.draw()

        if self.mouse_first_right_click:
            for x, y in self.ri:
                rl.draw_circle(
                    (x + 1) * self.tile_size - self.tile_size / 2,
                    (y + 1) * self.tile_size - self.tile_size / 2,
                    12, rl.GREEN
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


    def mouse_right_button(self, mouse_x, mouse_y):
        new_x = mouse_x // self.tile_size
        new_y = mouse_y // self.tile_size

        print(self.old_x, self.old_y, new_x, new_y)


        if not self.mouse_first_right_click:
            try:
                if self.motion == self.color_motion[self.chessboard.get_chessboard()[new_y][new_x].color]:

                    self.mouse_first_right_click = True
                    self.old_x = new_x
                    self.old_y = new_y

                    for i in self.chessboard.get_chessboard():
                        for j in i:
                            print(j, end=" ")
                        print()
                    print()
                    return self.chessboard.get_chessboard()[new_y][new_x].draw_move()
                else:
                    return [6, False]
            except Exception as e:
                print("Пустая клетка", e)
                return [4, False]
        else:
            self.mouse_first_right_click = False

            try:
                self.chessboard.redact_board_move(old_cord=(self.old_x, self.old_y), new_cord=(new_x, new_y))
                self.motion = not self.motion
            except Exception as e:
                print("Перемещение не удалось", e)
                return [2, False]

            for i in self.chessboard.get_chessboard():
                for j in i:
                    print(j, end=" ")
                print()
            print()
            return [2, True]


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

if __name__ == "game":
    game = Game()
    game.run()