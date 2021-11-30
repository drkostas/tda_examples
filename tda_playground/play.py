import traceback
import logging
import argparse
import os
import time
import numpy as np
from multidim import PointCloud
import imageio
from glob import glob
from ripser import ripser
from mogutda import SimplicialComplex

from tda_playground.fancy_log.colorized_log import ColorizedLog
from tda_playground.configuration.configuration import Configuration
from tda_playground.plotter.pyplot_plotter import plt, config_point_to_np_points, complex_plot, \
    simple_scatter, plot_simplicial_complex, point_cloud_fig, plot_persistence_diagram

logger = ColorizedLog(logging.getLogger('Main'), 'yellow')


def timeit(method: object) -> object:
    """Decorator for counting the execution times of functions

    Args:
        method (object):
    """

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            logger.info('%r  %2.2f ms' % (method.__name__, (te - ts) * 1000))
        return result

    return timed


def _setup_log(log_path: str = '../logs/default.log', debug: bool = False) -> None:
    """Set the parameters of the logger

    Args:
        log_path (str): The path the log file is going to be saved
        debug (bool): Whether to print debug messages or not
    """
    log_path = log_path.split(os.sep)
    if len(log_path) > 1:

        try:
            os.makedirs((os.sep.join(log_path[:-1])))
        except FileExistsError:
            pass
    log_filename = os.sep.join(log_path)
    # noinspection PyArgumentList
    logging.basicConfig(level=logging.INFO if debug is not True else logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        handlers=[
                            logging.FileHandler(log_filename),
                            logging.StreamHandler()
                        ]
                        )


def _argparser() -> argparse.Namespace:
    """Setup the argument parser

    Returns:
        argparse.Namespace:
    """
    parser = argparse.ArgumentParser(
        description='TDA playground main runtime.',
        add_help=False)
    # Required Args
    required_args = parser.add_argument_group('Required Arguments')
    config_file_params = {
        'type': argparse.FileType('r'),
        'required': True,
        'help': "The configuration yml file"
    }
    required_args.add_argument('-c', '--config-file', **config_file_params)
    # Optional args
    optional_args = parser.add_argument_group('Optional Arguments')
    optional_args.add_argument('-l', '--log',
                               default='logs/default.log',
                               help="Name of the output log file")
    optional_args.add_argument('-d', '--debug', action='store_true',
                               help='Enables the debug log messages')
    optional_args.add_argument("-h", "--help", action="help", help="Show this help message and exit")

    return parser.parse_args()


def run_gda(conf):
    # Cleanup
    base_folder = conf['results_folder']
    if not os.path.isdir(base_folder):
        os.makedirs(base_folder)
    [os.remove(os.path.join(base_folder, file)) for file in os.listdir(base_folder) if
     file.endswith('.png')]
    # Create PointCloud
    scatter_points = config_point_to_np_points(conf['points'])
    sc_cloud = PointCloud(scatter_points.astype(np.float64), max_length=-1.0)
    # Iterate for each cutoff
    cutoffs = np.arange(conf['cutoff_min'], conf['cutoff_lim'], conf['cutoff_step'])
    max_epsilon = cutoffs[-1] + 1
    for cutoff in cutoffs:
        sc_cloud.reset()
        # sc_cloud.make_pers0(cutoff=cutoff)
        sc_cloud.make_pers1_rca1(cutoff=cutoff)

        show_fig = True if cutoff == cutoffs[-1] else conf['show_fig']
        complex_plot(cutoff, scatter_points, sc_cloud,
                     max_epsilon=max_epsilon, base_folder=base_folder,
                     show_fig=show_fig, save_fig=conf['save_fig'])

    if conf['create_gif']:
        images = []
        for img in sorted(glob(base_folder + '/*.png')):
            images.append(imageio.imread(img))
        imageio.mimsave(base_folder + '/2_squares.gif', images, format='GIF',
                        duration=len(cutoffs) / 16)


def run_rips(conf):
    # Cleanup
    base_folder = conf['results_folder']
    if not os.path.isdir(base_folder):
        os.makedirs(base_folder)
    [os.remove(os.path.join(base_folder, file)) for file in os.listdir(base_folder) if
     file.endswith('.png')]
    # Create Rips object
    scatter_points = config_point_to_np_points(conf['points']).astype(np.float64)
    # Run and plot
    cutoffs = np.arange(conf['cutoff_min'], conf['cutoff_lim'], conf['cutoff_step'])
    xy_range = (scatter_points[:, 0].min() - 1, scatter_points[:, 0].max() + 1,
                scatter_points[:, 1].min() - 1, scatter_points[:, 1].max() + 1)
    pers_range = (-1, cutoffs[-1] + 1, -1, cutoffs[-1] + 1)
    rand_x = np.random.uniform(0.05, 0.15, 100)
    rand_y = np.random.uniform(0.05, 0.1, 100)
    for cutoff in cutoffs:
        result = ripser(scatter_points, thresh=cutoff, maxdim=2,
                        do_cocycles=True)
        diagrams = result['dgms']
        cocycles = result['cocycles']
        D = result['dperm2all']
        # Plot
        fig, canvas = plt.subplots(nrows=1, ncols=3, figsize=(18, 6), dpi=100)
        # fig.suptitle("Rips Algorithm (Epsilon: %.3g)" % cutoff)
        fig.tight_layout(pad=0.5)
        point_cloud_fig(canvas=canvas[0], points_np=scatter_points, cutoff=cutoff, xy_range=xy_range)
        dgm1 = diagrams[1]
        if len(dgm1) > 0:
            idx = np.argmax(dgm1[:, 1] - dgm1[:, 0])
            cocycle = cocycles[1][idx]
        else:
            cocycle = np.array([])
        plot_simplicial_complex(canvas[1], D, scatter_points, cocycle, cutoff)
        plot_persistence_diagram(canvas[2], diagrams, xy_range=pers_range,
                                 rand_x=rand_x, rand_y=rand_y)

        if conf['save_fig']:
            logger.info("Saving fig..")
            fig.savefig(os.path.join(base_folder, 'cutoff_{:.2f}.png'.format(cutoff)))
        if conf['show_fig']:
            logger.info("Showing fig..")
            plt.show()
        else:
            plt.close(fig)


@timeit
def main():
    """This is the main function of tda_playground.py

    Example: python tda_playground/main.py -m run_mode_1

        -c confs/template_conf.yml -l logs/output.log
    """

    # Initializing
    args = _argparser()
    _setup_log(args.log, args.debug)
    # Load the configuration
    config = Configuration(config_src=args.config_file)
    # Prints
    for conf in config.get_config(config_name='tda'):
        if conf['type'] == 'simple_scatter':
            logger.info("Plotting simple points selected.")
            simple_scatter(points=conf['config']['points'])
        elif conf['type'] == 'gda':
            logger.info("GDA and plotting is selected.")
            run_gda(conf=conf['config'])
        elif conf['type'] == 'rips':
            logger.info("RIPS and plotting is selected.")
            run_rips(conf=conf['config'])
        else:
            raise NotImplementedError("Not yet implemented")
    plt.show(block=True)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logging.error(str(e) + '\n' + str(traceback.format_exc()))
        raise e
