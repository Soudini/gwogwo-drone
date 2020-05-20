import numpy as np

GRADIENT_STEP = 0.1
class Robot:
    def __init__(self, pos=[0, 0, 0]):
        self.pos = pos

    def get_distance(self, target):
        return np.linalg.norm(self.pos[:2] - target.pos[:2])

    def get_potential_direction(self, potential):
        gradient = np.array([
                potential(self.pos + GRADIENT_STEP * np.array([1,0])),
                potential(self.pos + GRADIENT_STEP * np.array([0,1]))
            ])
        return gradient