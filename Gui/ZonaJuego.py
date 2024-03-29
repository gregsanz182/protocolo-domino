from PyQt5.QtWidgets import QWidget, QFrame
from Gui.Ficha import Ficha

class ZonaJuego(QFrame):

    def __init__(self, padre=None):
        super().__init__(padre)
        self.ancho = 744
        self.alto = 402
        self.x = 103
        self.y = 100
        self.fichas = []

        self.setGeometry(self.x, self.y, self.ancho, self.alto)

    def ponerFicha(self, entero_uno, entero_dos, punta):
        if len(self.fichas) == 0:
            ficha = Ficha(entero_uno, entero_dos, Ficha.vertical, self)
            ficha.move((self.ancho / 2)-(ficha.width() / 2), (self.alto / 2)-(ficha.height() / 2))
            ficha.posicion = 0
            self.fichas.append(ficha)
        elif punta:
            if self.fichas[0].posicion in (-17, -18):
                ficha = Ficha(entero_uno, entero_dos, Ficha.vertical if self.fichas[0].posicion == -17 else Ficha.horizontal, self)
                ficha.move(self.fichas[0].xFinal() - ficha.width(), self.fichas[0].y() - ficha.height())
            elif -19 < self.fichas[0].posicion < -6:
                ficha = Ficha(entero_uno, entero_dos, Ficha.horizontal, self)
                ficha.move(self.fichas[0].xFinal(), self.fichas[0].yCentral()-(ficha.height() / 2))
            elif self.fichas[0].posicion in (-5, -6):
                ficha = Ficha(entero_uno, entero_dos, Ficha.vertical if self.fichas[0].posicion == -5 else Ficha.horizontal, self)
                ficha.move(self.fichas[0].x(), self.fichas[0].y() - ficha.height())
            else:
                ficha = Ficha(entero_uno, entero_dos, Ficha.horizontal, self)
                ficha.move(self.fichas[0].x() - ficha.width(), self.fichas[0].yCentral()-(ficha.height() / 2))
            ficha.posicion = self.fichas[0].posicion - 1
            self.fichas.insert(0, ficha)
        else:
            if self.fichas[len(self.fichas)-1].posicion in (17, 18):
                ficha = Ficha(entero_uno, entero_dos, Ficha.vertical if self.fichas[len(self.fichas)-1].posicion == 17 else Ficha.horizontal, self)
                ficha.move(self.fichas[len(self.fichas)-1].x(), self.fichas[len(self.fichas)-1].yFinal())
            elif 6 < self.fichas[len(self.fichas)-1].posicion < 19:
                ficha = Ficha(entero_uno, entero_dos, Ficha.horizontal, self)
                ficha.move(self.fichas[len(self.fichas)-1].x()-ficha.width(), self.fichas[len(self.fichas)-1].yCentral()-(ficha.height() / 2))
            elif self.fichas[len(self.fichas)-1].posicion in (5, 6):
                ficha = Ficha(entero_uno, entero_dos, Ficha.vertical if self.fichas[len(self.fichas)-1].posicion == 5 else Ficha.horizontal, self)
                ficha.move(self.fichas[len(self.fichas)-1].xFinal() - ficha.width(), self.fichas[len(self.fichas)-1].yFinal())
            else:
                ficha = Ficha(entero_uno, entero_dos, Ficha.horizontal, self)
                ficha.move(self.fichas[len(self.fichas)-1].xFinal(), self.fichas[len(self.fichas)-1].yCentral()-(ficha.height() / 2))
            ficha.posicion = self.fichas[len(self.fichas)-1].posicion + 1
            self.fichas.append(ficha)
        ficha.show()

    def limpiarZonaJuego(self):
        for ficha in self.fichas:
            ficha.hide()
            ficha.deleteLater()
        self.fichas = []