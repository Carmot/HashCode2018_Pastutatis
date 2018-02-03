# coding=utf-8
import argparse
from operator import add

TOMATO = 'T'
MUSHROOM = 'M'


def calculate_score(nslices, *slices):
    """
    Dada una solucion valida, calcula el scoring
    :param nslices: Numero de porciones
    :param slices: Lista de definicion de porciones
    :return: Numero de celdas utilizadas en una porcion.
    """
    return 0


def validate(nslices, *slices):
    """
    Valida si la solucion es valida
    :param nslices: Numero de porciones
    :param slices: Lista de definicion de porciones
    :return: True si la solucion es válida
    """
    return False


def odd(number):
    """
    Devuelve true si el numero es impar
    :param number: Numero a comprobar
    :type number: int
    :return: True si el numero es impar
    :rtype: bool
    """
    return number % 2 == 1


class Cutter(object):
    def __init__(self, nrows, ncols, slicemin, slicemax, pizza):
        self.nrows = nrows
        self.ncols = ncols
        self.slicemin = slicemin
        self.slicemax = slicemax
        self.pizza = pizza[:]
        self.nslices = 0
        self.slices = []

    def get_next_untouched(self, r1, c1):
        """
        Devuelve la primera celda de la pizza que no está asignada a ninguna porcion
        :return:
        """
        for r in range(min(r1, self.nrows), self.nrows):
            for c in range(self.ncols):
                if (r != r1 or c > c1) and (self.pizza[r][c] in [TOMATO, MUSHROOM]):
                    return r, c
        return -1, -1

    def is_zone_free(self, r1, c1, r2, c2):
        """
        Mira a ver si la seccion está libre
        :param r1:
        :param c1:
        :param r2:
        :param c2
        :return:
        """
        for r in range(r1, min(r2 + 1, self.nrows)):
            for c in range(c1, min(c2 + 1, self.ncols)):
                if self.pizza[r][c] not in [TOMATO, MUSHROOM]:
                    return False
        return True

    def sum_ingredients(self, r1, c1, r2, c2):
        tomatoes, mushrooms = 0, 0
        for r in range(r1, r2 + 1):
            for c in range(c1, c2 + 1):
                if self.pizza[r][c] == TOMATO:
                    tomatoes += 1
                elif self.pizza[r][c] == MUSHROOM:
                    mushrooms += 1
        return tomatoes, mushrooms

    def has_enoguh_ingredients(self, r1, c1, r2, c2):
        t, m = self.sum_ingredients(r1, c1, r2, c2)
        print('Tomatoes: {}, Mushrooms: {}'.format(t, m))
        return t >= self.slicemin and m >= self.slicemin

    def size_correct(self, r1, c1, r2, c2):
        return (max(r2, r1) - min(r2, r1)) * (max(c2, c1) - min(c1, c2)) < self.slicemax

    def portion_in_pizza(self, r1, c1, r2, c2):
        return 0 <= r1 < self.nrows and 0 <= r2 < self.nrows and 0 <= c1 < self.ncols and 0 <= c2 < self.ncols

    def reserve_slice(self, r1, c1, r2, c2):
        print('Reservamos la porcion')
        for r in range(r1, r2 + 1):
            for c in range(c1, c2 + 1):
                self.pizza[r][c] = str(self.nslices)

    def cut_pizza(self):
        """
        Corta la pizza teniendo en cuenta los requisitos
        :param ncols: Numero de columnas de la pizza
        :param nrows: Numero de filas de la pizza
        :param slicemin: Numero minimo de ingredientes de cada porcion
        :param slicemax: Numero máximo de celdas por porcion
        :param pizza: Matriz con la distribucion de ingredientes de la pizza
        :return: (nslices, *porciones) Tupla con numero de de porciones y lista de definicion de porciones
        """

        r1, c1 = 0, 0
        while self.portion_in_pizza(r1, c1, r1, c1):
            self.step(r1, c1, r1, c1, 2)
            r1, c1 = self.get_next_untouched(r1, c1)
        r1, c1 = 0, 0
        while self.portion_in_pizza(r1, c1, r1, c1):
            self.step(r1, c1, r1, c1, 3)
            r1, c1 = self.get_next_untouched(r1, c1)

        self.print_pizza(-1, -1, -1, -1)

    def print_pizza(self, r1, c1, r2, c2):
        for r in range(self.nrows):
            row = []
            for c in range(self.ncols):

                spaces = (len(str(self.nslices)) - len(self.pizza[r][c]) + 1) * ' '
                if r2 >= r >= r1 and c2 >= c >= c1:
                    template = '({}){}'
                else:
                    template = ' {}{}'
                row.append(template.format(self.pizza[r][c], spaces))
            print(*row)

    def step(self, r1, c1, r2, c2, position):
        portion = [r1, c1, r2, c2]
        mask = [0, 0, 0, 0]
        mask[position] = 1
        nextportion = list(map(add, portion, mask))
        if self.portion_in_pizza(*nextportion) and self.size_correct(*nextportion) and self.is_zone_free(*nextportion):
            portion = nextportion[:]
            if self.has_enoguh_ingredients(*nextportion):
                self.reserve_slice(*portion)
                self.slices.append(portion)
                self.nslices += 1
                return True
        else:
            print('Camino muerto')
            return False


def process_requirements(filename):
    with open(filename) as fp:
        definition = fp.readline().strip()
        nrows, ncols, slicemin, slicemax = map(int, definition.split(' '))
        matrix = [list(line) for line in fp.read().splitlines()]
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
    cutter = Cutter(**requirements)
    cutter.cut_pizza()


if __name__ == '__main__':
    main()
