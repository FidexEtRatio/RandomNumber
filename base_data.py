from bernstein import djb2
import time

class BaseData:
    def __init__(self, data):
        self.data = data
        self.pos = 0
        self.last_run = 0

    def get_base(self):
        base = self.data[self.pos:self.pos+20]
        self.pos = (self.pos + 20) % len(self.data)
        return djb2(base, 60000)
    
    def about_to_finish(self):
        current_time = time.time()
        return current_time - self.last_run >= 1200
    
    def update_data(self, data):
        self.data = data
        self.pos = 0
        self.last_run = 0

    def get_len(self):
        return len(self.data)
