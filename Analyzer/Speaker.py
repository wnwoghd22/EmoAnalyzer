

class Speaker:
    def __init__(self) :
        self.tokens = []

    def respond(self, record) :
        for r in record :
            print(r, record[r])

        #answer

        return record