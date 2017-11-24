import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dominó")

        #Tamaño minimo de la ventana
        self.setMinimumWidth(640)
        self.setMinimumHeight(480)

if __name__ == '__main__':
    try:
        mainApp = QApplication(sys.argv)

        mainWindow = MainWindow()
        mainWindow.show()

        mainApp.exec_()
        sys.exit(0)
    except NameError:
        print('Nombre del error: ', sys.exc_info()[1])
    except SystemExit:
        print('Cerrando ventana')
    except Exception:
        print(sys.exc_info()[1])
