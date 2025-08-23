from main import CK, myChessboard




rows = 8
tile_size = 70
class Mouse:
    def __init__(self):
        self.x = None
        self.y = None
        self.t = False





    def mouse_right_button(self, mouse_x, mouse_y):
        self.t = False
        new_x = mouse_x // tile_size
        new_y = mouse_y // tile_size

        print(self.x, self.y, new_x, new_y)

        # Ломается при перемежении фигуры в тоже место

        if self.x is not None and self.y is not None:
            try:

                myChessboard.get_chessboard()[self.y][self.x].move(new_cord=(new_x, new_y))

                for i in myChessboard.get_chessboard():
                    for j in i:
                        print(j, end=" ")
                    print()
                print()

                self.t = True
            except Exception as e:
                print("Перемещение не удалось", e)

                self.t = False


        if not self.t:
            self.x = new_x
            self.y = new_y
            try:

                for i in myChessboard.get_chessboard():
                    for j in i:
                        print(j, end=" ")
                    print()
                print()
                return myChessboard.get_chessboard()[new_y][new_x].draw_move()

            except Exception as e:
                print("Перемещение не удалось", e)
                return  []
        else:
            self.x = None
            self.y = None
            return []

