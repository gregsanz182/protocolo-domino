from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QTransform

class Ficha(QLabel):

    horizontal = 0
    vertical = 1

    def __init__(self, entero_uno, entero_dos, sentido, padre=None):
        super().__init__(padre)
        if entero_dos > entero_uno:
            self.entero_uno = entero_dos
            self.entero_dos = entero_uno
        else:
            self.entero_uno = entero_uno
            self.entero_dos = entero_dos
        if sentido == self.horizontal:
            if entero_dos > entero_uno:
                self.pixmap = QPixmap("res/horizontal/{0}_{1}.png".format(self.entero_uno, self.entero_dos))
            else:
                self.pixmap = QPixmap("res/horizontal/{0}_{1}.png".format(self.entero_uno, self.entero_dos)).transformed(QTransform().scale(-1, 1))
        elif sentido == self.vertical:
            self.pixmap = QPixmap("res/vertical/{0}_{1}.png".format(self.entero_uno, self.entero_dos))
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