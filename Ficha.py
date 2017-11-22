from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QTransform

class Ficha(QLabel):

    horizontal = 0
    vertical = 1

    def __init__(self, puntaA, puntaB, sentido, padre=None):
        super().__init__(padre)
        if puntaB > puntaA:
            self.puntaA = puntaB
            self.puntaB = puntaA
        else:
            self.puntaA = puntaA
            self.puntaB = puntaB
        if sentido == self.horizontal:
            self.pixmap = QPixmap("res/horizontal/{0}_{1}.png".format(self.puntaA, self.puntaB))
        elif sentido == self.vertical:
            self.pixmap = QPixmap("res/vertical/{0}_{1}.png".format(self.puntaA, self.puntaB))
        self.setPixmap(self.pixmap)
        self.setFixedSize(self.pixmap.size())
        self.posicion = 0
        
    def xCentral(self):
        return self.x()+(self.width() / 2)

    def yCentral(self):
        return self.y()+(self.height() / 2)

    def xFinal(self):
        return self.x()+self.width()
    
    def yFinal(self):
        return self.y()+self.height()