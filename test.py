from queue import PriorityQueue


def __init__(self, value, parent,
                 start = 0,
                 goal = 0):

        self.children = []
        self.parent = parent
        self.value = value
        self.dist = 0

        if parent:
            self.start  = parent.start
            self.goal   = parent.goal
            self.path   = parent.path[:]
            self.path.append(value)
        else:
            self.path   = [value]
            self.start  = start
            self.goal   = goal

def GetDistance(self):
        pass

def CreateChildren(self):
        pass

class State_String(State):
    def __init__(self,value,parent,
                 start = 0,
                 goal = 0):

        super(State_String, self).__init__(value, parent, start, goal)
        self.dist = self.GetDistance()