from PyQt5.QtWidgets import QFrame
from Ficha import Ficha

class PanelJugador(QFrame):

    def __init__(self, nombre, numJug, fichas=None, padre=None):
        super().__init__(padre)
        self.fichas = []
        self.numJug = numJug
        if self.numJug == 0:
            self.setGeometry(181, 519, 450, 80)
        elif self.numJug == 1:
            self.setGeometry(786, 154, 160, 362)
        elif self.numJug == 2:
            self.setGeometry(329, 11, 450, 80)
        elif self.numJug == 3:
            self.setGeometry(4, 93, 160, 362)
        """self.setFrameStyle(QFrame.StyledPanel)
        self.setStyleSheet('border: 1px solid #FFFFFF;')"""
        self.inicializarManoWidget()
        self.inicializarFichas(fichas)

    def inicializarFichas(self, fichas):
        if fichas:
           for ficha in fichas:
               peer = Ficha(ficha['entero_uno'], ficha['entero_dos'], Ficha.vertical if self.numJug in (0, 2) else Ficha.horizontal, self.manoWidget)
        else:
            for i in range(0, 7):
                peer = Ficha(-1, -1, Ficha.vertical if self.numJug in (0, 2) else Ficha.horizontal, self.manoWidget)
                if len(self.fichas) == 0:
                    peer.move(0, 0)
                elif self.numJug in (0, 2):
                    peer.move(self.fichas[len(self.fichas) - 1].xFinal() + 11, 0)
                else:
                    peer.move(0, self.fichas[len(self.fichas) - 1].yFinal() + 11)
                self.fichas.append(peer)

    def inicializarManoWidget(self):
        self.manoWidget = QFrame(self)
        if self.numJug == 0:
            self.manoWidget.setGeometry(self.width() - 280, 15, 255, 57)
        elif self.numJug == 1:
            self.manoWidget.setGeometry(self.width() - 64, 25, 57, 255)
        elif self.numJug == 2:
            self.manoWidget.setGeometry(25, 9, 255, 57)
        elif self.numJug == 3:
            self.manoWidget.setGeometry(9, 85, 57, 255)
