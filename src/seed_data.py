from bernstein import djb2

class SeedData:
    def __init__(self, data):
        self.data = data
        self.pos = 0
        self.finish = False

    def get_seed(self):
        base = self.data[self.pos:self.pos+50]
        self.pos = (self.pos + 50) % len(self.data)
        if self.pos + 50 >= len(self.data):
            self.finish = True
        return djb2(base, 60000)
    
    def about_to_finish(self):
        return self.finish
    
    def update_data(self, data):
        self.data = data
        self.pos = 0
        self.finish = False

    def get_len(self):
        return len(self.data)
