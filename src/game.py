import raylibpy as rl
import shapes


from src.chessboard import ChessBoard
from typing import Optional
from src.enums import MoveResult, PieceColor, MoveSpecial
from src.render import TextureManager, Render
from src.dataclass import Move, MoveRecord, CastlingRights, History






class Game:
    def __init__(self):
        self.rows, self.cols = 8, 8
        self.tile_size = 70

        self.chessboard = ChessBoard()
        self.texture_manager = TextureManager()

        self.render = Render(chessboard=self.chessboard, texture_manager=self.texture_manager)
        self.texture_manager.load_textures()

        self.create_figures()

        self.mouse_first_right_click = False
        self.selected_piece: shapes.Figure

        self.has_move: PieceColor = PieceColor.WHITE
        self.available_moves = []

        self.history: list[MoveRecord] = []


    def run(self):
        while not rl.window_should_close():
            self.render.draw()
            self.update()

        rl.close_window()


    def update(self):
        mouse_x = rl.get_mouse_x()
        mouse_y = rl.get_mouse_y()

        if rl.is_mouse_button_pressed(rl.MOUSE_LEFT_BUTTON):
            print(mouse_x, mouse_y)
            self.mouse_right_button(mouse_x, mouse_y)


    def create_figures(self):
        self.create_white_figures()
        self.create_black_figures()
        self.chessboard.print_board()


    def create_white_figures(self):

        # Create king
        white_king_texture = self.texture_manager.get_texture("white_king")
        x, y = 3, 0
        king = shapes.King(x=x, y=y, texture=white_king_texture, color = PieceColor.WHITE)
        status = self.chessboard.add_figure(x=x, y=y, figure=king)
        view_status_add_figure(status)

        # Create queen
        white_queen_texture = self.texture_manager.get_texture("white_queen")
        x, y = 4, 0
        queen = shapes.Queen(x=x, y=y, texture=white_queen_texture, color = PieceColor.WHITE)
        status = self.chessboard.add_figure(x=x, y=y, figure=queen)
        view_status_add_figure(status)

        # Creates bishops
        white_bishop_texture = self.texture_manager.get_texture("white_bishop")
        x, y = None, 0
        for x in (2, 5):
            bishop = shapes.Bishop(x=x, y=y, texture=white_bishop_texture, color=PieceColor.WHITE)
            status = self.chessboard.add_figure(x=x, y=y, figure=bishop)
            view_status_add_figure(status)

        # Creates knights
        white_knight_texture = self.texture_manager.get_texture("white_knight")
        x, y = None, 0
        for x in (1, 6):
            knight = shapes.Knight(x=x, y=y, texture=white_knight_texture, color=PieceColor.WHITE)
            status = self.chessboard.add_figure(x=x, y=y, figure=knight)
            view_status_add_figure(status)

        # Creates rooks
        white_rook_texture = self.texture_manager.get_texture("white_rook")
        x, y = None, 0
        for x in (0, 7):
            rook = shapes.Rook(x=x, y=y, texture=white_rook_texture, color=PieceColor.WHITE)
            status = self.chessboard.add_figure(x=x, y=y, figure=rook)
            view_status_add_figure(status)

        # Creates pawns
        white_pawn_texture = self.texture_manager.get_texture("white_pawn")
        x, y = None, 1
        for x in range(self.rows):
            pawn = shapes.Pawn(x=x, y=y, texture=white_pawn_texture, color=PieceColor.WHITE)
            status = self.chessboard.add_figure(x=x, y=y, figure=pawn)
            view_status_add_figure(status)


    def create_black_figures(self):

        # Create king
        black_king_texture = self.texture_manager.get_texture("black_king")
        x, y = 3, 7
        king = shapes.King(x=x, y=y, texture=black_king_texture, color = PieceColor.BLACK)
        status = self.chessboard.add_figure(x=x, y=y, figure=king)
        view_status_add_figure(status)

        # Create queen
        black_queen_texture = self.texture_manager.get_texture("black_queen")
        x, y = 4, 7
        queen = shapes.Queen(x=x, y=y, texture=black_queen_texture, color = PieceColor.BLACK)
        status = self.chessboard.add_figure(x=x, y=y, figure=queen)
        view_status_add_figure(status)

        # Creates bishops
        black_bishop_texture = self.texture_manager.get_texture("black_bishop")
        x, y = None, 7
        for x in (2, 5):
            bishop = shapes.Bishop(x=x, y=y, texture=black_bishop_texture, color=PieceColor.BLACK)
            status = self.chessboard.add_figure(x=x, y=y, figure=bishop)
            view_status_add_figure(status)

        # Creates knights
        black_knight_texture = self.texture_manager.get_texture("black_knight")
        x, y = None, 7
        for x in (1, 6):
            knight = shapes.Knight(x=x, y=y, texture=black_knight_texture, color=PieceColor.BLACK)
            status = self.chessboard.add_figure(x=x, y=y, figure=knight)
            view_status_add_figure(status)

        # Creates rooks
        black_rook_texture = self.texture_manager.get_texture("black_rook")
        x, y = None, 7
        for x in (0, 7):
            rook = shapes.Rook(x=x, y=y, texture=black_rook_texture, color=PieceColor.BLACK)
            status = self.chessboard.add_figure(x=x, y=y, figure=rook)
            view_status_add_figure(status)

        # Creates pawns
        black_pawn_texture = self.texture_manager.get_texture("black_pawn")
        x, y = None, 6
        for x in range(self.rows):
            pawn = shapes.Pawn(x=x, y=y, texture=black_pawn_texture, color=PieceColor.BLACK)
            status = self.chessboard.add_figure(x=x, y=y, figure=pawn)
            view_status_add_figure(status)


    def after_move(self):
        self.has_move = PieceColor.WHITE if self.has_move == PieceColor.BLACK else PieceColor.BLACK


    def mouse_right_button(self, mouse_x, mouse_y):
        board_x = mouse_x // self.tile_size
        board_y = mouse_y // self.tile_size

        board = self.chessboard.get_board()

        if not self.mouse_first_right_click:
            self.selected_piece = board[board_y][board_x]

            if self.selected_piece.color == self.has_move:

                status = self._first_click(piece=self.selected_piece)

                print(status)
                if status == MoveResult.OK:
                    self.mouse_first_right_click = True

            else:
                print("Error, this piece don't have move")

        elif self.mouse_first_right_click:
            status = self._second_click(board_x=board_x, board_y=board_y)



    def _first_click(self, *, piece):
        if not piece == 0:
            moves = piece.get_moves(chessboard=self.chessboard)
            right_moves = self.filter_moves(moves=moves)
            self.render.change_highlighting(new_moves=right_moves)\

            self.available_moves = right_moves
            return MoveResult.OK
        else:
            return MoveResult.INVALID_MOVE


    def _second_click(self, *, board_x, board_y):
        move = self.find_move_to(x=board_x, y=board_y)

        if move:
            self.make_move(move)
            self.after_move()
            self.render.clear_highlighting()
            self.mouse_first_right_click = False
            return MoveResult.OK
        else:
            self.render.clear_highlighting()
            self.mouse_first_right_click = False
            return MoveResult.INVALID_MOVE


    def make_move(self, move):
        record = self.move_to_move_record(move=move)

        self.chessboard.apply_move(record)

        self.history.append(record)
        self.available_moves.clear()




    def find_move_to(self, x, y) -> Optional[Move]:
        for move in self.available_moves:
            if move.to_pos == (x, y):
                return move
        return None


    def filter_moves(self, moves: list):
        right_moves: list[Move] = []

        if moves:

            for move in moves:
                status = self.filter_move(move)

                if status == MoveResult.OK:
                    right_moves.append(move)


            return right_moves
        return []


    def filter_move(self, move):
        mr = MoveRecord(
            piece=move.piece,
            from_pos=move.from_pos,
            to_pos=move.to_pos
        )
        self.chessboard.apply_move(mr)
        king_is_check: bool = self.chessboard.king_is_check(move.piece.color)
        self.chessboard.undo(mr)

        if king_is_check:
            return MoveResult.CHECK
        return MoveResult.OK


    def move_to_move_record(self, move: Move):

        captured_piece: Optional[shapes.Figure] = None
        captured_pos: Optional[tuple[int, int]] = None

        rook: Optional[shapes.Figure] = None
        rook_from: Optional[tuple[int, int]] = None
        rook_to: Optional[tuple[int, int]] = None

        prev_castling_rights: CastlingRights = self.chessboard.castling_rights
        prev_en_passant: Optional[tuple[int, int]] = self.chessboard.en_passant_target


        board = self.chessboard.get_board()
        new_x, new_y = move.to_pos

        match move:
            case MoveSpecial.CAPTURE:
                captured_piece = board[new_y][new_x]
                captured_pos = (new_x, new_y)

            case MoveSpecial.CASTLE_KINGSIDE:
                rook = board[new_y][new_x + 1]
                rook_from = (new_y, new_x + 1)
                rook_to = (new_y, new_x - 1)

            case MoveSpecial.CASTLE_QUEENSIDE:
                rook = board[new_y][new_x - 2]
                rook_from = (new_y, new_x - 2)
                rook_to = (new_y, new_x + 1)

            case MoveSpecial.EN_PASSANT:
                captured_piece = self.chessboard.get_figure(prev_en_passant)
                captured_pos = self.chessboard.en_passant_target


        mr = MoveRecord(
            piece=move.piece,
            from_pos=move.from_pos,
            to_pos=move.to_pos,

            captured_piece = captured_piece,
            captured_pos = captured_pos,

            rook = rook,
            rook_from = rook_from,
            rook_to = rook_to,

            prev_castling_rights= prev_castling_rights,
            prev_en_passant= prev_en_passant


        )
        return mr


def view_status_add_figure(status: MoveResult):
    match status:
        case MoveResult.OK:
            print(f"Figure added")
        case MoveResult.CELL_OCCUPIED:
            print("Cell is not empty")