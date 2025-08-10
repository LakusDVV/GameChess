
class Chessboard:
    def __init__(self, *, different: int = 50, rows: int = 8, line: int = 8):
        self.difference = different
        self.y = [str(i) for i in range(1, line + 1)]
        self.x = ["a", "b", "c", "d", "e", "f", "g", "h"]
        self.chessboard = {
            str(cord_y): {
                cord_x: (int(self.difference * index_x), int(self.difference * index_y))
                for index_x, cord_x in enumerate(self.x)
            }
            for index_y, cord_y in enumerate(self.y)
        }

    def find_cords(self, chess_cord) -> (int, int):
        x, y = chess_cord
        return self.chessboard[y][x]


    def get_chessboard(self):
        return self.chessboard


    def __str__(self):
        print(self.chessboard)


c = Chessboard(width=8*50, height=8*50, rows=8, line=8)

