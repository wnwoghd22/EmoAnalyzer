import math
from numbers import Number

class Vector:
    def __init__(self, x, y) :
        if type(x) is str :
            deg = float(int(x[:-1]) / 180) * math.pi
            self.x = y * math.cos(deg)
            self.y = y * math.sin(deg)
        elif isinstance(x, Number) :
            self.x = x
            self.y = y

    def magnitude(self) :
        return math.sqrt(self.x * self.x + self.y * self.y)

    def rad(self) : 
        return math.atan2(self.x, self.y)

    def deg(self) : 
        return self.rad() * 180 / math.pi

    def __add__(self, v) :
        return Vector(
            self.x + v.x,
            self.y + v.y
        )

    def __mul__(self, v) :
        if isinstance(v, Vector):
            return self.x * v.x + self.y * v.y
        elif isinstance(v, Number) :
            return Vector(
                self.x * v,
                self.y * v
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

    def strength(self) :
        mag = self.magnitude()
        if mag >= 0 and mag < 0.5 :
            return 'slightly'
        elif mag >= 0.5 and mag < 1.5 :
            return 'moderately'
        elif mag >= 1.5 and mag < 2.5 :
            return 'very'
        elif mag >= 2.5 :
            return 'extremely'
        else :
            return 'not'

    def emot(self) :
        deg  = self.deg()
        if deg >= -169 and deg < -146 :
            return 'sad'
        elif deg >= -146 and deg < -123 :
            return 'depressed'
        elif deg >= -123 and deg < -100 :
            return 'bored'
        elif deg >= -100 and deg < -81 :
            return 'sleepy'
        elif deg >= -81 and deg < -63 :
            return 'calm'
        elif deg >= -63 and deg < -45 :
            return 'relaxed'
        elif deg >= -45 and deg < -27 :
            return 'serene'
        elif deg >= -27 and deg < -9 :
            return  'contented'
        elif deg >= -9 and deg < 9 :
            return 'pleasant'
        elif deg >= 9 and deg < 27 :
            return 'happy'
        elif deg >= 27 and deg < 45 :
            return 'elated'
        elif deg >= 45 and deg < 63 :
            return 'excited'
        elif deg >= 63 and deg < 81 :
            return  'alert'
        elif deg >= 81 and deg < 99 :
            return 'awakened'
        elif deg >= 99 and deg < 117 :
            return 'tense'
        elif deg >= 117 and deg < 135 :
            return  'nervous'
        elif deg >= 135 and deg < 153 :
            return 'stressed'
        elif deg >= 153 and deg < 171 :
            return 'upset'
        else :
            return 'unpleasant'

    def getEmot(self) :
        return self.strength() + ' ' + self.emot()

class EmoAnalyzer:
    def __init__(self):
        self.emot = Emotion()