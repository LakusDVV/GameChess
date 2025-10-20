import raylibpy as rl


def in_bounds(x, y):
    return 0 <= x < 8 and 0 <= y < 8


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

    def draw_move(self):
        moves = []
        x, y = self.cord
        board = self.board.get_chessboard()

        # Направление движения зависит от цвета
        direction = -1 if self.color == "white" else 1


        self.append_attack_move(moves=moves, x=x, y=y, board=board, direction=direction, get_all=False)
        self.append_motion_moves(moves=moves, x=x, y=y, board=board, direction=direction)

        return moves

    # Return all cells that the pawn can resemble and attack, even if there is no piece of a different color on them.
    def get_attack_moves(self):
        """
        Return all cells that the pawn can resemble and attack, even if there is no piece of a different color on them.
        """

        moves = []
        x, y = self.cord
        board = self.board.get_chessboard()

        # Направление движения зависит от цвета
        direction = -1 if self.color == "white" else 1

        self.append_attack_move(moves=moves, x=x, y=y, board=board, direction=direction, get_all= True)
        self.append_motion_moves(moves=moves, x=x, y=y, board=board, direction=direction)

        return moves


    # Adds cells to the transmitted list that the pawn can resemble.
    def append_motion_moves(self, *, moves: list, x, y, board, direction):
        """
        Adds cells to the transmitted list that the pawn can resemble.

        :param moves:       the list to added
        :param x:           coordinate x on which the figure stands
        :param y:           coordinate y on which the figure stands
        :param board:       the board on which the piece stands
        :param direction:   direction for which figure will move

        :return: None
        """
        # 1 шаг вперёд
        if in_bounds(x, y + direction) and board[y + direction][x] == 0:
            moves.append((x, y + direction))

            # 2 шага вперёд, если первый ход
            if self.first_move and in_bounds(x, y + 2 * direction) and board[y + 2 * direction][x] == 0:
                moves.append((x, y + 2 * direction))
        return


    # Adds cells to the transmitted list that the pawn can attack.
    # The get_all parameter returns all the moves to attack, even if there is no piece of a different color on them.
    def append_attack_move(self, *, moves: list, x, y, board, direction, get_all: bool):
        # Атака по диагонали
        for dx in (-1, 1):
            nx, ny = x + dx, y + direction
            if in_bounds(nx, ny):
                target = board[ny][nx]
                if get_all or (target != 0 and target.color != self.color):
                    moves.append((nx, ny))
        return


    def __str__(self):
        return "♟" if self.color == "white" else "♙"


class King(Figure):

    def draw_move(self):
        deltas = [(-1, 0), (1, 0), (0, -1), (0, 1),
                  (-1, -1), (-1, 1), (1, -1), (1, 1)]
        moves = []
        x, y = self.cord
        for dy, dx in deltas:
            ny, nx = y + dy, x + dx
            if not in_bounds(ny, nx):
                continue

            piece = self.board.get_chessboard()[ny][nx]

            if piece == 0:  # пустая клетка
                moves.append((nx, ny))
            elif piece.color != self.color:  # враг
                moves.append((nx, ny))

        return moves


    def get_attack_moves(self):
        return self.draw_move()


    def is_in_check(self, *, figures):
        for x in figures:
            if self.color == x.color:
                continue

            if self.cord in x.get_attack_moves():
                return True
        return False


    def get_cord(self):
        return self.cord


    def __str__(self):
        return "♚" if self.color == "white" else "♔"


class Rook(Figure):

    def draw_move(self):
        moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        x, y = self.cord

        for dx, dy in directions:
            ny, nx = y + dy, x + dx

            if not in_bounds(ny, nx):
                continue

            tx = nx
            ty = ny

            while True:


                if not in_bounds(tx, ty):  # проверка выхода за границы
                    break

                piece = self.board.get_chessboard()[ty][tx]

                if piece == 0:  # пустая клетка
                    moves.append((tx, ty))

                elif piece.color != self.color:  # враг
                    moves.append((tx, ty))
                    break

                else:  # своя фигура → стоп
                    break
                tx += dx
                ty += dy
        return moves


    def get_attack_moves(self):
        return self.draw_move()


    def __str__(self):
        return "♜" if self.color == "white" else "♖"


class Bishop(Figure):

    def draw_move(self):
        moves = []
        directions = [(1,1), (-1,-1), (-1, 1), (1,-1)]

        x, y = self.cord

        for dx, dy in directions:
            ny, nx = y + dy, x + dx

            if not in_bounds(ny, nx):
                continue

            tx = nx
            ty = ny

            while True:

                if not in_bounds(tx, ty):  # проверка выхода за границы
                    break

                piece = self.board.get_chessboard()[ty][tx]

                if piece == 0:  # пустая клетка
                    moves.append((tx, ty))

                elif piece.color != self.color:  # враг
                    moves.append((tx, ty))
                    break

                else:  # своя фигура → стоп
                    break

                tx += dx
                ty += dy
        return moves


    def get_attack_moves(self):
        return self.draw_move()


    def __str__(self):
        return "♝" if self.color == "white" else "♗"


class Knight(Figure):

    def draw_move(self):
        deltas = [(-1, 2), (1, 2), (2, -1), (2, 1),
                  (-1, -2), (1, -2), (-2, -1), (-2, 1)]
        moves = []

        x, y = self.cord

        for dy, dx in deltas:
            ny, nx = y + dy, x + dx

            if not in_bounds(ny, nx):
                continue

            piece = self.board.get_chessboard()[ny][nx]

            if piece == 0:  # пустая клетка
                moves.append((nx, ny))

            elif piece.color != self.color:  # враг
                moves.append((nx, ny))






        return moves


    def get_attack_moves(self):
        return self.draw_move()


    def __str__(self):
        return "♞" if self.color == "white" else "♘"


class Queen(Figure):

    def draw_move(self):
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                  (-1, -1), (-1, 1), (1, -1), (1, 1)]

        x, y = self.cord

        for dx, dy in directions:
            ny, nx = y + dy, x + dx

            if not in_bounds(ny, nx):
                continue


            tx = nx
            ty = ny

            while True:

                if not in_bounds(tx, ty):  # проверка выхода за границы
                    break

                piece = self.board.get_chessboard()[ty][tx]

                if piece == 0:  # пустая клетка
                    moves.append((tx, ty))

                elif piece.color != self.color:  # враг
                    moves.append((tx, ty))
                    break

                else:  # своя фигура → стоп
                    break

                tx += dx
                ty += dy
        return moves


    def get_attack_moves(self):
        return self.draw_move()


    def __str__(self):
        return "♛" if self.color == "white" else "♕"