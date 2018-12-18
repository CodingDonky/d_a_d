import os, sys
ENV_DIR = os.environ['ENV_DIR']
sys.path.append(ENV_DIR+'src/utilities/')
from globals import *

class Timer:

    def __init__(self, interval = 1):
        self.Interval = interval
        self.Value = 0
        self.LastInt = 0
        self.Active = False
        self.OnNext = None

    def Update(self):
        if self.Active:
            self.Value += Globals.deltatime / self.Interval
            if int(self.Value) != int(self.LastInt):
                self.LastInt = int(self.Value)
                if self.OnNext != None:
                    self.OnNext()

    def Start(self):
        self.Active = True

    def Pause(self):
        self.Active = False

    def Stop(self):
        self.Reset()
        self.Active = False

    def Reset(self):
        self.Value = 0
        self.LastInt = 0
        self.Active = True
