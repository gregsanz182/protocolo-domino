import sys
from PyQt5.QtWidgets import QApplication, QInputDialog
from MainWindow import MainWindow
from InputDialog import InputDialog
from Cliente.HiloJuego import HiloJuego

if __name__ == '__main__':
    try:
        mainApp = QApplication(sys.argv)

        mainWindow = MainWindow('Cliente')
        mainWindow.show()

        nombre = InputDialog.getText("Nombre", "Ingrese su nombre de jugador", mainWindow)

        juego = HiloJuego(mainWindow, nombre)
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
        juego.cerrarTodo()