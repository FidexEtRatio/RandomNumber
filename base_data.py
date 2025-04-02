from bernstein import djb2

class BaseData:
    def __init__(self, data):
        self.data = data
        self.pos = 0
        self.round = 0
        self.finish = False

    def get_base(self):
        base = self.data[self.pos:self.pos+20]
        self.pos = (self.pos + 20) % len(self.data)
        if self.pos + 20 >= len(self.data):
            self.round += 1
            if self.round == 2:
                self.finish = True
        return djb2(base, 60000)
    
    def about_to_finish(self):
        return self.finish
    
    def update_data(self, data):
        self.data = data
        self.pos = 0
        self.round = 0
        self.finish = False

    def get_len(self):
        return len(self.data)
