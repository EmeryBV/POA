from tkinter import *


class interface:
    ##associe la fenetre passé en paramètre et lui donne un titre
    def __init__(self, fen, env):
        self.fenetre = fen
        self.fenetre.title("Ronde d'un garde")
        self.env = env
        self.creerCanvas(20, 20, self.env.grille)

    ##entrée:
    # L, l : nombre de cases
    # case : matrice des cases de la grille, permet d'associer l'objet graphique a la chaque case
    # LiCaseExclure : liste des case a exclure (ne ressevra pas le tag "carre" et serra colorer d'une autre couleur
    ##Sortie:
    # canevas crée avec un cadriage avec les mur.
    # le label indiquant le nombre de coup effectuer est placer
    def creerCanvas(self, L, l, case, LiCaseExclure=[]):
        ##crée la fenetre de dimmension 600x600
        self.canvas = Canvas(self.fenetre, width=600, height=600,
                             borderwidth=5, background="white")
        ##recentre la fenetre pour laisser une marge de 25px pour un aspect plus esthétique
        self.canvas['scrollregion'] = (-25, -25, 575, 575)

        ##définie la dimension des case par rapport a leurs quantité
        self.tailleCase = (550 / max(L, l))

        for li in range(1, L):
            for co in range(1, l):

                if case[co][li].mur == True or (co, li) in LiCaseExclure:
                    Id = self.canvas.create_rectangle(li * self.tailleCase, co * self.tailleCase,
                                                      (li + 1) * self.tailleCase, (co + 1) * self.tailleCase,
                                                      fill='#2c2c2c', outline='#2c2c2c', tags='exterieur')
                    case[co][li].setId(Id)

                else:
                    if case[co][li].perso != False:
                        Id = self.canvas.create_oval(li * self.tailleCase, co * self.tailleCase,
                                                     (li + 1) * self.tailleCase, (co + 1) * self.tailleCase,
                                                     fill='green', tags='garde')

                        case[co][li].setId(Id)
                        case[co][li].perso.id = Id

                    elif case[co][li].espion != False:
                        Id = self.canvas.create_oval(li * self.tailleCase, co * self.tailleCase,
                                                     (li + 1) * self.tailleCase, (co + 1) * self.tailleCase,
                                                     fill='red', tags='espion')

                        case[co][li].setId(Id)
                        case[co][li].espion.id = Id
                    Id = self.canvas.create_rectangle(li * self.tailleCase, co * self.tailleCase,
                                                      (li + 1) * self.tailleCase, (co + 1) * self.tailleCase,
                                                      fill=self.couleurLumiere(case[co][li].lumiere), tags='carre')
                    ##associe l'id de l'objet rectangle a la case associé (pour permettre une passerelle entre la matrice et l'interface graphique)
                    case[co][li].setId(Id)

        ##on met les garde en tete de pile (premier plan)
        for i in self.env.listGarde:
            if not i.id == None:
                self.canvas.tag_raise(i.id)
        for i in self.env.listEspion:
            if not i.id == None:
                self.canvas.tag_raise(i.id)

        self.canvas.grid(column=2, row=1, columnspan=2)

    def couleurLumiere(self, lum, lumMin=0, lumMax=15):
        ratio = 255 / max((lumMax - lumMin), 1)
        value = int((lum - lumMin) * ratio)
        return "#%02x%02x%02x" % (value, value, value)

    def moveGarde(self, id, newx, newy):
        if not id == None:
            self.canvas.coords(id, newy * self.tailleCase, newx * self.tailleCase,
                               (newy + 1) * self.tailleCase, (newx + 1) * self.tailleCase)

    def moveEspion(self, id, newx, newy):
        if not id == None:
            self.canvas.coords(id, newy * self.tailleCase, newx * self.tailleCase,
                               (newy + 1) * self.tailleCase, (newx + 1) * self.tailleCase)

    def modifColor(self, id, nbe):
        if not id == None:
            self.canvas.config(id, fill=self.couleurLumiere(nbe))