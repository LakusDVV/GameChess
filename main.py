import raylibpy as rl


rows = 8               # Кол-во строк
cols = 8               # Кол-во столбцов
tile_size = 70        # Размер квадрата (пиксели)
width = cols * tile_size
height = rows * tile_size
light_color = rl.Color(240, 217, 181, 255)
dark_color = rl.Color(181, 136, 99, 255)



# Инициализация окна
rl.init_window(width=width, height=height, title="Chess")
rl.set_target_fps(60)
texture = rl.load_texture("images/black_king.png")


while not rl.window_should_close():
    rl.begin_drawing()
    rl.clear_background(rl.RAYWHITE)

    # Рисуем доску
    for y in range(rows):
        for x in range(cols):
            color = dark_color if (x + y) % 2 == 0 else light_color
            rl.draw_rectangle(x * tile_size, y * tile_size, tile_size, tile_size, color)


    rl.draw_texture(texture, 100, 100, rl.WHITE)
    rl.end_drawing()

rl.unload_texture(texture)
rl.close_window()