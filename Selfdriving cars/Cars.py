#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import sys
import argparse

#import matplotlib.pyplot as plt

class Vehicle:
    def __init__(self):
        self.location = [0, 0]
        self.n = 0
        self.nrides = []
        self.cride = []

class Ride:
    def __init__(self, values, n):
        self.start = [int(values[0]), int(values[1])]
        self.end = [int(values[2]), int(values[3])]
        self.early = int(values[4])
        self.latest = int(values[5])
        self.number = n

class Problem:
    def __init__(self, values):
        self.Vehicles = []
        self.r = int(values[0])
        self.rx = self.r
        self.c = int(values[1])
        self.cx = self.c
        self.f = int(values[2])
        for nv in range(0, self.f):
            self.Vehicles.append(Vehicle())
        self.n = int(values[3])
        self.b = int(values[4])
        self.t = int(values[5])
        self.Rides = []

    def __str__(self):
        print("Rows: ", self.r)
        print("Columns: ", self.c)
        print("Vehicles: ", self.f)
        print("Rides: ", self.n)
        print("Bonus: ", self.b)
        print("Steps: ", self.t)

    def Ride_Cmp(self, ride1, ride2):
        # El cacho más grande primero
        if (ride1[0] * ride1[1]) > (ride2[0] * ride2[1]):
            return 1
        elif (ride1[0] * ride1[1]) < (ride2[0] * ride2[1]):
            return -1
        # Si están empatados buscamos el más cuadrado
        elif abs(ride1[0] - ride1[1]) < abs(ride2[0] - ride2[1]):
            return 1
        elif abs(ride1[0] - ride1[1]) > abs(ride2[0] - ride2[1]):
            return -1
        # Si siguen empatados buscamos empezar por el que mas ocupe del total
        elif min(abs(self.cx - ride1[1]), abs(self.rx - ride1[0])) <= min(abs(self.cx - ride2[1]), abs(self.rx - ride2[0])):
            return 1
        else:
            return -1

    def calculate_route(self):
        #self.Rides.sort(self.Ride_Cmp, reverse=True)
        steps = 0
        while (steps < self.b):
            """
            1. Asigno rutas a coches
            2. Avanzo para completar todas las rutas
            3. Vuelvo a empezar hasta que complete el máximo número de steps
            """
            for index in range(0, min(self.f, self.n)):
                self.Vehicles[index].cride.append(self.Rides[index])
                self.Vehicles[index].n = self.Vehicles[index].n + 1
                self.Rides.pop()
            max = 0
            for nv in range(0, self.f):
                it = self.Vehicles[nv].n - 1
                tmp = abs(self.Vehicles[nv].location[0] - self.Vehicles[nv].cride[it].end[0]) + abs(self.Vehicles[nv].location[1] - self.Vehicles[nv].cride[it].end[1])
                if (tmp > max):
                    max = tmp
            steps = steps + max
        return self.Vehicles

def print_result(result, o):
    tmp = ''
    for v in result:
        tmp = tmp + str(v.n)
        for r in v.cride:
            tmp = tmp + " "
            tmp = tmp + str(r.number),
        o.write(tmp[0])
        o.write('\n')
        tmp = ''
    o.close()

def calculate_score(result):
    print(result)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculating routes.')
    #parser.add_argument("-f", "--file", default='c:\\Users\\jagariburo\\Documents\\Google Hash Code 2018\\HashCode2018_Pastutatis\\Selfdriving cars\\a_example.in', type=argparse.FileType('r'), help='Filename with input data')
    #parser.add_argument("-f", "--file", default='c:\\Users\\jagariburo\\Documents\\Google Hash Code 2018\\HashCode2018_Pastutatis\\Selfdriving cars\\b_should_be_easy.in', type=argparse.FileType('r'), help='Filename with input data')
    #parser.add_argument("-f", "--file", default='c:\\Users\\jagariburo\\Documents\\Google Hash Code 2018\\HashCode2018_Pastutatis\\Selfdriving cars\\c_no_hurry.in', type=argparse.FileType('r'), help='Filename with input data')
    #parser.add_argument("-f", "--file", default='c:\\Users\\jagariburo\\Documents\\Google Hash Code 2018\\HashCode2018_Pastutatis\\Selfdriving cars\\d_metropolis.in', type=argparse.FileType('r'), help='Filename with input data')
    parser.add_argument("-f", "--file", default='c:\\Users\\jagariburo\\Documents\\Google Hash Code 2018\\HashCode2018_Pastutatis\\Selfdriving cars\\e_high_bonus.in', type=argparse.FileType('r'), help='Filename with input data')
    args = parser.parse_args()
    outFile = open(args.file.name.split(".")[0] + ".out", "w")
    lines = args.file.readlines()
    problems = Problem(lines[0].split())
    rideCounter = 0
    for line in lines[1:]:
        problems.Rides.append(Ride(line.split(), rideCounter))
        rideCounter = rideCounter + 1
    args.file.close()
    result = problems.calculate_route()
    print_result(result, outFile)
