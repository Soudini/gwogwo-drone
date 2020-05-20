from robot import Robot
import numpy as np
from math import exp

d_star = 1
alpha = exp(d_star)


class Shepherd(Robot):
    def __init__(self, pos=[0, 0]):
        super().__init__(pos)

    def get_control(self, sheeps, sheperds):
        """returns dxu for the robot in numpy array formated as [x,y]"""
        potential = lambda x: self.to_sheeps_potential(x, sheeps)
        return self.get_potential_direction(potential)

    def to_sheeps_potential(self, location, sheeps):
        distances = np.array([np.linalg.norm(location - sheep.pos) for sheep in sheeps])
        # distances = np.apply_along_axis(lambda sheep: np.linalg.norm(location - sheep.pos), axis=0, arr=sheeps)
        potentials = distances + alpha * np.exp(-distances)

        return np.sum(potentials)
