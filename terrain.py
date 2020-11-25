from random import *
from espion import *
from case import *
from random import *
from garde import *
import time

from collections import OrderedDict  # /


class terrain:
    def __init__(self, tailleX=10, tailleY=10, grille=[], listGarde=[], listEspion=[]):
        self.tailleX = tailleX
        self.tailleY = tailleY
        self.grille = grille
        self.listGarde = listGarde
        self.listEspion = listEspion
        self.lumen = [[3] * tailleX for _ in range(tailleY)]

    def addFenetre(self, fen):
        self.fenetre = fen

    def placerGarde(self):
        for i in range(len(self.listGarde)):
            placer = False or self.listGarde[i].x != 0 and self.listGarde[i].y != 0
            while (placer == False):
                x = randint(1, self.tailleX - 2)
                y = randint(1, self.tailleY - 2)
                if (self.grille[x][y] == 0):
                    self.listGarde[i] = garde(x, y)
                    placer = True
            self.grille[self.listGarde[i].x][self.listGarde[i].y] = self.listGarde[i]

    def placerEspion(self):
        for i in range(len(self.listEspion)):
            placer = False or self.listEspion[i].x != 0 and self.listEspion[i].y != 0
            while (placer == False):
                x = randint(2, self.tailleX - 2)
                y = randint(2, self.tailleY - 2)
                if (self.grille[x][y] == 0):
                    self.listEspion[i] = espion(x, y)
                    placer = True

    def addLamp(self, x, y, strengh, minus):  # Permet de diffuser une lumière comme une lampe
        strengh1 = strengh
        if (x < self.tailleX) and (y < self.tailleY) and (x >= 0) and (
                y >= 0):  # On considère qu'une lumière n'influe pas hors des limites de la carte
            if (isinstance(self.grille[x][y], garde) or (self.grille[x][y] == 0)) and (self.grille[x][
                                                                                           y] != 1):  # On mofifie la lumière sur un case si ce n'est pas un mur, s'il y a une case vide ou une case avec un garde
                if ((self.lumen[x][y] == 0) or (self.lumen[x][
                                                    y] < strengh1)):  # S'il n'y a pas de lumière sur une case ou s'il y a une lumière moins puissante
                    if strengh1 > 2:
                        self.lumen[x][y] = strengh1
                        strengh1 = strengh1 - minus
                        self.addLamp(x + 1, y, strengh1, minus)
                        self.addLamp(x - 1, y, strengh1, minus)
                        self.addLamp(x, y + 1, strengh1, minus)
                        self.addLamp(x, y - 1, strengh1, minus)
                        self.addLamp(x + 1, y + 1, strengh1, minus)
                        self.addLamp(x + 1, y - 1, strengh1, minus)
                        self.addLamp(x - 1, y + 1, strengh1, minus)
                        self.addLamp(x - 1, y - 1, strengh1, minus)

    #                 Direction :
    #				     1  2  3
    #				     8  X  4
    #                   7  6  5
    def addProj(self, x, y, strengh, direction):  # Permet de diffuser une lumière comme un projecteur
        if (isinstance(self.grille[x][y], garde)) or (self.grille[x][y] == 0) and (self.grille[x][y] != 1) and (
                (x < self.tailleX) and (y < self.tailleY)) and ((x >= 0) and (
                y >= 0)):  # On considère qu'une lumière n'influe pas hors des limites de la carte, si ce n'est pas un mur, s'il y a une case vide ou une case avec un garde
            if ((self.lumen[x][y] == 0) or (self.lumen[x][y] < strengh)) and (
                    strengh > 2):  # S'il n'y a pas de lumière sur une case ou s'il y a une lumière moins puissante
                self.lumen[x][y] = strengh
                if direction == 1:
                    self.addProj(x - 1, y - 1, strengh - 0.25, direction)
                    self.addLamp(x - 1, y, strengh - strengh * 25 / 100, 1)
                    self.addLamp(x, y - 1, strengh - strengh * 25 / 100, 1)
                elif direction == 2:
                    self.addProj(x - 1, y, strengh - 0.25, direction)
                    self.addLamp(x - 1, y - 1, strengh - strengh * 25 / 100, 1)
                    self.addLamp(x - 1, y + 1, strengh - strengh * 25 / 100, 1)
                elif direction == 3:
                    self.addProj(x - 1, y + 1, strengh - 0.25, direction)
                    self.addLamp(x - 1, y, strengh - strengh * 25 / 100, 1)
                    self.addLamp(x, y + 1, strengh - strengh * 25 / 100, 1)
                elif direction == 4:
                    self.addProj(x, y + 1, strengh - 0.25, direction)
                    self.addLamp(x - 1, y + 1, strengh - strengh * 25 / 100, 1)
                    self.addLamp(x + 1, y + 1, strengh - strengh * 25 / 100, 1)
                elif direction == 8:  # J'ai pas testé celui-là
                    self.addProj(x, y - 1, strengh - 0.25, direction)
                    self.addLamp(x - 1, y - 1, strengh - strengh * 25 / 100, 1)
                    self.addLamp(x + 1, y - 1, strengh - strengh * 25 / 100, 1)
                elif direction == 5:
                    self.addProj(x + 1, y + 1, strengh - 0.25, direction)
                    self.addLamp(x, y + 1, strengh - strengh * 25 / 100, 1)
                    self.addLamp(x + 1, y, strengh - strengh * 25 / 100, 1)
                elif direction == 6:
                    self.addProj(x + 1, y, strengh - 0.25, direction)
                    self.addLamp(x + 1, y - 1, strengh - strengh * 25 / 100, 1)
                    self.addLamp(x + 1, y + 1, strengh - strengh * 25 / 100, 1)
                elif direction == 7:
                    self.addProj(x + 1, y - 1, strengh - 0.25, direction)
                    self.addLamp(x, y - 1, strengh - strengh * 25 / 100, 1)
                    self.addLamp(x + 1, y, strengh - strengh * 25 / 100, 1)

    def toDisplay(self):
        # clear()
        for i in range(1, self.tailleX):
            for j in range(1, self.tailleY):
                if isinstance(self.grille[i][j], garde):
                    print('\033[42m', "  ", end="")
                elif self.grille[i][j] == 0:
                    print('\033[0m', "  ", end="")
                elif self.grille[i][j] == 1:
                    print('\033[47m', "  ", end="")
            print('\033[0m');

    def addGardeToGrille(self):
        for i in self.listGarde:
            self.grille[i.x][i.y] = i

    def ConvertGrilleIntToObj(self):
        tab = [[0] * self.tailleX for _ in range(len(self.grille))]

        for i in range(len(self.grille)):
            for j in range(len(self.grille[i])):
                if isinstance(self.grille[i][j], garde):
                    tab[i][j] = case(perso=self.grille[i][j])
                    tab[i][j].setLumen(self.lumen[i][j])
                elif self.grille[i][j] == 0:
                    tab[i][j] = case()
                    tab[i][j].setLumen(self.lumen[i][j])
                elif self.grille[i][j] == 1:
                    tab[i][j] = case(mur=True)
        self.placerEspion()
        self.grille = tab
        self.addEspionToGrille()

    def deplacementGarde(self):
        for garde in self.listGarde:
            garde.exploreOpti(self)

    def fuiteEspion(self):
        for espion in self.listEspion:
            espion.ifCachetteTrouver()
            espion.fuite(self)

    def addEspionToGrille(self):
        for i in self.listEspion:
            self.grille[i.x][i.y].espion = i;

    def addGardeToGrille(self):
        for i in self.listGarde:
            self.grille[i.x][i.y].garde = i;

    def caisse(self, obstacle, l, larg, x, y):
        if l < 0:
            return 1
        if larg < 0:
            return 1
        if larg + y > self.tailleY:
            return 0
        if l + x > self.tailleX:
            return 0
        for i in range(y, y + larg):
            obstacle[l + x][i] = 1
        self.caisse(obstacle, l - 1, larg, x, y)