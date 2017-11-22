import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFrame, QStyle
from ZonaJuego import ZonaJuego

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Dominó (Servidor)')
        self.ancho = 950
        self.alto = 610

        self.setFixedWidth(self.ancho)
        self.setFixedHeight(self.alto)
        self.setWidgetCentral()
        self.zonaJuego = ZonaJuego(self)

        for i in range(0, 28):
            self.zonaJuego.ponerFicha(random.randint(0, 6), random.randint(0, 6), 0)
        for i in range(0, 28):
            self.zonaJuego.ponerFicha(random.randint(0, 6), random.randint(0, 6), 1)

        


    def setWidgetCentral(self):
        self.widgetCentral = QFrame()
        self.setCentralWidget(self.widgetCentral)
        self.widgetCentral.setFixedHeight(self.alto)
        self.widgetCentral.setFixedWidth(self.ancho)
        self.widgetCentral.setFrameStyle(QFrame.StyledPanel)
        self.widgetCentral.setStyleSheet('background-image: url(res/background.png); border: 5px solid #736427;')



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