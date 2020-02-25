import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import enum
import random


def bubbleSort(arr):
	n = len(arr)

	# Traverse through all array elements
	for i in range(n):

		# Last i elements are already in place
		for j in range(0, n-i-1):

			# traverse the array from 0 to n-i-1
			# Swap if the element found is greater
			# than the next element
			if arr[j][2] > arr[j+1][2] :
				arr[j], arr[j+1] = arr[j+1], arr[j]

def getGrid():
    return [[0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,5000,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0]]

def update(frameNum, img, grid, N):
    #get value cells
    arr = []
    for i in range(N - 1):
        for j in range(N - 1):
            if grid[i][j] > 0:
                arr.append([i,j,grid[i][j]])

    # Python program for implementation of Bubble Sort
    sortedarr = bubbleSort(arr)[::-1]

    for i in sortedarr:
        if grid[i[0]-1][i[1]] < i[2]:
            grid[i[0] - 1][i[1]]


    img.set_data(grid)
    return img

def main():

    N = 11
    updateInterval = 50

    grid_show = getGrid()

    fig, ax = plt.subplots()
    img = ax.imshow(grid_show, interpolation='nearest')

    ani = animation.FuncAnimation(fig, update, fargs=(img, grid_show, N,),
                                  frames=100,
                                  interval=updateInterval,
                                  save_count=50)

    plt.show()


if __name__ == '__main__':
    main()