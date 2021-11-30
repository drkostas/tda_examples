import traceback
import argparse
from itertools import product

def _argparser() -> argparse.Namespace:
    """Setup the argument parser

    Returns:
        argparse.Namespace:
    """
    parser = argparse.ArgumentParser(
        description='Generate data points for tda',
        add_help=False)
    # Required Args
    required_args = parser.add_argument_group('Required Arguments')
    required_args.add_argument('-n', '--num-rectangles', type=int, required=True)
    # Optional args
    optional_args = parser.add_argument_group('Optional Arguments')
    optional_args.add_argument("-h", "--help", action="help", help="Show this help message and exit")

    return parser.parse_args()


def main():
    """This is the main function of tda_playground.py

    Example: python tda_playground/generate_points.py -n 2

    """

    # Initializing
    args = _argparser()
    num_rectangles = args.num_rectangles
    base_distance = 2*2**(num_rectangles/2)
    for rect_ind in range(num_rectangles):
        edge_length = 2**(rect_ind/2)
        base_coords = [base_distance*rect_ind, base_distance*rect_ind+edge_length]
        points = product(base_coords, repeat=2)
        [print("        - x: {}\n          y: {}".format(*point)) for point in points]


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(str(e) + '\n' + str(traceback.format_exc()))
        raise e
