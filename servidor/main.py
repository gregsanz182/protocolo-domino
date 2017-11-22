import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFrame, QStyle

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Dominó (Servidor)')
        self.ancho = 950
        self.alto = 610

        self.setFixedWidth(self.ancho)
        self.setFixedHeight(self.alto)
        self.setWidgetCentral()

    def setWidgetCentral(self):
        self.widgetCentral = QFrame()
        self.setCentralWidget(self.widgetCentral)
        self.widgetCentral.setFixedHeight(self.alto)
        self.widgetCentral.setFixedWidth(self.ancho)
        self.widgetCentral.setFrameStyle(QFrame.StyledPanel)
        self.widgetCentral.setStyleSheet('background-image: url(res/background.png); border-color: #736427; border-width: 10px;')



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