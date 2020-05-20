from sheep import Sheep
from shepherd import Shepherd

import numpy as np
import time

sheep = Sheep(pos = np.array([1,1,0]))
sheep_2 = Sheep(pos = np.array([1,2,0]))
shepherd = Shepherd(pos = np.array([0,0,0]))

print(shepherd.get_control([sheep, sheep_2], [shepherd]))
