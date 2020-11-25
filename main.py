from random import *
from tkinter import *
from garde import *
from espion import *
from terrain import *
from case import *
from interface import *
import time
from collections import OrderedDict  # /
import os

clear = lambda: os.system('clear')  # on Linux System
clear()

max1 = 20  #

###########################################
obstacle = [[0] * max1 for _ in range(max1)]
for i in range(1, 4):
    obstacle[i][3] = 1
for i in range(6, max1):
    obstacle[i][3] = 1
for i in range(1, max1):
    obstacle[max1 - 1][i] = 1
for i in range(1, max1):
    obstacle[i][1] = 1
for i in range(1, max1):
    obstacle[1][i] = 1
for i in range(1, max1):
    obstacle[max1 - 1][i] = 1
for i in range(1, max1):
    obstacle[i][max1 - 1] = 1
for i in range(1, 3):
    obstacle[i][12] = 1
for i in range(4, max1 - 2):
    obstacle[i][12] = 1
for i in range(1, 3):
    obstacle[i][17] = 1
for i in range(4, 7):
    obstacle[i][17] = 1
for i in range(8, 9):
    obstacle[i][17] = 1
for i in range(12, 18):
    obstacle[i][17] = 1
for i in range(19, max1):
    obstacle[i][17] = 1

obstacle[10][18] = 1
obstacle[15][18] = 1
obstacle[5][18] = 1
obstacle[10][14] = 1

###instance de garde:
listGarde = []
for i in range(8):
    listGarde.append(garde())
###instance d'espion:
listEspion = []
for i in range(1):
    listEspion.append(espion())

for i in range(10, max1 - 2):
    obstacle[i][15] = 1

for i in range(3, 8):
    obstacle[i][14] = 1

environnement = terrain(max1, max1, obstacle, listGarde, listEspion)

# Caisse
####################
environnement.caisse(obstacle, 2, 3, 5, 5)
environnement.caisse(obstacle, 2, 3, 5, 9)
environnement.caisse(obstacle, 2, 3, 9, 5)
environnement.caisse(obstacle, 2, 3, 12, 5)
environnement.caisse(obstacle, 2, 3, 9, 5)
environnement.caisse(obstacle, 2, 3, 9, 9)
environnement.caisse(obstacle, 2, 3, 13, 8)
environnement.caisse(obstacle, 2, 3, 9, 9)
####################

# Lumiere
####################
environnement.addLamp(18, 4, 13, 1)  # Rajoute une lampe sur la carte
environnement.addLamp(8, 8, 15, 1)
environnement.addLamp(2, 11, 10, 1)

environnement.addProj(2, 16, 11, 6)  # Rajoute un projecteur sur la carte
environnement.addLamp(11, 16, 9, 1)
environnement.addLamp(15, 14, 13, 2)
environnement.addLamp(16, 18, 9, 1)
####################

# Garde
####################
environnement.placerGarde()
####################

# Espion
####################
environnement.placerEspion()
####################

# carte
####################
environnement.ConvertGrilleIntToObj()
environnement.toDisplay()
fenetre = interface(Tk(), environnement)
environnement.addFenetre(fenetre)


def boucleaffichage():
    boucleaffichage.cpt += 1
    environnement.deplacementGarde()
    environnement.fuiteEspion()

    fenetre.fenetre.after(800, boucleaffichage)


boucleaffichage.cpt = 0
a = input("appuyez sur entrer pour lancer la simulation")
boucleaffichage()

fenetre.fenetre.mainloop()