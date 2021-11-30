from itertools import combinations
import matplotlib
import matplotlib.pyplot as plt
import logging
import numpy as np
from persim import plot_diagrams
import os

from tda_playground.fancy_log.colorized_log import ColorizedLog

matplotlib.use('Qt5Agg')
logger = ColorizedLog(logging.getLogger('Plotter'), 'blue')


def config_point_to_np_points(points):
    points = [(point['x'], point['y']) for point in points]
    return np.array(points)


def combo(arr, r):
    # return list of all subsets of length r
    # to deal with duplicate subsets use
    # set(list(combinations(arr, r)))
    return list(combinations(arr, r))


def are_circles_touching(circle_1_x, circle_1_y, circle_2_x, circle_2_y, rad):
    dist_sq = (circle_1_x - circle_2_x) ** 2 + (circle_1_y - circle_2_y) ** 2;
    rad_sum_sq = 4 * rad ** 2;
    if (dist_sq <= rad_sum_sq):
        return True
    else:
        return False


def complex_plot(cutoff, points_np, sc_cloud, max_epsilon, base_folder, show_fig, save_fig):
    try:
        fig, canvas = plt.subplots(nrows=1, ncols=3, figsize=(12, 6), dpi=100)
        fig.tight_layout()
        sc_cloud_pers0 = sc_cloud.pers0
    except ValueError as e:
        print("Persistence exception for cutoff={}\n{}".format(cutoff, e))
        return
    min_x = points_np[:, 0].min() - 1
    max_x = points_np[:, 0].max() + 1
    min_y = points_np[:, 1].min() - 1
    max_y = points_np[:, 1].max() + 1
    # Calculate plot boundaries
    canvas[0] = point_cloud_fig(canvas=canvas[0], points_np=points_np, cutoff=cutoff)

    # Plot 2 - Simplicial Complex
    circle_groups = {}
    for circle_1_ind, circle_1 in enumerate(points_np):
        circle_1_x, circle_1_y = circle_1[0], circle_1[1]
        circle_groups[circle_1_ind] = [circle_1_ind]
        for circle_2_ind, circle_2 in enumerate(points_np):
            if circle_1_ind != circle_2_ind:
                circle_2_x, circle_2_y = circle_2[0], circle_2[1]
                if are_circles_touching(circle_1_x, circle_1_y, circle_2_x, circle_2_y, cutoff):
                    canvas[1].plot((circle_1_x, circle_2_x), (circle_1_y, circle_2_y), color='cyan',
                                   alpha=0.5)
                    circle_groups[circle_1_ind].append(circle_2_ind)

    circle_triples = combo(range(len(points_np)), 3)
    for circle_1, circle_2, circle_3 in circle_triples:
        if circle_1 in circle_groups[circle_2] and circle_1 in circle_groups[circle_3] and \
                circle_2 in circle_groups[circle_3]:
            x1, y1 = points_np[circle_1][0], points_np[circle_1][1]
            x2, y2 = points_np[circle_2][0], points_np[circle_2][1]
            x3, y3 = points_np[circle_3][0], points_np[circle_3][1]
            canvas[1].add_patch(
                plt.Polygon(((x1, y1), (x2, y2), (x3, y3)),
                            facecolor='yellow', alpha=0.3))

    canvas[1].scatter(points_np[:, 0], points_np[:, 1], color='black')

    canvas[1].set_title('Simplicial Complex')
    canvas[1].set_xlabel('X-coordinate')
    canvas[1].set_ylabel('Y-coordinate')
    canvas[1].set_xlim([min_x, max_x])
    canvas[1].set_ylim([min_y, max_y])
    canvas[1].set_aspect('equal')

    # Plot 2 - Persistence Diagram
    canvas[2].axhline(y=cutoff, xmin=0, xmax=11, color='r')
    canvas[2].plot([0.0, 100.0], [0.0, 100.0], color='black')

    rectified = sc_cloud_pers0.transform()
    canvas[2].scatter(rectified[:, 0] + 0.1, rectified[:, 1], color='blue', alpha=0.7)
    canvas[2].set_title("Persistence Diagram")
    canvas[2].set_xlabel('Birth')
    canvas[2].set_ylabel('Death')
    canvas[2].legend(("Current Epsilon: %s" % cutoff,), loc="lower right")
    canvas[2].set_xlim([0, max_epsilon])
    canvas[2].set_ylim([0, max_epsilon])
    canvas[2].set_aspect('equal')

    if save_fig:
        logger.info("Saving fig..")
        fig.savefig(os.path.join(base_folder, '2_squares_{:.2f}.png'.format(cutoff)))
    if show_fig:
        logger.info("Showing fig..")
        plt.show(block=False)
    else:
        plt.close(fig)


def simple_scatter(points):
    scatter_points = config_point_to_np_points(points)
    plt.scatter(scatter_points[:, 0], scatter_points[:, 1], color='c')
    plt.title('Data Points Scatter Plot')
    plt.axis('equal')
    plt.show()
    plt.cla()


def point_cloud_fig(canvas, points_np, cutoff, xy_range):
    # Plot 1 - Point Cloud
    for point in points_np:
        canvas.add_patch(
            plt.Circle((point[0], point[1]), radius=cutoff, facecolor='cyan', alpha=0.8, lw=2,
                       edgecolor='black'))
    for point in points_np:
        canvas.add_patch(
            plt.Circle((point[0], point[1]), radius=0.01, facecolor='black', alpha=1, lw=1,
                       edgecolor='black'))

    # canvas[0].scatter(points_np[:, 0], points_np[:, 1], color='orange')

    canvas.set_title('Point Cloud')
    canvas.set_xlabel('X')
    canvas.set_ylabel('Y')
    canvas.set_xlim([xy_range[0], xy_range[1]])
    canvas.set_ylim([xy_range[2], xy_range[3]])
    canvas.set_aspect('equal')
    return canvas


def plot_persistence_diagram(canvas, diagrams, xy_range, rand_x, rand_y):
    for d_ind in range(len(diagrams)):
        for c_ind in range(len(diagrams[d_ind])):
            diagrams[d_ind][c_ind, 0] += rand_x[c_ind]
            diagrams[d_ind][c_ind, 1] += rand_y[c_ind]
    dgm1 = diagrams[1]
    if len(dgm1) > 0:
        idx = np.argmax(dgm1[:, 1] - dgm1[:, 0])
        x_coords = dgm1[idx, 0]
        y_coords = dgm1[idx, 1]
        plt.scatter(x_coords, y_coords, 20, 'k', 'x', zorder=3)
        # plt.figtext(0.95, 0.1, "Max 1D birth = %.3g, death = %.3g" % (x_coords, y_coords),
        #             va="bottom", ha="right", fontsize=8)
    else:
        plt.figtext(0.95, 0.1, "(No Data yet)",
                    va="bottom", ha="right", fontsize=8)

    canvas.set_title("Persistence Diagram")
    plot_diagrams(diagrams, show=False, ax=canvas, xy_range=xy_range)
    canvas.set_aspect('equal')


def drawLineColored(canvas, X, C):
    for i in range(X.shape[0] - 1):
        canvas.plot(X[i:i + 2, 0], X[i:i + 2, 1], c=C[i, :], linewidth=3, zorder=1)


def plot_simplicial_complex(canvas, D, X, cocycle, thresh):
    """
    Given a 2D point cloud X, display a cocycle projected
    onto edges under a given threshold "thresh"
    """
    # Plot all edges under the threshold
    N = X.shape[0]
    t = np.linspace(0, 1, 10)
    c = plt.get_cmap('Blues')
    C = c(np.array(np.round(np.linspace(0, 255, len(t))), dtype=np.int32))
    C = C[:, 1:4]

    for i in range(N):
        for j in range(N):
            if D[i, j] <= thresh:
                Y = np.zeros((len(t), 2))
                Y[:, 0] = X[i, 0] + t * (X[j, 0] - X[i, 0])
                Y[:, 1] = X[i, 1] + t * (X[j, 1] - X[i, 1])
                drawLineColored(canvas, Y, C)
    point_triples = combo(range(N), 3)
    for a, b, c in point_triples:
        if (D[a, b] <= thresh and D[a, c] <= thresh and D[b, c] <= thresh) \
                and (a != b and a != c and b != c):
            x1, y1 = X[a, 0], X[a, 1]
            x2, y2 = X[b, 0], X[b, 1]
            x3, y3 = X[c, 0], X[c, 1]
            canvas.add_patch(
                plt.Polygon(((x1, y1), (x2, y2), (x3, y3)),
                            facecolor='yellow', alpha=0.2, zorder=0))
    # Plot vertex labels
    canvas.scatter(X[:, 0], X[:, 1], s=5, color='black', zorder=2)
    min_x = X[:, 0].min() - 1
    max_x = X[:, 0].max() + 1
    min_y = X[:, 1].min() - 1
    max_y = X[:, 1].max() + 1
    canvas.set_title('Simplicial Complex')
    canvas.set_xlabel('X')
    canvas.set_ylabel('Y')
    canvas.set_xlim([min_x, max_x])
    canvas.set_ylim([min_y, max_y])
    canvas.set_aspect('equal')
    plt.figtext(0.50, 0.1, "Rips Algorithm (Epsilon: %.3g)" % thresh,
                va="bottom", ha="center", fontsize=8)
