import raylibpy as rl


class Chessboard:
    def __init__(self, rows=8, cols=8, tile_size=70):
        self.rows = rows
        self.cols = cols
        self.tile_size = tile_size
        self.light_color = rl.Color(240, 217, 181, 255)
        self.dark_color = rl.Color(181, 136, 99, 255)

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
        self.chessboard = [[0 for _ in range(8)] for _ in range(8)]


    def draw(self):
        for y in range(self.rows):
            for x in range(self.cols):
                color = self.dark_color if (x + y) % 2 == 0 else self.light_color
                rl.draw_rectangle(x * self.tile_size, y * self.tile_size,
                                  self.tile_size, self.tile_size, color)

    def get_cords_for_array(self, chess_cord) -> (int, int):
        x, y = chess_cord
        y = str(int(y) - 1)
        return self.chessboard_chess_cords_to_array[y][x]


    def get_chessboard(self):
        return self.chessboard


    def redact_board_add(self, *, element, cord: (int, int)):
        x, y = cord
        element.cord = (x, y)  # фигура знает где она стоит
        element.board = self  # фигура знает на какой доске
        self.chessboard[y][x] = element


    def redact_board_move(self, *, new_cord, cord):
        x, y = cord
        new_x, new_y = new_cord
        if (new_x, new_y) != (x, y):
            piece = self.chessboard[y][x]
            self.chessboard[new_y][new_x] = piece
            self.chessboard[y][x] = 0
            piece.cord = (new_x, new_y)  # обновляем координаты у фигуры