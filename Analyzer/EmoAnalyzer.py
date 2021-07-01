import math

class Vector:
    def __init__(self, x, y) :
        self.x = x
        self.y = y

    def magnitude(self) :
        return math.sqrt(self.x * self.x + self.y * self.y)

    def deg(self) :
        # get degree
        return

    def __add__(self, v) :
        return Vector(
            self.x + v.x,
            self.y + v.y
        )
    
    def __gt__(self, v) :
        if isinstance(v, Vector) :
            return self.magnitude() > v.magnitude()
        else :
            return self.magnitude() > v

    def __str__(self) :
        return 'Vector({0}, {1})'.format(self.x, self.y)

class Emotion(Vector):
    def __init__(self, x = 0, y = 0) :
        super().__init__(x, y)

    def getEmot(self) :
        return

class EmoAnalyzer:
    def __init__(self):
        self.emot = Emotion()