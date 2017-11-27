import sys
from PyQt5.QtWidgets import QApplication
from Gui.MainWindow import MainWindow
from Gui.InputDialog import InputDialog
from Servidor.HiloJuego import HiloJuego

if __name__ == '__main__':
    try:
        mainApp = QApplication(sys.argv)

        mainWindow = MainWindow('Servidor')
        mainWindow.show()

        nombre = InputDialog.getText("Nombre", "Ingrese el nombre para la mesa", mainWindow)

        juego = HiloJuego(nombre, mainWindow)
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