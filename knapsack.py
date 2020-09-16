import numpy as np

class PlayersPoints(object):
    def __init__(self, points=0,players=[]):
        self.points = points
        self.players = players

    def setPoints(self,points):
        self.points = points

    def getPoints(self):
        return self.points

    def getPlayers(self):
        return self.players

    def addPlayer(self,index):
        self.players.append(index)
    def addPlayers(self,listOfPlayers):
        self.players = self.players + listOfPlayers

def solve(salary, cost, points, n):
    K = [[PlayersPoints() for x in range(salary+1)] for x in range(n+1)]
    
    for i in range(n+1):
        for w in range(salary+1):
            if (i==0) or (w==0):
                K[i][w].setPoints = 0
            elif cost[i-1] <= w:
                K[i][w].addPlayers(K[i-1][w].getPlayers())
                if K[i-1][w-int(cost[i-1])].getPoints() + points[i-1] > K[i-1][w].getPoints():
                    K[i][w].setPoints(K[i-1][w-int(cost[i-1])].getPoints() + points[i-1])
                    K[i][w].addPlayer(i-1)
                else:
                    K[i][w].setPoints(K[i-1][w].getPoints())
            else:
                K[i][w].setPoints(K[i-1][w].getPoints())
    return K[n][salary].getPlayers()