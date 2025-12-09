






class ChessBoard:
    def __init__(self):
        self.rows = 8
        self.cols = 8




        self.board = [[0 for _ in range(self.rows)] for _ in range(self.cols)]


    def get_board(self):
        return self.board




