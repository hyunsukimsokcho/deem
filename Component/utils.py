import time

class Timer:
    def __init__(self):
        pass

    def tictic(self):
        self.tic = time.time()

    def toctoc(self, msg):
        print("====="+msg+"=====\n", "%0.5f" % (time.time() - self.tic), "sec")

if __name__ == "__main__":
    timer = Timer()
    timer.tic()
    time.sleep(3)
    timer.toc('hello, world')
