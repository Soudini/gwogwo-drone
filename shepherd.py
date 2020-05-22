from robot import Robot
import numpy as np
from math import exp, log, pi

D_STAR = 0.2  # distance to sheeps
ALPHA = D_STAR**2  # for repulsive potential towards sheep
BETA = exp(D_STAR)  # for repulsive potential towards sheep links

REPULSIVE_CONSTANT = 10*ALPHA  # between shepherds
COVERAGE_DIST = 10*D_STAR
SPEED_MULTIPLIER = 0.1 # for the speed command


class Shepherd(Robot):
    def __init__(self, pos=[0, 0]):
        super().__init__(pos)

    def get_control(self, sheeps, shepherds):
        """returns dxu for the robot in numpy array formated as [x,y]"""
        return SPEED_MULTIPLIER * self.get_potential_direction(self.get_potential(sheeps, shepherds))

    def get_potential(self, sheeps, shepherds):
        potential = lambda x: self.to_sheep_potential(x, sheeps) + self.to_shepherd_potential(x, shepherds) + self.to_sheep_line_potential(x, sheeps)
        # potential = lambda x: self.to_sheep_potential(x, sheeps) + self.to_shepherd_potential(x, shepherds)
        # potential = lambda x: self.to_sheep_line_potential(x, sheeps)
        # potential = lambda x: self.to_sheeps_potential(x, sheeps)
        # potential = lambda x: 1

        return potential

    def to_shepherd_potential(self, location, shepherds):
        distance = np.min(np.array([np.linalg.norm(location - shepherd.pos[:2]) for shepherd in shepherds if shepherd != self]))
        # distances = np.apply_along_axis(lambda sheep: np.linalg.norm(location - sheep.pos[:2]), axis=0, arr=sheeps)
        potential = REPULSIVE_CONSTANT / distance + REPULSIVE_CONSTANT * exp(-distance/COVERAGE_DIST)
        return potential

    def to_sheep_potential(self, location, sheeps):
        # finally we take into account only the closest sheep
        distance = np.min([np.linalg.norm(location - sheep.pos) for sheep in sheeps])
        return distance + ALPHA / distance

    def to_sheep_line_potential(self, location, sheeps):
        line_distances = [line_distance(location, sheeps[i].pos, sheeps[j].pos) for j in range(len(sheeps)) for i in range(j+1, len(sheeps))]
        potential = BETA * exp(-np.min(line_distances))
        return potential


TARGET_DIST = 0.5

class NewShepherd(Robot):
    def __init__(self, pos=[0, 0]):
        super().__init__(pos)

    def get_control(self, sheeps, shepherds):
        """returns dxu for the robot in numpy array formated as [x,y]"""
        return SPEED_MULTIPLIER * self.get_potential_direction(self.get_potential(sheeps, shepherds))

    def get_potential(self, sheeps, shepherds):
        # potential = lambda x: self.to_sheep_potential(x, sheeps) + self.to_shepherd_potential(x, shepherds) + self.to_sheep_line_potential(x, sheeps)
        # potential = lambda x: self.to_sheep_potential(x, sheeps) + self.to_shepherd_potential(x, shepherds)
        # potential = lambda x: self.to_sheep_line_potential(x, sheeps)
        # potential = lambda x: self.to_sheep_potential(x, sheeps) + self.to_target_potential(x, shepherds, sheeps)
        potential = lambda x: self.to_sheep_line_potential(x, sheeps) + self.to_target_potential(x, shepherds, sheeps)
        # potential = lambda x: self.to_target_potential(x, shepherds, sheeps)
        # potential = lambda x: 1

        return potential

    def to_shepherd_potential(self, location, shepherds):
        distance = np.min(np.array([np.linalg.norm(location - shepherd.pos[:2]) for shepherd in shepherds if shepherd != self]))
        # distances = np.apply_along_axis(lambda sheep: np.linalg.norm(location - sheep.pos[:2]), axis=0, arr=sheeps)
        potential = REPULSIVE_CONSTANT / distance + REPULSIVE_CONSTANT * exp(-distance/COVERAGE_DIST)
        return potential

    # def to_sheep_potential(self, location, sheeps):
    #     # finally we take into account only the closest sheep
    #     distance = np.min([np.linalg.norm(location - sheep.pos) for sheep in sheeps])
    #     # return distance + ALPHA / distance
    #     return ALPHA / distance

    def to_sheep_line_potential(self, location, sheeps):
        line_distances = [line_distance(location, sheeps[i].pos, sheeps[j].pos) for j in range(len(sheeps)) for i in range(j+1, len(sheeps))]
        # potential = BETA * exp(-np.min(line_distances))
        # return potential
        return ALPHA / np.min(line_distances)

    def compute_target_position(self, shepereds, sheeps):
        sheeps_pos = np.array([sheep.pos for sheep in sheeps])
        herd_center = np.mean(sheeps_pos, axis=0)

        sheep_spreading = np.apply_along_axis(lambda sheep: np.linalg.norm(sheep - herd_center), 1, sheeps_pos)
        herd_radius = np.max(sheep_spreading)  # radius of the circle that surrounds the herd

        furthest_sheep = sheeps_pos[np.argmax(sheep_spreading)]

        # generating target positions for the shepherds all around the herd
        first_target = furthest_sheep + TARGET_DIST * (furthest_sheep - herd_center)/np.linalg.norm(furthest_sheep - herd_center)
        n = len(shepereds)
        thetas = np.array([i*2*pi/n for i in range(n)])
        C, S = np.cos(thetas), np.sin(thetas)
        target_positions = [herd_center + np.dot(np.array(((c, -s), (s, c))), first_target - herd_center) for c, s in zip(C, S)]



        return target_positions

    def to_target_potential(self, location, shepereds, sheeps):
        # target = self.compute_target_position(shepereds, sheeps)
        # return np.linalg.norm(target - location)

        targets = self.compute_target_position(shepereds, sheeps)
        return sum([1/np.linalg.norm(location - target) for target in targets])


def line_distance(location, point_1, point_2):
    u = point_2 - point_1
    n = u/np.linalg.norm(u)

    v1 = location - point_1
    v2 = location - point_2

    d_norm = np.cross(v1, n)
    d_tan = np.dot(v1, n)

    if d_tan < 0:
        return np.linalg.norm(v1)
    if d_tan > np.dot(u, n):
        return np.linalg.norm(v2)

    return abs(d_norm)

