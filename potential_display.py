import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
from sheep import Sheep
from shepherd import Shepherd

# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import


def plot_potential(potential):
    # set up a figure twice as wide as it is tall
    fig = plt.figure(figsize=plt.figaspect(1))

    # set up the axes for the first plot
    ax = fig.add_subplot(1, 1, 1, projection='3d')

    # plot a 3D surface like in the example mplot3d/surface3d_demo
    X = np.arange(-2, 2, 0.1)
    Y = np.arange(-2, 2, 0.1)
    X, Y = np.meshgrid(X, Y)

    # POTENTIAL
    Z = np.apply_along_axis(potential, 0, np.array((X, Y)))
    Z = np.clip(Z, -4, 4)

    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm,
                           linewidth=0, antialiased=False)
    # ax.set_zlim(-3, 3)
    fig.colorbar(surf, shrink=0.5, aspect=10)

    plt.show()


if __name__ == "__main__":
    sheep = Sheep([0, 0])
    shepered = Shepherd([1, 0])

    # potential = lambda pos: shepered.to_sheep_potential(pos, [sheep])
    potential = lambda pos: shepered.line_potential(pos, np. zeros(2), np.array((0, 1)))

    plot_potential(potential)
