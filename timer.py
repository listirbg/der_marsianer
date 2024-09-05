import time


class Timer:
    def __init__(self):
        self.start_time = 0
        self.elapsed_time = 0
        self.active = False

    def activate(self):
        self.start_time = time.time()
        self.active = True

    def update(self):
        self.elapsed_time = int(time.time() - self.start_time)

    def reset(self):
        self.start_time = 0
        self.elapsed_time = 0
        self.active = False


if __name__ == '__main__':
    t = Timer()
    t.activate()
    while t.elapsed_time < 100:
        t.update()
        print(t.elapsed_time)