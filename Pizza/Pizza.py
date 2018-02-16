#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import sys
import argparse

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

Opción 2:
Contar los ingredientes y empezar a cortar la pizza utilizando el ingrediente minoritario. Recorres la matriz hasta que
encuentras ese ingrediente e intentas hacer la mayor particion posible, intentando maximizar las celdas de las que
vienes porque no incluían ese ingrediente.

"""

class Pizza:
    def __init__(self, values):
        self.r = int(values[0])
        self.rx = self.r
        self.c = int(values[1])
        self.cx = self.c
        self.l = int(values[2])
        self.h = int(values[3])
        self.p = [[0 for x in range(self.c)] for y in range(self.r)]
        self.px = [[0 for x in range(self.c)] for y in range(self.r)]
        self.figures = []
        self.slice_list = []

    def __str__(self):
        print("Rows: ", self.r)
        print("Columns: ", self.c)
        print("Min ingredients: ", self.l)
        print("Max cells/slice: ", self.h)
        print("Matrix: ")
        for row in self.p:
            print(row)
        return ''

    def figure_Cmp(self, figure1, figure2):
        # El cacho más grande primero
        if (figure1[0] * figure1[1]) > (figure2[0] * figure2[1]):
            return 1
        elif (figure1[0] * figure1[1]) < (figure2[0] * figure2[1]):
            return -1
        # Si están empatados buscamos el más cuadrado
        elif abs(figure1[0] - figure1[1]) < abs(figure2[0] - figure2[1]):
            return 1
        elif abs(figure1[0] - figure1[1]) > abs(figure2[0] - figure2[1]):
            return -1
        # Si siguen empatados buscamos empezar por el que mas ocupe del total
        elif min(abs(self.cx - figure1[1]), abs(self.rx - figure1[0])) <= min(abs(self.cx - figure2[1]), abs(self.rx - figure2[0])):
            return 1
        else:
            return -1            

    def is_figure(self, x, y):
        for element in self.figures:
            if ((element[0] == x) & (element[1] == y)):
                return True
        return False

    def create_figures(self):
        minim = min(self.r, self.c, self.h)
        for i in range(1, minim + 1):
            for j in range(1, self.h + 1):
                if ((self.h % i == 0) & (i*j >= 2*self.l) & (i*j <= self.h)):
                    if not self.is_figure(i,j):
                        self.figures.append([i, j])
                    if not self.is_figure(j,i):
                        self.figures.append([j, i])
        self.figures.sort(self.figure_Cmp, reverse = True)

    def cut(self):
        print("Cutting pizza...")

    def cut_first_approach(self, x, y):
        """
        1.- Comprobar que no hemos llegado al final de la matriz
        2.- Comprobar que esa celda no esté cortada ya, es decir, no pertenezca a la solución.
        3.- Seleccionar figura a aplicar, mayor prioridad más grande.
        4.- Comprobar que la figura a aplicar cumple los mínimos de ingredientes
        5.- Añadir la porción a slice_list
        6.- Si en un caso no se puede aplicar ninguna figura pasamos a la siguiente celda hasta la última de la matriz.
        """
        for x in range(0, self.c):
            self.cx = self.c - x
            for y in range(0, self.r):
                # Hemos llegado al final de la matriz
                if (x >= (self.c - 1)) & (y >= (self.r - 1)):
                    print_result(self.slice_list)
                    #calculate_score(self.slice_list)
                else:
                    if not self.is_in_solution(x, y):
                        self.rx = self.r - y
                        self.figures.sort(self.figure_Cmp, reverse = True)
                        for figure in self.figures:
                            if self.can_cut_slice(x, y, figure):
                                # Add Figure to slice_list
                                self.add_slice_to_solution([[y, x], [y+figure[0]-1, x+figure[1]-1]])
                                self.slice_list.append([[y, x], [y+figure[0]-1, x+figure[1]-1]])
                                break

    def add_slice_to_solution(self, slice):
        for i in range(slice[0][0], slice[1][0] + 1):
            for j in range(slice[0][1], slice[1][1] + 1):
                self.px[i][j] = 1
        return

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
        for indexX in range(x, x + slice[1]):
            for indexY in range(y, y + slice[0]):
                if self.p[indexY][indexX] == 'T':
                    count_tomatoes = count_tomatoes + 1
                elif self.p[indexY][indexX] == 'M':
                    count_mushrooms = count_mushrooms + 1
                else:
                    print("Found a strange ingredient in the pizza: ", self.p[indexY][indexX])
        return count_tomatoes >= self.l & count_mushrooms >= self.l

    def all_cells_are_free(self, x, y, figure):
        # x + figure[0] & y + figure[1]
        # no estan en slice_list
        for indexX in range(x, x + figure[1]):
            for indexY in range(y, y + figure[0]):
                if self.is_in_solution(indexX, indexY):
                    return False
        return True

    def can_cut_slice(self, x, y, figure):
        if (((x + figure[1]) > self.c) | ((y + figure[0]) > self.r)):
            return False
        else:
            if not self.has_enough_ingredients(x, y, figure):
                return False
            elif not self.all_cells_are_free(x, y, figure):
                return False
            return True

    def is_in_solution(self, x, y):
        return self.px[y][x] == 1

def print_result(result):
    sys.stdout = open(outFileName, "w")
    print len(result)
    for slice_pizza in result:
        print slice_pizza[0][0],
        print slice_pizza[0][1],
        print slice_pizza[1][0],
        print slice_pizza[1][1]


def calculate_score(result):
    score = 0
    for slice_pizza in result:
        score = score + (((slice_pizza[1][0] - slice_pizza[0][0]) + 1) * ((slice_pizza[1][1] - slice_pizza[0][1]) + 1))
    print(score)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Cuts pizza.')
    parser.add_argument("-f", "--file", default='example.in', type=argparse.FileType('r'), help='Filename with input data')
    args = parser.parse_args()
    lines = args.file.readlines()
    pizza = Pizza(lines[0].split())
    for indexX, line in enumerate(lines[1:]):
        for indexY, ingredient in enumerate(line):
            if ingredient != '\n':
                pizza.p[indexX][indexY] = ingredient
    args.file.close()
    outFileName = args.file.name.split(".")[0] + ".out"
    pizza.create_figures()
    pizza.cut_first_approach(0, 0)
