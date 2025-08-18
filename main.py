import raylibpy as rl
import chessboard











rows = 8               # Кол-во строк
cols = 8               # Кол-во столбцов
tile_size = 70        # Размер квадрата (пиксели)
width = cols * tile_size
height = rows * tile_size
light_color = rl.Color(240, 217, 181, 255)
dark_color = rl.Color(181, 136, 99, 255)


myChessboard = chessboard.Chessboard()
CK = chessboard.ChessboardCords()

# Инициализация окна
import draw


