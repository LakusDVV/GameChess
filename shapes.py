import raylibpy as rl
from main import myChessboard, CK


class Figure:
    def __init__(self, *, texture, color, start_cord: str):
        self.texture = texture
        self.color = color
        self.cord_for_array = CK.find_cords(start_cord)
        myChessboard.redact_board_add(
            cord=CK.get_cords_for_array(start_cord),
            element=self
        )


    def draw(self):
        x, y = self.cord_for_array
        rl.draw_texture(self.texture, x, y, rl.WHITE)


    def move(self, cord, new_cord):
        myChessboard.redact_board_move(
            new_cord=CK.get_cords_for_array(new_cord),
            cord= CK.get_cords_for_array(cord)
        )
        self.cord_for_array = new_cord




class Pawn(Figure):
    def __init__(self, *, texture, color,start_cord: str):
        super().__init__(texture=texture, color=color, start_cord=start_cord)


class King(Figure):
    def __init__(self, *, texture, color, start_cord):
        super().__init__(texture=texture, color=color, start_cord=start_cord)
