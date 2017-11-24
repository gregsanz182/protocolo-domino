import sys
import random
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFrame, QStyle
from ZonaJuego import ZonaJuego
from PanelJugador import PanelJugador

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Dominó (Servidor)')
        self.ancho = 960
        self.alto = 610

        self.setFixedWidth(self.ancho)
        self.setFixedHeight(self.alto)
        self.setWidgetCentral()

        self.jugadores = []
        self.zonaJuego = ZonaJuego(self)

        for i in range(0, 28):
            self.zonaJuego.ponerFicha(-1, -1, 0)
        for i in range(0, 28):
            self.zonaJuego.ponerFicha(random.randint(0, 6), random.randint(0, 6), 1)

        f = PanelJugador('AAAAAAAAAAAAA...', 0, padre=self)
            f.inicializarFichas(None)
        PanelJugador('AAAAAAAAAAAAA...', 1, padre=self)
        PanelJugador('AAAAAAAAAAAAA...', 2, padre=self)
        PanelJugador('AAAAAAAAAAAAA...', 3, padre=self)
        
    def setWidgetCentral(self):
        self.widgetCentral = QFrame()
        self.setCentralWidget(self.widgetCentral)
        self.widgetCentral.setFixedHeight(self.alto)
        self.widgetCentral.setFixedWidth(self.ancho)
        self.widgetCentral.setFrameStyle(QFrame.StyledPanel)
        self.widgetCentral.setStyleSheet('background-image: url(res/background.png); border: 5px solid #736427;')

    def inicializarJugador(self, mensaje_dict, nombre):
        jug = PanelJugador(nombre, len(self.jugadores), self)
        self.jugadores[mensaje_dict['jugador']] = jug

    def inicializarJugadores(self, mensaje_dict):
        for jugador in mensaje_dict["jugadores"]:
            if jugador['identificador'] not in iter(self.jugadores.keys()):
                jug = PanelJugador(jugador.get('nombre', "Jugador #{}".format(len(self.jugadores)+1)), len(self.jugadores), self)
                jug.inicializarFichas(None)
                self.jugadores[jugador['identificador']] = jug

    def ponerManoJugador(self, mensaje_dict, idenJugador):
        self.jugadores[idenJugador].inicializarFichas(mensaje_dict['fichas'])

    def procesarJugada(self, mensaje_dict):
        if mensaje_dict['evento_pasado']['tipo'] == 0:
            if mensaje_dict['punta']:
                if mensaje_dict['punta_uno'] == mensaje_dict['evento_pasado']['entero_uno']:
                    self.zonaJuego.ponerFicha(mensaje_dict['evento_pasado']['entero_dos'], mensaje_dict['evento_pasado']['entero_uno'], mensaje_dict['punta'])
                else:
                    self.zonaJuego.ponerFicha(mensaje_dict['evento_pasado']['entero_uno'], mensaje_dict['evento_pasado']['entero_dos'], mensaje_dict['punta'])
            else:
                if mensaje_dict['punta_dos'] == mensaje_dict['evento_pasado']['entero_uno']:
                    self.zonaJuego.ponerFicha(mensaje_dict['evento_pasado']['entero_uno'], mensaje_dict['evento_pasado']['entero_dos'], mensaje_dict['punta'])
                else:
                    self.zonaJuego.ponerFicha(mensaje_dict['evento_pasado']['entero_dos'], mensaje_dict['evento_pasado']['entero_uno'], mensaje_dict['punta'])
            self.jugadores[mensaje_dict['evento_pasado']['jugador']].quitarFicha(mensaje_dict['evento_pasado']['ficha'])
            
    
if __name__ == '__main__':
    try:
        QApplication.setStyle('Fusion')
        mainApp = QApplication(sys.argv)

        mainWindow = MainWindow()
        mainWindow.show()

        mainApp.exec_()

        sys.exit(0)
    except NameError:
        print("Nombre del error:", sys.exc_info()[1])
    except SystemExit:
        print("Cerrando la ventana...")
    except Exception:
        print(sys.exc_info()[1])