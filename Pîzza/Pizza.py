import argparse

parser = argparse.ArgumentParser(description='Cuts pizza.')
parser.add_argument("-f", "--file", default='example.in', type=argparse.FileType('r'), help='Filename with input data')
args = parser.parse_args()

parameters = args.file.readline().split(" ")
rows = int(parameters[0])
columns = int(parameters[1])
min = int(parameters[2])
max = int(parameters[3])

iPizza = 0
Pizza = rows*[columns*[0]]

for line in args.file.readlines():
    Pizza[iPizza] = line
    iPizza = iPizza + 1

# We have in Pizza matrix from 0 to columns-1
# In columns we have '\n' character from reading the file
args.file.close()

# Open output file for writing
outFileName = args.file.name.split(".")[0] + ".out"
outFile = open(outFileName, 'w')

getSlice(Pizza)

outFile.write()


totalSlices = 0
# Each slice [rowStart, rowEnd] [columnStart, columnEnd]


def getSlice(pizza):   
    r,c = 0
    counter, tC, mC = 0

    while r < rows:
        while c < columns:
            if Pizza[r][c] = 'M':
                mC = mC + 1
            else:
                tC = tC + 1
            counter = counter + 1
            c = c + 1
        c = 0
        r = r + 1