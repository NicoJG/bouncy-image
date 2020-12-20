import sys
import time

class ProgressBar:

    bar_length = 60

    def __init__(self,min_value,max_value,label):
        self.max = max_value
        self.min = min_value
        self.label = label
        self.current = min_value
        self.percent = 0
        self.running = False
        self.starting_time = 0
    
    def start(self):
        self.running = True
        self.starting_time = time.time()
        self.draw()

    def update(self,value):
        self.current = value
        self.percent = round( (self.current - self.min)/(self.max - self.min), 3 )
        if self.percent > 1: 
            self.percent = 1.0
        if self.running:
            self.draw()

    def draw(self):
        filled_length = int(round(ProgressBar.bar_length*self.percent))
        bar_str = '█' * filled_length + '-' * (ProgressBar.bar_length - filled_length)
        print(f"  {self.label} |{bar_str}| {round(self.percent*100,1)}%", end = "\r")

    def end(self):
        if self.running:
            self.running = False
            elapsed_time = round(time.time() - self.starting_time,1)
            print()
            print(f"  {self.label} finished (it took {elapsed_time} seconds)")
