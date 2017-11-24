import random
from PyQt5.QtWidgets import QFrame, QLabel
from PyQt5.QtCore import Qt
from Ficha import Ficha

class PanelJugador(QFrame):

    def __init__(self, nombre, numJug, fichas=None, padre=None):
        super().__init__(padre)
        self.fichas = []
        self.numJug = numJug
        self.nombre = nombre
        self.nombreLabel = QLabel(self.nombre+" ", self)
        self.nombreLabel.setStyleSheet('font-size: 13px; color: #FFFFFF; font-weight: 500; font-style: italic;')
        self.puntosLabel = QLabel("0 puntos", self) 
        self.puntosLabel.setStyleSheet('font-size: 12px; color: #FFFFFF;')
        self.estadoLabel = QLabel('Jugó', self)
        self.estadoLabel.setStyleSheet('font-size: 19px; color: #00FF40;')
        if self.numJug == 0:
            self.setGeometry(181, 519, 450, 80)
            self.nombreLabel.setAlignment(Qt.AlignRight)
            self.nombreLabel.setFixedWidth(140)
            self.nombreLabel.move(0, 4)

            self.puntosLabel.setAlignment(Qt.AlignRight)
            self.puntosLabel.setFixedWidth(138)
            self.puntosLabel.move(0, 20)

            self.estadoLabel.setAlignment(Qt.AlignRight)
            self.estadoLabel.setFixedWidth(138)
            self.estadoLabel.move(0, 38)
        elif self.numJug == 1:
            self.setGeometry(786, 154, 160, 365)
            self.nombreLabel.setAlignment(Qt.AlignRight)
            self.nombreLabel.setFixedWidth(154)
            self.nombreLabel.move(0, 308)

            self.puntosLabel.setAlignment(Qt.AlignRight)
            self.puntosLabel.setFixedWidth(152)
            self.puntosLabel.move(0, 324)

            self.estadoLabel.setAlignment(Qt.AlignRight)
            self.estadoLabel.setFixedWidth(152)
            self.estadoLabel.move(0, 342)
        elif self.numJug == 2:
            self.setGeometry(329, 11, 470, 80)
            self.estadoLabel.setAlignment(Qt.AlignLeft)
            self.estadoLabel.setFixedWidth(158)
            self.estadoLabel.move(310, 11)
            
            self.nombreLabel.setAlignment(Qt.AlignLeft)
            self.nombreLabel.setFixedWidth(158)
            self.nombreLabel.move(310, 43)

            self.puntosLabel.setAlignment(Qt.AlignLeft)
            self.puntosLabel.setFixedWidth(158)
            self.puntosLabel.move(310, 59)
        elif self.numJug == 3:
            self.setGeometry(4, 81, 160, 370)
            self.estadoLabel.setAlignment(Qt.AlignLeft)
            self.estadoLabel.setFixedWidth(145)
            self.estadoLabel.move(13, 0)
            
            self.nombreLabel.setAlignment(Qt.AlignLeft)
            self.nombreLabel.setFixedWidth(145)
            self.nombreLabel.move(13, 32)

            self.puntosLabel.setAlignment(Qt.AlignLeft)
            self.puntosLabel.setFixedWidth(145)
            self.puntosLabel.move(13, 50)
        """self.setFrameStyle(QFrame.StyledPanel)
        self.setStyleSheet('border: 1px solid #FFFFFF;')"""
        self.inicializarManoWidget()

    def inicializarFichas(self, fichas):
        self.fichas = []
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
            self.manoWidget.setGeometry(15, 93, 57, 255)

    def quitarFicha(self, fichaJugada):
        for ficha in self.fichas:
            if fichaJugada['entero_dos'] > fichaJugada['entero_uno'] \
                and fichaJugada['entero_dos'] == ficha.entero_uno \
                and fichaJugada['entero_uno'] == ficha.entero_dos:
                self.fichas.remove(ficha)
                ficha.deleteLater()
                return
            elif fichaJugada['entero_uno'] == ficha.entero_uno \
                and fichaJugada['entero_dos'] == ficha.entero_dos:
                self.fichas.remove(ficha)
                ficha.deleteLater()
                return
        if len(self.fichas) > 0:
            f = random.choice(self.fichas)
            f.deleteLater()
            self.fichas.remove(f)


