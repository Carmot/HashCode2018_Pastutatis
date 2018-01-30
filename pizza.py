# coding=utf-8
import argparse


def process_requirements(filename):
    with open(filename) as fp:
        definition = fp.readline().strip()
        ncols, nrows, slicemin, slicemax = map(int, definition.split(' '))
        matrix = fp.read().splitlines()
        return {'ncols': ncols, 'nrows': nrows, 'slicemin': slicemin, 'slicemax': slicemax, 'pizza': matrix}


def define_parser():
    """
    Crea un procesador de argumentos de entrada con un único argumento posicional
    :return:
    """
    parser = argparse.ArgumentParser(description='Let\'s cut some pizzas!')
    parser.add_argument('filename', metavar='filename', type=str, help='path to description file')
    return parser


def main():
    parser = define_parser()
    args = parser.parse_args()
    filename = args.filename
    requirements = process_requirements(filename)
    print(requirements)


if __name__ == '__main__':
    main()
