import raylibpy as rl

rows = 8               # Кол-во строк
cols = 8               # Кол-во столбцов
tile_size = 50         # Размер квадрата (пиксели)
width = cols * tile_size
height = rows * tile_size

# Инициализация окна
rl.init_window(width=width, height=height, title="Chess")
rl.set_target_fps(60)

while not rl.window_should_close():
    rl.begin_drawing()
    rl.clear_background(rl.RAYWHITE)

    # Рисуем доску
    for y in range(rows):
        for x in range(cols):
            color = rl.BLACK if (x + y) % 2 == 0 else rl.WHITE
            rl.draw_rectangle(x * tile_size, y * tile_size, tile_size, tile_size, color)

    rl.end_drawing()

rl.close_window()
