import raylibpy as rl

# Инициализация окна
rl.init_window(600, 600, "Chess")
rl.set_target_fps(60)

while not rl.window_should_close():
    rl.begin_drawing()


    rl.draw_text("Привет от raylib!", 10, 10, 20, rl.DARKGRAY)
    rl.draw_circle(300, 300, 50, rl.RED)

    rl.end_drawing()

rl.close_window()
