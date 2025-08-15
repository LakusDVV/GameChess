class ChessboardCords:
    def __init__(self):
        self.line = 8
        self.rows = 8
        self.difference = 70
        self.y = [str(i) for i in range(self.line-1, -1,-1)]
        self.x = ["a", "b", "c", "d", "e", "f", "g", "h"]

        self.chessboard_cords_xy = {
            str(cord_y): {
                cord_x: (int(self.difference * index_x), int(self.difference * index_y))
                for index_x, cord_x in enumerate(self.x)
            }
            for index_y, cord_y in enumerate(self.y)
        }

        self.chessboard_cords = {
            str(cord_y): {
                cord_x: (int(index_x + 1), int(index_y + 1))
                for index_x, cord_x in enumerate(self.x)
            }
            for index_y, cord_y in enumerate(self.y)
        }

        self.chessboard = [[None for _ in range(8)] for _ in range(8)]

    def find_cords(self, chess_cord: str) -> (int, int):
        x, y = chess_cord
        y = str(int(y) - 1)
        return self.chessboard_cords_xy[y][x]


    def get_cords_for_array(self, chess_cord) -> (int, int):
        x, y = chess_cord
        y = str(int(y) - 1)
        return self.chessboard_cords[y][x]


    def get_chessboard_cords_xy(self):
        return self.chessboard_cords_xy


    def __str__(self):
        print(self.chessboard_cords_xy)




class Chessboard:
    def __init__(self):
        self.chessboard = [[None for _ in range(8)] for _ in range(8)]

    def get_chessboard(self):
        return self.chessboard


    def redact_board_add(self, *, element, cord: (int, int)):
        x, y = cord
        y -= 1
        self.chessboard[y][x] = element


    def redact_board_move(self, *, new_cord, cord):
        x, y = cord
        new_x, new_y = new_cord
        self.chessboard[new_y][new_x] = self.chessboard[y][x]
        self.chessboard[y][x] = None