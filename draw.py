import raylibpy as rl
import shapes as s
from mouse_move import Mouse



m = Mouse()
rows = 8               # Кол-во строк
cols = 8               # Кол-во столбцов
tile_size = 70        # Размер квадрата (пиксели)
width = cols * tile_size
height = rows * tile_size
light_color = rl.Color(240, 217, 181, 255)
dark_color = rl.Color(181, 136, 99, 255)

rl.init_window(width=width, height=height, title="Chess")
rl.set_target_fps(60)

black_king_texture = rl.load_texture("images/black_king.png")
white_king_texture = rl.load_texture("images/white_king.png")


my_Black_King = s.King(color="black", texture=black_king_texture, start_cord="e8")
my_White_King = s.King(color="white", texture=white_king_texture, start_cord="e1")


while not rl.window_should_close():
    rl.begin_drawing()
    rl.clear_background(rl.RAYWHITE)

    # Рисуем доску
    for y in range(rows):
        for x in range(cols):
            color = dark_color if (x + y) % 2 == 0 else light_color
            rl.draw_rectangle(x * tile_size, y * tile_size, tile_size, tile_size, color)
    my_Black_King.draw()
    my_White_King.draw()

    mouse_x = rl.get_mouse_x()
    mouse_y = rl.get_mouse_y()

    # Проверяем нажатия кнопок мыши
    left_pressed = rl.is_mouse_button_pressed(rl.MOUSE_LEFT_BUTTON)  # нажата в этом кадре
    if left_pressed:
        print(mouse_x,mouse_y)
        m.mouse_right_button(mouse_x, mouse_y)






    rl.end_drawing()


rl.close_window()