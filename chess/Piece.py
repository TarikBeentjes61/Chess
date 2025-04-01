class Piece:
    def __init__(self, color):
        self.color = color
        self.legalMoves = []
    def get_type(self):
        return type(self).__name__


        