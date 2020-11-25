from random import *
from collections import OrderedDict  # /


class garde:
    def __init__(self, coordX=0, coordY=0, ):
        self.x = coordX
        self.y = coordY
        self.id = None
        self.orientation = 0  #
        self.lastchemin = []

    def prevenir(self, gardeProche):
        print("garde prévenu")

    def explore(self, env):
        ok = False
        chooseDirection = self.modifRandomDirectionChoice([0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3], env)

        while not ok:
            try:
                direction = chooseDirection[randint(0, len(chooseDirection) - 1)]
            except:
                direction = chooseDirection[0]

            if direction == 0:
                if self.y > 0 and not env.grille[self.x][self.y - 1].mur and env.grille[self.x][
                    self.y - 1].perso == False and env.grille[self.x][self.y - 1].espion == False:
                    self.move(self.x, self.y - 1, env)
                    ok = True
                else:
                    chooseDirection[:] = (i for i in chooseDirection if i != 0)
            elif direction == 1:
                if self.y < len(env.grille[self.x]) - 1 and not env.grille[self.x][self.y + 1].mur and \
                        env.grille[self.x][self.y + 1].perso == False and env.grille[self.x][
                    self.y + 1].espion == False:
                    self.move(self.x, self.y + 1, env)
                    ok = True
                else:
                    chooseDirection[:] = (i for i in chooseDirection if i != 1)
            elif direction == 2:
                if self.x > 0 and not env.grille[self.x - 1][self.y].mur and env.grille[self.x - 1][
                    self.y].perso == False and env.grille[self.x - 1][self.y].espion == False:
                    self.move(self.x - 1, self.y, env)
                    ok = True
                else:
                    chooseDirection[:] = (i for i in chooseDirection if i != 2)
            elif direction == 3:
                if self.x < len(env.grille) - 1 and not env.grille[self.x + 1][self.y].mur and env.grille[self.x + 1][
                    self.y].perso == False and env.grille[self.x + 1][self.y].espion == False:
                    self.move(self.x + 1, self.y, env)
                    ok = True
                else:
                    chooseDirection[:] = (i for i in chooseDirection if i != 3)

            if len(chooseDirection) == 0:
                ok = True  # si aucun deplacement possible, on ne bouge pas

    def getPosition(self, grille):
        return self.x, self.y

    def move(self, x, y, env):
        self.actualiseLastChemin(self.x, self.y)
        env.grille[self.x][self.y].perso = False;
        env.grille[x][y].perso = self;
        self.x = x
        self.y = y
        env.fenetre.moveGarde(self.id, x, y)

    def actualiseLastChemin(self, x, y):
        self.lastchemin.append((x, y))
        if len(self.lastchemin) > 15:
            self.lastchemin.pop(0)

    def modifRandomDirectionChoice(self, tab, env):
        for i in self.lastchemin:
            if (abs((i[0] + i[1]) - (self.x + self.y)) == 1):
                if (i[0] > self.x):
                    tab = list(filter((3).__ne__, tab))
                    tab.append(3)
                    if self.lastchemin.index(i) < 5: tab.append(3)
                elif (i[0] < self.x):
                    tab = list(filter((2).__ne__, tab))
                    tab.append(2)
                    if self.lastchemin.index(i) < 5: tab.append(2)
                elif (i[1] > self.y):
                    tab = list(filter((1).__ne__, tab))
                    tab.append(1)
                    if self.lastchemin.index(i) < 5: tab.append(1)
                elif (i[1] < self.y):
                    tab = list(filter((0).__ne__, tab))
                    tab.append(0)
                    if self.lastchemin.index(i) < 5: tab.append(0)
        tab = self.modifDirectionByShadow(tab, env)
        return tab

    def modifDirectionByShadow(self, tab, env):
        # ordre: (0,lum), (1,lum), (2,lum), (3,lum)
        lum = [(0, env.grille[self.x][self.y - 1].lumiere),
               (1, env.grille[self.x][self.y + 1].lumiere),
               (2, env.grille[self.x - 1][self.y].lumiere),
               (3, env.grille[self.x + 1][self.y].lumiere)]
        lum.sort(key=lambda tup: tup[1])
        tab.append(lum[0][0]);
        tab.append(lum[0][0]);
        tab.append(lum[1][0]);
        return tab;

    def exploreOpti(self, env):
        directionAccessible = []
        repere = self.repereEspion(env)
        if repere != False:
            self.move(repere[0], repere[1], env)
        else:
            if self.y > 0 and not env.grille[self.x][self.y - 1].mur and env.grille[self.x][self.y - 1].perso == False:
                directionAccessible.append(0)
            if self.y < len(env.grille[self.x]) - 1 and not env.grille[self.x][self.y + 1].mur and env.grille[self.x][
                self.y + 1].perso == False:
                directionAccessible.append(1)

            if self.x > 0 and not env.grille[self.x - 1][self.y].mur and env.grille[self.x - 1][self.y].perso == False:
                directionAccessible.append(2)
            if self.x < len(env.grille) - 1 and not env.grille[self.x + 1][self.y].mur and env.grille[self.x + 1][
                self.y].perso == False:
                directionAccessible.append(3)

            if len(directionAccessible) != 0:
                dir = self.chooseBestDir(directionAccessible, env)
                if dir == 0:
                    self.move(self.x, self.y - 1, env)
                elif dir == 1:
                    self.move(self.x, self.y + 1, env)
                elif dir == 2:
                    self.move(self.x - 1, self.y, env)
                elif dir == 3:
                    self.move(self.x + 1, self.y, env)

    def chooseBestDir(self, directionAccessible, env):
        cheminNonVisiter = directionAccessible
        voisin = OrderedDict()
        maxTab = len(self.lastchemin)
        for i in self.lastchemin:
            if abs(abs(i[0] - self.x) + abs(self.y - i[1])) == 1:
                if (i[0] > self.x and 3 in directionAccessible):
                    voisin[3] = maxTab - self.lastchemin.index(i)
                    cheminNonVisiter = list(filter((3).__ne__, cheminNonVisiter))
                elif (i[0] < self.x and 2 in directionAccessible):
                    voisin[2] = maxTab - self.lastchemin.index(i)
                    cheminNonVisiter = list(filter((2).__ne__, cheminNonVisiter))

                elif (i[1] > self.y and 1 in directionAccessible):
                    voisin[1] = maxTab - self.lastchemin.index(i)
                    cheminNonVisiter = list(filter((1).__ne__, cheminNonVisiter))

                elif (i[1] < self.y and 0 in directionAccessible):
                    voisin[0] = maxTab - self.lastchemin.index(i)
                    cheminNonVisiter = list(filter((0).__ne__, cheminNonVisiter))
        if len(cheminNonVisiter) > 0:
            return self.modifDirectionByShadow2(list(set(directionAccessible) & set(cheminNonVisiter)), env)
        voisin = sorted(voisin.items(), key=lambda t: t[1])
        voisinEloigne = []
        for i in voisin[::-1]:

            if i[1] >= 5:
                voisinEloigne.append((i[0], i[1]))
        if len(voisinEloigne) <= 0:
            return voisin[len(voisin) - 1][0]
        else:
            return self.modifDirectionByShadow2(voisinEloigne, env, True)

    def modifDirectionByShadow2(self, tab, env, voisin=False):
        # ordre: (0,lum), (1,lum), (2,lum), (3,lum)
        lum = [(0, env.grille[self.x][self.y - 1].lumiere),
               (1, env.grille[self.x][self.y + 1].lumiere),
               (2, env.grille[self.x - 1][self.y].lumiere),
               (3, env.grille[self.x + 1][self.y].lumiere)]
        if voisin == False:
            for i in range(len(tab)):
                tab[i] = (tab[i], lum[tab[i]][1])
            tab = sorted(tab, key=lambda t: t[1])
            # print(tab)

            tabPlusObscure = []
            for i in tab:
                if i[1] == tab[0][1]:
                    tabPlusObscure.append(i)
            if len(tabPlusObscure) > 1:
                return tabPlusObscure[randint(0, len(tabPlusObscure) - 1)][0]
            else:
                return tab[0][0]

        if voisin:
            newTab = []
            for i in range(len(tab)):
                newTab.append((tab[i][0], lum[tab[i][0]]))

            newTab = sorted(newTab, key=lambda t: t[1])
            return newTab[0][0]

    def repereEspion(self, env):
        if (len(env.listEspion) > 0 and abs(env.listEspion[0].x - self.x) +
                abs(self.y - env.listEspion[0].y) <= 7):
            soluce = (env.listEspion[0].x, env.listEspion[0].y)
            dirOrd = env.listEspion[0].y - self.y;
            dirAbs = env.listEspion[0].x - self.x;
            listCasePossible = [(self.x, self.y, 7)]
            closedList = [((self.x, self.y, 7), [(self.x, self.y, 7)])]
            while len(listCasePossible) > 0:
                coord = [listCasePossible.pop(0)]
                if (soluce[0] == coord[0][0] and soluce[1] == coord[0][1]):
                    if coord[0][2] + env.grille[soluce[0]][soluce[1]].lumiere >= 8:
                        env.listEspion[0].ifReperer(self)
                        parents = closedList[-1]

                        while parents[1][0] != (self.x, self.y, 7):
                            parents = list(filter(lambda a: a[0] == parents[1][0], closedList))[0]
                        return parents[0][0], parents[0][1]

                if (coord[0][2] > 0):
                    if (abs(dirOrd) > 0 and self.verifCaseLibre(coord[0][0], coord[0][1] + (dirOrd // abs(dirOrd)), env,
                                                                True)):
                        listCasePossible.append((coord[0][0], coord[0][1] + (dirOrd // abs(dirOrd)), coord[0][2] - 1))
                        closedList.append((listCasePossible[-1], coord))

                if (abs(dirAbs) > 0 and self.verifCaseLibre(coord[0][0] + (dirAbs // abs(dirAbs)), coord[0][1], env,
                                                            True)):
                    listCasePossible.append((coord[0][0] + (dirAbs // abs(dirAbs)), coord[0][1], coord[0][2] - 1))
                    closedList.append((listCasePossible[-1], coord))
        return False

    def verifCaseLibre(self, newx, newy, env, espion=False):
        try:
            if ((env.grille[newx][newy].mur == False) and env.grille[newx][newy].perso == False and (
                    espion or env.grille[newx][newy].espion == False)):
                return True
            else:
                return False
        except:
            print('erreur survenu')
            return False





