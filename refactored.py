import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import enum
import random

soilInfiltraionMap = {
    'default': {
        'f0': 0.01,
        'fc': 0.02,
        'k': 0.03
    },

    'waterarea': {
        'f0': 0,
        'f1': 0,
        'k': 0
    },

    'settlement': {
        'f0': 4.06,
        'fc': 0.03,
        'k': 0.45
    },

    'rocks': {
        'f0': 0.03,
        'fc': 0.002,
        'k': 0.02
    }
}


class SoilType(enum.Enum):
    Default = 'default'
    Water = 'waterarea'
    Soil = 'settlement'
    Rock = 'rocks'


class Cell:
    def __init__(self, i, j, soil_level, water_level, soil_type):
        self.i = i
        self.j = j
        self.soil_level = soil_level
        self.water_level = water_level
        self.soilType = soil_type

    def getWaterLevel(self):
        return self.water_level

    def getSoilLevel(self):
        return self.soil_level

    def getSoilType(soilType):
        return soilType

    def setWaterLevel(self, water_level):
        if water_level > 0:
            self.water_level = water_level
        else:
            water_level = 0

    def setSoilLevel(self, soil_level):
        self.soil_level = int(soil_level)


def get_random_cell_grid(N):
    grid = []
    for i in range(N):
        row = []
        for j in range(N):
            row.append(Cell(i, j, random.randint(1000, 2000), random.randint(1000, 2000), 'default'))
        grid.append(row)

    grid2 = [[Cell(i, j, 10, 0, 'default'),Cell(i, j, 10, 0, 'default'),Cell(i, j, 10, 0, 'default'),Cell(i, j, 10, 0, 'default'),Cell(i, j, 10, 0, 'default')],
    [Cell(i, j, 10, 0, 'default'),Cell(i, j, 10, 0, 'default'),Cell(i, j, 10, 0, 'default'),Cell(i, j, 10, 0, 'default'),Cell(i, j, 10, 0, 'default')],
    [Cell(i, j, 10, 0, 'default'),Cell(i, j, 10, 0, 'default'),Cell(i, j, 10, 5000, 'default'),Cell(i, j, 10, 0, 'default'),Cell(i, j, 10, 0, 'default')],
    [Cell(i, j, 10, 0, 'default'),Cell(i, j, 10, 0, 'default'),Cell(i, j, 10, 0, 'default'),Cell(i, j, 10, 0, 'default'),Cell(i, j, 10, 0, 'default')],
    [Cell(i, j, 10, 0, 'default'),Cell(i, j, 10, 0, 'default'),Cell(i, j, 10, 0, 'default'),Cell(i, j, 10, 0, 'default'),Cell(i, j, 10, 0, 'default')]]


    return grid


def get_show_grid(grid_cell):
    grid_show = []

    for i in grid_cell:
        row = []
        for j in i:
            row.append(int(j.water_level))
        grid_show.append(row)

    return grid_show


# get cells which has water
def GetWaterCells(grid):
    arr = []
    n = len(grid)
    for i in range(1, n - 1):
        for j in range(1, n - 1):
            if grid[i][j].water_level > 0:
                arr.append(grid[i][j])
    return arr


def SortWaterCellArray(array):
    return sorted(array, key=lambda i: i.water_level)


def GetAverageHeight(cell, grid):
    left = grid[cell.i][cell.j + 1].water_level + grid[cell.i][cell.j + 1].soil_level
    top = grid[cell.i + 1][cell.j].water_level + grid[cell.i + 1][cell.j].soil_level
    right = grid[cell.i][cell.j + 1].water_level + grid[cell.i][cell.j + 1].soil_level
    bottom = grid[cell.i - 1][cell.j].water_level + grid[cell.i - 1][cell.j].soil_level
    center = cell.soil_level + cell.water_level

    return (left + top + right + bottom + center) / 5


def GetFlowWaterAmount(centerCellHeight, numberOfNeighbours):
    return centerCellHeight / (numberOfNeighbours + 1)


def OverFlowWaterToNeighbour(grid, cell, waterFlowAmount):
    # left
    if (grid[cell.i][cell.j - 1].water_level + grid[cell.i][
        cell.j - 1].soil_level + waterFlowAmount <= cell.water_level + cell.soil_level):
        grid[cell.i][cell.j - 1].setWaterLevel(grid[cell.i][cell.j - 1].water_level + waterFlowAmount)
        ###print("left", grid[cell.i][cell.j - 1].water_level)
    else:

        grid[cell.i][cell.j - 1].setWaterLevel(grid[cell.i][cell.j - 1].water_level + (cell.water_level + cell.soil_level) - (
                grid[cell.i][cell.j - 1].water_level + grid[cell.i][cell.j - 1].soil_level))

        grid[cell.i][cell.j].setWaterLevel(grid[cell.i][cell.j].water_level + (waterFlowAmount - ((cell.water_level + cell.soil_level) - (
                grid[cell.i][cell.j - 1].water_level + grid[cell.i][cell.j - 1].soil_level))))

        ###print("left else", grid[cell.i][cell.j - 1].water_level)

    # top
    if (grid[cell.i - 1][cell.j].water_level + grid[cell.i - 1][
        cell.j].soil_level + waterFlowAmount <= cell.water_level + cell.soil_level):

        grid[cell.i - 1][cell.j].setWaterLevel(grid[cell.i - 1][cell.j].water_level + waterFlowAmount)

        ###print("top", grid[cell.i - 1][cell.j].water_level)
    else:

        grid[cell.i - 1][cell.j].setWaterLevel(grid[cell.i - 1][cell.j].water_level + (cell.water_level + cell.soil_level) - (
                grid[cell.i - 1][cell.j].water_level + grid[cell.i - 1][cell.j].soil_level))

        grid[cell.i][cell.j].setWaterLevel(grid[cell.i][cell.j].water_level + (waterFlowAmount - ((cell.water_level + cell.soil_level) - (
                grid[cell.i - 1][cell.j].water_level + grid[cell.i - 1][cell.j].soil_level))))

    # right
    if (grid[cell.i][cell.j + 1].water_level + grid[cell.i][
        cell.j + 1].soil_level + waterFlowAmount <= cell.water_level + cell.soil_level):

        grid[cell.i][cell.j + 1].setWaterLevel(grid[cell.i][cell.j + 1].water_level + waterFlowAmount)

        ###print("right", grid[cell.i][cell.j + 1].water_level)
    else:

        grid[cell.i][cell.j + 1].setWaterLevel(grid[cell.i][cell.j + 1].water_level + (cell.water_level + cell.soil_level) - (
                grid[cell.i][cell.j + 1].water_level + grid[cell.i][cell.j + 1].soil_level))

        grid[cell.i][cell.j].setWaterLevel(grid[cell.i][cell.j].water_level + (waterFlowAmount - ((cell.water_level + cell.soil_level) - (
                grid[cell.i][cell.j + 1].water_level + grid[cell.i][cell.j + 1].soil_level))))

        ###print("right else", grid[cell.i][cell.j + 1].water_level)
    # bottom
    if (grid[cell.i + 1][cell.j].water_level + grid[cell.i + 1][
        cell.j].soil_level + waterFlowAmount <= cell.water_level + cell.soil_level):

        grid[cell.i + 1][cell.j].setWaterLevel(grid[cell.i + 1][cell.j].water_level + waterFlowAmount)

        ###print("bottom", grid[cell.i + 1][cell.j].water_level)
    else:

        grid[cell.i + 1][cell.j].setWaterLevel(grid[cell.i + 1][cell.j].water_level + (cell.water_level + cell.soil_level) - (
                grid[cell.i + 1][cell.j].water_level + grid[cell.i + 1][cell.j].soil_level))

        grid[cell.i][cell.j].setWaterLevel(grid[cell.i][cell.j].water_level + (waterFlowAmount - ((cell.water_level + cell.soil_level) - (
                grid[cell.i + 1][cell.j].water_level + grid[cell.i + 1][cell.j].soil_level))))

        ###print("botom else", grid[cell.i + 1][cell.j].water_level)

    return grid


def ReduceWaterInfiltration(grid, soilInfiltraionMap, time):
    for i in grid:
        for j in i:
            p = soilInfiltraionMap[j.soilType]['fc']
            q = soilInfiltraionMap[j.soilType]['f0']
            k = soilInfiltraionMap[j.soilType]['k']
            ft = p + ((p - q) * 2.78) ** ((-1) * k) * time

            ql = ft * time

            if (j.water_level - ql >= 0):
                j.water_level = j.water_level - ql
            else:
                j.water_level = 0

    return grid


def update(frameNum, img, grid_cell, N):
    # get cells which has water
    waterCells = GetWaterCells(grid_cell)
    ###print(waterCells)

    # Get sorted cells acording to water level
    sortedWaterCell = SortWaterCellArray(waterCells)[::-1]
    ###print(sortedWaterCell)

    # iterate over all water cells
    for cell in sortedWaterCell:
        # get avarage height of water + soil
        averageHeight = GetAverageHeight(cell, grid_cell)
        ###print(averageHeight)

        # get amout of flow water
        waterFlowAmount = GetFlowWaterAmount(cell.water_level + cell.soil_level, 4)
        ###print(waterFlowAmount)

        # flow water to neighbour cells    =========== check this function ============
        grid_cell = OverFlowWaterToNeighbour(grid_cell, cell, waterFlowAmount)
        ###print(get_show_grid(grid_cell))

        # reduce water from infiltraion
        grid_cell = ReduceWaterInfiltration(grid_cell, soilInfiltraionMap, 3)

    # make grid_show and set to img
    grid_show = get_show_grid(grid_cell)

    # debug#
    # print(grid_show)

    img.set_data(grid_show)
    return img


def main():
    parser = argparse.ArgumentParser(description="Its Flooding")

    # parsing arguments
    parser.add_argument('--grid-size', dest='N', required=False)
    parser.add_argument('--mov-file', dest='movfile', required=False)
    parser.add_argument('--interval', dest='interval', required=False)
    parser.add_argument('--glider', action='store_true', required=False)
    parser.add_argument('--gosper', action='store_true', required=False)
    args = parser.parse_args()

    # set grid size
    N = 50
    if args.N and int(args.N) > 8:
        N = int(args.N)

    updateInterval = 500
    if args.interval:
        updateInterval = int(args.interval)

    grid_cell = get_random_cell_grid(N)

    # debug#
    # for i in grid_cell:
    #     for j in i:
    #         print(j.water_level)

    grid_show = get_show_grid(grid_cell)

    fig, ax = plt.subplots()
    img = ax.imshow(grid_show, interpolation='nearest')

    ani = animation.FuncAnimation(fig, update, fargs=(img, grid_cell, N,),
                                  frames=100,
                                  interval=updateInterval,
                                  save_count=50)

    plt.show()


main()