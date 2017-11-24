import sys
from PyQt5.QtWidgets import QApplication
from MainWindow import MainWindow
from Servidor.HiloJuego import HiloJuego

if __name__ == '__main__':
    try:
        QApplication.setStyle('Fusion')
        mainApp = QApplication(sys.argv)

        mainWindow = MainWindow()
        mainWindow.show()

        juego = HiloJuego(mainWindow)
        juego.start()

        mainApp.exec_()
        juego.join()

        sys.exit(0)
    except NameError:
        print("Nombre del error:", sys.exc_info()[1])
    except SystemExit:
        print("Cerrando la ventana...")
    except Exception:
        print(sys.exc_info()[1])