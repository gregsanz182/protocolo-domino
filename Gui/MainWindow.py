import sys
import random
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFrame, QStyle, QLabel
from PyQt5.QtCore import pyqtSignal, Qt
from Gui.ZonaJuego import ZonaJuego
from Gui.PanelJugador import PanelJugador
from Gui.ServidoresDialog import ServidoresDialog

class MainWindow(QMainWindow):

    inicializarJugador = pyqtSignal(dict, str)
    inicializarJugadores = pyqtSignal(dict)
    ponerManoJugador = pyqtSignal(dict, str)
    procesarJugada = pyqtSignal(dict)
    cambiarRonda = pyqtSignal(dict)
    abrirServidoresDialog = pyqtSignal(object)
    nuevoServidor = pyqtSignal(dict)
    setLabelMesa = pyqtSignal(str)

    def __init__(self, tituloVentana):
        super().__init__()
        self.setWindowTitle('Dominó ({})'.format(tituloVentana))
        self.ancho = 960
        self.alto = 610

        self.setFixedWidth(self.ancho)
        self.setFixedHeight(self.alto)
        self.setWidgetCentral()

        self.jugadores = {}
        self.zonaJuego = ZonaJuego(self)

        self.labelRonda = QLabel('', self)
        self.labelRonda.setStyleSheet('font-size: 23px; color: #FFFFFF; font-weight: 500')
        self.labelRonda.setFixedWidth(200)
        self.labelRonda.move(16, 14)

        self.labelMensaje = QLabel('', self)
        self.labelMensaje.setStyleSheet('font-size: 13px; color: #FFFFFF; font-weight: 400')
        self.labelMensaje.setFixedWidth(300)
        self.labelMensaje.move(17, 40)

        self.labelMesa = QLabel('', self)
        self.labelMesa.setAlignment(Qt.AlignRight)
        self.labelMesa.setStyleSheet('font-size: 13px; color: #FFFFFF; font-weight: 400; font-style: italic')
        self.labelMesa.setFixedWidth(250)
        self.labelMesa.move(690, 565)

        self.realizarConexiones()

    def realizarConexiones(self):
        self.inicializarJugador.connect(self.inicializarJugadorSlot)
        self.inicializarJugadores.connect(self.inicializarJugadoresSlot)
        self.ponerManoJugador.connect(self.ponerManoJugadorSlot)
        self.procesarJugada.connect(self.procesarJugadaSlot)
        self.cambiarRonda.connect(self.cambiarRondaSlot)
        self.abrirServidoresDialog.connect(self.abrirServidoresDialogSlot)
        self.nuevoServidor.connect(self.nuevoServerDialogSlot)
        self.setLabelMesa.connect(self.setLabelMesaSlot)

    def setWidgetCentral(self):
        self.widgetCentral = QFrame()
        self.setCentralWidget(self.widgetCentral)
        self.widgetCentral.setFixedHeight(self.alto)
        self.widgetCentral.setFixedWidth(self.ancho)
        self.widgetCentral.setFrameStyle(QFrame.StyledPanel)
        self.widgetCentral.setStyleSheet('background-image: url(res/background.png); border: 5px solid #736427;')

    def inicializarJugadorSlot(self, mensaje_dict, nombre):
        jug = PanelJugador(nombre, len(self.jugadores), self)
        jug.show()
        self.jugadores[mensaje_dict['jugador']] = jug

    def inicializarJugadoresSlot(self, mensaje_dict):
        for jugador in mensaje_dict["jugadores"]:
            if jugador['identificador'] not in iter(self.jugadores.keys()):
                jug = PanelJugador(jugador.get('nombre', "Jugador #{}".format(len(self.jugadores)+1)), len(self.jugadores), self)
                jug.inicializarFichas(None)
                self.jugadores[jugador['identificador']] = jug

    def ponerManoJugadorSlot(self, mensaje_dict, idenJugador):
        self.jugadores[idenJugador].inicializarFichas(mensaje_dict['fichas'])

    def procesarJugadaSlot(self, mensaje_dict):
        if 'evento_pasado' in mensaje_dict:
            if mensaje_dict['evento_pasado']['tipo'] == 0:
                if mensaje_dict['evento_pasado']['punta']:
                    if mensaje_dict['punta_uno'] == mensaje_dict['evento_pasado']['ficha']['entero_uno']:
                        self.zonaJuego.ponerFicha(mensaje_dict['evento_pasado']['ficha']['entero_dos'], mensaje_dict['evento_pasado']['ficha']['entero_uno'], mensaje_dict['evento_pasado']['punta'])
                    else:
                        self.zonaJuego.ponerFicha(mensaje_dict['evento_pasado']['ficha']['entero_uno'], mensaje_dict['evento_pasado']['ficha']['entero_dos'], mensaje_dict['evento_pasado']['punta'])
                else:
                    if mensaje_dict['punta_dos'] == mensaje_dict['evento_pasado']['ficha']['entero_uno']:
                        self.zonaJuego.ponerFicha(mensaje_dict['evento_pasado']['ficha']['entero_uno'], mensaje_dict['evento_pasado']['ficha']['entero_dos'], mensaje_dict['evento_pasado']['punta'])
                    else:
                        self.zonaJuego.ponerFicha(mensaje_dict['evento_pasado']['ficha']['entero_dos'], mensaje_dict['evento_pasado']['ficha']['entero_uno'], mensaje_dict['evento_pasado']['punta'])
                self.jugadores[mensaje_dict['evento_pasado']['jugador']].quitarFicha(mensaje_dict['evento_pasado']['ficha'])
            self.jugadores[mensaje_dict['evento_pasado']['jugador']].cambiarEstado(mensaje_dict['evento_pasado']['tipo'])
        self.jugadores[mensaje_dict['jugador']].cambiarEstado(3)
        if mensaje_dict['tipo'] == 4:
            self.jugadores[mensaje_dict['jugador']].cambiarPuntuacion(mensaje_dict['puntuacion'])


    def cambiarRondaSlot(self, mensaje_dict):
        self.labelRonda.setText("Ronda #{}".format(mensaje_dict['ronda']))
        for key in self.jugadores.keys():
            self.jugadores[key].borrarFichas()
        self.zonaJuego.limpiarZonaJuego()

    def abrirServidoresDialogSlot(self, metodoSlot):
        self.dialog = ServidoresDialog(metodoSlot, self)
        self.dialog.show()
    
    def nuevoServerDialogSlot(self, serverInfo):
        self.dialog.nuevoServer(serverInfo)

    def setLabelMesaSlot(self, nombreMesa):
        self.labelMesa.setText(nombreMesa+" ")

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