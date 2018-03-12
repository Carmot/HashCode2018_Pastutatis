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
        self.distance = 0

class Ride:
    def __init__(self, values, n):
        self.start = [int(values[0]), int(values[1])]
        self.end = [int(values[2]), int(values[3])]
        self.early = int(values[4])
        self.latest = int(values[5])
        self.number = n
        self.distance = abs(self.end[0]-self.start[0]) + \
            abs(self.end[1]-self.start[1])
        self.points = 0.0

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
        self.averageX = 0.0
        self.averageY = 0.0

    def __str__(self):
        print("Rows: ", self.r)
        print("Columns: ", self.c)
        print("#Vehicles: ", self.f)
        print("#Rides: ", self.n)
        print("Bonus: ", self.b)
        print("Steps: ", self.t)

    def ridePointsInit(self):
        bonus = False
        for r in self.Rides: 
            if (r.start[0] + r.start[1]) <= r.early:
                bonus = True
            r.points = 1.0 / (r.early - (r.start[0] + r.start[1]))
            r.points = r.points + (1.0 / (abs(r.end[0] - self.averageX) + abs(r.end[1] - self.averageY)))
            if bonus:
                r.points = r.points + self.b
                bonus = False
    
    def averagePoint(self):
        self.averageX = self.Rides[0].start[0]
        self.averageY = self.Rides[0].start[1]
        for index in range(1, len(self.Rides)):
            self.averageX = (self.averageX + self.Rides[index].start[0]) / 2.0
            self.averageY = (self.averageY + self.Rides[index].start[1]) / 2.0
    
    def ridePoints(self, carIndex):
        """
        Calculamos el mejor viaje para cada coche una vez que se han movido
        """
        bonus = False
        previousPoints = -999999.99
        rideIndex = 0
        returnIndex = 0
        for r in self.Rides: 
            if (abs(self.Vehicles[carIndex].location[0] - r.start[0]) + abs(self.Vehicles[carIndex].location[1] - r.start[1]) + self.Vehicles[carIndex].distance) <= r.early:
                bonus = True
            if (abs(self.Vehicles[carIndex].location[0] - r.start[0]) + abs(self.Vehicles[carIndex].location[1] - r.start[1]) + self.Vehicles[carIndex].distance + abs(r.start[0] - r.end[0]) + abs(r.start[1] - r.end[1])) <= r.latest:
                if (r.early - ((abs(self.Vehicles[carIndex].location[0] - r.start[0])) + (abs(self.Vehicles[carIndex].location[1] - r.start[1])))) == 0.0:
                    r.points = (self.b / 2.0) + (1.0 / (abs(r.end[0] - self.averageX) + abs(r.end[1] - self.averageY)))
                else:
                    r.points = 1.0 / (r.early - ((abs(self.Vehicles[carIndex].location[0] - r.start[0])) + (abs(self.Vehicles[carIndex].location[1] - r.start[1]))))
                    r.points = r.points + (1.0 / (abs(r.end[0] - self.averageX) + abs(r.end[1] - self.averageY)))
                #abs(r.start[0] - r.end[0]) + abs(r.start[1] - r.end[1]) - (abs(self.Vehicles[carIndex].location[0] - r.start[0]) + abs(self.Vehicles[carIndex].location[1] - r.start[1]))
            if bonus:
                r.points = r.points + self.b
                bonus = False
            if r.points > previousPoints:
                previousPoints = r.points
                returnIndex = rideIndex
            rideIndex = rideIndex + 1
        return returnIndex

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

    def calculate_route(self):
        self.Rides.sort(self.Ride_CmpInit, reverse=True)
        steps = self.iterate(True)
        """
        Tenemos los viajes con mayor puntuacion asignados
        Iteramos hasta llegar al numero de steps o no tener mas viajes.
        """
        while ((steps < self.t) and (len(self.Rides) > 0)):
            self.Rides.sort(self.Ride_CmpInit, reverse=True)
            steps = steps + self.iterate(False)
        return self.Vehicles

    def iterate(self, initial):
        # Total steps, me voy a quedar con el menor
        mn = self.t
        for index in range(0, min(self.f, len(self.Rides))):
            """
            Tenemos los viajes ordenador de mayor a menor puntuacion
            por lo tanto añadimos el primero al coche.
            """
            if initial:
                rI = 0
            else:
                rI = self.ridePoints(index)
            self.Vehicles[index].rides.append(self.Rides[rI])
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
            self.Rides.remove(self.Rides[rI])
        """
        Devuelvo las menores steps consumidas por un viaje
        """            
        return mn

    def calculate_steps(self, i):
        # Nos movemos al comienzo del viaje
        tmp = abs(self.Vehicles[i].location[0] - self.Rides[0].start[0]) + abs(self.Vehicles[i].location[1] - self.Rides[0].start[1])
        # Nos movemos al final del recorrido de este viaje
        tmp = tmp + self.Rides[0].distance
        self.Vehicles[i].distance = tmp
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
    """
    parser.add_argument("-f", "--file", default='C:\\git\\HashCode2018_Pastutatis\\Selfdriving cars\\a_example.in',
                        type=argparse.FileType('r'), help='Filename with input data.')
    """
    parser.add_argument("-f", "--file", default='C:\\Users\\jagariburo\\Documents\\Google Hash Code 2018\\HashCode2018_Pastutatis\\Selfdriving cars\\b_should_be_easy.in',
                        type=argparse.FileType('r'), help='Filename with input data.')
    """
    parser.add_argument("-f", "--file", default='C:\\git\\HashCode2018_Pastutatis\\Selfdriving cars\\c_no_hurry.in',
                        type=argparse.FileType('r'), help='Filename with input data.')
    parser.add_argument("-f", "--file", default='C:\\git\\HashCode2018_Pastutatis\\Selfdriving cars\\d_metropolis.in',
                        type=argparse.FileType('r'), help='Filename with input data.')
    parser.add_argument("-f", "--file", default='C:\\git\\HashCode2018_Pastutatis\\Selfdriving cars\\e_high_bonus.in',
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
    problems.ridePointsInit()
    problems.averagePoint()
    result = problems.calculate_route()
    print_result(result, outFile)
