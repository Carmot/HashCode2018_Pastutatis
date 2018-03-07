#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

#import sys
import argparse

#import matplotlib.pyplot as plt


class Vehicle:
    def __init__(self):
        self.location = [0, 0]
        self.n = 0
        self.cride = []


class Ride:
    def __init__(self, values, n):
        self.start = [int(values[0]), int(values[1])]
        self.end = [int(values[2]), int(values[3])]
        self.early = int(values[4])
        self.latest = int(values[5])
        self.number = n
        self.distance = abs(self.end[0]-self.start[0]) + \
            abs(self.end[1]-self.start[1])


class Problem:
    def __init__(self, values):
        self.Vehicles = []
        self.r = int(values[0])
        self.c = int(values[1])
        self.f = int(values[2])
        for dummyI in range(0, self.f):
            self.Vehicles.append(Vehicle())
        self.n = int(values[3])
        self.b = int(values[4])
        self.t = int(values[5])
        self.Rides = []
        self.mVehicles = []
        self.bonus = self.b > ((self.r * self.c) / 2)

    """
    def __str__(self):
        print("Rows: ", self.r)
        print("Columns: ", self.c)
        print("#Vehicles: ", self.f)
        print("#Rides: ", self.n)
        print("Bonus: ", self.b)
        print("Steps: ", self.t)
    """

    def isBonus(self):
        storage = abs(self.Rides[0].end[0] - self.Rides[0].start[0]) + \
            abs(self.Rides[0].end[1] - self.Rides[0].start[1])
        for r in range(1, len(self.Rides)):
            storage = (storage + abs(self.Rides[r].end[0] - self.Rides[r].start[0]) + abs(
                self.Rides[r].end[1] - self.Rides[r].start[1])) / 2
        self.bonus = self.b > storage

    def Ride_Cmp(self, ride1, ride2):
        # Ordena la primera vez en la que los coches estan en [0, 0]
        if self.bonus:
            # Ordeno el que tiene un margen menor de empezar en tiempo primero para asignarlo lo antes posible a un coche y ganar bonus.
            if ((ride1.early - (ride1.start[0] + ride1.start[1])) > 0) and ((ride1.early - (ride1.start[0] + ride1.start[1])) > (ride2.early - (ride2.start[0] + ride2.start[1]))) and (ride1.early <= ride2.early):
                return 1
            else:
                return -1
        else:
            # Los mas cercanos y mas largos
            if (ride1.start[0] + ride1.start[1]) < (ride2.start[0] + ride2.start[1]) and (ride1.distance > ride2.distance):
                return 1
            elif ride1.latest < ride2.latest:
                return 1
            else:
                return -1

    def Ride_Cmp_Orig(self, ride1, ride2):
        if self.bonus:
            if (ride1.early + ride1.distance) < (ride2.early + ride2.distance):
                return 1
            else:
                return -1
        else:
            if (abs(self.mVehicles[0].location[0] - ride1.start[0]) + abs(self.mVehicles[0].location[1] - ride1.start[1])) < (abs(self.mVehicles[0].location[0] - ride2.start[0]) + abs(self.mVehicles[0].location[1] - ride2.start[1])) and (ride1.distance > ride2.distance):
                return 1
            elif ride1.latest < ride2.latest:
                return 1
            else:
                return -1

    def calculate_route(self):
        self.Rides.sort(self.Ride_Cmp, reverse=True)
        steps = self.first_iteration()
        while ((steps < self.t) and (len(self.Rides) > 0)):
            """
            1. Asigno rutas a coches
            2. Avanzo para completar todas las rutas
            3. Vuelvo a empezar hasta que complete el máximo número de steps
            """
            for v in self.Vehicles:
                self.mVehicles.append(v)
            for index in range(0, min(self.f, len(self.Rides))):
                self.Rides.sort(self.Ride_Cmp_Orig, reverse=True)
                self.Vehicles[index].cride.append(self.Rides[0])
                self.Vehicles[index].n = self.Vehicles[index].n + 1
                self.move_car(index)
                self.Rides.remove(self.Rides[0])
                self.mVehicles.remove(self.mVehicles[0])
            mn = self.t
            if len(self.Rides) > 0:
                for nv in range(0, self.f):
                    tmp = self.Vehicles[nv].location[0] + self.Vehicles[nv].location[1]
                    if (tmp < mn):
                        mn = tmp
                steps = steps + mn
        return self.Vehicles

    def first_iteration(self):
        for index in range(0, min(self.f, len(self.Rides))):
            self.Vehicles[index].cride.append(self.Rides[0])
            self.Vehicles[index].n = self.Vehicles[index].n + 1
            self.move_car(index)
            self.Rides.remove(self.Rides[0])
        mn = self.t
        for nv in range(0, self.f):
            tmp = self.Vehicles[nv].location[0] + self.Vehicles[nv].location[1]
            if (tmp < mn):
                mn = tmp
        return mn

    def move_car(self, vIndex):
        self.Vehicles[vIndex].location[0] = self.Rides[0].end[0]
        self.Vehicles[vIndex].location[1] = self.Rides[0].end[1]

def print_result(vehiculesResult, o):
    for v in vehiculesResult:
        o.write(str(v.n))
        for r in v.cride:
            o.write(" ")
            o.write(str(r.number))
        o.write('\n')
    o.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculating routes.')
    """
    parser.add_argument("-f", "--file", default='c:\\Users\\jagariburo\\Documents\\Google Hash Code 2018\\HashCode2018_Pastutatis\\Selfdriving cars\\a_example.in',
                        type=argparse.FileType('r'), help='Filename with input data')
    """
    parser.add_argument("-f", "--file", default='c:\\Users\\jagariburo\\Documents\\Google Hash Code 2018\\HashCode2018_Pastutatis\\Selfdriving cars\\b_should_be_easy.in',
                        type=argparse.FileType('r'), help='Filename with input data')
    """
    parser.add_argument("-f", "--file", default='c:\\Users\\jagariburo\\Documents\\Google Hash Code 2018\\HashCode2018_Pastutatis\\Selfdriving cars\\c_no_hurry.in',
                        type=argparse.FileType('r'), help='Filename with input data')
    parser.add_argument("-f", "--file", default='c:\\Users\\jagariburo\\Documents\\Google Hash Code 2018\\HashCode2018_Pastutatis\\Selfdriving cars\\d_metropolis.in',
                        type=argparse.FileType('r'), help='Filename with input data')
    parser.add_argument("-f", "--file", default='c:\\Users\\jagariburo\\Documents\\Google Hash Code 2018\\HashCode2018_Pastutatis\\Selfdriving cars\\e_high_bonus.in',
                        type=argparse.FileType('r'), help='Filename with input data')
    """
    args = parser.parse_args()
    outFile = open(args.file.name.split(".")[0] + ".out", "w")
    lines = args.file.readlines()
    problems = Problem(lines[0].split())
    rideCounter = 0
    for line in lines[1:]:
        problems.Rides.append(Ride(line.split(), rideCounter))
        rideCounter = rideCounter + 1
    args.file.close()
    problems.isBonus()
    result = problems.calculate_route()
    print_result(result, outFile)
