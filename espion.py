from random import *


class espion:
    def __init__(self, coordX=0, coordY=0):
        self.x = coordX
        self.y = coordY
        self.id = None
        self.estTrouver = False
        self.distance = 5
        self.tourRestantfuite = 0;
        self.gardeProche = []

    def moveEspion(self, x, y, env):
        env.grille[self.x][self.y].espion = False;
        env.grille[x][y].espion = self;
        self.x = x
        self.y = y
        env.fenetre.moveGarde(self.id, x, y)

    def getPosition(self, grille):
        return self.x, self.y

    def ifCachetteTrouver(self):
        if self.tourRestantfuite > 0:
            self.tourRestantfuite -= 1
        else:
            self.estTrouver = False
            del self.gardeProche[:]

    def ifReperer(self, garde):
        self.tourRestantfuite = 5
        self.estTrouver = True
        if not (garde in self.gardeProche):
            self.gardeProche.append(garde)

    def fuite(self, env):
        direction = [[], []]
        if self.estTrouver and len(self.gardeProche) > 0:

            closedGarde = self.returnPlusProcheGarde(self.gardeProche)

            distance = abs(closedGarde.x - self.x) + abs(closedGarde.y - self.y)
            if not self.verifCaseLibre(self.x - 1, self.y, env) and not self.verifCaseLibre(self.x, self.y + 1,
                                                                                            env) and not self.verifCaseLibre(
                    self.x, self.y - 1, env) and not self.verifCaseLibre(self.x + 1, self.y, env):
                placer = False
                while (placer == False):
                    x = randint(2, env.tailleX - 2)
                    y = randint(2, env.tailleY - 2)
                    if (not env.grille[x][y].mur and not env.grille[x][y].espion and not env.grille[x][y].perso):
                        self.moveEspion(x, y, env)
                        placer = True

            if self.verifCaseLibre(self.x, self.y + 1, env) and abs(closedGarde.x - self.x) + abs(
                    closedGarde.y - (self.y + 1)) > distance:
                direction[0].append(self.x)
                direction[1].append(self.y + 1)
            if self.verifCaseLibre(self.x, self.y - 1, env) and abs(closedGarde.x - self.x) + abs(
                    closedGarde.y - (self.y - 1)) > distance:
                direction[0].append(self.x)
                direction[1].append(self.y - 1)
            if self.verifCaseLibre(self.x + 1, self.y, env) and abs(closedGarde.x - (self.x + 1)) + abs(
                    closedGarde.y - self.y) > distance:
                direction[0].append(self.x + 1)
                direction[1].append(self.y)
            if self.verifCaseLibre(self.x - 1, self.y, env) and abs(closedGarde.x - (self.x - 1)) + abs(
                    closedGarde.y - self.y) > distance:
                direction[0].append(self.x - 1)
                direction[1].append(self.y)

            if len(direction[0]) != 0:
                n = randint(0, len(direction[0]) - 1)
                if env.grille[direction[0][n]][direction[1][n]].perso == False:
                    self.moveEspion(direction[0][n], direction[1][n], env)

    def verifCaseLibre(self, newx, newy, env, espion=True):
        try:
            if ((env.grille[newx][newy].mur == False) and env.grille[newx][newy].perso == False and env.grille[newx][
                newy].espion == False) and env.grille[self.x][self.y].perso == False:
                return True
            else:
                return False
        except:
            print('erreur survenu dans espion')
            return False

    def returnPlusProcheGarde(self, listGarde):
        closedGarde = listGarde[0]
        distance = abs(listGarde[0].x - self.x) + abs(listGarde[0].y - self.y)
        for garde in listGarde:
            distTemp = abs(garde.x - self.x) + abs(garde.y - self.y)
            if distTemp < distance:
                distance = distTemp
                closedGarde = garde
        return closedGarde

