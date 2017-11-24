import sys
from PyQt5.QtWidgets import QApplication, QInputDialog
from MainWindow import MainWindow
from Cliente.HiloJuego import HiloJuego

if __name__ == '__main__':
    try:
        mainApp = QApplication(sys.argv)

        mainWindow = MainWindow()
        mainWindow.show()
        nombre = QInputDialog.getText(mainWindow, "Nombre de jugador", "Ingrese su nombre de jugador")

        juego = HiloJuego(mainWindow, nombre[0])
        juego.start()

        mainApp.exec_()

        sys.exit(0)
    except NameError:
        print("Nombre del error:", sys.exc_info()[1])
    except SystemExit:
        print("Cerrando la ventana...")
        juego.cerrarTodo()
    except Exception:
        print(sys.exc_info()[1])