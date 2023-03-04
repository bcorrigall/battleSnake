
red = (255,0,0)
blue = (0,0,255)
yellow = (0,255,0)
black = (0,0,0)
white = (255,255,255)
orange = (255, 150, 0)
purple = (200, 0, 160)
turquoise = (64,224,208)
green = (0,200,0)

colourDict = {"Open":white, "Start":blue, "End":red, "Bloc":black, "Crossed":yellow, "Dead":orange, "Best":purple,"Next":green, "Checked":turquoise}

class Node:
    def __init__(self, x_cord=None, y_cord = None):
        self.tick = 0
        self.value = None
        self.cord = [x_cord, y_cord]
        self.dict = {}
        self.colour = None
        self.distance = float('inf')
        self.visited = False
        self.GScore = float('inf')
        self.HScore = float('inf')

        
    def setValue(self, value):
        self.value = value
        try:
            self.colour = colourDict[value]
        except:
            self.color=red

    def getValue(self):
        return self.value

    def getPos(self):
        x = self.cord[0]//32
        y = self.cord[1]//32
        
        return((x,y))
    
    def setCord(self, cord):
        self.cord = cord
        #The Coordinates are of pixels on the screen

    def setDist(self, dist):
        #this will only be used in the dijkstra's algorhythm
        #this will take the distance from the starting node 
        self.distance = round(dist,2)
    
    def getDist(self):
        return(self.distance)

    def setGScore(self, F):
        self.GScore = F
    
    def getGScore(self):
        return(self.GScore)

    def setHScore(self, h):
        self.HScore = h

    def getHScore(self):
        return(round(self.HScore, 2))

    def setColour(self, colour):
        self.colour = colour

    def ticked(self):
        self.tick += 1
    
    def setVisited(self):
        self.visited = True

    def getVisited(self):
        return(self.visited)
