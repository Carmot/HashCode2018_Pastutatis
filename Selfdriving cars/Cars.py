#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import argparse
#import sys
#import matplotlib.pyplot as plt

class Vehicle:
    def __init__(self):
        self.location = [0, 0]
        self.n = 0
        self.rides = []

class Ride:
    def __init__(self, values, n):
        self.start = [int(values[0]), int(values[1])]
        self.end = [int(values[2]), int(values[3])]
        self.early = int(values[4])
        self.latest = int(values[5])
        self.number = n
        self.distance = abs(self.end[0]-self.start[0]) + \
            abs(self.end[1]-self.start[1])
        self.points = 0

class Problem:
    def __init__(self, values):
        self.r = int(values[0])
        self.c = int(values[1])
        self.f = int(values[2])
        self.Vehicles = []
        """
        Creamos todos los vehículos al comienzo [0, 0]
        """
        for dummyI in range(0, self.f):
            self.Vehicles.append(Vehicle())
        self.n = int(values[3])
        self.b = int(values[4])
        self.t = int(values[5])
        self.Rides = []

    def __str__(self):
        print("Rows: ", self.r)
        print("Columns: ", self.c)
        print("#Vehicles: ", self.f)
        print("#Rides: ", self.n)
        print("Bonus: ", self.b)
        print("Steps: ", self.t)

    def ridePoints(self):
        bonus = False
        points = 0
        for r in self.Rides: 
            if (r.start[0] + r.start[1]) <= r.early:
                bonus = True
            points = abs(r.start[0] - r.end[0]) + abs(r.start[1] - r.end[1])
            if bonus:
                points = points + self.b
                bonus = False
            r.points = points

    def Ride_CmpInit(self, ride1, ride2):
        """
        Usada solo la primera vez que todos los coches parten del mismo punto
        """ 
        if ride1.points > ride2.points:
            return 1
        elif ride1.points == ride2.points and ride1.latest < ride2.latest:
            return 1
        else:
            return -1

    def Ride_Cmp(self, ride1, ride2):
        mts1 = self.t
        mts2 = self.t
        m1 = 0
        m2 = 0
        h1 = self.t
        h2 = self.t
        for v in self.Vehicles:
            movetostart1 = abs(ride1.start[0] - v.location[0]) + abs(ride1.start[1] - v.location[1])
            movetostart2 = abs(ride2.start[0] - v.location[0]) + abs(ride2.start[1] - v.location[1])
            if movetostart1 < mts1:
                mts1 = movetostart1
            if movetostart2 < mts2:
                mts2 = movetostart2
            move1 = abs(ride1.start[0] - ride1.end[0]) + abs(ride1.start[1] - ride1.end[1])
            move2 = abs(ride2.start[0] - ride2.end[0]) + abs(ride2.start[1] - ride2.end[1])
            if move1 > m1:
                m1 = move1
            if move2 > m2:
                m2 = move2
            hurry1 = ride1.latest
            hurry2 = ride2.latest
            if hurry1 < h1:
                h1 = hurry1
            if hurry2 < h2:
                h2 = hurry2
        if (mts1 <= mts2 and m1 >= m2 and h1 <= h2) or (mts1 > mts2 and m1 >= m2 and h1 <= h2) or (mts1 <= mts2 and m1 < m2 and h1 <= h2) or (mts1 <= mts2 and m1 >= m2 and h1 > h2):
            return 1
        else:
            return -1

    def calculate_route(self):
        self.Rides.sort(self.Ride_CmpInit, reverse=True)
        steps = self.iterate()
        """
        Tenemos los viajes con mayor puntuacion asignados
        Iteramos hasta llegar al numero de steps o no tener mas viajes.
        """
        while ((steps < self.t) and (len(self.Rides) > 0)):
            self.Rides.sort(self.Ride_Cmp, reverse=True)
            steps = steps + self.iterate()
        return self.Vehicles

    def iterate(self):
        # Total steps, me voy a quedar con el menor
        mn = self.t
        for index in range(0, min(self.f, len(self.Rides))):
            """
            Tenemos los viajes ordenador de mayor a menor puntuacion
            por lo tanto añadimos el primero al coche.
            """
            self.Vehicles[index].rides.append(self.Rides[0])
            self.Vehicles[index].n = self.Vehicles[index].n + 1
            """
            Calculamos las steps consumidas para ese viaje por este coche
            """
            steps = self.calculate_steps(index)
            if steps < mn:
                mn = steps
            """
            Movemos el coche
            """
            self.move_car(index)
            """
            Borramos el viaje puesto que ya lo hemos asignado
            """
            self.Rides.remove(self.Rides[0])
        """
        Devuelvo las menores steps consumidas por un viaje
        """            
        return mn

    def calculate_steps(self, i):
        # Nos movemos al comienzo del viaje
        tmp = abs(self.Vehicles[i].location[0] - self.Rides[0].start[0]) + abs(self.Vehicles[i].location[1] - self.Rides[0].start[1])
        # Nos movemos al final del recorrido de este viaje
        tmp = tmp + self.Rides[0].distance
        return tmp

    def move_car(self, vIndex):
        # Moverse el coche hasta el punto de salida y hacer el recorrido
        self.Vehicles[vIndex].location[0] = self.Rides[0].end[0]
        self.Vehicles[vIndex].location[1] = self.Rides[0].end[1]

def print_result(vehiculesResult, o):
    for v in vehiculesResult:
        o.write(str(v.n))
        for r in v.rides:
            o.write(" ")
            o.write(str(r.number))
        o.write('\n')
    o.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Spreading vehicles fleet arounde the city.')
    parser.add_argument("-f", "--file", default='c:\\Users\\jagariburo\\Documents\\Google Hash Code 2018\\HashCode2018_Pastutatis\\Selfdriving cars\\a_example.in',
                        type=argparse.FileType('r'), help='Filename with input data.')
    """
    parser.add_argument("-f", "--file", default='c:\\Users\\jagariburo\\Documents\\Google Hash Code 2018\\HashCode2018_Pastutatis\\Selfdriving cars\\b_should_be_easy.in',
                        type=argparse.FileType('r'), help='Filename with input data.')
    parser.add_argument("-f", "--file", default='c:\\Users\\jagariburo\\Documents\\Google Hash Code 2018\\HashCode2018_Pastutatis\\Selfdriving cars\\c_no_hurry.in',
                        type=argparse.FileType('r'), help='Filename with input data.')
    parser.add_argument("-f", "--file", default='c:\\Users\\jagariburo\\Documents\\Google Hash Code 2018\\HashCode2018_Pastutatis\\Selfdriving cars\\d_metropolis.in',
                        type=argparse.FileType('r'), help='Filename with input data.')
    parser.add_argument("-f", "--file", default='c:\\Users\\jagariburo\\Documents\\Google Hash Code 2018\\HashCode2018_Pastutatis\\Selfdriving cars\\e_high_bonus.in',
                        type=argparse.FileType('r'), help='Filename with input data.')
    """
    args = parser.parse_args()
    outFile = open(args.file.name.split(".")[0] + ".out", "w")
    lines = args.file.readlines()
    args.file.close()
    problems = Problem(lines[0].split())
    rideCounter = 0
    for line in lines[1:]:
        problems.Rides.append(Ride(line.split(), rideCounter))
        rideCounter = rideCounter + 1
    problems.ridePoints()
    result = problems.calculate_route()
    print_result(result, outFile)
