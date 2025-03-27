class BaseData:
    def __init__(self, data):
        self.data = data
        self.pos = 0

    def get_base(self):
        base = self.data[self.pos:self.pos+20]
        self.pos = (self.pos + 20) % len(self.data)
        return base