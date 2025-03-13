class Piece:
    def __init__(self, type_, color):
        self.type = type_
        self.color = color
    def __str__(self):
        name = ''
        name += self.color.value[0]
        name += '-'
        name += self.type.value[0:2]
        return name
        