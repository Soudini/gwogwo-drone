from robot import Robot


class Sheep(Robot):
    def __init__(self,  pos = [0,0,0]):
        super().__init__(pos)
    
    def get_control(self, sheeps, sheperds):
        """returns dxu for the robot in numpy array formated as [x,y]"""
        pass