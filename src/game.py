import raylibpy as rl
from copy import deepcopy
from typing import Optional
from src.chessboard import ChessBoard
from src.enums import MoveResult, PieceColor, MoveSpecial, GameStatus
from src.render import TextureManager, Render
from src.dataclass import Move, MoveRecord, CastlingRights, History
from src.shapes import Figure, King, Queen, Bishop, Knight, Rook, Pawn



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
        self.selected_piece: Figure

        self.has_move: PieceColor = PieceColor.WHITE
        self.available_moves = []
        self.avl_moves: list[tuple[int, int]] = []
        self.promotion = False

        self.history: History = History()
        print(self.chessboard.castling_rights)


    def run(self):
        while not rl.window_should_close():
            self.render.draw()
            self.update()

        rl.close_window()


    def update(self):
        mouse_x = rl.get_mouse_x()
        mouse_y = rl.get_mouse_y()



        if self.mouse_first_right_click and self.available_moves:
            board_x = mouse_x // self.tile_size
            board_y = mouse_y // self.tile_size

            if (board_x, board_y) in self.avl_moves:
                self.render.change_highlighting_of_the_selected_cell_data(cord=(board_x, board_y))
            else:
                self.render.clear_highlighting_of_the_selected_cell_data()


        if rl.is_mouse_button_pressed(rl.MOUSE_LEFT_BUTTON):
            print(mouse_x, mouse_y)
            board_x = mouse_x // self.tile_size
            board_y = mouse_y // self.tile_size
            self.mouse_right_button(board_x=board_x, board_y=board_y)


    def create_figures(self):
        self.create_white_figures()
        self.create_black_figures()
        print(self.chessboard)


    def create_white_figures(self):
        # Create king
        self.create_white_king()

        # Create queen
        self.create_white_queen()

        # Creates bishops
        self.creates_white_bishops()

        # Creates knights
        self.creates_white_knights()

        # Creates rooks
        self.creates_white_rooks()

        # Creates pawns
        self.creates_white_pawns()


    def create_black_figures(self):
        # Create king
        self.create_black_king()

        # Create queen
        self.create_black_queen()

        # Creates bishops
        self.creates_black_bishops()

        # Creates knights
        self.creates_black_knights()

        # Creates rooks
        self.creates_black_rooks()

        # Creates pawns
        self.creates_black_pawns()


    def after_move(self):
        record = self.history.top()
        if self.promotion:


            self.render.change_promotion_pawn_data(
                color=record.piece.color,
                cord=record.to_pos,
                direction=record.piece.direction
            )

            print("Promotion")
            return

        self.render.change_last_move_data(from_pos=record.from_pos, to_pos=record.to_pos)
        self.has_move = self.has_move.opposite()

        kx, ky = self.chessboard.find_king(color=self.has_move)
        if self.chessboard.is_square_attacked(x=kx, y=ky, enemy=self.has_move.opposite()):
            self.render.change_check_data(new_pos=(kx, ky))

        else:
            self.render.clear_check_data()

        game_status = self.this_end(self.has_move)
        print(game_status)
        print(self.chessboard.castling_rights)


    def mouse_right_button(self, board_x, board_y):


        board = self.chessboard.get_board()

        if self.promotion:
            record = self.history.top()
            try:
                fig = select_promotion_figure(
                    cord=record.to_pos,
                    direction=record.piece.direction,
                    board_x=board_x,
                    board_y=board_y
                )
                self.chessboard.undo(record)
                self.history.pop()
                color = record.piece.color
                texture_name = f"{color}_{fig.texture_key}"
                texture = self.texture_manager.get_texture(texture_name)

                x, y = record.to_pos

                figure = fig(x=x, y=y, texture=texture, color=record.piece.color)


                record.promotion_pawn = figure


                self.promotion = False
                self.chessboard.apply_move(record)
                self.history.push(record)
                self.render.clear_promotion_pawn_data()
                self.after_move()



            except Exception() as ex:
                print(ex)
                self.promotion = False
                self.render.clear_promotion_pawn_data()
                print("Error in promotion")
                self.chessboard.undo(record)
                self.history.pop()
                return

        if not self.mouse_first_right_click:
            piece = board[board_y][board_x]

            if piece == 0:
                print("Cell is empty")
                return

            self.selected_piece = piece

            if self.selected_piece.color == self.has_move:

                status = self._first_click(piece=self.selected_piece)

                print(status)
                if status == MoveResult.OK:
                    self.mouse_first_right_click = True

            else:
                print("Error, this piece don't have move")

        elif self.mouse_first_right_click:
            status = self._second_click(board_x=board_x, board_y=board_y)

            if status == MoveResult.OK:
                self.after_move()

        print(self.chessboard)


    def _first_click(self, *, piece):
        self.render.change_highlighting_selected_cell_data(cord=piece.cord)

        moves = piece.get_moves(chessboard=self.chessboard)
        status = self.filter_moves(moves=moves)

        if status:
            right_moves = status["right_moves"]
            if not right_moves:
                return MoveResult.CHECK

            cap = []
            mov = []

            for move in right_moves:
                if move.special in (MoveSpecial.CAPTURE, MoveSpecial.EN_PASSANT):
                    cap.append(move.to_pos)
                elif (move.special is None or
                      move.special in (MoveSpecial.CASTLE_KINGSIDE, MoveSpecial.CASTLE_QUEENSIDE)):
                    mov.append(move.to_pos)
                self.avl_moves.append(move.to_pos)

            self.render.change_highlighting_data(captures=cap, moves=mov)
            self.available_moves = right_moves
            return MoveResult.OK
        return MoveResult.INVALID_MOVE





    def _second_click(self, *, board_x, board_y):
        move = self.find_move_to(to_x=board_x, to_y=board_y)
        board = self.chessboard.get_board()
        piece = board[board_y][board_x]

        if move:
            record = self.move_to_move_record(move=move)
            last_line = 7 if record.piece.color == PieceColor.WHITE else 0
            to_x, to_y = record.to_pos

            if isinstance(record.piece, Pawn) and to_y == last_line:
                self.promotion = True

            self.make_move(record)

            self.render.clear_highlighting_data()

            self.render.clear_highlighting_selected_cell_data()
            self.mouse_first_right_click = False
            self.available_moves = []
            self.avl_moves = []
            return MoveResult.OK

        elif piece.color == self.selected_piece.color:
            self.render.clear_highlighting_data()
            self.render.clear_highlighting_selected_cell_data()
            self.available_moves = []
            self.avl_moves = []

            self.mouse_first_right_click = False
            self.mouse_right_button(board_x=board_x, board_y=board_y)

        else:
            self.render.clear_highlighting_data()
            self.render.clear_highlighting_selected_cell_data()
            self.mouse_first_right_click = False

            return MoveResult.INVALID_MOVE


    def make_move(self, record: MoveRecord):


        self.chessboard.apply_move(record)

        self.history.push(record)
        self.available_moves.clear()


    def this_end(self, color) -> GameStatus:
        board = self.chessboard.get_board()
        king_pos = self.chessboard.find_king(color=color)
        kx, ky = king_pos
        king: Figure = board[ky][kx]
        king_moves = king.get_moves(chessboard=self.chessboard)
        right_moves = self.filter_moves(king_moves)["right_moves"]

        status = GameStatus.IN_PROGRESS

        # If king don't have moves
        if not right_moves:
            figures = self.chessboard.get_figures()

            for fig in figures:
                if fig.color == color:
                    moves = fig.get_moves(chessboard=self.chessboard)
                    right_moves = self.filter_moves(moves)["right_moves"]


                    # If any figure can move
                    if right_moves:
                        break
            # If all figures cannot make move
            else:
                king_is_check = self.chessboard.king_is_check(color=color)
                # Checkmate
                if king_is_check:
                    status = GameStatus.CHECKMATE
                else:
                    status = GameStatus.PAT
        return status


    def find_move_to(self, to_x, to_y) -> Optional[Move]:
        for move in self.available_moves:
            if move.to_pos == (to_x, to_y):
                return move
        return None


    def filter_moves(self, moves: list) -> dict:
        dic: dict = {
            "right_moves": [],
            "moves_and_statuses": {}
        }

        if moves:
            for move in moves:
                status = self.filter_move(move)

                dic["moves_and_statuses"][move] = status
                if status == MoveResult.OK:
                    dic["right_moves"].append(move)


            return dic
        return dic


    def filter_move(self, move):
        mr = self.move_to_move_record(move=move)
        self.chessboard.apply_move(mr)
        king_is_check: bool = self.chessboard.king_is_check(move.piece.color)
        self.chessboard.undo(mr)
        print(mr, self.chessboard.castling_rights)

        if move.special in (MoveSpecial.CASTLE_KINGSIDE, MoveSpecial.CASTLE_QUEENSIDE):
            if not self.can_king_castle(move_record=mr):
                return MoveResult.INVALID_MOVE


        if king_is_check:
            return MoveResult.CHECK
        return MoveResult.OK


    def can_king_castle(self, *, move_record: MoveRecord):
        from_x, _ = move_record.from_pos
        to_x, _ = move_record.to_pos
        y = _
        direction = move_record.piece.direction
        for x in range(from_x, to_x + direction, direction):
            if self.chessboard.is_square_attacked(
                        x=x,
                        y=y,
                        enemy=move_record.piece.color.opposite()
                    ):
                return False
        return True


    def move_to_move_record(self, move: Move):

        captured_piece: Optional[Figure] = None
        captured_pos: Optional[tuple[int, int]] = None

        rook: Optional[Figure] = None
        rook_from: Optional[tuple[int, int]] = None
        rook_to: Optional[tuple[int, int]] = None

        prev_castling_rights: CastlingRights = deepcopy(self.chessboard.castling_rights)
        prev_en_passant: Optional[tuple[int, int]] = self.chessboard.en_passant_target



        board = self.chessboard.get_board()
        new_x, new_y = move.to_pos

        rank = move.piece.direction

        match move.special:
            case MoveSpecial.CAPTURE:
                captured_piece = board[new_y][new_x]
                captured_pos = (new_x, new_y)

            case MoveSpecial.CASTLE_KINGSIDE:

                rook = board[new_y][new_x - 1]
                rook_from = (new_x - 1, new_y)
                rook_to = (new_x + 1, new_y)

            case MoveSpecial.CASTLE_QUEENSIDE:

                rook = board[new_y][new_x + 2]
                rook_from = (new_x + 2, new_y)
                rook_to = (new_x - 1, new_y)

            case MoveSpecial.EN_PASSANT:
                prev_en_pas_x, prev_en_pas_y = prev_en_passant
                prev_en_pas_y -= rank
                captured_piece = self.chessboard.get_piece(cord=(prev_en_pas_x, prev_en_pas_y))
                captured_pos = (prev_en_pas_x, prev_en_pas_y)


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









    def create_white_king(self):
        # Create king
        white_king_texture = self.texture_manager.get_texture("white_king")
        x, y = 3, 0
        king = King(x=x, y=y, texture=white_king_texture, color=PieceColor.WHITE)
        status = self.chessboard.add_figure(x=x, y=y, figure=king)
        view_status_add_figure(status)


    def create_white_queen(self):
        # Create queen
        white_queen_texture = self.texture_manager.get_texture("white_queen")
        x, y = 4, 0
        queen = Queen(x=x, y=y, texture=white_queen_texture, color=PieceColor.WHITE)
        status = self.chessboard.add_figure(x=x, y=y, figure=queen)
        view_status_add_figure(status)


    def creates_white_bishops(self):
        white_bishop_texture = self.texture_manager.get_texture("white_bishop")
        x, y = None, 0
        for x in (2, 5):
            bishop = Bishop(x=x, y=y, texture=white_bishop_texture, color=PieceColor.WHITE)
            status = self.chessboard.add_figure(x=x, y=y, figure=bishop)
            view_status_add_figure(status)


    def creates_white_knights(self):
        white_knight_texture = self.texture_manager.get_texture("white_knight")
        x, y = None, 0
        for x in (1, 6):
            knight = Knight(x=x, y=y, texture=white_knight_texture, color=PieceColor.WHITE)
            status = self.chessboard.add_figure(x=x, y=y, figure=knight)
            view_status_add_figure(status)


    def creates_white_rooks(self):
        white_rook_texture = self.texture_manager.get_texture("white_rook")
        x, y = None, 0
        for x in (0, 7):
            rook = Rook(x=x, y=y, texture=white_rook_texture, color=PieceColor.WHITE)
            status = self.chessboard.add_figure(x=x, y=y, figure=rook)
            view_status_add_figure(status)


    def creates_white_pawns(self):
        white_pawn_texture = self.texture_manager.get_texture("white_pawn")
        x, y = None, 1
        for x in range(self.rows):
            pawn = Pawn(x=x, y=y, texture=white_pawn_texture, color=PieceColor.WHITE)
            status = self.chessboard.add_figure(x=x, y=y, figure=pawn)
            view_status_add_figure(status)


    def create_black_king(self):
        # Create king
        black_king_texture = self.texture_manager.get_texture("black_king")
        x, y = 3, 7
        king = King(x=x, y=y, texture=black_king_texture, color=PieceColor.BLACK)
        status = self.chessboard.add_figure(x=x, y=y, figure=king)
        view_status_add_figure(status)


    def create_black_queen(self):
        # Create queen
        black_queen_texture = self.texture_manager.get_texture("black_queen")
        x, y = 4, 7
        queen = Queen(x=x, y=y, texture=black_queen_texture, color=PieceColor.BLACK)
        status = self.chessboard.add_figure(x=x, y=y, figure=queen)
        view_status_add_figure(status)


    def creates_black_bishops(self):
        # Creates bishops
        black_bishop_texture = self.texture_manager.get_texture("black_bishop")
        x, y = None, 7
        for x in (2, 5):
            bishop = Bishop(x=x, y=y, texture=black_bishop_texture, color=PieceColor.BLACK)
            status = self.chessboard.add_figure(x=x, y=y, figure=bishop)
            view_status_add_figure(status)


    def creates_black_knights(self):
        # Creates knights
        black_knight_texture = self.texture_manager.get_texture("black_knight")
        x, y = None, 7
        for x in (1, 6):
            knight = Knight(x=x, y=y, texture=black_knight_texture, color=PieceColor.BLACK)
            status = self.chessboard.add_figure(x=x, y=y, figure=knight)
            view_status_add_figure(status)


    def creates_black_rooks(self):
        # Creates rooks
        black_rook_texture = self.texture_manager.get_texture("black_rook")
        x, y = None, 7
        for x in (0, 7):
            rook = Rook(x=x, y=y, texture=black_rook_texture, color=PieceColor.BLACK)
            status = self.chessboard.add_figure(x=x, y=y, figure=rook)
            view_status_add_figure(status)


    def creates_black_pawns(self):
        # Creates pawns
        black_pawn_texture = self.texture_manager.get_texture("black_pawn")
        x, y = None, 6
        for x in range(self.rows):
            pawn = Pawn(x=x, y=y, texture=black_pawn_texture, color=PieceColor.BLACK)
            status = self.chessboard.add_figure(x=x, y=y, figure=pawn)
            view_status_add_figure(status)


def view_status_add_figure(status: MoveResult):
    match status:
        case MoveResult.OK:
            print(f"Figure added")
        case MoveResult.CELL_OCCUPIED:
            print("Cell is not empty")


def select_promotion_figure(cord, direction, board_x, board_y):
    x, y = cord

    dict_cord = {
        cord: Queen,
        (x, y - direction * 1): Knight,
        (x, y - direction * 2): Rook,
        (x, y - direction * 3): Bishop
    }
    if not (board_x, board_y) in dict_cord.keys():
        raise Exception("Er")
    fig = dict_cord[(board_x, board_y)]
    return fig