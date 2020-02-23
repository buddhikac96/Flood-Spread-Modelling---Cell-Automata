import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


matplotlib.rcParams['figure.figsize'] = (8, 5.5)

sampleSoil = [[2,5,6,6], [5,3,5,5], [6,5,2,5], [6,6,5,2]]

sampleWater = [[6,0,0,0], [0,5,2,0], [0,0,6,0], [0,0,0,6]]

soilInfiltraionMap = {
    'default' : {
        'f0' : 0.01,
        'fc' : 0.02,
        'k' : 0.03
    },
    
    'waterarea' : {
        'f0' : 0,
        'f1' : 0,
        'k' : 0
    },
    
    'settlement' : {
        'f0' : 4.06,
        'fc' : 0.03,
        'k' : 0.45
    },
    
    'rocks' : {
        'f0' : 0.03,
        'fc' : 0.002,
        'k' : 0.02
    }
}

class Cell:
    
    soilType = 'default'
    
    def __init__(self, i, j, soil, water):
        self.i = i
        self.j = j
        self.soil = soil
        self.water = water

#get a single 2d array of tuples of water level and soil level
def getSoilLevelPlusWaterLevel(soil, water):
  grid = []
  for i in range(len(soil)):
    row = []
    for j in range(len(soil[i])):
      #row.append((soilLevel[i][j], waterLevel[i][j])) 2d array of tupes
      row.append(Cell(i, j, soil[i][j], water[i][j]))
    grid.append(row)

  return grid

#get cells which has water
def GetWaterCells(grid):
  arr = []
  n = len(grid)
  for i in range(1, n - 1):
    for j in range(1, n - 1):
      if grid[i][j].water > 0:
        arr.append(grid[i][j])
  return arr

def SortWaterCellArray(array):
  return sorted(array, key = lambda i: i.water)

def GetAverageHeight(cell, grid):
  left = grid[cell.i][cell.j + 1].water + grid[cell.i][cell.j + 1].soil 
  top = grid[cell.i + 1][cell.j].water + grid[cell.i + 1][cell.j].soil 
  right = grid[cell.i][cell.j + 1].water + grid[cell.i][cell.j + 1].soil 
  bottom = grid[cell.i - 1][cell.j].water + grid[cell.i - 1][cell.j].soil 
  center = cell.soil + cell.water

  return (left + top + right + bottom + center) / 5

def GetFlowWaterAmount(centerCellHeight, numberOfNeighbours):
  return centerCellHeight / (numberOfNeighbours + 1)

def OverFlowWaterToNeighbour(grid, cell, waterFlowAmount):
  #left
  if(grid[cell.i][cell.j - 1].water + grid[cell.i][cell.j - 1].soil + waterFlowAmount <= cell.water + cell.soil):
    grid[cell.i][cell.j - 1].water += waterFlowAmount
  else:
    grid[cell.i][cell.j - 1].water += (cell.water + cell.soil) - (grid[cell.i][cell.j - 1].water + grid[cell.i][cell.j - 1].soil)
    grid[cell.i][cell.j].water += waterFlowAmount - ((cell.water + cell.soil) - (grid[cell.i][cell.j - 1].water + grid[cell.i][cell.j - 1].soil))

  #top
  if(grid[cell.i - 1][cell.j].water + grid[cell.i - 1][cell.j].soil + waterFlowAmount <= cell.water + cell.soil):
    grid[cell.i - 1][cell.j].water += waterFlowAmount
  else:
    grid[cell.i - 1][cell.j].water += (cell.water + cell.soil) - (grid[cell.i - 1][cell.j].water + grid[cell.i - 1][cell.j].soil)
    grid[cell.i][cell.j].water += waterFlowAmount - ((cell.water + cell.soil) - (grid[cell.i - 1][cell.j].water + grid[cell.i - 1][cell.j].soil))

  #right
  if(grid[cell.i][cell.j + 1].water + grid[cell.i][cell.j + 1].soil + waterFlowAmount <= cell.water + cell.soil):
    grid[cell.i][cell.j + 1].water += waterFlowAmount
  else:
    grid[cell.i][cell.j + 1].water += (cell.water + cell.soil) - (grid[cell.i][cell.j + 1].water + grid[cell.i][cell.j + 1].soil)
    grid[cell.i][cell.j].water += waterFlowAmount - ((cell.water + cell.soil) - (grid[cell.i][cell.j + 1].water + grid[cell.i][cell.j + 1].soil))

  #bottom
  if(grid[cell.i + 1][cell.j].water + grid[cell.i + 1][cell.j].soil + waterFlowAmount <= cell.water + cell.soil):
    grid[cell.i + 1][cell.j].water += waterFlowAmount
  else:
    grid[cell.i + 1][cell.j].water += (cell.water + cell.soil) - (grid[cell.i + 1][cell.j].water + grid[cell.i + 1][cell.j].soil)
    grid[cell.i][cell.j].water += waterFlowAmount - ((cell.water + cell.soil) - (grid[cell.i + 1][cell.j].water + grid[cell.i + 1][cell.j].soil))

def ReduceWaterInfiltration(grid, soilInfiltraionMap, time):
    for i in grid:
        for j in i:
            p = soilInfiltraionMap[j.soilType]['fc']
            q = soilInfiltraionMap[j.soilType]['f0']
            k = soilInfiltraionMap[j.soilType]['k']
            ft = p + ((p - q)*2.78) ** ((-1) * k) * time
            
            ql = ft * time
            
            if(j.water - ql >= 0):
                j.water = j.water - ql
            else:
                j.water = 0

def Driver():
    for cell in sortedWaterCell:
        averageHeight = GetAverageHeight(cell, grid)
      
        waterFlowAmount = GetFlowWaterAmount(cell.water + cell.soil, 4)

        OverFlowWaterToNeighbour(grid, cell, waterFlowAmount)
        
        ReduceWaterInfiltration(grid, soilInfiltraionMap, 3)

#create grid
grid = getSoilLevelPlusWaterLevel(sampleSoil, sampleWater)

#get cells which has water
waterCells = GetWaterCells(grid)

#sort water cells
sortedWaterCell = SortWaterCellArray(waterCells)[::-1]

#iterate over all water cells
for cell in sortedWaterCell:
  averageHeight = GetAverageHeight(cell, grid)
  
  waterFlowAmount = GetFlowWaterAmount(cell.water + cell.soil, 4)

  OverFlowWaterToNeighbour(grid, cell, waterFlowAmount)
    
  ReduceWaterInfiltration(grid, soilInfiltraionMap, 3)

  
