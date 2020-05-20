from robot import Robot


class Sheep(Robot):
    def __init__(self,  pos = [0,0,0]):
        super().__init__(pos)
    
    def get_control(self, sheeps, sheperds):
        pass