from main import CK, myChessboard




rows = 8
tile_size = 70
class Mouse:
    def __init__(self):
        self.x = None
        self.y = None





    def mouse_right_button(self, mouse_x, mouse_y):
        self.t = False
        new_x = mouse_x // tile_size
        new_y = mouse_y // tile_size

        print(self.x, self.y, new_x, new_y)


        if self.x is not None and self.y is not None:
            try:

                myChessboard.get_chessboard()[self.y][self.x].move(new_cord=(new_x, new_y))
                self.t = True
            except Exception as e:
                print("Перемещение не удалось", e)
                self.t = False



        if not self.t:
            self.x = mouse_x // tile_size
            self.y = mouse_y // tile_size
            try:
                return myChessboard.get_chessboard()[new_y][new_x].draw_move()
            except Exception as e:
                print("Перемещение не удалось", e)
                return  []
        else:
            self.x = None
            self.y = None
            return []

