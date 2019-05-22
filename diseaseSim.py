# 
# diseaseSim.py - simulates the spread of disease through a population
#
# Student Name   : 
# Student Number :
#
# Version history:
#
# 25/4/19 - beta version released for FOP assignment
#
import numpy as np
import matplotlib.pyplot as plt
import random

random.seed(2)
np.random.seed(3)

# # # # # # # # # # # # # # # # # # # # # # #
# # --------- PARAMETER SETTINGS -------- # #
# # # # # # # # # # # # # # # # # # # # # # #
INIT_PPL = 10
INIT_INFCT = 4
SIZE_X = 5              # size of x-domain
SIZE_Y = 5              # size of y-domain
NEIGHB = 0              # 0: Moore neighbourhoods, 1: Von Neumann neighbourhoods
BARRIER_VER_X = -1      # location of the vertical barrier. set to -1 to disable
BARRIER_HOR_Y = -1      # location of the horizontal barrier. set to -1 to disable
NUM_STEPS = 10
INFCT_THRES = 0.8
CURE_THRES = 0.1
DEAD_THRES = 0.1

# # # # # # # # # # # # # # # # # # # # # # # # # #
# # --------- FUNCTIONS AND CLASSES ---------- # # 
# # # # # # # # # # # # # # # # # # # # # # # # # #
def initWorld():
    world = []
    for y in range(SIZE_Y-1, -1, -1):
        row = []
        for x in range(0, SIZE_X):
            row.append(Grid(x, y))
        world.append(row)
    return world
def initPpl():
    ppl = []
    for i in range(0, INIT_PPL):
        x = BARRIER_VER_X
        y = BARRIER_HOR_Y
        while x == BARRIER_VER_X or y == BARRIER_HOR_Y:
        # This loop avoid initiation at the barrier location
            x = np.random.randint(0, SIZE_X)
            y = np.random.randint(0, SIZE_Y)
        if i < INIT_INFCT:
            ppl.append(People(x=x, y=y, status="infected"))
        else:
            ppl.append(People(x=x, y=y, status="healthy"))
    return ppl
def refreshPpl(world):
    for w in world:
        for grid in w:
            grid.numPpl = 0
    return world

def updatePeopleInWorld(world, ppl):
    world = refreshPpl(world)
    for p in ppl:
        world[SIZE_Y-1 - p.pos[1]][p.pos[0]].numPpl += 1
    return world

def updateInfectPeople(ppl):
    for p1 in ppl:
        if p1.status == "infected":
            hazardPos = p1.pos
            for p2 in ppl:
                if (p2.pos == hazardPos).all() and p2.status != "infected":
                    prob = np.random.uniform(0,1)
                    if prob < INFCT_THRES:
                        p2.status = "infected"
                        print("People get infected at grid", hazardPos)
    return ppl
def curePeople(ppl):
    for p in ppl:
        if p.status == "infected":
            prob = np.random.uniform(0,1)
            if prob < CURE_THRES:
                p.status = "healthy"
                print("People get cured at grid", p.pos)
    return ppl
def deadPeople(ppl):
    for p in ppl:
        if p.status == "infected":
            prob = np.random.uniform(0,1)
            if prob < DEAD_THRES:
                p.status = "dead"
                print("People died at grid", p.pos)
def movePeople(ppl):
    for p in ppl:
        if p.status != "dead":
            p.move()
    return ppl
def printPplStatus(ppl):
    stat = []
    for p in ppl:
        stat.append(p.status)
    print(stat)
def countInfected(ppl):
    cnt = 0
    for p in ppl:
        if p.status == "infected":
            cnt+=1
    return cnt

class Grid():
    '''
    The Grid object represents one particular grid.
    '''
    def __init__(self, x, y):
        self.pos = np.array([x, y])
        self.state = "safe"
        self.numPpl = 0
    
    def toHazard(self):
        self.state = "hazard"
    
    def __repr__(self):
        '''
        This function prints the returned value if print() is used.
        '''
        return str(self.numPpl)
    

class People():
    '''
    
    '''
    def __init__(self, x, y, status="healthy"):
        self.x = x
        self.y = y
        self.pos = np.array([x, y])
        self.status = status
    def move(self):
        '''
        Move the people according to Moore or Von Neumann neighbourhoods.
        The moving direction is based on random function which is decoded by 
        numpad direction as follows:
            
            7 8 9
            4 5 6
            1 2 3   for Moore neighbourhoods,
        and    
              8
            4 5 6
              2     for Von Neumann neighbourhoods.
        
        The moving step is validated by updatePos() function.        
        '''
        if NEIGHB == 0: # if Moore neighbourhoods
            new_grid = np.random.choice([1,2,3,4,5,6,7,8,9])
        if NEIGHB == 1: # if Von Neumann neighbourhoods
            new_grid = np.random.choice([  2,  4,5,6,  8  ])
        
        if new_grid == 1:
            self.x += -1
            self.y += -1
        elif new_grid == 2:
            self.x +=  0
            self.y += -1
        elif new_grid == 3:
            self.x +=  1
            self.y += -1
        elif new_grid == 4:
            self.x += -1
            self.y +=  0
        elif new_grid == 5:
            self.x +=  0
            self.y +=  0
        elif new_grid == 6:
            self.x +=  1
            self.y +=  0
        elif new_grid == 7:
            self.x += -1
            self.y +=  1
        elif new_grid == 8:
            self.x +=  0
            self.y +=  1
        elif new_grid == 9:
            self.x +=  1
            self.y +=  1
        # check and update the new grid
        self.updatePos(self.x, self.y)
        
    def updatePos(self, x, y):
        '''
        Check whether the new step exceeds the domain of the problem or 
        clashes the barrier.
        '''
        # if x exceeds the boundary, keep it at boundary
        if x < 0:
            x = 0
        if x >= SIZE_X:
            x = SIZE_X-1
        # if y exceeds the boundary, keep it at boundary
        if y < 0:
            y = 0
        if y >= SIZE_Y:
            y = SIZE_Y-1
        # if x or y crashes the barrier, do not move
        if x == BARRIER_VER_X or y == BARRIER_HOR_Y:
            self.x = self.pos[0] # restore to previous value
            self.y = self.pos[1] # restore to previous value
        else:
            self.x = x
            self.y = y
            self.pos = np.array([x, y]) # update position
    def __repr__(self):
        '''
        This function prints the returned value if print() is used.
        '''
        return str(self.pos)
            
    
        
# # # # # # # # # # # # # # # # # # # # # #        
# # ----------- START HERE ------------ # #       
# # # # # # # # # # # # # # # # # # # # # #
world = initWorld()
ppl = initPpl()
world = updatePeopleInWorld(world, ppl)
infctHist = [countInfected(ppl)]

for t in range(0, NUM_STEPS):
    print("======= Time step {} =======".format(t) )
    print("** World Map Showing how many people in each grid **")
    print(np.array(world))
    world = updatePeopleInWorld(world, ppl)   
    print("People position:")
    print(ppl) # This print shows location of each People
    print("People status:")
    printPplStatus(ppl) # This print shows the status of each People
    ppl = updateInfectPeople(ppl)
    ppl = curePeople(ppl)
    ppl = movePeople(ppl)
    infctHist.append(countInfected(ppl))

plt.plot(infctHist)