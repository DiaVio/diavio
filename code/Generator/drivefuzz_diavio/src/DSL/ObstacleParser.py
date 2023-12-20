import DSL as sd

class Obstacles(object):
    def __init__(self) -> None:
        self.type = "unmentioned"
        self.Location = None

    def setType(self,type):
        self.type = type

    def setLocation(self, location):
        self.location = location

    def hasObstacle(self):
        if self.Location is not None:
            return True
        else:
            return False
        
    def get_dict(self):
        if self.hasObstacle():
            return self.__dict__
        else:
            return "unmentioned"