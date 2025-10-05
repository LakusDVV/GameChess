import raylibpy as rl

class Figure:
    def __init__(self, *, texture, color, cord: (int, int)=(None, None), board=None):
        self.rows, self.cols = 8, 8
        self.tile_size =  70
        self.texture = texture
        self.color = color
        self.board = board
        self.cord = cord
        self.first_move = True


    def draw(self):
        x, y = self.cord

        rl.draw_texture(self.texture, x * self.tile_size, y * self.tile_size, rl.WHITE)


class Pawn(Figure):
    def __init__(self, *, texture, color, cord: (int, int) = (None, None), board=None):
        super().__init__(
            texture=texture,
            color=color,
            cord=cord,
            board=board
        )


    def draw_move(self):
        moves = []
        eat_moves = []
        x, y = self.cord
        board = self.board.get_chessboard()

        # Направление движения зависит от цвета
        direction = -1 if self.color == "white" else 1

        # 1 шаг вперёд
        if self.board.in_bounds(x, y + direction) and board[y + direction][x] == 0:
            moves.append((x, y + direction))

            # 2 шага вперёд, если первый ход
            if self.first_move and self.board.in_bounds(x, y + 2 * direction) and board[y + 2 * direction][x] == 0:
                moves.append((x, y + 2 * direction))

        # Атака по диагонали
        for dx in (-1, 1):
            nx, ny = x + dx, y + direction
            if self.board.in_bounds(nx, ny):
                target = board[ny][nx]
                if target != 0 and target.color != self.color:
                    moves.append((nx, ny))

        return moves


    def __str__(self):
        return "♙" if self.color == "white" else "♟"


class King(Figure):
    def __init__(self, *, texture, color, cord: (int, int) = (None, None), board=None):
        super().__init__(
            texture=texture,
            color=color,
            cord=cord,
            board=board
        )


    def draw_move(self):
        deltas = [(-1, 0), (1, 0), (0, -1), (0, 1),
                  (-1, -1), (-1, 1), (1, -1), (1, 1)]
        moves = []
        x, y = self.cord
        for dy, dx in deltas:
            ny, nx = y + dy, x + dx
            if not self.board.in_bounds(ny, nx):
                continue

            piece = self.board.get_chessboard()[ny][nx]

            if piece == 0:  # пустая клетка
                moves.append((nx, ny))
            elif piece.color != self.color:  # враг
                moves.append((nx, ny))

        return moves


    def __str__(self):
        return "♚" if self.color == "white" else "♔"


class Rook(Figure):
    def __init__(self, *, texture, color, cord: (int, int) = (None, None), board=None):
        super().__init__(
            texture=texture,
            color=color,
            cord=cord,
            board=board
        )

    def draw_move(self):
        moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        x, y = self.cord

        for dx, dy in directions:
            ny, nx = y + dy, x + dx

            if not self.board.in_bounds(ny, nx):
                continue

            while True:
                x += dx
                y += dy

                if not self.board.in_bounds(nx, ny): # проверка выхода за границы
                    break

                piece = self.board.get_chessboard()[ny][nx]

                if piece == 0:  # пустая клетка
                    moves.append((nx, ny))

                elif piece.color != self.color:  # враг
                    moves.append((nx, ny))
                    break

                else:  # своя фигура → стоп
                    break
        return moves

    def __str__(self):
        return "♖" if self.color == "white" else "♜"


class Bishop(Figure):
    def __init__(self, *, texture, color, cord: (int, int) = (None, None), board=None):
        super().__init__(
            texture=texture,
            color=color,
            cord=cord,
            board=board
        )


    def draw_move(self):
        moves = []
        directions = [(1,1), (-1,-1), (-1, 1), (1,-1)]

        x, y = self.cord

        for dx, dy in directions:
            ny, nx = y + dy, x + dx

            if not self.board.in_bounds(ny, nx):
                continue

            while True:
                x += dx
                y += dy

                if not self.board.in_bounds(nx, ny):  # проверка выхода за границы
                    break

                piece = self.board.get_chessboard()[ny][nx]

                if piece == 0:  # пустая клетка
                    moves.append((nx, ny))

                elif piece.color != self.color:  # враг
                    moves.append((nx, ny))
                    break

                else:  # своя фигура → стоп
                    break
        return moves


    def __str__(self):
        return "♗" if self.color == "white" else "♝"


class Knight(Figure):

    def draw_move(self):
        deltas = [(-1, 2), (1, 2), (2, -1), (2, 1),
                  (-1, -2), (1, -2), (-2, -1), (-2, 1)]
        moves = []

        x, y = self.cord

        for dy, dx in deltas:
            ny, nx = y + dy, x + dx

            if not self.board.in_bounds(ny, nx):
                continue

            piece = self.board.get_chessboard()[ny][nx]

            if piece == 0:  # пустая клетка
                moves.append((nx, ny))

            elif piece.color != self.color:  # враг
                moves.append((nx, ny))

        return moves


    def __str__(self):
        return "♘" if self.color == "white" else "♞"


class Queen(Figure):
    def __init__(self, *, texture, color, cord: (int, int) = (None, None), board=None):
        super().__init__(
            texture=texture,
            color=color,
            cord=cord,
            board=board
        )


    def draw_move(self):
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                  (-1, -1), (-1, 1), (1, -1), (1, 1)]

        x, y = self.cord

        for dx, dy in directions:
            ny, nx = y + dy, x + dx

            if not self.board.in_bounds(ny, nx):
                continue

            while True:
                x += dx
                y += dy

                if not self.board.in_bounds(nx, ny):  # проверка выхода за границы
                    break

                piece = self.board.get_chessboard()[ny][nx]

                if piece == 0:  # пустая клетка
                    moves.append((nx, ny))

                elif piece.color != self.color:  # враг
                    moves.append((nx, ny))
                    break

                else:  # своя фигура → стоп
                    break
        return moves


    def __str__(self):
        return "♕" if self.color == "white" else "♛"