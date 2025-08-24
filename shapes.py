import raylibpy as rl

class Figure:
    def __init__(self, *, texture, color, start_cord, board):
        self.rows, self.cols = 8, 8
        self.tile_size =  70
        self.texture = texture
        self.color = color
        self.board = board
        self.cord = self.board.get_cords_for_array(start_cord)



    def draw(self):
        x, y = self.cord

        rl.draw_texture(self.texture, x * self.tile_size, y * self.tile_size, rl.WHITE)


    def move(self, new_cord):
        self.board.redact_board_move(
            new_cord=new_cord,
            cord=self.cord
        )
        self.cord = new_cord
        self.draw()



class Pawn(Figure):
    def __init__(self, *, texture, color, start_cord, board):
        super().__init__(
            texture=texture,
            color=color,
            start_cord=start_cord,
            board=board
        )

    def get_moves(self, board):
        pass


class King(Figure):
    def __init__(self, *, texture, color, start_cord, board):
        super().__init__(
            texture=texture,
            color=color,
            start_cord=start_cord,
            board=board
        )

    def draw_move(self):
        deltas = [(-1, 0), (1, 0), (0, -1), (0, 1),
                  (-1, -1), (-1, 1), (1, -1), (1, 1)]
        neighbors = []
        x, y = self.cord
        for dy, dx in deltas:
            ny, nx = y + dy, x + dx
            if 0 <= ny < self.rows and 0 <= nx < self.cols:
                neighbors.append((nx, ny))

        return neighbors

    def get_moves(self, board):
        pass
    def __str__(self):
        return "♚" if self.color == "white" else "♔"


