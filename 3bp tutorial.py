
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

plt.style.use('dark_background')

G = 6.674e-11

def arr(arg: list):
    return np.array(arg)

def get_accelerations(p1, p2, p3, m1, m2, m3):
    """
    Find acceleration of each planet in a three-body system based on Newton's laws
    
    :param p1: Position vector of planet 1
    :param p2: Position vector of planet 2
    :param p3: Position vector of planet 3
    """
    a1 = G * m2 * (p1 - p2)/(np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 + (p1[2] - p2[2])**2)**3) + \
        G * m3 * (p1 - p3)/(np.sqrt((p1[0] - p3[0])**2 + (p1[1] - p3[1])**2 + (p1[2] - p3[2])**2)**3)

    a2 = G * m3 * (p2 - p3)/(np.sqrt((p2[0] - p3[0])**2 + (p2[1] - p3[1])**2 + (p2[2] - p3[2])**2)**3) + \
	    G * m1 * (p2 - p1)/(np.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2 + (p2[2] - p1[2])**2)**3)

    a3 = G * m1 * (p3 - p1)/(np.sqrt((p3[0] - p1[0])**2 + (p3[1] - p1[1])**2 + (p3[2] - p1[2])**2)**3) + \
	    G * m2 * (p3 - p2)/(np.sqrt((p3[0] - p2[0])**2 + (p3[1] - p2[1])**2 + (p3[2] - p2[2])**2)**3)

    return a1, a2, a3

def plot_arr(arr, colour = 'white'):
    plt.plot([i[0] for i in arr], [j[1] for j in arr], [k[2] for k in arr], '^', color=colour, lw = 0.05, markersize = 0.01, alpha=0.5)

def main():
    
    # Initial conditions
    # Planet masses
    m1 = 10
    m2 = 20
    m3 = 30

    # Starting positions where p1_0 = [x1, y1, z1]
    p1_0 = arr([-10, 10, -11])
    v1_0 = arr([-3, 0, 0])

    p2_0 = arr([0, 0, 0])
    v2_0 = arr([0, 0, 0])
    
    p3_0 = arr([10, 10, 12])
    v3_0 = arr([3, 0, 0])

    # Parameters
    delta_t = 0.001
    steps = 200000

    # Trajectory array
    p1arr = arr([np.zeros(3) for _ in range(steps)])
    v1arr = arr([np.zeros(3) for _ in range(steps)])

    p2arr = arr([np.zeros(3) for _ in range(steps)])
    v2arr = arr([np.zeros(3) for _ in range(steps)])

    p3arr = arr([np.zeros(3) for _ in range(steps)])
    v3arr = arr([np.zeros(3) for _ in range(steps)])

    # Put in starting values
    p1arr[0], p2arr[0], p3arr[0] = p1_0, p2_0, p3_0
    v1arr[0], v2arr[0], v3arr[0] = v1_0, v2_0, v3_0

    # Evolve system
    for i in range(1, steps):
        a1, a2, a3 = get_accelerations(p1arr[i-1], p2arr[i-1], p3arr[i-1], m1, m2, m3)

        v1arr[i] = v1arr[i-1] + a1 * delta_t
        v2arr[i] = v2arr[i-1] + a2 * delta_t
        v3arr[i] = v3arr[i-1] + a3 * delta_t

        p1arr[i] = p1arr[i-1] + v1arr[i-1] * delta_t
        p2arr[i] = p2arr[i-1] + v2arr[i-1] * delta_t
        p3arr[i] = p3arr[i-1] + v3arr[i-1] * delta_t
    

    # Matplotlib plot
    fig = plt.figure(figsize = (8,8))
    axes = fig.add_subplot(projection = '3d')
    plt.gca().patch.set_facecolor('black')

    plot_arr(p1arr, 'red')
    plot_arr(p2arr, 'blue')
    plot_arr(p3arr, 'green')

    plt.axis('on')
    axes.set_xticks([]), axes.set_yticks([]), axes.set_zticks([])

    axes.xaxis.set_pane_color((0.0, 0.0, 0.0, 1.0)), axes.yaxis.set_pane_color((0.0, 0.0, 0.0, 1.0)), axes.zaxis.set_pane_color((0.0, 0.0, 0.0, 1.0))
    plt.show()
    plt.close()

if __name__ == "__main__":
    main()