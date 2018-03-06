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
        if ride1.early < ride2.early:
            return 1
        if (ride1.start[0] + ride1.start[1]) < (ride2.start[0] + ride2.start[1]):
            return 1
        elif ride1.latest < ride2.latest:
            return 1
        elif (ride1.latest - ride1.early) < (ride2.latest - ride2.early):
            return 1
        else:
            return -1

    def calculate_route(self):
        self.Rides.sort(self.Ride_Cmp, reverse=True)
        steps = 0
        while (steps < self.t):
            """
            1. Asigno rutas a coches
            2. Avanzo para completar todas las rutas
            3. Vuelvo a empezar hasta que complete el máximo número de steps
            """
            for index in range(0, min(self.f, len(self.Rides))):
                self.Vehicles[index].cride.append(self.Rides[0])
                self.Vehicles[index].n = self.Vehicles[index].n + 1
                self.Rides.remove(self.Rides[0])
            mn = self.b
            for nv in range(0, self.f):
                it = self.Vehicles[nv].n - 1
                tmp = abs(self.Vehicles[nv].location[0] - self.Vehicles[nv].cride[it].end[0]) + abs(self.Vehicles[nv].location[1] - self.Vehicles[nv].cride[it].end[1])
                if (tmp < mn):
                    mn = tmp
            steps = steps + mn
        return self.Vehicles

def print_result(result, o):
    for v in result:
        o.write(str(v.n))
        for r in v.cride:
            o.write(" ")
            o.write(str(r.number))
        o.write('\n')
    o.close()

def calculate_score(result):
    print(result)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculating routes.')
    parser.add_argument("-f", "--file", default='c:\\Users\\jagariburo\\Documents\\Google Hash Code 2018\\HashCode2018_Pastutatis\\Selfdriving cars\\a_example.in', type=argparse.FileType('r'), help='Filename with input data')
    #parser.add_argument("-f", "--file", default='c:\\Users\\jagariburo\\Documents\\Google Hash Code 2018\\HashCode2018_Pastutatis\\Selfdriving cars\\b_should_be_easy.in', type=argparse.FileType('r'), help='Filename with input data')
    #parser.add_argument("-f", "--file", default='c:\\Users\\jagariburo\\Documents\\Google Hash Code 2018\\HashCode2018_Pastutatis\\Selfdriving cars\\c_no_hurry.in', type=argparse.FileType('r'), help='Filename with input data')
    #parser.add_argument("-f", "--file", default='c:\\Users\\jagariburo\\Documents\\Google Hash Code 2018\\HashCode2018_Pastutatis\\Selfdriving cars\\d_metropolis.in', type=argparse.FileType('r'), help='Filename with input data')
    #parser.add_argument("-f", "--file", default='c:\\Users\\jagariburo\\Documents\\Google Hash Code 2018\\HashCode2018_Pastutatis\\Selfdriving cars\\e_high_bonus.in', type=argparse.FileType('r'), help='Filename with input data')
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
