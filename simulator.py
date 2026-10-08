import random
import math
from matplotlib import lines, pyplot as plt
import numpy as np

# The following functions are used to calculate the probability of a cell 
# dying at a certain time step after being infected.
def normpdf(x, mean, sd):
    """
    Return the value of the normal distribution 
    with the specified mean and standard deviation (sd) at position x.
    You do not have to understand how this function works exactly. 
    """
    var = float(sd)**2
    denom = (2*math.pi*var)**.5
    num = math.exp(-(float(x)-float(mean))**2/(2*var))
    return num/denom # return value of normal distribution of x with mean and sd

def pdeath(x, mean, sd): # return probability of death at time step x, mortality rate
    start = x-0.5
    end = x+0.5
    step =0.01    
    integral = 0.0
    while start<=end:
        integral += step * (normpdf(start,mean,sd) + normpdf(start+step,mean,sd)) / 2
        start += step            
    return integral    

# tuning parameters
recovery_time = 4 # recovery time in time-steps
virality = 0.4  # probability that a neighbor cell is infected in each time step 
mean = 4 # mean time to death after infection
sd = 1    


class Cell(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y 
        self.state = "S" # can be "S" (susceptible), "R" (resistant = dead), or "I" (infected)
        self.time = 0 # need to keep track of each time step
        
    def infect(self): # Step 2.1: if a cell infected, it's time resets to 0
        self.state = "I"
        self.time = 0

    def process(self, adjacent_cells): # Step 2.3
        if self.state == "I":
            if self.time >= recovery_time:
                self.state = "S"
                self.time = 0 # reset time of recovered cells to 0
                return # return so that this function stops, goes to next time step
            
            if random.random() <= pdeath(self.time, mean, sd): # if a random number generated is less than or equal to probability of death at a time step, cell dies
                self.state = "R"
                return
                
            if self.time >= 1:   # if cell is infected for at least 1 time step, it can infect others
                for cells in adjacent_cells:
                    if cells.state == "S":
                        if random.random() <= virality: # if random number(0,1) <= virality, cells get infected
                            cells.infect()           
            self.time += 1
        else:
            return 
            

class Map(object): # used to represent the grid of cells
    
    def __init__(self):
        self.height = 150
        self.width = 150          
        self.cells = {} # dictionary to store cells

    def add_cell(self, cell): # Step 1.1 
        self.cells[(cell.x, cell.y)] = cell # add cell to map, key is (x, y) coordinates (tuples) immutable, value is cell object
        
    def display(self): # Step 1.3
        data_array = np.zeros((self.height, self.width, 3)) # create 3D array of zeroes
        
        # extract values from self.cells(dictionary) and add it to array
        # replace the 0 with color of each cell
        for (x, y) in self.cells: # iterate through all cells by their coordinates
            cell = self.cells[(x, y)] # extract cell from key (x, y)
            if cell.state == "S":
                data_array[x][y] = [0, 1, 0] # green
            elif cell.state == "I":
                data_array[x][y] = [1, 0, 0] # red
            elif cell.state == "R":
                data_array[x][y] = [0.3, 0.3, 0.3] # grey
        
        plt.imshow(data_array)
        plt.draw()  # display the map
        plt.ylabel('x')
        plt.xlabel('y')
    
    def adjacent_cells(self, x, y): # Step 2.2
        lst = []
        # check cells in the same row
        for i in range(x-1, x+2): # let x = 42, then i loops from 41 to 43
            cell = self.cells.get((i, y))
            if cell is not None: # ensure cell exists, not out of range
                    if cell != self.cells[(x, y)]:
                        lst.append(cell)

        # check cells in the same column
        for j in range(y-1, y+2): # let y = 82, then j loops form 81 to 83
                cell = self.cells.get((x, j)) # get cell at (i, j), returns None if no cell at (i, j) [used LLM to learn this function]
                if cell is not None: # ensure cell exists, not out of range
                    if cell != self.cells[(x, y)]:
                        lst.append(cell)
                        
        # lst.remove(self.cells[(x, y)])
        
        return lst # list now contains all adjacent cells 

    def time_step(self): # Step 2.4
        for (x, y) in self.cells:
            cell = self.cells[(x, y)]
            if cell.state == "I": # only check for infected cells, don't need to check all cells
                adjacent_cells = self.adjacent_cells(x, y)
                cell.process(adjacent_cells)



def read_map(filename):
    
    m = Map() # create a 150 x 150 grid
    
    def getLines(filename):
        with open(filename, "r") as f:
            text = f.read()
        lines = text.split("\n")
        output = []
        for line in lines:
            if len(lines) != 0:
                output.append(line)
        return output # returns list of strings, each entry represent a line in file

    def getCSVFields(filename):
        lines = getLines(filename)
        data = []
        for line in lines:
            if line.strip() != "":
                row = line.split(",")
                data.append(row)
        return data # returns list of lists of strings, each sublist represent a row, each entry in sublist is a string
    
    data = getCSVFields(filename)
    for data in data:
        cell = Cell(int(data[0]), int(data[1])) # create cell class
        m.add_cell(cell) # using add_cell function to at this cell object to dictionary
        
    return m


def main():
    m = read_map("nyc_map.csv")
    m.cells[(42, 82)].infect() # first infected cell

    steps = 50  # number of time steps to run

    for t in range(steps): # loop through every time step
        m.time_step() # start checking adjacent cells, infect them or recovery, main function
        m.display()
        plt.pause(0.1) # LLM, pauses the loop by 0.1s, display refreshes every loop, smooth animation
        
main()