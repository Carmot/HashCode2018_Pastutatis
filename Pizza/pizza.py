class Pizza:
    def __init__(self, values):
        self.r = values[0]
        self.c = values[1]
        self.l = values[2]
        self.h = values[3]
        self.p = []

    def __str__(self):
        print("Rows: ", self.r)
        print("Columns: ", self.c)
        print("Min ingredients: ", self.l)
        print("Max cells/slice: ", self.h)
        print("Matrix: ", self.p.__str__())

    def cut(self):
        print("Cutting pizza...")
        for line in self.p:
            print(line)


if __name__ == '__main__':
    file = open("input/example.in", "r")
    lines = file.readlines()
    pizza = Pizza(lines[0].split())
    for line in lines[1:]:
        pizza.p.append(line.replace('\n', ''))
    pizza.cut()
