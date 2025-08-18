from main import CK, myChessboard




rows = 8
tile_size = 70
class Mouse:
    def __init__(self):
        self.x = None
        self.y = None





    def mouse_right_button(self, mouse_x, mouse_y):
        new_x = mouse_x // tile_size
        new_y = (rows * tile_size - mouse_y) // tile_size

        print(self.x, self.y, new_x, new_y)

        if self.x is not None and self.y is not None:
            myChessboard.get_chessboard()[self.y][self.x].move(new_cord=(new_x, new_y))
            self.y = None
            self.x = None

        else:
            self.x = mouse_x // tile_size
            self.y = (rows * tile_size - mouse_y) // tile_size