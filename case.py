
from random import *

class case:
  def __init__(self,mur = False, perso = False,espion = False, lumiere = 10):
    self.mur = mur
    self.perso=perso
    self.espion = espion
    if self.mur != False :
      self.lumiere = 10
    else:
      self.lumiere=3
    self.idInterface=None
  def C(self):
    return self.idInterface

  def setId(self, a):
    self.idInterface = a

  def setLumen(self,a):
	  self.lumiere=a
  def getMur(self):
	  return self.mur
