from vectors import Vector

class Emotion:
    def __init__(self, x = 0, y = 0) :
        self.x = x
        self.y = y

class EmoAnalyzer:
    def __init__(self):
        self.emot = Emotion()