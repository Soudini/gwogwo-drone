import rps.robotarium as robotarium
from rps.utilities.transformations import *
from rps.utilities.barrier_certificates import *
from rps.utilities.misc import *
from rps.utilities.controllers import *


from sheep import Sheep
from shepherd import Shepherd

import numpy as np
import time

# Instantiate Robotarium object
N_SHEEP = 3
N_SHEPHERD = 2
N = N_SHEEP + N_SHEPHERD

ITERATIONS = 500

sheeps = [Sheep() for _ in range(N_SHEEP)]
shepherds = [Shepherd() for _ in range(N_SHEPHERD)]

initial_conditions = np.array(np.mat('1 0.5 -0.5 0 0.28; 0.8 -0.3 -0.75 0.1 0.34; 0 0 0 0 0'))
r = robotarium.Robotarium(number_of_robots=N, show_figure=True, initial_conditions=initial_conditions,sim_in_real_time=True)

# Create barrier certificates to avoid collision
uni_barrier_cert = create_unicycle_barrier_certificate()

# define x initially
x = r.get_poses()
r.step()

# While the number of robots at the required poses is less
# than N...

for iteration in range(ITERATIONS):

    # Get poses of agents
    x = r.get_poses()

    for i in range(x.shape[1]):
        (sheeps + shepherds)[i].pos = x[:,i].T

    dxu = np.zeros((2,N))
    for i in range(x.shape[1]):
        dxu[:,i] = (sheeps + shepherds)[i].get_control(sheeps, shepherds).T

    # Create safe control inputs (i.e., no collisions)
    dxu = uni_barrier_cert(dxu, x)

    # Set the velocities
    r.set_velocities(np.arange(N), dxu)

    # Iterate the simulation
    r.step()

#Call at end of script to print debug information and for your script to run on the Robotarium server properly
r.call_at_scripts_end()