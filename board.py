import raylibpy as rl
from shapes import King

def get_tile_color(x, y):
    light_color = rl.Color(240, 217, 181, 255)
    dark_color = rl.Color(181, 136, 99, 255)
    return dark_color if (x + y) % 2 == 0 else light_color





class Chessboard:
    def __init__(self, rows=8, cols=8, tile_size=70):
        self.rows = rows
        self.cols = cols
        self.tile_size = tile_size
        self.light_color = rl.Color(240, 217, 181, 255)
        self.dark_color = rl.Color(181, 136, 99, 255)
        self.figures = []


        self.chessboard = [[0 for _ in range(8)] for _ in range(8)]


    def draw_tiles(self):
        for y in range(self.rows):
            for x in range(self.cols):
                color = get_tile_color(x, y)
                rl.draw_rectangle(x * self.tile_size, y * self.tile_size,
                                  self.tile_size, self.tile_size, color)


    def draw_pieces(self):
        for y in range(self.rows):
            for x in range(self.cols):
                piece = self.chessboard[y][x]
                if piece != 0:
                    piece.draw()


    def get_chessboard(self):
        return self.chessboard


    def redact_board_add(self, *, element, cord: (int, int)):
        x, y = cord
        if not self.chessboard[y][x]:
            element.cord = (x, y)  # фигура знает где она стоит
            element.board = self  # фигура знает на какой доске
            self.chessboard[y][x] = element
            self.figures.append(element)
            return 1
        else:
            return 0

    def redact_board_move(self, *, new_cord, old_cord, simulate = False):
        old_x, old_y = old_cord
        new_x, new_y = new_cord

        if (new_x, new_y) == (old_x, old_y):
            return False

        piece = self.chessboard[old_y][old_x]
        target = self.chessboard[new_y][new_x]
        self.chessboard[new_y][new_x], self.chessboard[old_y][old_x] = piece, 0
        piece.cord = (new_x, new_y)

        if isinstance(piece, King):
            in_check = piece.is_in_check(figures=self.figures)

        else:
            k = self.find_and_return_king(color=piece.get_color())
            if k:
                in_check = k.is_in_check(figures=self.figures)
            else:
                in_check = False

        # Если поле хода, король под шахом, то откат
        if in_check:
            self.chessboard[new_y][new_x], self.chessboard[old_y][old_x] = target, piece
            piece.cord = (old_x, old_y)
            return False

        # Если симулируем - откатываем все назад
        if simulate:
            self.chessboard[new_y][new_x], self.chessboard[old_y][old_x] = target, piece
            piece.cord = (old_x, old_y)
            return True


        piece.cord = (new_x, new_y)
        piece.first_move = False

        if target:
            self.figures.remove(target)

        return True





    def find_king(self, color):
        for x in self.figures:
            if x.color == color and isinstance(x, King):
                return x.get_cord()
        return None


    def find_and_return_king(self, color):
        x, y = self.find_king(color=color)
        return self.chessboard[y][x]
