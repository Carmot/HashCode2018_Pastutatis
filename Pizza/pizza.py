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
FIGURES = [[1, 2], [1, 3], [1, 4], [1, 5], [2, 3], [3, 2]]
L = 1;

class Pizza:
    def __init__(self, values):
        self.r = int(values[0])
        self.c = int(values[1])
        self.l = int(values[2])
        self.h = (values[3])
        self.p = [[0 for x in range(self.c)] for y in range(self.r)]

    def __str__(self):
        print("Rows: ", self.r)
        print("Columns: ", self.c)
        print("Min ingredients: ", self.l)
        print("Max cells/slice: ", self.h)
        print("Matrix: ")
        for row in self.p:
            print(row)
        return ''

    def cut(self):
        print("Cutting pizza...")


def validate_slice(slice, L):
    """
    Return true if a slice contains at least 'L' tomatoes and 'L' mushrooms. Otherwise, return false.
    :param slice: a part of the pizza
    :type slice: [][]
    :param L: minimum number of each ingredient cells in a slice
    :type L: int
    :return:
    :rtype boolean
    """
    count_tomatoes = 0
    count_mushrooms = 0
    for row in slice:
        for cell in row:
            if cell == 'T':
                count_tomatoes =+ 1
            elif cell == 'M':
                count_mushrooms =+ 1
            else:
                print("Found a strange ingredient in the pizza: ", cell)
    return count_tomatoes > L & count_mushrooms > L


def validate(matrix, x, y, slice_list):
    print("Validating pizza...")
    for r, c in FIGURES:
        try:
            matrix[x+r][y+c]
        except IndexError:
            pass
        else:
            slice = []
            for row in matrix[x:r]:
                for item in row[y:c]:
                    slice.append(item)
            if validate_slice(slice, L):
                slice_list.append(slice)
                validate(matrix, x+r, y+c, slice_list)
                break


if __name__ == '__main__':
    file = open("input/example.in", "r")
    lines = file.readlines()
    pizza = Pizza(lines[0].split())
    for indexX, line in enumerate(lines[1:]):
        for indexY, ingredient in enumerate(line):
            if ingredient != '\n':
                pizza.p[indexX][indexY] = ingredient
    print(pizza)
    slice_list = []
    validate(pizza.p, 0, 0, slice_list)
    pizza.cut()
