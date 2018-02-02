"""
NOTAS:
Es importante tener en cuenta que si la partición tiene más de una fila, todas las filas deben tener el mismo número de
elementos y lo mismo pasa para las columnas.

Opción 1: Calcular primero las posibles formas según la cantidad mínima de ingredientes diferentes y del número máximo
de celdas en la partición y el tamaño de la matriz.
Ejemplo:
l = 1; h=4
Figuras posibles = 1x2, 1x3, 1x4 y 2x2
l=2; h=4
Figuras posibles = 1x4 y 2x2
l=1; h=6
Figuras posibles = 1x2, 1x3, 1x4, 1x5, 1x6, 2x2 y 2x3
Obviamente si r*c es 5*3, la figura 1x6 no tendría sentido, se descartaría comprobando el tamaño de la matriz
Se podría resolver recursivamente (de manera no eficiente)  probando cada una de las figuras desde la posición [0,0] y
llamando a la función con la matrix recortada. Creo que es una explosión de combinatoria demasiado tocha para casos
grandes.

Opción 2:
Contar los ingredientes y empezar a cortar la pizza utilizando el ingrediente minoritario. Recorres la matriz hasta que
encuentras ese ingrediente e intentas hacer la mayor particion posible, intentando maximizar las celdas de las que
vienes porque no incluían ese ingrediente.

"""
FIGURES_EXAMPLE = [[2, 3], [3, 2], [2, 2], [1, 5], [1, 4], [1, 3], [1, 2]]
FIGURES = [[1, 5], [5, 1], [2, 2], [1, 4], [4, 1], [1, 3], [3, 1], [1, 2], [2, 1]]


class Pizza:
    def __init__(self, values):
        self.r = int(values[0])
        self.c = int(values[1])
        self.l = int(values[2])
        self.h = (values[3])
        self.p = [[0 for x in range(self.c)] for y in range(self.r)]
        self.figures = []

    def __str__(self):
        print("Rows: ", self.r)
        print("Columns: ", self.c)
        print("Min ingredients: ", self.l)
        print("Max cells/slice: ", self.h)
        print("Matrix: ")
        for row in self.p:
            print(row)
        return ''

    def figures(self):
        m = min(self.r, self.c)
        for i in range(1,m):
            self.figures.append()

    def cut(self):
        print("Cutting pizza...")

    def cut_first_approach(self, x, y, slice_list):
        """
        1.- Comprobar que no hemos llegado al final de la matriz
        2.- Comprobar que esa celda no esté cortada ya, es decir, no pertenezca a la solución.
        3.- Seleccionar figura a aplicar, mayor prioridad más grande.
        4.- Comprobar que la figura a aplicar cumple los mínimos de ingredientes
        5.- Añadir la porción a slice_list y volver a llamar a la función.
        6.- Si en un caso no se puede aplicar ninguna figura pasamos a la siguiente celda hasta la última de la matriz.
        """
        # Hemos llegado al final de la matriz
        if (x >= self.c-1) & (y >= self.r-1):
            print_result(slice_list)
        else:
            if not is_in_solution(x, y, slice_list):
                for figure in FIGURES:
                    if self.can_cut_slice(x, y, figure, slice_list):
                        # Add Figure to slice_list
                        slice_list.append([[x, y], [x+figure[0]-1, y+figure[1]-1]])
                        break
            x, y = self.next_cell(x, y)
            self.cut_first_approach(x, y, slice_list)

    def next_cell(self, column, row):
        if column == self.c-1:
            column = 0
            row += 1
        else:
            column += 1
        return column, row

    def has_enough_ingredients(self, x, y, slice):
        """
        Return true if a slice contains at least 'L' tomatoes and 'L' mushrooms. Otherwise, return false.
        :param slice: a part of the pizza [[r1,r2], [c1,c2]]
        :type slice: [][]
        :return:
        :rtype boolean
        """
        count_tomatoes = 0
        count_mushrooms = 0
        for indexX in range(x, x + slice[0]):
            for indexY in range(y, y + slice[1]):
                if self.p[indexY][indexX] == 'T':
                    count_tomatoes = + 1
                elif self.p[indexY][indexX] == 'M':
                    count_mushrooms = + 1
                else:
                    print("Found a strange ingredient in the pizza: ", self.p[indexX][indexY])
        return count_tomatoes >= self.l & count_mushrooms >= self.l

    def all_cells_are_free(self, x, y, figure, slice_list):
        # x + figure[0] & y + figure[1]
        # no estan en slice_list
        for indexX in range(x, x + figure[0]-1):
            for indexY in range(y, y + figure[1]-1):
                if is_in_solution(indexX, indexY, slice_list):
                    return False
        return True

    def can_cut_slice(self, x, y, figure, slice_list):
        if ((x + figure[0] - 1) > self.c - 1) | (y + figure[1] - 1 > self.r - 1):
            return False
        else:
            return self.has_enough_ingredients(x, y, figure) & self.all_cells_are_free(x, y, figure, slice_list)


def print_result(result):
    print("Pizza cut!")
    print(len(result))
    for slice_pizza in result:
        print(slice_pizza)


def is_in_solution(x, y, slice_list):
    """
    Return true if cell(x,y) is in any rectangle define by slice_list
    :param x:
    :param y:
    :param slice_list: -> [ [[r1,r2], [c1,c2]], [[r3,r4],[c3,c4]], ...]
    :return:
    :rtype: boolean
    """
    for slice in slice_list:
        if (x >= slice[0][0]) & (x <= slice[1][0]) & (y >= slice[0][1]) & (y <= slice[1][1]):
            return True
    return False


if __name__ == '__main__':
    file = open("input/small.in", "r")
    lines = file.readlines()
    pizza = Pizza(lines[0].split())
    for indexX, line in enumerate(lines[1:]):
        for indexY, ingredient in enumerate(line):
            if ingredient != '\n':
                pizza.p[indexX][indexY] = ingredient
    print(pizza)
    slice_list = []
    pizza.cut_first_approach(0, 0, slice_list)
