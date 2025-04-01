from enum import Enum
class Color(Enum):
    White = "White"
    Black = "Black"
    Empty = "Empty"

    def opposite(self):
        if self == Color.Empty:
            return Color.Empty 
        
        return Color.Black if self == Color.White else Color.White
