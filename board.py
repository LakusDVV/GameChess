import raylibpy as rl
from shapes import King, Figure, Rook
import copy



def get_tile_color(x, y):
    light_color = rl.Color(240, 217, 181, 255)
    dark_color = rl.Color(181, 136, 99, 255)
    return light_color if (x + y) % 2 == 0 else dark_color


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
        for piece in self.figures:
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


    def redact_board_move(self, *, new_cord, old_cord, simulate=False, _board=None, _figures=None):
        old_x, old_y = old_cord
        new_x, new_y = new_cord

        # Нельзя ходить в ту же клетку
        if (new_x, new_y) == (old_x, old_y):
            return False


        board = _board if copy.deepcopy(_board) is not None else self.chessboard
        figures = _figures if copy.deepcopy(_figures) is not None else self.figures

        piece = board[old_y][old_x]
        target = board[new_y][new_x]

        # Перемещаем фигуру в копии доски


        if not piece:
            return False

        original_board = copy.deepcopy(board)
        original_figures = copy.deepcopy(figures)

        for f in figures:
            f.board = board


        board[new_y][new_x], board[old_y][old_x] = piece, 0

        if not simulate:
            piece.cord = (new_x, new_y)

        is_king = isinstance(piece, King)

        # Проверка шаха
        if is_king:
            in_check = piece.is_in_check(figures=figures)
        else:
            k: King = self.find_and_return_king(color=piece.get_color(), board=board, figures=figures)
            in_check = k.is_in_check(figures=figures) if k else False

        # --- Проверка рокировки ---
        if is_king and abs(old_x - new_x) == 2 and not simulate:
            step = 1 if new_x > old_x else -1
            sx = range(old_x + step, new_x + step, step)

            # Проверяем, не под шахом ли путь
            for ix in sx:

                snapshot_board = copy.deepcopy(original_board)
                snapshot_figures = copy.deepcopy(original_figures)

                ok = self.redact_board_move(
                    simulate=True,
                    old_cord=old_cord,
                    new_cord=(ix, old_y),
                    _board=snapshot_board,
                    _figures=snapshot_figures
                )

                if not ok:
                    if _board is None:
                        self.chessboard = original_board
                        piece.board = original_board
                    return False

            rook_old_x = 7 if step == 1 else 0
            rook_new_x = new_x - step

            rook_piece = board[old_y][rook_old_x]
            board[old_y][rook_old_x] = 0
            board[old_y][rook_new_x] = rook_piece

            if not simulate:
                # обновляем координаты реальных объектов
                rook_piece.cord = (rook_new_x, old_y)
                piece.cord = (new_x, new_y)
                piece.board = original_board
                rook_piece.board = original_board
                piece.first_move = False

            # если работаем на реальной доске, сохранить изменения в self
            if _board is None:
                self.chessboard = board
                self.update_sync_figures()
                piece.board = original_board

            return True

        # --- Если шах, откат хода ---
        if in_check:
            # откатить рабочую доску
            if _board is None:
                # откатываем self.chessboard до original_board
                self.chessboard = original_board
                piece.board = self
                # не меняем реальные атрибуты piece.cord потому что мы их не трогали в simulate
            else:
                # если работаем на переданной доске, просто вернуть False — вызывающий код это учтёт
                pass
            return False

        # --- Если симуляция, просто вернуть результат ---
        if simulate:
            # не изменяем реальные объекты; если board == self.chessboard, откатим
            if _board is None:
                self.chessboard = original_board
                piece.board = self
            return True

        piece.cord = (new_x, new_y)
        piece.first_move = False
        if target:
            if target in self.figures:
                self.figures.remove(target)

        # если работали с локальной копией (иначе board == self.chessboard уже и так)
        if _board is not None:
            # если кто-то передал _board — это внутренний вызов, не коммитим в self
            return True

        # зафиксировать изменения в self
        self.chessboard = board
        self.figures = figures
        self.update_sync_figures()
        piece.board = self
        return True


    def find_king(self, color, figures = None):
        if figures is None:
            figures = self.figures
        for x in figures:
            if x.color == color and isinstance(x, King):
                return x.get_cord()
        return None



    def update_sync_figures(self):
        self.figures = []
        for row in self.chessboard:
            for piece in row:
                if piece:
                    self.figures.append(piece)


    def find_and_return_king(self, *, color, board = None, figures = None):
        if figures is None:
            figures = self.figures
        if board is None:
            board = self.chessboard
        x, y = self.find_king(color=color, figures=figures)
        return board[y][x]
